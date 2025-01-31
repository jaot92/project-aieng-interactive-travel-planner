"""
Motor de consultas para landmarks y municipios.
"""
import chromadb
from chromadb.utils import embedding_functions
from typing import Dict, List, Optional, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryEngine:
    """Motor de consultas para interactuar con la base de datos de landmarks y municipios."""
    
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Inicializa el motor de consultas.
        
        Args:
            persist_directory: Directorio donde se encuentra la base de datos ChromaDB
        """
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        )
        
        # Obtener las colecciones
        self.landmarks = self.client.get_collection(
            name="landmarks",
            embedding_function=self.embedding_function
        )
        self.municipalities = self.client.get_collection(
            name="municipalities",
            embedding_function=self.embedding_function
        )
    
    def search_landmarks(
        self,
        query: str,
        n_results: int = 5,
        min_score: float = 0.0
    ) -> List[Dict]:
        """
        Busca landmarks que coincidan con la consulta.
        
        Args:
            query: Texto de búsqueda
            n_results: Número máximo de resultados
            min_score: Puntuación mínima de similitud (0-1)
            
        Returns:
            Lista de landmarks encontrados con sus metadatos
        """
        try:
            results = self.landmarks.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Procesar resultados
            landmarks = []
            for i in range(len(results['ids'][0])):
                landmarks.append({
                    'id': results['ids'][0][i],
                    'name': results['metadatas'][0][i]['name'],
                    'description': results['documents'][0][i],
                    'categories': results['metadatas'][0][i]['categories'].split(', '),
                    'coordinates': {
                        'latitude': float(results['metadatas'][0][i]['latitude']) if results['metadatas'][0][i]['latitude'] else None,
                        'longitude': float(results['metadatas'][0][i]['longitude']) if results['metadatas'][0][i]['longitude'] else None
                    }
                })
            
            return landmarks
            
        except Exception as e:
            logger.error(f"Error buscando landmarks: {str(e)}")
            return []
    
    def search_municipalities(
        self,
        query: str,
        n_results: int = 5,
        min_score: float = 0.0
    ) -> List[Dict]:
        """
        Busca municipios que coincidan con la consulta.
        
        Args:
            query: Texto de búsqueda
            n_results: Número máximo de resultados
            min_score: Puntuación mínima de similitud (0-1)
            
        Returns:
            Lista de municipios encontrados con sus metadatos
        """
        try:
            results = self.municipalities.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Procesar resultados
            municipalities = []
            for i in range(len(results['ids'][0])):
                municipalities.append({
                    'id': results['ids'][0][i],
                    'name': results['metadatas'][0][i]['name'],
                    'description': results['documents'][0][i],
                    'categories': results['metadatas'][0][i]['categories'].split(', '),
                    'coordinates': {
                        'latitude': float(results['metadatas'][0][i]['latitude']) if results['metadatas'][0][i]['latitude'] else None,
                        'longitude': float(results['metadatas'][0][i]['longitude']) if results['metadatas'][0][i]['longitude'] else None
                    }
                })
            
            return municipalities
            
        except Exception as e:
            logger.error(f"Error buscando municipios: {str(e)}")
            return []
    
    def get_nearby_landmarks(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 10.0,
        max_results: int = 5
    ) -> List[Dict]:
        """
        Encuentra landmarks cercanos a unas coordenadas dadas.
        
        Args:
            latitude: Latitud del punto central
            longitude: Longitud del punto central
            radius_km: Radio de búsqueda en kilómetros
            max_results: Número máximo de resultados
            
        Returns:
            Lista de landmarks cercanos ordenados por distancia
        """
        # TODO: Implementar búsqueda por proximidad usando las coordenadas
        pass
    
    def get_recommendations(
        self,
        categories: List[str],
        n_results: int = 5
    ) -> List[Dict]:
        """
        Obtiene recomendaciones de landmarks basadas en categorías.
        
        Args:
            categories: Lista de categorías de interés
            n_results: Número de recomendaciones
            
        Returns:
            Lista de landmarks recomendados
        """
        # TODO: Implementar sistema de recomendaciones basado en categorías
        pass 