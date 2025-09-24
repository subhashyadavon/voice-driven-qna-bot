# vectorstore.py
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_ENV
import hashlib

import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ---------------------------
# Initialize embedding model
# ---------------------------
embedding_model = SentenceTransformer("all-mpnet-base-v2")  # 768D

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
nltk.download("punkt")
nltk.download("stopwords")
def preprocess_and_chunk(text, chunk_size=300, overlap=150, language="english"):
    """
    Cleans, tokenizes, removes stopwords, and chunks text into overlapping windows.
    """
    # Lowercase and remove noise (non-alphabetic chars)
    text = re.sub(r"[^a-zA-Z\s]", " ", text.lower())

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words(language))
    tokens = [word for word in tokens if word not in stop_words]

    # Chunk with overlap
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunks.append(" ".join(tokens[start:end]))
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



