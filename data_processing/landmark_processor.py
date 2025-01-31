from bs4 import BeautifulSoup
import json
import os

def process_landmark(html_content: str) -> dict:
    """Extrae información estructurada de HTML crudo"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    return {
        "name": soup.find('h1').text.strip(),
        "coordinates": extract_coordinates(soup),
        "summary": soup.find('div', {'class': 'mw-parser-output'}).p.text[:500],
        "category": "Historical" if "history" in html_content.lower() else "Natural"
    }

def extract_coordinates(soup):
    # Lógica para extraer coordenadas geográficas
    geo_tag = soup.find('span', {'class': 'geo'})
    if geo_tag:
        return list(map(float, geo_tag.text.split(';')))
    return None 

def process_all_landmarks():
    data_path = os.path.join(os.getcwd(), 'data', 'landmarks')
    for filename in os.listdir(data_path):
        if filename.endswith('.html'):
            with open(os.path.join(data_path, filename)) as f:
                content = f.read()
                process_landmark(content) 