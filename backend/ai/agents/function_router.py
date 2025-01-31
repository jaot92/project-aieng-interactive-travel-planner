from langchain.tools import tool
from .agent_functions import get_weather_forecast

class AgentTools:
    @tool("Obtener pronóstico del tiempo")
    def get_weather(location: dict, date: str):
        """Devuelve el pronóstico del tiempo para una ubicación y fecha específicas"""
        return get_weather_forecast(location["lat"], location["lon"], date)
    
    @tool("Buscar lugares relevantes")
    def find_locations(user_query: str):
        """Encuentra lugares de interés basados en los intereses del usuario"""
        # Implementación temporal - se conectará con el RAG después
        return ["El Morro", "Bosque Nacional El Yunque", "Viejo San Juan"] 