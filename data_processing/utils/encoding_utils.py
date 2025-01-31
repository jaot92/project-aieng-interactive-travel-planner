"""
Utilidades para manejar la codificación de caracteres y normalización de texto.
"""
import unicodedata
import chardet
from typing import Dict, Optional

def normalize_filename(filename: str) -> str:
    """
    Normaliza el nombre del archivo, corrigiendo caracteres especiales.
    
    Args:
        filename: Nombre del archivo a normalizar
        
    Returns:
        str: Nombre del archivo normalizado
    """
    # Mapa de reemplazos para caracteres especiales comunes
    replacements = {
        '‚': 'e',  # Para é
        'ค': 'n',  # Para ñ
        '¡': 'i',  # Para í
        '¤': 'n',  # Para ñ
        '｣': 'a',  # Para á
        'ข': 'o',  # Para ó
        '‡': 'u',  # Para ú
    }
    
    # Primero aplicar reemplazos específicos
    for old, new in replacements.items():
        filename = filename.replace(old, new)
    
    # Normalizar caracteres Unicode
    filename = unicodedata.normalize('NFKD', filename)
    
    # Reemplazar caracteres no deseados
    filename = filename.replace(' ', '_')
    filename = filename.replace(',', '')
    filename = filename.replace('(', '')
    filename = filename.replace(')', '')
    
    return filename

def read_html_file(file_path: str) -> str:
    """
    Lee un archivo HTML asegurando la correcta codificación.
    
    Args:
        file_path: Ruta al archivo HTML
        
    Returns:
        str: Contenido del archivo correctamente decodificado
        
    Raises:
        UnicodeDecodeError: Si no se puede decodificar el archivo
    """
    # Lista de codificaciones a intentar
    encodings = ['utf-8', 'latin1', 'cp1252']
    
    # Intentar codificaciones conocidas
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    # Si ninguna codificación funciona, intentar detección automática
    with open(file_path, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        return raw.decode(result['encoding'])

def clean_text(text: str) -> str:
    """
    Limpia y normaliza el texto.
    
    Args:
        text: Texto a limpiar
        
    Returns:
        str: Texto limpio y normalizado
    """
    # Normalizar caracteres Unicode
    text = unicodedata.normalize('NFKD', text)
    
    # Eliminar caracteres no ASCII pero mantener ñ y acentos
    text = ''.join(c for c in text if not unicodedata.combining(c) 
                  and (c.isascii() or c in 'áéíóúñÁÉÍÓÚÑ'))
    
    # Eliminar espacios múltiples
    text = ' '.join(text.split())
    
    return text

def detect_encoding(file_path: str) -> Dict[str, Optional[str]]:
    """
    Detecta la codificación de un archivo.
    
    Args:
        file_path: Ruta al archivo
        
    Returns:
        Dict con la codificación detectada y confianza
    """
    with open(file_path, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        return {
            'encoding': result['encoding'],
            'confidence': str(result['confidence'])
        } 