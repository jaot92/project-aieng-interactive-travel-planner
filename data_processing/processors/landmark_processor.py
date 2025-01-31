"""
Procesador de landmarks históricos de Puerto Rico.
"""
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
import chromadb
from chromadb.config import Settings

from data_processing.utils.html_utils import parse_html_file, extract_coordinates, extract_description, extract_categories
from data_processing.utils.text_utils import clean_text, create_embeddings, split_into_chunks
from data_processing.utils.geo_utils import is_within_bounds, PR_BOUNDS
from data_processing.utils.encoding_utils import normalize_filename

class LandmarkProcessor:
    def __init__(self, data_dir: str, output_dir: str):
        """
        Inicializa el procesador de landmarks.
        
        Args:
            data_dir: Directorio con los archivos HTML de landmarks
            output_dir: Directorio donde guardar los resultados
        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar ChromaDB
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=str(self.output_dir / "chromadb"),
            is_persistent=True
        ))
        self.collection = self.chroma_client.get_or_create_collection(
            name="landmarks",
            metadata={"description": "Landmarks históricos de Puerto Rico"}
        )
        
    def process_landmark_file(self, file_path: Path) -> Optional[Dict]:
        """
        Procesa un archivo de landmark individual.
        
        Args:
            file_path: Ruta al archivo HTML del landmark
            
        Returns:
            Dict con la información del landmark, o None si no se puede procesar
        """
        try:
            # Obtener nombre normalizado del landmark
            name = normalize_filename(file_path.stem.replace('_', ' '))
            
            # Parsear HTML
            soup = parse_html_file(str(file_path))
            
            # Extraer coordenadas
            coords = extract_coordinates(soup)
            if coords and not is_within_bounds(coords, PR_BOUNDS):
                print(f"Warning: {name} coordinates outside Puerto Rico bounds")
                coords = None
                
            # Extraer descripción
            description = extract_description(soup)
            if not description:
                print(f"Warning: No description found for {name}")
                return None
                
            # Extraer categorías
            categories = extract_categories(soup)
            
            # Convertir coordenadas a formato compatible con ChromaDB
            coords_dict = None
            if coords:
                coords_dict = {
                    "latitude": coords[0],
                    "longitude": coords[1]
                }
            
            return {
                "name": name,
                "coordinates": coords_dict,
                "description": description,
                "categories": categories,
                "source_file": str(file_path)
            }
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return None
            
    def process_all_landmarks(self) -> List[Dict]:
        """
        Procesa todos los archivos de landmarks en el directorio.
        
        Returns:
            List[Dict]: Lista de landmarks procesados
        """
        landmarks = []
        
        # Procesar cada archivo
        for file_path in self.data_dir.glob("*.txt"):
            if landmark := self.process_landmark_file(file_path):
                landmarks.append(landmark)
                
        print(f"\nProcessed {len(landmarks)} landmarks")
        return landmarks
        
    def create_embeddings_db(self, landmarks: List[Dict]):
        """
        Crea una base de datos de embeddings con los landmarks procesados.
        
        Args:
            landmarks: Lista de landmarks procesados
        """
        documents = []
        metadatas = []
        ids = []
        
        for i, landmark in enumerate(landmarks):
            # Dividir descripción en chunks si es muy larga
            chunks = split_into_chunks(landmark["description"])
            
            for j, chunk in enumerate(chunks):
                chunk_id = f"landmark_{i}_{j}"
                
                # Crear metadata para el chunk
                metadata = {
                    "name": landmark["name"],
                    "categories": ", ".join(landmark["categories"][:5]),  # Limitar a 5 categorías principales
                    "chunk_index": j,
                    "total_chunks": len(chunks)
                }
                
                # Añadir coordenadas si existen
                if landmark["coordinates"]:
                    metadata.update({
                        "latitude": landmark["coordinates"]["latitude"],
                        "longitude": landmark["coordinates"]["longitude"]
                    })
                
                documents.append(chunk)
                metadatas.append(metadata)
                ids.append(chunk_id)
        
        # Crear embeddings y guardar en ChromaDB
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"\nCreated embeddings database with {len(documents)} entries") 