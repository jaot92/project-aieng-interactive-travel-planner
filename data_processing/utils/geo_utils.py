"""
Utilidades para manejo de coordenadas geográficas.
"""
from geopy.distance import geodesic
from typing import Tuple, List, Optional
from math import radians, sin, cos, sqrt, atan2

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

def is_within_puerto_rico(lat: float, lon: float) -> bool:
    """
    Verifica si unas coordenadas están dentro de los límites de Puerto Rico.
    
    Args:
        lat: Latitud
        lon: Longitud
        
    Returns:
        bool: True si las coordenadas están dentro de Puerto Rico
    """
    # Límites aproximados de Puerto Rico (incluyendo Vieques y Culebra)
    PR_BOUNDS = {
        'min_lat': 17.8,  # Sur
        'max_lat': 18.6,  # Norte
        'min_lon': -67.3, # Oeste
        'max_lon': -65.2  # Este
    }
    
    return (PR_BOUNDS['min_lat'] <= lat <= PR_BOUNDS['max_lat'] and
            PR_BOUNDS['min_lon'] <= lon <= PR_BOUNDS['max_lon'])

def get_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calcula la distancia entre dos puntos usando la fórmula de Haversine.
    
    Args:
        coord1: Tupla (latitud, longitud) del primer punto
        coord2: Tupla (latitud, longitud) del segundo punto
        
    Returns:
        float: Distancia en kilómetros
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    R = 6371  # Radio de la Tierra en kilómetros
    
    # Convertir coordenadas a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Diferencias
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Fórmula de Haversine
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return distance
