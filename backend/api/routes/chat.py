from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.ai.agents.function_router import AgentTools
from backend.ai.rag.chain import RAGChain
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    suggestions: list = []

rag = RAGChain()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Usar RAG para obtener resultados
        response = await rag.process_query(request.message)
        
        return ChatResponse(
            response=response,
            suggestions=[]  # Por ahora dejamos las sugerencias vacías hasta implementar la lógica
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Lo siento, hubo un error al procesar tu solicitud. Por favor, intenta de nuevo."
        ) 