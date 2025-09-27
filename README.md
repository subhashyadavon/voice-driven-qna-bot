# 🎤 AI-Powered Chat Application with Speech Recognition & RAG  

An intelligent chat application that combines **speech-to-text**, **vector search**, and **retrieval-augmented generation (RAG)** to enable natural, voice-driven conversations. Users can interact via microphone or text, while the system leverages **OpenAI models, Pinecone, and LangChain** to provide contextual, AI-powered responses.  

---

## ✨ Key Features  
- **Speech-to-Text** – Uses `gpt-4o-mini-transcribe` for accurate, real-time transcription.  
- **Embeddings** – Converts text into vector representations using `all-mpnet-base-v2`.  
- **Vector Database** – Stores and retrieves semantic embeddings with **Pinecone**.  
- **Retrieval-Augmented Generation (RAG)** – Enhances LLM `facebook/bart-large-xsum`responses with context-aware retrieval.  
- **LangChain Integration** – Manages the RAG pipeline, prompt orchestration, and conversational flow.  
- **Hybrid Input** – Supports both typed messages and voice commands.  

---

## 🛠️ Tech Stack  
- **Speech Recognition:** OpenAI `gpt-4o-mini-transcribe`  
- **Embeddings:** `all-mpnet-base-v2`  
- **Vector Store:** Pinecone  
- **Frameworks & Tools:** LangChain, Python backend, HTML/CSS/JavaScript frontend  
- **Version Control:** Git  

---

## 🚀 How It Works  

1. **Voice Input** – User clicks mic → app records audio.  
2. **Speech-to-Text** – Audio is transcribed using `gpt-4o-mini-transcribe`.  
3. **Embedding** – Transcribed text is embedded into vector space with `all-mpnet-base-v2`.  
4. **Vector Retrieval** – Pinecone retrieves semantically relevant chunks.  
5. **RAG Pipeline** – LangChain combines retrieved context with user query.  
6. **LLM Response** – OpenAI (GPT) generates a context-aware reply.  
7. **Output** – Reply is displayed in chat UI.  

### Backend Setup (Python)  
```bash
git clone https://github.com/your-username/voice-driven-qna-bot.git
cd voice-driven-qna-bot
pip install -r requirements.txt
```

### Create a .env file with these in the parent directory:
```bash
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
```

### Run the application with:
```bash
python3 app.py
```

## Future Enchancements
1. Support multilingual transcription and embeddings.

2. Add session memory for long conversations.

3. Implement real-time voice replies (TTS).

4. Deploy as a Progressive Web App (PWA) for mobile use.

## License

This project is licensed under the [MIT License](./LICENSE).


