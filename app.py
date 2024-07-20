import streamlit as st
import fitz  # PyMuPDF
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Check environment variable
print("HF_TOKEN:", HF_TOKEN)

# Define the Hugging Face API endpoint
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def extract_text_from_pdf(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        pdf_document.close()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def chunk_text(text, chunk_size=1000):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def get_embeddings(texts, model):
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings

def create_faiss_index(embeddings):
    embeddings_np = embeddings.cpu().numpy()  # Move to CPU and convert to numpy
    dim = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dim)
    faiss_index = faiss.IndexIDMap(index)
    faiss_index.add_with_ids(embeddings_np, np.arange(len(embeddings_np)))
    return faiss_index

def query_faiss_index(index, query_embedding, k=5):
    query_embedding_np = query_embedding.cpu().numpy()  # Move to CPU and convert to numpy
    distances, indices = index.search(query_embedding_np, k)
    return distances, indices

def query_huggingface_api(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        generated_text = response.json()[0]['generated_text']
        # Extract only the final answer
        answer_start = generated_text.find("Answer: ")
        if answer_start != -1:
            answer = generated_text[answer_start + len("Answer: "):].strip()
        else:
            answer = generated_text
        return answer
    else:
        print(f"Error {response.status_code}: {response.text}")
        return "Error in API request"

# Initialize the sentence transformer model
model_name = 'all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

# Streamlit UI
st.title("NoteBot - Notes Retrieval System")
st.write("Upload PDFs and ask questions about their content.")

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    all_chunks = []
    for uploaded_file in uploaded_files:
        pdf_path = os.path.join("temp", uploaded_file.name)
        if not os.path.exists("temp"):
            os.makedirs("temp")
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    embeddings = get_embeddings(all_chunks, model)
    faiss_index = create_faiss_index(embeddings)
    
    query_text = st.text_input("Enter your query:")
    if query_text:
        query_embedding = get_embeddings([query_text], model)
        distances, indices = query_faiss_index(faiss_index, query_embedding)
        similar_chunks = [all_chunks[i] for i in indices[0]]

        # Ensure we only use a manageable number of chunks
        num_chunks_to_use = min(5, len(similar_chunks))
        selected_chunks = similar_chunks[:num_chunks_to_use]

        template = """Based on the following chunks: {similar_chunks}
        Question: {question}
        Answer:"""

        prompt_text = template.format(similar_chunks="\n".join(selected_chunks), question=query_text)
        
        # Generate response from Hugging Face API
        response = query_huggingface_api(prompt_text)
        
        st.write("**Answer:**", response)
