from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    request: str

@router.post("/chat")
async def chat(chat_request: ChatRequest):
    
    return { "result": chat_request.request + " response"}