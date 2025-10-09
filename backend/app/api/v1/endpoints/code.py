# backend/app/api/v1/endpoints/code.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services import gemini_service

router = APIRouter()

# Định nghĩa cấu trúc dữ liệu cho yêu cầu (Request Body)
class CodeExplanationRequest(BaseModel):
    code: str = Field(..., min_length=10, description="Đoạn code cần được giải thích")


@router.post("/explain")
async def explain_code(request: CodeExplanationRequest):
    """
    Nhận một đoạn code từ client, gửi đến Gemini để giải thích, và trả về kết quả.
    """
    try:
        # Gọi hàm xử lý từ gemini_service
        result = gemini_service.explain_code_from_gemini(request.code)
        
        # Kiểm tra nếu có lỗi từ service trả về
        if "error" in result:
            print(f"❌ Lỗi từ gemini_service: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])
            
        return result
        
    except HTTPException:
        # Re-raise HTTPException để không bị catch lại
        raise
    except Exception as e:
        # Bắt các lỗi không mong muốn khác
        print(f"❌ Lỗi không mong muốn: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
