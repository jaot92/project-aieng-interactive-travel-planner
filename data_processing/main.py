"""
Script principal para procesar los datos.
"""
import argparse
import logging
from .processors.landmark_processor import LandmarkProcessor
from .processors.municipality_processor import MunicipalityProcessor
from .processors.news_processor import NewsProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_landmarks(force_reprocess: bool = False):
    """Procesa los landmarks históricos."""
    logger.info("Procesando landmarks...")
    processor = LandmarkProcessor()
    processor.create_embeddings_db(force_reprocess=force_reprocess)

def process_municipalities(force_reprocess: bool = False):
    """Procesa los municipios."""
    logger.info("\nProcesando municipios...")
    processor = MunicipalityProcessor()
    processor.create_embeddings_db(force_reprocess=force_reprocess)

def process_news(force_reprocess: bool = False):
    """Procesa las noticias históricas."""
    logger.info("\nProcesando noticias históricas...")
    processor = NewsProcessor()
    processor.create_embeddings_db(force_reprocess=force_reprocess)

def main():
    parser = argparse.ArgumentParser(description='Procesa datos para el planificador de viajes.')
    parser.add_argument('--landmarks', action='store_true', help='Procesar landmarks')
    parser.add_argument('--municipalities', action='store_true', help='Procesar municipios')
    parser.add_argument('--news', action='store_true', help='Procesar noticias históricas')
    parser.add_argument('--force', action='store_true', help='Forzar reprocesamiento aunque existan datos')
    parser.add_argument('--all', action='store_true', help='Procesar todos los tipos de datos')
    
    args = parser.parse_args()
    
    # Si no se especifica ningún argumento, mostrar ayuda
    if not (args.landmarks or args.municipalities or args.news or args.all):
        parser.print_help()
        return
    
    # Procesar según los argumentos
    if args.all or args.landmarks:
        process_landmarks(force_reprocess=args.force)
    
    if args.all or args.municipalities:
        process_municipalities(force_reprocess=args.force)
    
    if args.all or args.news:
        process_news(force_reprocess=args.force)
    
    logger.info("\n¡Procesamiento completado!")

if __name__ == "__main__":
    main()
