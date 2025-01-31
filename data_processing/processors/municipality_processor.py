"""
Procesador de municipios de Puerto Rico.
"""
from typing import Dict, List, Optional, Tuple
import os
import logging
from pathlib import Path

from .base_processor import BaseProcessor
from ..utils.html_utils import (
    parse_html_file,
    extract_coordinates,
    extract_description,
    extract_categories
)
from ..utils.encoding_utils import normalize_filename, clean_text
from ..utils.geo_utils import is_within_puerto_rico

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MunicipalityProcessor(BaseProcessor):
    """Procesa archivos HTML de municipios y los almacena en ChromaDB."""
    
    def __init__(self, data_dir: str = "data/municipalities", persist_directory: str = "chroma_db"):
        """
        Inicializa el procesador de municipios.
        
        Args:
            data_dir: Directorio que contiene los archivos HTML de municipios
            persist_directory: Directorio para persistir los datos de ChromaDB
        """
        super().__init__(persist_directory=persist_directory)
        self.data_dir = data_dir
        
    def process_municipality_file(self, file_path: str) -> Optional[Dict]:
        """
        Procesa un archivo HTML de municipio y extrae información relevante.
        
        Args:
            file_path: Ruta al archivo HTML del municipio
            
        Returns:
            Dict con la información extraída o None si hay error
        """
        try:
            # Obtener el nombre del municipio del nombre del archivo
            municipality_name = normalize_filename(Path(file_path).stem)
            
            # Parsear el HTML
            soup = parse_html_file(file_path)
            if not soup:
                logger.warning(f"No se pudo parsear el archivo {file_path}")
                return None
                
            # Extraer coordenadas
            coords = extract_coordinates(soup)
            if coords:
                lat, lon = coords
                if not is_within_puerto_rico(lat, lon):
                    logger.warning(f"Coordenadas de {municipality_name} fuera de Puerto Rico")
            
            # Extraer descripción
            description = extract_description(soup)
            if not description:
                logger.warning(f"No se encontró descripción para {municipality_name}")
                return None
                
            # Extraer categorías
            categories = extract_categories(soup)
            
            # Crear diccionario con la información
            municipality_info = {
                "name": municipality_name,
                "description": description,
                "categories": categories,
                "coordinates": {"latitude": lat, "longitude": lon} if coords else None
            }
            
            return municipality_info
            
        except Exception as e:
            logger.error(f"Error procesando {file_path}: {str(e)}")
            return None
            
    def create_embeddings_db(self, collection_name: str = "municipalities", force_reprocess: bool = False) -> None:
        """
        Crea una base de datos de embeddings con ChromaDB para los municipios.
        
        Args:
            collection_name: Nombre de la colección en ChromaDB
            force_reprocess: Si es True, reprocesa aunque la colección exista
        """
        try:
            # Verificar si la colección ya existe y tiene datos
            if not force_reprocess and self.collection_exists(collection_name):
                count = self.get_collection_count(collection_name)
                if count > 0:
                    logger.info(f"La colección {collection_name} ya existe con {count} elementos")
                    return
            
            # Obtener o crear la colección
            collection = self.get_or_create_collection(collection_name)
            
            # Procesar cada archivo
            processed_count = 0
            for filename in os.listdir(self.data_dir):
                if not filename.endswith('.txt'):
                    continue
                    
                file_path = os.path.join(self.data_dir, filename)
                municipality_info = self.process_municipality_file(file_path)
                
                if not municipality_info:
                    continue
                
                # Preparar datos para ChromaDB
                collection.add(
                    documents=[municipality_info["description"]],
                    metadatas=[{
                        "name": municipality_info["name"],
                        "categories": ", ".join(municipality_info["categories"][:5]) if municipality_info["categories"] else "",
                        "latitude": str(municipality_info["coordinates"]["latitude"]) if municipality_info["coordinates"] else "",
                        "longitude": str(municipality_info["coordinates"]["longitude"]) if municipality_info["coordinates"] else ""
                    }],
                    ids=[f"municipality_{municipality_info['name']}"]
                )
                
                processed_count += 1
                logger.info(f"Procesado {municipality_info['name']}")
            
            logger.info(f"Procesados {processed_count} municipios")
            
        except Exception as e:
            logger.error(f"Error creando base de datos de embeddings: {str(e)}")
            raise
