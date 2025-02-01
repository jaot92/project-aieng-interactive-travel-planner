from typing import Dict, Any, Optional, List
import logging
from backend.ai.rag.retriever import RAGRetriever
from backend.ai.rag.llm_interface import LLMInterface
from backend.ai.rag.prompt_templates import TravelQueryTemplate, HistoricalQueryTemplate, CulturalQueryTemplate, PromptTemplate

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGChain:
    """
    Clase principal que implementa la cadena completa de RAG (Retrieval-Augmented Generation).
    Coordina la recuperación de documentos, generación de prompts y la interacción con el LLM.
    """
    
    def __init__(
        self,
        collection_name: str = "travel_documents",
        model_name: str = "gpt-3.5-turbo-0125",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        Inicializa la cadena RAG.
        
        Args:
            collection_name (str): Nombre de la colección en ChromaDB
            model_name (str): Nombre del modelo de lenguaje a utilizar
            temperature (float): Temperatura para la generación de texto
            max_tokens (int): Número máximo de tokens en la respuesta
        """
        self.retriever = RAGRetriever(collection_name=collection_name)
        self.llm = LLMInterface(model_name=model_name)
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Inicializar plantillas
        self.templates = {
            'travel': TravelQueryTemplate(),
            'historical': HistoricalQueryTemplate(),
            'cultural': CulturalQueryTemplate()
        }
        
        logger.info(f"RAGChain inicializada con colección '{collection_name}' y modelo '{model_name}'")
    
    def _get_template(self, query_type: str) -> PromptTemplate:
        """
        Selecciona la plantilla apropiada según el tipo de consulta.
        
        Args:
            query_type (str): Tipo de consulta ('travel', 'historical', 'cultural')
            
        Returns:
            PromptTemplate: La plantilla correspondiente
        """
        if query_type not in self.templates:
            raise ValueError(f"Tipo de consulta no válido: {query_type}")
        return self.templates[query_type]
    
    def _classify_query(self, query: str) -> str:
        """
        Clasifica la consulta en uno de los tipos disponibles.
        
        Args:
            query (str): La consulta del usuario
            
        Returns:
            str: El tipo de consulta identificado
        """
        # Por ahora, una implementación simple basada en palabras clave
        # TODO: Implementar una clasificación más sofisticada
        query = query.lower()
        
        if any(word in query for word in ['visitar', 'viajar', 'turismo', 'hotel', 'restaurante', 'playa']):
            return 'travel'
        elif any(word in query for word in ['historia', 'histórico', 'pasado', 'evento', 'guerra', 'independencia']):
            return 'historical'
        elif any(word in query for word in ['cultura', 'tradición', 'costumbre', 'festival', 'música', 'comida']):
            return 'cultural'
            
        # Por defecto, usar la plantilla de viajes
        return 'travel'
    
    async def process_query(
        self,
        query: str,
        query_type: Optional[str] = None,
        n_documents: int = 3
    ) -> str:
        """
        Procesa una consulta del usuario utilizando la cadena RAG.
        
        Args:
            query (str): La consulta del usuario
            query_type (Optional[str]): Tipo de consulta (si se conoce)
            n_documents (int): Número de documentos a recuperar
            
        Returns:
            str: La respuesta generada
        """
        try:
            # Determinar el tipo de consulta si no se proporciona
            if query_type is None:
                query_type = self._classify_query(query)
            
            # Obtener la plantilla apropiada
            template = self._get_template(query_type)
            
            # Recuperar documentos relevantes
            documents = self.retriever.retrieve(query, n_results=n_documents)
            
            # Formatear el contexto
            context = "\n\n".join([
                f"Documento {i+1}:\n{doc['document']}\nFuente: {doc['metadata'].get('source', 'Desconocida')}"
                for i, doc in enumerate(documents)
            ])
            
            # Obtener la respuesta del LLM
            response = await self.llm.generate_response(
                prompt=query,
                context=documents,
                system_prompt=template.get_system_prompt(),
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            logger.info(f"Consulta procesada exitosamente. Tipo: {query_type}")
            return response
            
        except Exception as e:
            logger.error(f"Error al procesar la consulta: {str(e)}")
            raise
