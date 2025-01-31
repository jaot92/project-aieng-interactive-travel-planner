"""
Utilidades para procesar archivos HTML de Wikipedia.
"""
from bs4 import BeautifulSoup
import re
from typing import Optional, Tuple, List
from .encoding_utils import read_html_file, clean_text

def parse_html_file(file_path: str) -> BeautifulSoup:
    """
    Lee y parsea un archivo HTML.
    
    Args:
        file_path: Ruta al archivo HTML.
        
    Returns:
        BeautifulSoup: Objeto con el contenido parseado.
    """
    content = read_html_file(file_path)
    return BeautifulSoup(content, 'html.parser')

def extract_coordinates(soup: BeautifulSoup) -> Optional[Tuple[float, float]]:
    """
    Extrae las coordenadas de un artículo de Wikipedia.
    
    Args:
        soup: Objeto BeautifulSoup con el contenido parseado.
        
    Returns:
        Tuple[float, float]: Tupla con latitud y longitud, o None si no se encuentran.
    """
    try:
        # Buscar en el script de configuración de la página
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'wgCoordinates' in script.string:
                coords_match = re.search(r'"wgCoordinates":\{"lat":([\d.-]+),"lon":([\d.-]+)', script.string)
                if coords_match:
                    return float(coords_match.group(1)), float(coords_match.group(2))
        
        # Buscar en el span de coordenadas
        coords_span = soup.find('span', {'class': 'geo'})
        if coords_span:
            coords = coords_span.text.split(';')
            if len(coords) == 2:
                return float(coords[0]), float(coords[1])
        
        return None
    except Exception:
        return None

def extract_description(soup: BeautifulSoup) -> Optional[str]:
    """
    Extrae la descripción principal de un artículo de Wikipedia.
    
    Args:
        soup: Objeto BeautifulSoup con el contenido parseado.
        
    Returns:
        str: Descripción del artículo, o None si no se encuentra.
    """
    try:
        # Buscar en el contenido principal
        content = soup.find('div', {'id': 'mw-content-text'})
        if not content:
            return None
            
        # Buscar en la clase mw-parser-output
        parser_output = content.find('div', {'class': 'mw-parser-output'})
        if not parser_output:
            return None
            
        # Buscar el primer párrafo que no sea vacío y no tenga tablas o clases especiales
        for p in parser_output.find_all('p', recursive=False):
            # Ignorar párrafos con clases especiales
            if p.get('class'):
                continue
                
            # Ignorar párrafos que son parte de una tabla
            if p.find_parent('table'):
                continue
                
            # Limpiar el texto
            text = clean_text(p.get_text().strip())
            
            # Ignorar párrafos vacíos o que solo contienen coordenadas
            if text and not text.startswith('Coordinates:'):
                # Eliminar referencias [1], [2], etc.
                text = re.sub(r'\[\d+\]', '', text)
                return text
                
        return None
    except Exception as e:
        print(f"Error extracting description: {str(e)}")
        return None

def extract_categories(soup: BeautifulSoup) -> List[str]:
    """
    Extrae las categorías de un artículo de Wikipedia.
    
    Args:
        soup: Objeto BeautifulSoup con el contenido parseado.
        
    Returns:
        List[str]: Lista de categorías.
    """
    categories = []
    try:
        cat_links = soup.find_all('a', href=re.compile(r'^/wiki/Category:'))
        for link in cat_links:
            cat_name = clean_text(link.text.strip())
            if cat_name and not cat_name.startswith('Category:'):
                categories.append(cat_name)
    except Exception:
        pass
    return categories
