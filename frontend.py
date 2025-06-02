import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("Agentic PDF Chatbot")

if 'session_id' not in st.session_state:
    st.session_state['session_id'] = None

st.header("1. Upload a PDF")
pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if pdf_file is not None and st.button("Upload PDF"):
    files = {"file": (pdf_file.name, pdf_file, "application/pdf")}
    response = requests.post(f"{BACKEND_URL}/upload_pdf", files=files)
    if response.status_code == 200:
        st.session_state['session_id'] = response.json()['session_id']
        st.success("PDF uploaded and processed!")
    else:
        st.error("Failed to upload PDF.")

if st.session_state['session_id']:
    st.header("2. Ask a Question about the PDF")
    question = st.text_input("Your question:")
    if st.button("Ask") and question:
        data = {"session_id": st.session_state['session_id'], "question": question}
        response = requests.post(f"{BACKEND_URL}/ask", json=data)
        if response.status_code == 200:
            answer = response.json()['answer']
            st.markdown(f"**Answer:** {answer}")
            context = response.json().get('context', [])
            if context:
                with st.expander("Show context from PDF"):
                    for chunk in context:
                        st.write(chunk)
        else:
            st.error("Failed to get answer from backend.")
