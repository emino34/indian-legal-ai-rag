"""
Indian Legal AI RAG Chatbot
Backend for Terminal and Streamlit Application
"""

import os
import hashlib
from pathlib import Path

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter


# ==========================================
# PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DOCUMENT_PATH = BASE_DIR / "documents" / "motor_vehicles_act.pdf"

INDEX_PATH = BASE_DIR / "faiss_index"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "gpt-4o-mini"

CHUNK_SIZE = 800

CHUNK_OVERLAP = 100

TOP_K = 8


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(BASE_DIR / ".env")


# ==========================================
# LEGAL AI PROMPT
# ==========================================

PROMPT = ChatPromptTemplate.from_template(
    """
You are an Indian Legal AI Assistant.

Your task is to answer legal questions using ONLY
the retrieved legal document excerpts.

Instructions:

1. Answer questions using the provided legal information.

2. Mention relevant Acts and Sections when they are
   explicitly present in the retrieved documents.

3. Do not invent legal sections, penalties, exceptions,
   or court decisions.

4. If the retrieved documents do not contain enough
   information, clearly say so.

5. Explain legal information in simple English.

6. Do not provide personalized legal advice.

7. Do not assume that an exception in one legal section
   automatically applies to another section.

8. The supplied PDF may not reflect the latest amendments.
   Do not claim its provisions are verified current law.

9. If a question is unrelated to the supplied legal
   documents, explain that the knowledge base does
   not contain sufficient information.

Retrieved Legal Documents:

{context}

User Question:

{question}

Answer:
"""
)


# ==========================================
# CREATE EMBEDDING MODEL
# ==========================================

