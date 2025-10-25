from fastapi import APIRouter
from pydantic import BaseModel
from ..agent.agent import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    request: str

@router.post("/chat")
async def chat(chat_request: ChatRequest):
    
    result = await run_agent(chat_request.request)

    return { "result": result }