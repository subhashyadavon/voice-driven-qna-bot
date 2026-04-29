# rag_chain.py

from pinecone import Pinecone
from config import PINECONE_API_KEY, PINECONE_ENV
from vectorstore import index
from transformers import pipeline

# ---------------------------
# Setup Pinecone
# ---------------------------
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

# ---------------------------
# Setup HuggingFace model
# ---------------------------
qa_pipeline = pipeline(
    "text2text-generation",
    model="facebook/bart-large-xsum"
)

# ---------------------------
# RAG query function
# ---------------------------
def query_rag(user_vector, user_text, top_k=5):
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

    context = "\n\n".join(retrieved_texts)

    prompt = f"Answer the user's question based ONLY on the context below:\n\nContext: {context}\n\nQuestion: {user_text}"

    try:
        result = qa_pipeline(prompt, max_new_tokens=150, do_sample=False)
        answer = result[0].get('summary_text', result[0].get('generated_text', context))
    except Exception as e:
        print("Local LLM error:", e)
        answer = context

    return answer
