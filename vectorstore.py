# vectorstore.py
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_ENV
import hashlib


import re


from transformers import AutoTokenizer

# ---------------------------
# Initialize embedding model
# ---------------------------
embedding_model = SentenceTransformer("all-mpnet-base-v2")  # 768D
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-mpnet-base-v2")

# ---------------------------
# Initialize Pinecone
# ---------------------------
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

index_name = "my-index"
# Delete old index if exists
if "my-index" in pc.list_indexes().names():
    pc.delete_index("my-index")

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,  
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# ---------------------------
# Cleans, tokenizes, removes stopwords, and chunks text into overlapping windows.
# ---------------------------
# Download NLTK resources once

def preprocess_and_chunk(text, chunk_size=10, overlap=5):
    # Clean minimal noise
    text = re.sub(r"\s+", " ", text.strip())

    # Tokenize into mpnet tokens
    tokens = tokenizer.encode(text, add_special_tokens=False)

    # Sliding window chunking
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk = tokenizer.decode(tokens[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


# ---------------------------
# Create embeddings
# ---------------------------
def create_embeddings(text: str):
    """
    Splits text into cleaned chunks and generates embeddings locally.
    Returns a list of (id, vector, metadata).
    """
    chunks = preprocess_and_chunk(text)
    vectors = []

    for chunk in chunks:
        vector = embedding_model.encode(chunk).tolist()  # Local embedding
        uid = hashlib.sha256(chunk.encode("utf-8")).hexdigest()
        vectors.append((uid, vector, {"text": chunk}))

    return vectors

# ---------------------------
# Store into Pinecone
# ---------------------------
def store_vectors(vectors):
    """
    Inserts precomputed vectors into Pinecone.
    """
    if not vectors:
        print("No vectors to upsert.")
        return
    index.upsert(vectors)
    print(f"Upserted {len(vectors)} vectors into Pinecone.")



