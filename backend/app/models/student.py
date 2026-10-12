"""
models/student.py — Table for registered student profiles
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    university = Column(String(150), nullable=False)  # e.g., "INSAT", "ISG", "ENIT"
    degree_level = Column(String(50), default="Licence 3")  # "Licence 3", "Master 2", "Ingénieur"
    domain = Column(String(100), nullable=False, index=True)  # Academic domain
    preferred_city = Column(String(100), default="Tunis")
    skills = Column(JSON, default=list)  # List of student skills
    # Student bio / description of career goals used by Sentence-Transformers AI
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Student {self.id}: {self.full_name} ({self.university})>"