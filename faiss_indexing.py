import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

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
