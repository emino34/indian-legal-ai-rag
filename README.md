# ⚖️ Indian Legal AI Assistant Using RAG

### AI-Powered Legal Information Chatbot | Python | LangChain | FAISS | Streamlit | OpenAI

An AI-powered legal information assistant built using **Retrieval-Augmented Generation (RAG)** to help users understand Indian motor vehicle laws.

The application retrieves relevant information from the **Motor Vehicles Act, 1988**, and generates understandable answers using **OpenAI GPT-4o-mini**.

The project combines document processing, semantic search, vector databases, and large language models to provide context-grounded legal information.

> **Disclaimer:** This application is developed for educational and informational purposes. It does not provide professional legal advice. Legal information should be verified against current official legislation.

---

## 📌 1. Project Overview

Indian legal documents contain extensive information about laws, regulations, penalties, and legal procedures.

Finding specific information in these documents can be time-consuming, especially for users unfamiliar with legal terminology.

This project addresses that problem by developing an AI-powered chatbot that allows users to ask questions in natural language and receive answers based on retrieved legal documents.

### Example Questions

- What is the punishment for drunk driving in India?
- What does Section 185 of the Motor Vehicles Act explain?
- What are the legal requirements for obtaining a driving licence?
- What are the consequences of driving without a valid licence?
- What happens if someone drives under the influence of alcohol during a medical emergency?

The chatbot retrieves relevant legal passages and generates responses using an LLM.

**Important:** Complex legal scenarios, including medical emergencies, require careful interpretation. The chatbot should not assume that an emergency automatically creates an exception to an offence.

---

## 🎯 2. Project Objectives

The main objectives are:

- Develop an AI-powered chatbot for Indian legal information.
- Implement Retrieval-Augmented Generation.
- Extract and process legal information from PDF documents.
- Convert legal text into numerical embeddings.
- Store embeddings in a FAISS vector database.
- Retrieve relevant legal information using semantic similarity.
- Generate understandable answers using GPT-4o-mini.
- Display retrieved legal document references.
- Provide an interactive chatbot interface using Streamlit.

---

## 🚀 3. Key Features

### AI-Powered Legal Question Answering

Users can ask questions about Indian motor vehicle laws in natural language.

### Retrieval-Augmented Generation

The application retrieves relevant information from its knowledge base before generating an answer.

### Semantic Search

Uses Sentence Transformers to find relevant passages based on meaning rather than relying only on exact keyword matches.

### FAISS Vector Database

Stores document embeddings and supports efficient similarity searches.

### PDF Document Processing

Extracts legal information from the Motor Vehicles Act PDF using PyPDFLoader.

### Source References

Displays retrieved document references and PDF page information.

### Interactive Chat Interface

Provides a Streamlit-based interface for entering questions and viewing answers.

### Local Vector Index Caching

Reuses previously generated FAISS indexes when the document and indexing configuration have not changed.

---

## 🛠️ 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Streamlit | Chatbot frontend |
| LangChain | RAG pipeline integration |
| PyPDFLoader | PDF text extraction |
| RecursiveCharacterTextSplitter | Document chunking |
| Sentence Transformers | Text embedding generation |
| all-MiniLM-L6-v2 | Embedding model |
| FAISS | Vector storage and similarity search |
| OpenAI GPT-4o-mini | Answer generation |
| ChatPromptTemplate | Prompt construction |
| StrOutputParser | Output formatting |
| python-dotenv | Environment variable management |
| hashlib | Index cache validation |
| VS Code | Development and debugging |
| Git and GitHub | Version control |

---

## 🏗️ 5. System Architecture

The application follows a Retrieval-Augmented Generation architecture.

### Document Processing Pipeline

```text
Motor Vehicles Act PDF
          |
          v
      PyPDFLoader
          |
          v
    Text Extraction
          |
          v
RecursiveCharacterTextSplitter
          |
          v
     Text Chunks
          |
          v
 Sentence Transformers
   all-MiniLM-L6-v2
          |
          v
   Vector Embeddings
          |
          v
   FAISS Vector Store
```

### Question Answering Pipeline

```text
        User Question
              |
              v
      Streamlit Frontend
              |
              v
       RAG Backend
              |
              v
      Query Embedding
              |
              v
      FAISS Similarity Search
              |
              v
     Relevant Legal Chunks
              |
              v
       Prompt Template
              |
              v
       OpenAI GPT-4o-mini
              |
              v
       Generated Answer
              |
              v
      Streamlit Interface
              |
              v
    Answer + PDF References
```

---

## 📂 6. Project Structure

```text
ai_law_assistance/
│
├── .vscode/
│   └── launch.json
│
├── documents/
│   ├── motor_vehicles_act.pdf
│   └── Indian_Law_RAG_Source.txt
│
├── faiss_index/                 # Generated locally
│
├── venv/                        # Local virtual environment
│
├── .env                         # API key (not committed)
├── .gitignore
├── README.md
├── INDIAN_LAW_RAG_SOURCE_GUIDE.md
├── app.py
├── streamlit_app.py
└── requirements.txt
```

### Important Files

**`app.py`**

Contains the backend RAG logic, including document processing, embeddings, retrieval, and answer generation.

**`streamlit_app.py`**

Contains the chatbot user interface.

**`documents/`**

Contains the legal source documents used by the application.

**`faiss_index/`**

Stores the generated FAISS vector index locally.

**`requirements.txt`**

Contains the Python dependencies.

**`.env`**

Stores the OpenAI API key locally.

**`.gitignore`**

Prevents sensitive and unnecessary files from being committed to Git.

---

## ⚙️ 7. Installation and Setup

