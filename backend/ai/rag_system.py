from .embeddings import MultilingualEmbedder
from ..database.chromadb_setup import get_vector_client
import os

class NewsRAG:
    def __init__(self):
        self.embedder = MultilingualEmbedder()
        self.client = get_vector_client()
        self.collection = self.client.get_or_create_collection("news_articles")
        self.data_path = os.path.join(os.getcwd(), 'data', 'news')
        
    def add_documents(self, documents: list):
        embeddings = [self.embedder.embed(doc["content"]) for doc in documents]
        self.collection.add(
            ids=[str(doc["id"]) for doc in documents],
            embeddings=embeddings,
            documents=[doc["content"] for doc in documents],
            metadatas=[doc["metadata"] for doc in documents]
        )
        
    def query(self, question: str, k=3):
        query_embedding = self.embedder.embed(question)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results 