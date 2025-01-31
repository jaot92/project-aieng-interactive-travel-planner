import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENWEATHER_API_KEY = os.getenv("OWM_API_KEY")
    EMBEDDING_MODEL = os.getenv("RAG_EMBEDDING_MODEL")
    NEWS_CHUNK_SIZE = int(os.getenv("NEWS_CHUNK_SIZE", 512))
