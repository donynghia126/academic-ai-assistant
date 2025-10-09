# backend/app/models/subject.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Mối quan hệ: Một Subject có nhiều Topic
    topics = relationship("Topic", back_populates="subject")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"))

    # Mối quan hệ: Một Topic thuộc về một Subject
    subject = relationship("Subject", back_populates="topics")