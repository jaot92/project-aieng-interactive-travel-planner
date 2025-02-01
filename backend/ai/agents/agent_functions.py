import os
import requests

class AgentFunctions:
    @staticmethod
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
        return AgentFunctions.process_weather_data(response.json())
    
    @staticmethod
    def process_weather_data(data: dict) -> dict:
        # Implementar el procesamiento de datos del clima
        return {
            "temperature": data.get("current", {}).get("temp", 0),
            "description": data.get("current", {}).get("weather", [{}])[0].get("description", ""),
            "humidity": data.get("current", {}).get("humidity", 0)
        } 