def get_embeddings():

    print("Loading Sentence Transformer model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    return embeddings


# ==========================================
# LOAD PDF DOCUMENT
# ==========================================

def load_documents():

    if not DOCUMENT_PATH.is_file():

        raise FileNotFoundError(
            f"PDF document not found: {DOCUMENT_PATH}"
        )

    print("Loading PDF document...")

    loader = PyPDFLoader(str(DOCUMENT_PATH))

    documents = loader.load()

    print(f"Total PDF pages: {len(documents)}")

    for document in documents:

        document.metadata["source"] = DOCUMENT_PATH.name

    return documents


# ==========================================
# SPLIT DOCUMENT INTO CHUNKS
# ==========================================

def split_documents(documents):

    print("Splitting PDF into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    if not chunks:

        raise ValueError(
            "No usable text found in the PDF."
        )

    print(f"Total chunks created: {len(chunks)}")

    return chunks


# ==========================================
# GENERATE CACHE HASH
# ==========================================

def generate_document_hash():

    document_bytes = DOCUMENT_PATH.read_bytes()

    configuration = (
        f"{EMBEDDING_MODEL}"
        f"|chunk_size={CHUNK_SIZE}"
        f"|chunk_overlap={CHUNK_OVERLAP}"
        f"|normalize_embeddings=True"
    )

    hash_data = (
        document_bytes
        + configuration.encode("utf-8")
    )

    return hashlib.sha256(hash_data).hexdigest()


# ==========================================
# BUILD FAISS RETRIEVER
# ==========================================

def build_retriever():

    # Check PDF exists
    if not DOCUMENT_PATH.is_file():

        raise FileNotFoundError(
            f"Document missing: {DOCUMENT_PATH}"
        )

    # Initialize embedding model
    embeddings = get_embeddings()

    # Generate cache hash
    current_hash = generate_document_hash()

    hash_path = INDEX_PATH / "source_sha256.txt"

    faiss_file = INDEX_PATH / "index.faiss"

    pickle_file = INDEX_PATH / "index.pkl"

    # Check existing index
    saved_index = (
        faiss_file.is_file()
        and pickle_file.is_file()
        and hash_path.is_file()
    )

    # ======================================
    # LOAD EXISTING INDEX
    # ======================================

    if saved_index:

        saved_hash = hash_path.read_text(
            encoding="utf-8"
        ).strip()

        if saved_hash == current_hash:

            print("Loading existing FAISS index...")

            # Only load indexes created by this application
            # and stored in a trusted local directory.
            vectorstore = FAISS.load_local(
                str(INDEX_PATH),
                embeddings,
                allow_dangerous_deserialization=True
            )

            print("FAISS index loaded successfully.")

            return vectorstore.as_retriever(
                search_kwargs={"k": TOP_K}
            )

    # ======================================
    # CREATE NEW INDEX
    # ======================================

    print("Creating new FAISS index...")

    documents = load_documents()

    chunks = split_documents(documents)

    print("Generating Sentence Transformer embeddings...")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    INDEX_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    vectorstore.save_local(
        str(INDEX_PATH)
    )

    hash_path.write_text(
        current_hash,
        encoding="utf-8"
    )

    print("FAISS index created and saved successfully.")

    return vectorstore.as_retriever(
        search_kwargs={"k": TOP_K}
    )


# ==========================================
# INITIALIZE LANGUAGE MODEL
# ==========================================

def initialize_llm():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:

        raise RuntimeError(
            "OPENAI_API_KEY missing. "
            "Add it to your .env file."
        )

    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0
    )

    return llm


# ==========================================
# CREATE RAG CHAIN
# ==========================================

def create_rag_chain():

    llm = initialize_llm()

    chain = PROMPT | llm | StrOutputParser()

    return chain


# ==========================================
# ASK LEGAL AI
# ==========================================

def ask_legal_ai(question, retriever, chain):

    if not question or not question.strip():

        raise ValueError(
            "Please enter a legal question."
        )

    # STEP 1: Retrieve relevant legal chunks
    retrieved_docs = retriever.invoke(question)

    # STEP 2: Prepare context with page references
    context_parts = []

    for doc in retrieved_docs:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get("page")

        if page is not None:

            page_number = int(page) + 1

            reference = (
                f"Source: {source}, "
                f"PDF Page: {page_number}"
            )

        else:

            reference = f"Source: {source}"

        context_parts.append(
            f"{reference}\n{doc.page_content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # STEP 3: Generate answer
    answer = chain.invoke({
        "context": context,
        "question": question
    })

    return answer, retrieved_docs


# ==========================================
# TERMINAL CHATBOT
# ==========================================

def main():

    print("\n======================================")
    print("      INDIAN LEGAL AI ASSISTANT")
    print("======================================")

    print("\nInitializing RAG system...")

    retriever = build_retriever()

    chain = create_rag_chain()

    print("\nRAG system initialized successfully.")

    print("\nType 'exit' to quit.")
    print("Type 'debug' to inspect retrieved chunks.")

    while True:

        try:

            question = input(
                "\nYour legal question: "
            ).strip()

        except (EOFError, KeyboardInterrupt):

            print("\nGoodbye!")
            break

        if question.lower() in {"exit", "quit"}:

            print("Goodbye!")
            break

        if not question:

            continue

        # ==================================
        # DEBUG MODE
        # ==================================

        if question.lower() == "debug":

            debug_question = input(
                "Enter question to inspect: "
            ).strip()

            if not debug_question:
                continue

            retrieved_docs = retriever.invoke(
                debug_question
            )

            for i, doc in enumerate(
                retrieved_docs,
                start=1
            ):

                print(f"\nCHUNK {i}")

                print(
                    "Source:",
                    doc.metadata.get(
                        "source",
                        "Unknown"
                    )
                )

                page = doc.metadata.get("page")

                if page is not None:

                    print(
                        "PDF Page:",
                        int(page) + 1
                    )

                print("\n", doc.page_content)

            continue

        # ==================================
        # GENERATE ANSWER
        # ==================================

        try:

            answer, retrieved_docs = ask_legal_ai(
                question,
                retriever,
                chain
            )

            print("\nANSWER:\n")

            print(answer)

            print("\nRETRIEVED SOURCES:")

            seen_sources = set()

            for doc in retrieved_docs:

                source = doc.metadata.get(
                    "source",
                    "Unknown"
                )

                page = doc.metadata.get("page")

                if page is not None:
                    label = f"{source} - PDF Page {int(page) + 1}"
                else:
                    label = source

                if label not in seen_sources:

                    print("-", label)

                    seen_sources.add(label)

            print(
                "\nNote: This chatbot provides general "
                "legal information, not professional legal advice."
            )

        except Exception as error:

            print(f"\nError: {error}")


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    main()