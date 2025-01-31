"""
Script principal para procesar los datos de landmarks.
"""
import os
from pathlib import Path
from data_processing.processors.landmark_processor import LandmarkProcessor

def main():
    # Obtener directorios
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data" / "landmarks"
    output_dir = base_dir / "processed_data"
    
    # Verificar que existe el directorio de datos
    if not data_dir.exists():
        print(f"Error: Data directory not found at {data_dir}")
        return
    
    # Crear procesador
    processor = LandmarkProcessor(data_dir, output_dir)
    
    # Procesar landmarks
    print("Processing landmarks...")
    landmarks = processor.process_all_landmarks()
    
    # Crear base de datos de embeddings
    print("\nCreating embeddings database...")
    processor.create_embeddings_db(landmarks)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
