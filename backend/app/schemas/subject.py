# backend/app/schemas/subject.py
from pydantic import BaseModel
from typing import List

# Schema cho Topic (chỉ cần tên là đủ)
class TopicBase(BaseModel):
    name: str

# Schema cho Subject, sẽ bao gồm cả danh sách các topic con
class SubjectBase(BaseModel):
    id: int
    name: str
    description: str | None = None
    topics: List[TopicBase] = []

    # Cấu hình để Pydantic có thể đọc dữ liệu từ đối tượng SQLAlchemy
    class Config:
        from_attributes = True