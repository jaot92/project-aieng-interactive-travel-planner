import chromadb
from chromadb.config import Settings

def get_vector_client():
    return chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./chroma_db"
    )) 