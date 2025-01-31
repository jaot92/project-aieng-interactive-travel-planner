"""
Utilidades para manejo de coordenadas geográficas.
"""
from geopy.distance import geodesic
from typing import Tuple, List, Optional

def calculate_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calcula la distancia en kilómetros entre dos puntos usando sus coordenadas.
    
    Args:
        coord1: Tuple de (latitud, longitud) del primer punto
        coord2: Tuple de (latitud, longitud) del segundo punto
        
    Returns:
        Distancia en kilómetros
    """
    return geodesic(coord1, coord2).kilometers

def find_nearest_points(target: Tuple[float, float], points: List[Tuple[float, float]], max_distance: Optional[float] = None) -> List[Tuple[float, float]]:
    """
    Encuentra los puntos más cercanos a un punto objetivo.
    
    Args:
        target: Coordenadas del punto objetivo
        points: Lista de coordenadas de puntos a comparar
        max_distance: Distancia máxima en kilómetros (opcional)
        
    Returns:
        Lista de puntos ordenados por distancia
    """
    distances = [(p, calculate_distance(target, p)) for p in points]
    if max_distance:
        distances = [(p, d) for p, d in distances if d <= max_distance]
    return [p for p, _ in sorted(distances, key=lambda x: x[1])]

def is_within_bounds(coord: Tuple[float, float], bounds: Tuple[float, float, float, float]) -> bool:
    """
    Verifica si unas coordenadas están dentro de unos límites geográficos.
    
    Args:
        coord: Tuple de (latitud, longitud)
        bounds: Tuple de (min_lat, max_lat, min_lon, max_lon)
        
    Returns:
        Boolean indicando si está dentro de los límites
    """
    lat, lon = coord
    min_lat, max_lat, min_lon, max_lon = bounds
    return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon

# Límites aproximados de Puerto Rico
PR_BOUNDS = (17.9, 18.5, -67.3, -65.6)  # (min_lat, max_lat, min_lon, max_lon)
