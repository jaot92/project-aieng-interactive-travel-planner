from fastapi import APIRouter
from pydantic import BaseModel
from backend.ai.function_router import AgentTools
from backend.ai.rag_system import NewsRAG
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str

rag = NewsRAG()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Usar RAG para obtener resultados reales
        rag_results = rag.query(request.message)
        suggestions = process_rag_results(rag_results)
        
        return {
            "response": format_rag_response(rag_results),
            "suggestions": suggestions
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return error_response() 