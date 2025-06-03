import streamlit as st
import requests
import os

# Set custom page config and background color
st.set_page_config(page_title="Agentic PDF Chatbot", page_icon="🤖", layout="centered")

# Inject custom CSS for dark background and aesthetics
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #181818 !important;
        color: #f1f1f1 !important;
    }
    .stApp {
        background: linear-gradient(135deg, #181818 60%, #232526 100%);
    }
    .stTextInput > div > div > input {
        background: #232526 !important;
        color: #f1f1f1 !important;
        border-radius: 8px;
    }
    .stButton > button {
        background: #222 !important;
        color: #fff !important;
        border-radius: 8px;
        border: 1px solid #444;
        font-weight: bold;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background: #444 !important;
        color: #fff !important;
    }
    /* Custom drag-and-drop file uploader styling */
    .stFileUploader > div:first-child {
        border: 2px dashed #00c6ff !important;
        background: linear-gradient(135deg, #232526 60%, #1e2227 100%) !important;
        color: #f1f1f1 !important;
        border-radius: 16px !important;
        padding: 32px 0 32px 0 !important;
        box-shadow: 0 4px 24px 0 rgba(0,198,255,0.08);
        transition: border-color 0.3s;
        text-align: center;
    }
    .stFileUploader > div:first-child:hover {
        border-color: #00e6e6 !important;
        background: linear-gradient(135deg, #232526 40%, #00c6ff 100%) !important;
    }
    .stFileUploader label {
        color: #00c6ff !important;
        font-weight: bold;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    .stMarkdown, .stExpander, .stAlert, .stTextInput, .stFileUploader {
        background: transparent !important;
    }
    .stExpanderHeader {
        color: #f1f1f1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.markdown("<h1 style='text-align:center; color:#f1f1f1;'>🤖 Agentic PDF Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#aaa;'>Upload a PDF and ask questions. Answers are based on the document's content.</p>", unsafe_allow_html=True)

if 'session_id' not in st.session_state:
    st.session_state['session_id'] = None

st.markdown("---", unsafe_allow_html=True)
st.subheader("1. Upload a PDF", divider="rainbow")
pdf_file = st.file_uploader("Drag and drop or click to select a PDF file", type=["pdf"])

if pdf_file is not None and st.button("Upload PDF", use_container_width=True):
    files = {"file": (pdf_file.name, pdf_file, "application/pdf")}
    response = requests.post(f"{BACKEND_URL}/upload_pdf", files=files)
    if response.status_code == 200:
        st.session_state['session_id'] = response.json()['session_id']
        st.success("PDF uploaded and processed!")
    else:
        st.error("Failed to upload PDF.")

if st.session_state['session_id']:
    st.markdown("---", unsafe_allow_html=True)
    st.subheader("2. Ask a Question about the PDF", divider="rainbow")
    st.markdown("<label for='question_input' style='color:#00c6ff; font-weight:bold; font-size:1.1rem;'>Your question:</label>", unsafe_allow_html=True)
    question = st.text_input(" ", key="question_input", label_visibility="collapsed", placeholder="Type your question here...")
    if st.button("Ask", use_container_width=True) and question:
        data = {"session_id": st.session_state['session_id'], "question": question}
        response = requests.post(f"{BACKEND_URL}/ask", json=data)
        if response.status_code == 200:
            answer = response.json()['answer']
            st.markdown(f"<div style='background:#232526; border-radius:8px; padding:16px; margin-top:16px; color:#f1f1f1;'><b>Answer:</b> {answer}</div>", unsafe_allow_html=True)
            context = response.json().get('context', [])
            if context:
                with st.expander("Show context from PDF"):
                    for chunk in context:
                        st.write(chunk)
        else:
            st.error("Failed to get answer from backend.")
