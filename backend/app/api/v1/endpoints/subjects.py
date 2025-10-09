# backend/app/api/v1/endpoints/subjects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.subject import Subject
from app.schemas.subject import SubjectBase
from app.db.session import SessionLocal

router = APIRouter()

# Định nghĩa một "dependency" để lấy DB session cho mỗi request
# FastAPI sẽ tự động gọi hàm này và "tiêm" session vào endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[SubjectBase])
def read_subjects(db: Session = Depends(get_db)):
    """
    API endpoint để lấy danh sách tất cả các môn học và các chủ đề con.
    """
    # Sử dụng session (db) để truy vấn tất cả các đối tượng Subject
    subjects = db.query(Subject).all()
    return subjects