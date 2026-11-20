import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from app import build_retriever, PROMPT, ask_legal_ai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


# ------------------------------------
# PAGE CONFIGURATION
# ------------------------------------

st.set_page_config(
    page_title="Indian Legal AI Assistant",
    page_icon="⚖️",
    layout="wide"
)


# ------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


# ------------------------------------
# INITIALIZE RAG BACKEND
# ------------------------------------

@st.cache_resource(show_spinner=False)
def initialize_rag():

    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing from the .env file."
        )

    # Initialize FAISS retriever
    retriever = build_retriever()

    # Initialize OpenAI LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # Create LangChain pipeline
    chain = PROMPT | llm | StrOutputParser()

    return retriever, chain


# ------------------------------------
# CUSTOM CSS
# ------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        color: #60A5FA;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #94A3B8;
        margin-bottom: 30px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------
# INITIALIZE CHAT HISTORY
# ------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------------------------
# SIDEBAR
# ------------------------------------

with st.sidebar:

    st.title("⚖️ Legal AI")

    st.markdown("---")

    st.subheader("📚 Legal Categories")

    # Only Motor Vehicle Law is supported currently
    category = st.selectbox(
        "Select Legal Category",
        [
            "Motor Vehicle Law"
        ]
    )

    st.markdown("---")

    st.subheader("📄 Knowledge Base")

    st.info("Motor Vehicles Act, 1988")

    st.markdown("---")

    st.subheader("🤖 AI Technologies")

    st.write("LangChain")
    st.write("Sentence Transformers")
    st.write("FAISS Vector Database")
    st.write("GPT-4o-mini")
    st.write("Retrieval-Augmented Generation")

    st.markdown("---")

    # Clear chat history
    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    st.warning(
        "⚠️ This chatbot provides general legal information "
        "and should not be considered professional legal advice."
    )


# ------------------------------------
# MAIN PAGE
# ------------------------------------

st.markdown(
    '<div class="main-title">'
    '⚖️ Indian Legal AI Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered legal information using RAG technology'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# ------------------------------------
# WELCOME MESSAGE
# ------------------------------------

if not st.session_state.messages:

    st.info(
        "👋 Welcome to Indian Legal AI Assistant! "
        "Ask questions related to the Motor Vehicles Act, 1988."
    )


# ------------------------------------
# DISPLAY PREVIOUS MESSAGES
# ------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # Display saved sources if available
        if message.get("sources"):

            with st.expander("📚 Retrieved Legal Sources"):

                for source in message["sources"]:

                    st.write(
                        f"**Document:** {source['document']}"
                    )

                    if source["page"] is not None:

                        st.write(
                            f"**PDF Page:** {source['page']}"
                        )

                    st.markdown("---")


# ------------------------------------
# USER INPUT
# ------------------------------------

question = st.chat_input(
    "Ask your legal question here..."
)


if question:

    # Save user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Display user question
    with st.chat_message("user"):

        st.markdown(question)

    # Display AI response
    with st.chat_message("assistant"):

        with st.spinner("Searching legal documents..."):

            try:

                # Initialize RAG
                retriever, chain = initialize_rag()

                # Generate answer
                answer, retrieved_docs = ask_legal_ai(
                    question,
                    retriever,
                    chain
                )

                # Display answer
                st.markdown(answer)

                # Store retrieved sources
                sources = []

                for doc in retrieved_docs:

                    source_name = doc.metadata.get(
                        "source",
                        "Unknown"
                    )

                    page_number = doc.metadata.get("page")

                    # PyPDFLoader pages are usually zero-indexed
                    if page_number is not None:
                        page_number = int(page_number) + 1

                    sources.append({
                        "document": source_name,
                        "page": page_number
                    })

                # Display retrieved sources
                if sources:

                    with st.expander(
                        "📚 Retrieved Legal Sources"
                    ):

                        for source in sources:

                            st.write(
                                f"**Document:** {source['document']}"
                            )

                            if source["page"] is not None:

                                st.write(
                                    f"**PDF Page:** {source['page']}"
                                )

                            st.markdown("---")

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as e:

                st.error(
                    f"An error occurred: {str(e)}"
                )

                st.info(
                    "Please check your API key, "
                    "embedding model, FAISS index, "
                    "and RAG backend configuration."
                )


# ------------------------------------
# FOOTER
# ------------------------------------

st.markdown("---")

st.caption(
    "Indian Legal AI Assistant | "
    "Powered by LangChain, Sentence Transformers, FAISS & OpenAI"
)