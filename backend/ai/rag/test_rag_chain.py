import asyncio
import logging
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(project_root)

from backend.ai.rag.chain import RAGChain

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

async def test_rag_chain():
    """
    Función principal para probar el RAG Chain con diferentes tipos de consultas
    """
    try:
        # Inicializar el RAG Chain
        rag = RAGChain(
            collection_name="travel_documents",
            model_name="gpt-3.5-turbo-0125",
            temperature=0.7
        )
        
        # Lista de consultas de prueba para diferentes tipos
        test_queries = [
            # Consultas de viaje
            {
                "query": "¿Cuáles son los mejores lugares para visitar en San Juan?",
                "type": "travel"
            },
            {
                "query": "¿Qué playas recomiendas visitar en Rincón?",
                "type": "travel"
            },
            # Consultas históricas
            {
                "query": "¿Cuál es la historia del Castillo San Felipe del Morro?",
                "type": "historical"
            },
            {
                "query": "¿Qué papel jugó Ponce en la historia de Puerto Rico?",
                "type": "historical"
            },
            # Consultas culturales
            {
                "query": "¿Cuáles son las tradiciones más importantes de Puerto Rico?",
                "type": "cultural"
            },
            {
                "query": "¿Qué platos típicos debo probar en Puerto Rico?",
                "type": "cultural"
            }
        ]
        
        # Procesar cada consulta
        for test_query in test_queries:
            logger.info(f"\nProcesando consulta: {test_query['query']}")
            logger.info(f"Tipo esperado: {test_query['type']}")
            
            try:
                result = await rag.process_query(
                    query=test_query['query'],
                    query_type=test_query['type']
                )
                
                logger.info("Respuesta obtenida:")
                logger.info(f"Tipo detectado: {result['query_type']}")
                logger.info(f"Documentos utilizados: {result['documents_used']}")
                logger.info(f"Fuentes: {result['sources']}")
                logger.info(f"Respuesta: {result['response']}\n")
                logger.info("-" * 80)
                
            except Exception as e:
                logger.error(f"Error procesando la consulta: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"Error general: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_rag_chain()) 