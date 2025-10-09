from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def get_status():
    """
    Endpoint để kiểm tra trạng thái của API.
    """
    return {"status": "ok", "message": "API is running smoothly!"}