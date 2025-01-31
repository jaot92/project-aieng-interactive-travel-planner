"""
Script para probar las funcionalidades del motor de consultas.
"""
from data_querying.query_engine import QueryEngine
import json

def print_results(results: list, title: str):
    """Imprime los resultados de forma legible."""
    print(f"\n=== {title} ===")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['name']}")
        print(f"   Descripción: {result['description'][:200]}...")
        print(f"   Categorías: {', '.join(result['categories'])}")
        if result['coordinates']['latitude'] and result['coordinates']['longitude']:
            print(f"   Coordenadas: ({result['coordinates']['latitude']}, {result['coordinates']['longitude']})")

def main():
    # Inicializar el motor de consultas
    engine = QueryEngine()
    
    # Prueba 1: Buscar landmarks históricos
    results = engine.search_landmarks("lugares históricos en San Juan", n_results=3)
    print_results(results, "Landmarks Históricos en San Juan")
    
    # Prueba 2: Buscar playas
    results = engine.search_landmarks("mejores playas", n_results=3)
    print_results(results, "Mejores Playas")
    
    # Prueba 3: Buscar municipios con parques naturales
    results = engine.search_municipalities("municipios con parques naturales", n_results=3)
    print_results(results, "Municipios con Parques Naturales")
    
    # Prueba 4: Buscar municipios costeros
    results = engine.search_municipalities("municipios en la costa", n_results=3)
    print_results(results, "Municipios Costeros")

if __name__ == "__main__":
    main() 