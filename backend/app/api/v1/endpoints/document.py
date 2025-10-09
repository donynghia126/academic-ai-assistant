# backend/app/api/v1/endpoints/document.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services import ai_factory
from app.services.ai_factory import AIProvider

router = APIRouter()

class DocumentRequest(BaseModel):
    text: str

@router.post("/analyze")
def analyze_document(request: DocumentRequest):
    """
    Phân tích một đoạn văn bản sử dụng Azure AI.
    """
    return ai_factory.analyze_document(provider=AIProvider.AZURE, document_text=request.text)