### Prerequisites

Make sure you have:

- Python 3.10 or a compatible Python version.
- Git.
- VS Code or another Python editor.
- An OpenAI API key.
- An internet connection for OpenAI API requests and initial model downloads.

### Step 1: Clone the Repository

```bash
git clone https://github.com/emino34/indian-legal-ai-rag.git
```

```bash
cd indian-legal-ai-rag
```

> If you published the repository under a different name, replace the clone URL with your actual repository URL.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Configure the OpenAI API Key

Create a file named `.env` in the project root.

Add:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Replace the placeholder with your actual API key.

**Never upload your `.env` file or API key to GitHub.**

### Step 6: Verify the Legal Document

Ensure the required PDF exists at:

```text
documents/motor_vehicles_act.pdf
```

If the PDF is not included in the repository, obtain an appropriate copy and place it at this path.

### Step 7: Run the Streamlit Application

```powershell
python -m streamlit run streamlit_app.py
```

The application should become available at:

```text
http://localhost:8501
```

### Step 8: Start Asking Questions

Open the application and enter a question about Indian motor vehicle laws.

The chatbot will retrieve relevant legal passages and generate a response.

---

## 🧠 8. How the RAG System Works

### Step 1: Document Loading

The application loads the Motor Vehicles Act PDF using LangChain's PyPDFLoader.

### Step 2: Document Chunking

The extracted text is divided into smaller chunks.

Current configuration:

```python
chunk_size = 800
chunk_overlap = 100
```

### Step 3: Embedding Generation

The application uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This model converts text into 384-dimensional embeddings.

### Step 4: Vector Storage

The generated embeddings are stored in FAISS.

### Step 5: Query Processing

When a user asks a question, the query is converted into an embedding using the same embedding model.

### Step 6: Document Retrieval

FAISS retrieves the most relevant document chunks.

Current retrieval configuration:

```python
TOP_K = 8
```

### Step 7: Answer Generation

The retrieved text and user question are passed to GPT-4o-mini.

The model generates an answer based on the supplied context.

### Step 8: Response Display

The answer and retrieved PDF references are displayed in the Streamlit interface.

---

## ⚠️ 9. Current Limitations

Although the application implements a functional RAG pipeline, it has several limitations.

### Limited Knowledge Base

The current chatbot primarily focuses on the Motor Vehicles Act.

It does not provide comprehensive coverage of all Indian laws.

### Retrieval Accuracy

Semantic search may fail to retrieve the most relevant legal provision for certain questions.

### No Conversational Memory

The frontend displays previous chat messages, but the backend does not currently use previous questions and answers as conversational context.

### Complex Legal Scenarios

Questions involving medical emergencies, exceptions, and multiple legal provisions may require information that is not available in the retrieved context.

### Legal Information Updates

The application does not automatically track amendments or changes in legislation.

### Potential Hallucinations

The LLM may occasionally generate incorrect or unsupported information.

### No Formal Evaluation

The chatbot has not yet undergone comprehensive testing against a verified legal question-answer dataset.

---

## 🔮 10. Future Improvements

### 1. Add Conversational Memory

Enable the chatbot to understand follow-up questions using previous conversation context.

### 2. Expand the Legal Knowledge Base

Add more Indian legal documents to improve the range and completeness of answers.

### 3. Implement Hybrid Search

Combine semantic search with keyword-based retrieval to improve legal section matching.

### 4. Improve Answer Accuracy

Introduce better retrieval strategies and source-grounded response validation.

### 5. Handle Complex Legal Questions

Improve responses to questions involving multiple legal provisions and emergency situations, including drunk driving during a medical emergency.

### 6. Improve Source Citations

Provide more precise Act names, section numbers, PDF page references, and supporting passages.

### 7. Add Evaluation Metrics

Evaluate:

- Retrieval accuracy.
- Answer correctness.
- Faithfulness to sources.
- Citation accuracy.
- Response time.

---

## 📊 11. Project Status

| Component | Status |
|---|---|
| Python backend | Completed |
| PDF document loading | Completed |
| Document chunking | Completed |
| Sentence Transformer embeddings | Completed |
| FAISS vector database | Completed |
| OpenAI GPT-4o-mini integration | Completed |
| Streamlit frontend | Completed |
| Source reference display | Implemented |
| FAISS index caching | Implemented |
| Conversational memory | Planned |
| Hybrid search | Planned |
| Multiple legal documents | Planned |
| Automated legal updates | Planned |
| Comprehensive evaluation | Planned |

---

## 📚 12. What I Learned

This project provided practical experience with:

- Generative AI applications.
- Retrieval-Augmented Generation.
- Natural Language Processing.
- PDF document processing.
- Document chunking strategies.
- Text embeddings.
- Semantic similarity search.
- Vector databases.
- LangChain pipelines.
- OpenAI API integration.
- Prompt engineering.
- Streamlit frontend development.
- Python virtual environments.
- Git and GitHub version control.

---

## ⚖️ 13. Disclaimer

This project is intended for educational and informational purposes only.

The chatbot may produce incomplete, outdated, or incorrect information.

Users should verify important legal information against official legal sources and consult a qualified legal professional when necessary.

The application does not establish an attorney-client relationship.

---

## 👨‍💻 14. Developer

**GitHub:** [emino34](https://github.com/emino34)

**Project:** Indian Legal AI Assistant Using RAG

**Development Environment:** Python and Visual Studio Code

---

### ⭐ Support

If you find this project useful, consider starring the repository on GitHub.

Contributions and suggestions for improving retrieval accuracy, legal document coverage, and conversational capabilities are welcome.