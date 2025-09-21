# config.py
import os
from dotenv import load_dotenv

load_dotenv()  

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "")

if not OPENAI_API_KEY or not PINECONE_API_KEY or not PINECONE_ENV:
    raise RuntimeError("Missing OPENAI_API_KEY, PINECONE_API_KEY or PINECONE_ENV in .env")
