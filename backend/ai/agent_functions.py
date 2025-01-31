import os
import requests

# Ejemplo de función crítica para clima
def get_weather_forecast(lat: float, lon: float, date: str) -> dict:
    base_url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "date": date,
        "appid": os.getenv("OWM_API_KEY"),
        "units": "metric",
        "lang": "es"
    }
    response = requests.get(base_url, params=params)
    return process_weather_data(response.json())  # Función de transformación 