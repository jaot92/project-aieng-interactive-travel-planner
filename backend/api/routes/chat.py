from fastapi import APIRouter, Request
from backend.ai.function_router import AgentTools
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")
    
    try:
        # Respuesta temporal mejorada
        suggestions = AgentTools.find_locations(message)
        return {
            "response": f"Recibí tu mensaje: {message}",
            "suggestions": suggestions
        }
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return {
            "response": "Disculpa, estoy teniendo dificultades técnicas. Por favor intenta nuevamente más tarde.",
            "suggestions": []
        } 