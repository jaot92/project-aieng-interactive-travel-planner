"""
Procesador de noticias históricas de Puerto Rico.
"""
from typing import Dict, List, Optional, Tuple
import os
import logging
from pathlib import Path
from datetime import datetime

from .base_processor import BaseProcessor
from ..utils.text_utils import clean_text, create_embeddings, split_into_chunks
from ..utils.encoding_utils import normalize_filename

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsProcessor(BaseProcessor):
    """Procesa archivos de noticias históricas y los almacena en ChromaDB."""
    
    def __init__(self, data_dir: str = "data/elmundo_chunked_es_page1_40years", persist_directory: str = "chroma_db"):
        """
        Inicializa el procesador de noticias.
        
        Args:
            data_dir: Directorio que contiene los archivos de noticias
            persist_directory: Directorio para persistir los datos de ChromaDB
        """
        super().__init__(persist_directory=persist_directory)
        self.data_dir = data_dir
        
    def extract_date_info(self, filename: str) -> Tuple[str, str]:
        """
        Extrae la fecha y década de una noticia basado en su nombre de archivo.
        
        Args:
            filename: Nombre del archivo en formato YYYYMMDD_1.txt
            
        Returns:
            Tupla de (fecha_formateada, década)
        """
        try:
            # Extraer fecha del nombre del archivo
            date_str = filename.split('_')[0]
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            formatted_date = date_obj.strftime('%Y-%m-%d')
            decade = f"{date_str[:3]}0s"  # e.g., "1940s"
            return formatted_date, decade
        except Exception as e:
            logger.error(f"Error extrayendo fecha de {filename}: {str(e)}")
            return None, None
            
    def process_news_file(self, file_path: str) -> Optional[Dict]:
        """
        Procesa un archivo de noticias y extrae información relevante.
        
        Args:
            file_path: Ruta al archivo de noticias
            
        Returns:
            Dict con la información extraída o None si hay error
        """
        try:
            # Obtener información de la fecha del nombre del archivo
            filename = Path(file_path).name
            date, decade = self.extract_date_info(filename)
            if not date or not decade:
                return None
                
            # Leer el contenido del archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Limpiar el texto
            cleaned_content = clean_text(content)
            
            # Extraer título (primera línea después de limpiar)
            title = cleaned_content.split('\n')[0] if cleaned_content else "Sin título"
            
            # Preparar metadata
            metadata = {
                "date": date,
                "decade": decade,
                "title": title,
                "page": filename.split('_')[1].replace('.txt', ''),  # e.g., "1" from "_1.txt"
                "source": "El Mundo",
                "type": "news_article"
            }
            
            return {
                "content": cleaned_content,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error procesando archivo {file_path}: {str(e)}")
            return None
            
    def create_embeddings_db(self, force_reprocess: bool = False) -> bool:
        """
        Crea una base de datos de embeddings para las noticias.
        
        Args:
            force_reprocess: Si es True, reprocesa todos los archivos incluso si ya existen
            
        Returns:
            True si el proceso fue exitoso, False en caso contrario
        """
        try:
            # Verificar si la colección ya existe
            if not force_reprocess and self.collection_exists("news_articles"):
                logger.info("La colección de noticias ya existe. Usa force_reprocess=True para reprocesar.")
                return True
                
            # Crear o recuperar la colección
            collection = self.get_or_create_collection("news_articles")
            
            # Procesar cada archivo de noticias
            processed_count = 0
            for filename in os.listdir(self.data_dir):
                if not filename.endswith('.txt'):
                    continue
                    
                file_path = os.path.join(self.data_dir, filename)
                result = self.process_news_file(file_path)
                
                if result:
                    # Crear embeddings y almacenar en ChromaDB
                    collection.add(
                        documents=[result["content"]],
                        metadatas=[result["metadata"]],
                        ids=[f"news_{filename}"]
                    )
                    processed_count += 1
                    
                    if processed_count % 10 == 0:
                        logger.info(f"Procesadas {processed_count} noticias...")
            
            logger.info(f"Proceso completado. Se procesaron {processed_count} noticias.")
            return True
            
        except Exception as e:
            logger.error(f"Error creando base de datos de embeddings: {str(e)}")
            return False
