# Backend for Agentic Python-based AI Chatbot

This backend provides the core logic for a chatbot that reads, understands, and answers questions based on PDF content.

## Requirements

### 1. Python Packages
- fastapi
- uvicorn
- PyPDF2 or pdfplumber
- sentence-transformers
- faiss-cpu or chromadb
- openai (optional, for GPT integration)
- pydantic
- python-multipart (for file uploads)

### 2. API Endpoints
- `/upload_pdf` (POST): Accepts a PDF file upload, processes and stores its content.
- `/ask` (POST): Accepts a user query and returns an answer based on the uploaded PDF.

### 3. Backend Components
- **PDF Processor:** Extracts and preprocesses text from PDF files.
- **Embedding Engine:** Converts text into embeddings for semantic search.
- **Vector Store:** Stores and retrieves embeddings for context retrieval.
- **LLM Interface:** Generates answers using a language model (local or API-based).

### 4. Data Flow
1. User uploads a PDF via `/upload_pdf`.
2. Backend extracts and embeds the content, storing it in the vector store.
3. User sends a query to `/ask`.
4. Backend retrieves relevant PDF sections, sends them to the LLM, and returns the answer.

### 5. Example Directory Structure
```
backend/
├── main.py              # FastAPI app
├── pdf_processor.py     # PDF extraction logic
├── embedder.py          # Embedding logic
├── vector_store.py      # Vector DB logic
├── llm_interface.py     # LLM integration
├── requirements.txt     # Python dependencies
```

---

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the server: `uvicorn main:app --reload`
3. Use `/upload_pdf` to upload a PDF, then `/ask` to query.

---

This backend is modular and can be extended for additional features, security, and scalability.
