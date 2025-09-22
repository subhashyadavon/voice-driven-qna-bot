# rag_chain.py

from pinecone import Pinecone
from config import PINECONE_API_KEY, PINECONE_ENV
from vectorstore import index
from transformers import pipeline

# ---------------------------
# Setup Pinecone + HuggingFace LLM
# ---------------------------
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

# HuggingFace text-generation pipeline (small summarization / QA model)
# Swap with a bigger model like "tiiuae/falcon-7b-instruct" if you have GPU/VRAM
qa_pipeline = pipeline(
    "text2text-generation",
    model="facebook/bart-large-cnn"
)

# ---------------------------
# Helper: Chunking context
# ---------------------------
def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

# ---------------------------
# RAG query function
# ---------------------------
def query_rag(user_vector, user_text, top_k=5):
    """
    Retrieves relevant chunks from Pinecone and generates a concise answer using a local HuggingFace LLM.

    Args:
        user_vector: embedding vector of the query
        user_text: raw query text (string)
        top_k: number of top chunks to retrieve from Pinecone

    Returns:
        str: LLM-generated answer
    """
    # 1️⃣ Query Pinecone
    try:
        query_response = index.query(
            vector=user_vector,
            top_k=top_k,
            include_metadata=True
        )
        retrieved_texts = [match['metadata']['text'] for match in query_response.matches]
    except Exception as e:
        print("Pinecone query error:", e)
        return f"Failed to retrieve context for: {user_text}"

    if not retrieved_texts:
        return f"Sorry, I couldn’t find relevant info for: {user_text}"

    # 2️⃣ Build combined context
    context = "\n\n".join(retrieved_texts)

    # 3️⃣ Construct prompt instructing the LLM to avoid hallucinations
    prompt = (
        f"You are a helpful assistant. Use only the context below to answer the user's question. "
        f"If the answer is not present, respond with: 'I don't know.'\n\n"
        f"Context:\n{context}\n\nQuestion: {user_text}\nAnswer concisely:"
    )

    # 4️⃣ Run HuggingFace LLM
    try:
        result = qa_pipeline(prompt, max_length=300, do_sample=False)
        answer = result[0]['generated_text'].strip()
    except Exception as e:
        print("Local LLM error:", e)
        # fallback: return the retrieved context
        answer = f"Your question: {user_text}\n\nRelevant context:\n{context}"

    return answer



