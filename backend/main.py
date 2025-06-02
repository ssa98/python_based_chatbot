from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

sys.path.append("/workspaces/python_based_chatbot/backend")

from pdf_processor import extract_text_from_pdf
from embedder import get_embeddings
from vector_store import store_embeddings, query_embeddings
from llm_interface import generate_answer

app = FastAPI()

# In-memory store for uploaded PDF content and embeddings (for demo)
pdf_text_store = {}
pdf_embedding_store = {}

class AskRequest(BaseModel):
    session_id: str
    question: str

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    session_id = os.urandom(8).hex()
    content = await file.read()
    text = extract_text_from_pdf(content)
    embeddings = get_embeddings(text)
    store_embeddings(session_id, embeddings, text)
    pdf_text_store[session_id] = text
    pdf_embedding_store[session_id] = embeddings
    return {"session_id": session_id, "message": "PDF processed and stored."}

@app.post("/ask")
async def ask_question(request: AskRequest):
    session_id = request.session_id
    question = request.question
    if session_id not in pdf_embedding_store:
        return JSONResponse(status_code=404, content={"error": "Session not found."})
    relevant_chunks = query_embeddings(session_id, question)
    answer = generate_answer(question, relevant_chunks)
    return {"answer": answer, "context": relevant_chunks}
