# backend/app/api/v1/api.py

from fastapi import APIRouter
from app.api.v1.endpoints import health, code, chat 

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health Check"])
api_router.include_router(code.router, prefix="/code", tags=["Code Analysis"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"]) 