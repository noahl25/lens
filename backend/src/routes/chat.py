from fastapi import APIRouter
from pydantic import BaseModel
from ..agent.agent import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    request: str

@router.post("/chat")
async def chat(chat_request: ChatRequest):
    
    try:
        result = run_agent(chat_request.request)
    except Exception as e:
        return { "error": str(e) }

    return { "result": result }