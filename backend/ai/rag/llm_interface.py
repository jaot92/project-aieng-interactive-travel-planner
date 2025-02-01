from typing import Dict, Any, Optional, List
import logging
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

class LLMInterface:
    """
    Interfaz para interactuar con el modelo de lenguaje de OpenAI.
    Maneja la generación de respuestas y el conteo de tokens.
    """
    
    def __init__(self, model_name: str = "gpt-3.5-turbo-0125"):
        """
        Inicializa la interfaz del LLM.
        
        Args:
            model_name (str): Nombre del modelo a utilizar
        """
        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("No se encontró la clave de API de OpenAI en las variables de entorno")
            
        self.client = AsyncOpenAI(api_key=self.api_key)
        logger.info(f"LLMInterface inicializada con modelo {model_name}")
    
    async def generate_response(
        self,
        prompt: str,
        context: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Genera una respuesta utilizando el modelo de lenguaje.
        
        Args:
            prompt (str): La consulta del usuario
            context (List[Dict[str, Any]]): Lista de documentos relevantes
            system_prompt (Optional[str]): Prompt del sistema para guiar al modelo
            temperature (float): Temperatura para la generación de texto
            max_tokens (int): Número máximo de tokens en la respuesta
            
        Returns:
            str: La respuesta generada por el modelo
        """
        try:
            # Formatear el contexto
            formatted_context = "\n\n".join([
                f"Documento {i+1}:\n{doc['document']}\nFuente: {doc['metadata'].get('source', 'Desconocida')}"
                for i, doc in enumerate(context)
            ])
            
            # Construir los mensajes
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user",
                "content": f"Contexto:\n{formatted_context}\n\nPregunta: {prompt}"
            })
            
            # Realizar la llamada a la API de forma asíncrona
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extraer y retornar la respuesta
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error al generar respuesta: {str(e)}")
            raise
    
    def get_token_count(self, text: str) -> int:
        """
        Estima el número de tokens en un texto.
        Esta es una estimación aproximada basada en palabras.
        
        Args:
            text (str): El texto a analizar
            
        Returns:
            int: Número estimado de tokens
        """
        # Estimación simple: aproximadamente 4 caracteres por token
        return len(text) // 4 