import streamlit as st
import os

from pdf_processing import extract_text_from_pdf
from youtube_processing import extract_text_from_youtube
from faiss_indexing import get_embeddings, create_faiss_index, query_faiss_index
from utils import load_environment_variables, query_huggingface_api, chunk_text
from pdf_generator import generate_pdf
from text_to_speech import speak_text
from sentence_transformers import SentenceTransformer

# Load environment variables
hf_token = load_environment_variables()
if not hf_token:
    st.error("Hugging Face API token is missing. Please add it to your .env file.")
    st.stop()

# Define the Hugging Face API endpoint
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {
    "Authorization": f"Bearer {hf_token}"
}

# Initialize the sentence transformer model
model_name = 'all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

# Streamlit UI
st.title("NoteBot - Notes Retrieval System")
st.write("By - Aditya Goyal")
st.write("Upload PDFs or provide YouTube links to ask questions about their content.")

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
youtube_url = st.text_input("Enter YouTube video URL:")

all_chunks = []

# Process PDF files
if uploaded_files:
    for uploaded_file in uploaded_files:
        pdf_path = os.path.join("temp", uploaded_file.name)
        if not os.path.exists("temp"):
            os.makedirs("temp")
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

# Process YouTube video
if youtube_url:
    yt_text = extract_text_from_youtube(youtube_url)
    yt_chunks = chunk_text(yt_text)
    all_chunks.extend(yt_chunks)

if all_chunks:
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
        response = query_huggingface_api(prompt_text, API_URL, headers)
        
        if "Error" not in response:
            st.write("**Answer:**", response)

            # Add button to download response as PDF
            if st.button("Download Response as PDF"):
                pdf_path = os.path.join("temp", "response.pdf")
                generate_pdf(response, pdf_path)
                with open(pdf_path, "rb") as f:
                    st.download_button(label="Download PDF", data=f, file_name="response.pdf")

            # Add button to speak the response text
            if st.button("Speak Response"):
                speak_text(response)
        else:
            st.error(response)
