"""
Script para probar la recuperación de noticias de ChromaDB.
"""
import chromadb
from chromadb.utils import embedding_functions
import json

def main():
    # Inicializar el cliente de ChromaDB
    client = chromadb.PersistentClient(path="chroma_db")
    
    # Usar la misma función de embedding que usamos para procesar
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    )
    
    # Obtener la colección de noticias
    collection = client.get_collection(
        name="news_articles",
        embedding_function=embedding_function
    )
    
    # Obtener una noticia específica (usaremos la primera)
    results = collection.get(
        limit=1,
        include=['metadatas', 'documents']
    )
    
    # Imprimir los resultados de forma legible
    print("\n=== Metadata de la noticia ===")
    print(json.dumps(results['metadatas'][0], indent=2, ensure_ascii=False))
    
    print("\n=== Primeras líneas del contenido ===")
    content_preview = results['documents'][0].split('\n')[:5]
    for line in content_preview:
        print(line)

if __name__ == "__main__":
    main() 