import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# --- Import "bộ não" AI của chúng ta ---
from app.services import gemini_service

# Tải các biến môi trường từ file .env
load_dotenv()

# --- Định nghĩa cấu trúc dữ liệu cho yêu cầu (Request Body) ---
# Sử dụng Pydantic để FastAPI tự động kiểm tra dữ liệu đầu vào
class CodeExplanationRequest(BaseModel):
    code: str = Field(..., min_length=10, description="Đoạn code cần được giải thích")

# --- Khởi tạo ứng dụng FastAPI ---
app = FastAPI(
    title="Trợ Lý Học Thuật AI API",
    description="API cho dự án Trợ Lý Học Thuật AI, sử dụng FastAPI và Gemini.",
    version="1.0.0"
)

# --- Cấu hình CORS ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Các API Endpoints ---

@app.get("/api/v1/status", tags=["Health Check"])
def get_status():
    """
    Endpoint để kiểm tra trạng thái của API.
    """
    return {"status": "ok", "message": "API is running smoothly!"}


@app.post("/api/v1/code/explain", tags=["AI Features"])
def explain_code(request: CodeExplanationRequest):
    """
    Nhận một đoạn code từ client, gửi đến Gemini để giải thích, và trả về kết quả.
    """
    try:
        # Gọi hàm xử lý từ gemini_service
        result = gemini_service.explain_code_from_gemini(request.code)
        
        # Kiểm tra nếu có lỗi từ service trả về
        if "error" in result:
            print(f"❌ Lỗi từ gemini_service: {result['error']}")  # Debug log
            raise HTTPException(status_code=500, detail=result["error"])
            
        return result
        
    except HTTPException:
        # Re-raise HTTPException để không bị catch lại
        raise
    except Exception as e:
        # Bắt các lỗi không mong muốn khác
        print(f"❌ Lỗi không mong muốn: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")