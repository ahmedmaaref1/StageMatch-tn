"""
schemas/student.py — Pydantic validation schemas for Student profiles
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class StudentBase(BaseModel):
    full_name: str
    email: EmailStr
    university: str
    degree_level: str = "Licence 3"
    domain: str
    preferred_city: str = "Tunis"
    skills: list[str] = []
    bio: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)