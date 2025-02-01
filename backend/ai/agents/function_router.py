from langchain.tools import tool
from .agent_functions import AgentFunctions

class AgentTools:
    def __init__(self):
        self.agent_functions = AgentFunctions()

    @tool("Obtener pronóstico del tiempo")
    def get_weather(self, location: dict, date: str):
        """Devuelve el pronóstico del tiempo para una ubicación y fecha específicas"""
        return self.agent_functions.get_weather_forecast(location["lat"], location["lon"], date)
    
    @tool("Buscar lugares relevantes")
    def find_locations(self, user_query: str):
        """Encuentra lugares de interés basados en los intereses del usuario"""
        # Implementación temporal - se conectará con el RAG después
        return ["El Morro", "Bosque Nacional El Yunque", "Viejo San Juan"] 