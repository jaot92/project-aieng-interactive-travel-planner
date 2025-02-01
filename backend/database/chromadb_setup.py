import chromadb
from chromadb.config import Settings

def get_vector_client():
    return chromadb.PersistentClient(
        path="./chroma_db"
    ) 