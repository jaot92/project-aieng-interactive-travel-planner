"""
Base processor for all data types.
"""
import os
from pathlib import Path
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseProcessor:
    """Base class for all processors with common ChromaDB functionality."""
    
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Initialize the base processor.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.persist_directory = persist_directory
        self._ensure_persist_directory()
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize the multilingual embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        )
    
    def _ensure_persist_directory(self):
        """Ensure the persistence directory exists."""
        os.makedirs(self.persist_directory, exist_ok=True)
    
    def get_or_create_collection(self, collection_name: str):
        """
        Get an existing collection or create a new one.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            ChromaDB collection
        """
        try:
            # Try to get existing collection
            collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            logger.info(f"Using existing collection: {collection_name}")
        except:
            # Create new collection if it doesn't exist
            collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            logger.info(f"Created new collection: {collection_name}")
        
        return collection
    
    def collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists.
        
        Args:
            collection_name: Name of the collection to check
            
        Returns:
            bool: True if collection exists, False otherwise
        """
        try:
            self.client.get_collection(name=collection_name)
            return True
        except:
            return False
    
    def get_collection_count(self, collection_name: str) -> int:
        """
        Get the number of items in a collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            int: Number of items in collection
        """
        try:
            collection = self.client.get_collection(name=collection_name)
            return collection.count()
        except:
            return 0 