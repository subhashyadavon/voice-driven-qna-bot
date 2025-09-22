# convert frontend audio to text using whisper
# speech_recognition.py

import openai
import tempfile
from config import OPENAI_API_KEY

# Configure OpenAI with the API key from config.py
openai.api_key = OPENAI_API_KEY

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribes audio using OpenAI Whisper API.

    Args:
        audio_bytes (bytes): Raw audio data (e.g., WebM, MP3, WAV).
    
    Returns:
        str: Transcribed text.
    """
    try:
        with tempfile.NamedTemporaryFile(suffix=".webm") as tmp:
            tmp.write(audio_bytes)
            tmp.flush()

            transcript = openai.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=open(tmp.name, "rb")
            )

        return transcript.text
    except Exception as e:
        print("Transcription error:", e)
        return ""
