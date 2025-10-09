# backend/app/services/ai_factory.py
from enum import Enum
from typing import List, Dict, Any

from . import gemini_service
from . import azure_service

class AIProvider(str, Enum):
    GEMINI = "gemini"
    AZURE = "azure"

def get_ai_provider(provider: AIProvider):
    """
    Factory function để lấy ra module service tương ứng.
    """
    if provider == AIProvider.GEMINI:
        return gemini_service
    elif provider == AIProvider.AZURE:
        # Hiện tại chúng ta chưa có hàm tương đương trong azure_service
        # nhưng cấu trúc đã sẵn sàng
        return azure_service
    raise ValueError(f"Nhà cung cấp AI không hợp lệ: {provider}")

# --- Các hàm chức năng chung ---

def generate_chat_response(
    provider: AIProvider,
    history: List[Dict[str, Any]],
    message: str
) -> dict:
    """
    Tạo phản hồi chat từ một nhà cung cấp AI cụ thể.
    """
    service = get_ai_provider(provider)
    # Giả định rằng mỗi service module đều có hàm generate_chat_response
    return service.generate_chat_response(history=history, message=message)

def explain_code(
    provider: AIProvider,
    code_snippet: str
) -> dict:
    """
    Yêu cầu giải thích code từ một nhà cung cấp AI cụ thể.
    """
    service = get_ai_provider(provider)
    # Giả định rằng mỗi service module đều có hàm explain_code_from_gemini (hoặc tên tương tự)
    return service.explain_code_from_gemini(code_snippet=code_snippet)

def analyze_document(
    provider: AIProvider,
    document_text: str
) -> dict:
    """
    Phân tích tài liệu từ một nhà cung cấp AI cụ thể (ví dụ: Azure).
    """
    if provider != AIProvider.AZURE:
        return {"error": "Tính năng này chỉ được hỗ trợ bởi Azure."}

    service = get_ai_provider(provider)
    return service.analyze_document_with_azure(document_text)