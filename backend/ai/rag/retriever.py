from typing import List, Dict, Any
import logging
from ..embeddings import MultilingualEmbedder
from ...database.chromadb_setup import get_vector_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGRetriever:
    def __init__(self, collection_name: str = "travel_documents"):
        """
        Inicializa el retriever con el cliente de ChromaDB y el modelo de embeddings.
        
        Args:
            collection_name (str): Nombre de la colección en ChromaDB
        """
        self.embedder = MultilingualEmbedder()
        self.client = get_vector_client()
        self.collection_name = collection_name
        
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embedder
            )
            logger.info(f"Conectado exitosamente a la colección {collection_name}")
        except Exception as e:
            logger.error(f"Error al conectar con la colección {collection_name}: {str(e)}")
            raise

    def retrieve(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Recupera los documentos más relevantes para una consulta dada.
        
        Args:
            query (str): La consulta del usuario
            n_results (int): Número de resultados a retornar
            
        Returns:
            List[Dict[str, Any]]: Lista de documentos relevantes con sus metadatos
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # Formatear los resultados para facilitar su uso
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
            
            logger.info(f"Recuperados {len(formatted_results)} documentos para la consulta: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error al recuperar documentos para la consulta {query}: {str(e)}")
            raise

    def get_collection_stats(self) -> Dict[str, int]:
        """
        Obtiene estadísticas básicas de la colección.
        
        Returns:
            Dict[str, int]: Diccionario con estadísticas de la colección
        """
        try:
            count = self.collection.count()
            return {
                "total_documents": count
            }
        except Exception as e:
            logger.error(f"Error al obtener estadísticas de la colección: {str(e)}")
            raise
