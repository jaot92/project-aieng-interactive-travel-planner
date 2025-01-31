from fastapi import APIRouter
from pydantic import BaseModel
from backend.ai.function_router import AgentTools
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        suggestions = AgentTools.find_locations(request.message)
        return {
            "response": f"Recibí tu mensaje: {request.message}",
            "suggestions": suggestions
        }
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return {
            "response": "Disculpa, estoy teniendo dificultades técnicas. Por favor intenta nuevamente más tarde.",
            "suggestions": []
        } 