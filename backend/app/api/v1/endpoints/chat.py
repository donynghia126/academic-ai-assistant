# backend/app/api/v1/endpoints/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import List, Literal
from app.services import ai_factory 
from app.services.ai_factory import AIProvider 

# Định nghĩa cấu trúc cho một tin nhắn trong cuộc hội thoại
class ChatMessage(BaseModel):
    role: Literal["user", "model"]  # Chỉ cho phép "user" hoặc "model"
    parts: List[str]

# Định nghĩa cấu trúc cho request body gửi đến API chat
class ChatRequest(BaseModel):
    # Pydantic sẽ tự động chuyển đổi JSON từ frontend thành list các object ChatMessage
    history: List[ChatMessage] 
    message: str

router = APIRouter()

@router.post("/conversation")
async def post_conversation(chat_request: ChatRequest):
    """
    Nhận tin nhắn mới và lịch sử, gọi Gemini service để lấy phản hồi
    và trả về cho client.
    
    Body example:
    {
        "history": [
            {"role": "user", "parts": ["Hello"]},
            {"role": "model", "parts": ["Hi there!"]}
        ],
        "message": "How are you?"
    }
    """
    try:
        history_dicts = [msg.dict() for msg in chat_request.history]

        # [MỚI] Gọi qua "Tổng Đài", chỉ định rõ muốn "gặp" GEMINI
        ai_response = ai_factory.generate_chat_response(
            provider=AIProvider.GEMINI, # << THAY ĐỔI
            history=history_dicts,
            message=chat_request.message
        )

        if "error" in ai_response:
            raise HTTPException(status_code=500, detail=ai_response["error"])

        return ai_response
    except Exception as e:
        print(f"❌ Error in conversation endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))