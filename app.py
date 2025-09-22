# app.py

from flask import Flask, render_template, request, jsonify
from speech_recognition import transcribe_audio
from vectorstore import embed_and_store
from sentence_transformers import SentenceTransformer
from rag_chain import query_rag
import requests
from bs4 import BeautifulSoup
import io
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)

# Initialize embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------
# Upload document or URL
# ---------------------------
@app.route("/upload", methods=["POST"])
def upload_document():
    try:
        file = request.files.get("file")
        url = request.form.get("url")
        text_data = ""

        # Handle file uploads
        if file:
            filename = file.filename.lower()
            content = file.read()

            if filename.endswith(".txt"):
                text_data = content.decode("utf-8", errors="ignore")

            elif filename.endswith(".pdf"):
                pdf_reader = PdfReader(io.BytesIO(content))
                text_data = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)

            elif filename.endswith(".docx"):
                doc = docx.Document(io.BytesIO(content))
                text_data = "\n".join([p.text for p in doc.paragraphs])

            else:
                # fallback: try decoding as text
                text_data = content.decode("utf-8", errors="ignore")

        # Handle URLs
        elif url:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            text_data = soup.get_text(separator="\n")

        else:
            return jsonify({"message": "No file or URL provided"}), 400

        # Send text to vectorstore (store embeddings in Pinecone)
        embed_and_store(text_data)

        return jsonify({"message": "Document successfully uploaded and embedded!"})

    except Exception as e:
        print("Upload error:", e)
        return jsonify({"message": f"Error: {e}"}), 500


# ---------------------------
# Query: audio or text
# ---------------------------
@app.route("/query", methods=["POST"])
def handle_query():
    text = ""
    audio_file = request.files.get("audio")

    if audio_file:
        text = transcribe_audio(audio_file.read())
        if not text:
            return jsonify({"message": "Failed to transcribe audio"}), 500

    elif request.is_json:
        data = request.get_json()
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"message": "Empty text received"}), 400

    else:
        return jsonify({"message": "No text or audio provided"}), 400

    # embedding
    vector = embedding_model.encode(text).tolist()

    # local RAG (no OpenAI)
    try:
        answer = query_rag(vector, text)
    except Exception as e:
        print("Local RAG error:", e)
        return jsonify({"message": f"RAG query failed: {e}"}), 500

    return jsonify({"answer": answer})





if __name__ == "__main__":
    app.run(debug=True, port=50018)



