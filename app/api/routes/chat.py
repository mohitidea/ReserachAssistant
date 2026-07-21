from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat import chat, reset

router= APIRouter(prefix= "/chat", tags= ["chat"])

class ChatRequest(BaseModel):
    session_id: str
    question: str
    k: int= 4

class ChatResponse(BaseModel):
    answer: str
    rewritten_question: str


@router.post("", response_model= ChatResponse)
async def chat_endpoint(req: ChatRequest):
    answer, standalone= chat(req.session_id, req.question , req.k)
    return ChatResponse(answer= answer, rewritten_question= standalone)


@router.delete("/{session_id}")
async def clear_session(session_id: str):
    reset(session_id)
    return {"status": "cleared", "session_id": session_id}


                  