"""
Script para probar consultas a la base de datos de embeddings.
"""
import chromadb
from chromadb.config import Settings
from pathlib import Path
from data_processing.utils.text_utils import create_embeddings

def load_collection():
    """Carga la colección de landmarks desde ChromaDB."""
    output_dir = Path(__file__).parent.parent / "processed_data"
    client = chromadb.Client(Settings(
        persist_directory=str(output_dir / "chromadb"),
        is_persistent=True
    ))
    return client.get_collection("landmarks")

def semantic_search(collection, query: str, n_results: int = 5):
    """
    Realiza una búsqueda semántica en la colección.
    
    Args:
        collection: Colección de ChromaDB
        query: Consulta en texto natural
        n_results: Número de resultados a retornar
    """
    print(f"\nConsulta: '{query}'")
    print("-" * 50)
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["metadatas", "documents", "distances"]
    )
    
    for i, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    )):
        print(f"\nResultado {i+1} (distancia: {distance:.4f}):")
        print(f"Nombre: {metadata.get('name', 'N/A')}")
        if coords := metadata.get('coordinates'):
            print(f"Coordenadas: {coords}")
        print(f"Categorías: {metadata.get('categories', [])}")
        print(f"Texto: {doc[:200]}...")
        print("-" * 50)

def main():
    # Cargar colección
    collection = load_collection()
    
    # Ejemplos de consultas
    queries = [
        "Lugares históricos en San Juan con arquitectura colonial española",
        "Playas con aguas cristalinas y arena blanca",
        "Sitios relacionados con la cultura taína y los indígenas",
        "Parques naturales con buenas rutas de senderismo",
        "Museos de arte y cultura en Puerto Rico"
    ]
    
    # Realizar consultas
    for query in queries:
        semantic_search(collection, query)

if __name__ == "__main__":
    main() 