"""
Utilidades para procesamiento de texto.
"""
import re
from typing import List, Optional
from sentence_transformers import SentenceTransformer

# Modelo para embeddings multilingüe
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
model = None  # Lazy loading

def get_embedding_model() -> SentenceTransformer:
    """
    Obtiene el modelo de embeddings, cargándolo si es necesario.
    
    Returns:
        Modelo de SentenceTransformer
    """
    global model
    if model is None:
        model = SentenceTransformer(MODEL_NAME)
    return model

def clean_text(text: str) -> str:
    """
    Limpia un texto eliminando caracteres especiales y espacios extra.
    
    Args:
        text: Texto a limpiar
        
    Returns:
        Texto limpio
    """
    # Eliminar caracteres especiales y espacios extra
    text = re.sub(r'[\n\r\t]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_into_chunks(text: str, max_length: int = 512) -> List[str]:
    """
    Divide un texto en chunks más pequeños respetando frases.
    
    Args:
        text: Texto a dividir
        max_length: Longitud máxima de cada chunk
        
    Returns:
        Lista de chunks de texto
    """
    # Dividir por oraciones
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence)
        if current_length + sentence_length <= max_length:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def create_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Crea embeddings para una lista de textos.
    
    Args:
        texts: Lista de textos
        
    Returns:
        Lista de embeddings (vectores)
    """
    model = get_embedding_model()
    return model.encode(texts).tolist()

def extract_dates(text: str) -> List[str]:
    """
    Extrae fechas de un texto usando expresiones regulares.
    
    Args:
        text: Texto del que extraer fechas
        
    Returns:
        Lista de fechas encontradas
    """
    # Patrones comunes de fechas
    patterns = [
        r'\d{1,2}/\d{1,2}/\d{2,4}',  # dd/mm/yyyy
        r'\d{4}-\d{2}-\d{2}',         # yyyy-mm-dd
        r'\d{1,2}\s+(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+(?:de\s+)?\d{4}',  # dd mes yyyy
    ]
    
    dates = []
    for pattern in patterns:
        dates.extend(re.findall(pattern, text, re.IGNORECASE))
    return dates
