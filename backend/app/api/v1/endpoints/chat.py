# backend/app/api/v1/endpoints/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import List, Literal
# [MỚI] Import service của chúng ta
from app.services import gemini_service 

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
        # Chuyển đổi history từ Pydantic model thành dictionary thuần túy
        # mà thư viện Gemini có thể hiểu được.
        history_dicts = [msg.dict() for msg in chat_request.history]

        # Debug log
        print(f"📝 History: {history_dicts}")
        print(f"📝 New message: {chat_request.message}")

        # [MỚI] Gọi hàm service mới để lấy phản hồi từ AI
        ai_response = gemini_service.generate_chat_response(
            history=history_dicts,
            message=chat_request.message
        )

        # Kiểm tra xem service có trả về lỗi không
        if "error" in ai_response:
            raise HTTPException(status_code=500, detail=ai_response["error"])

        return ai_response

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in conversation endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))