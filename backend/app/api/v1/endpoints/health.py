from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthCheck(BaseModel):
    status: str
    message: str

@router.get("/health", response_model=HealthCheck)
def health_check():
    """
    Endpoint kiểm tra "sức khỏe" của API.
    """
    return HealthCheck(status="OK", message="API is running smoothly")