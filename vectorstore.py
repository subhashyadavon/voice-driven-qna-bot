# vectorstore.py

from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_ENV
import hashlib

# ---------------------------
# Initialize embedding model
# ---------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

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
        dimension=384,  # all-MiniLM-L6-v2 outputs 384-dimensional vectors
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# ---------------------------
# Helper: split text into chunks
# ---------------------------
def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into overlapping chunks.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks

# ---------------------------
# Main: embed and store
# ---------------------------
def embed_and_store(text: str):
    """
    Splits text into chunks, generates embeddings locally, and inserts into Pinecone.
    """
    chunks = chunk_text(text)
    vectors_to_upsert = []

    for chunk in chunks:
        vector = embedding_model.encode(chunk).tolist()  # Local embedding
        uid = hashlib.sha256(chunk.encode("utf-8")).hexdigest()
        vectors_to_upsert.append((uid, vector, {"text": chunk}))

    # Upsert all vectors into Pinecone
    index.upsert(vectors_to_upsert)


