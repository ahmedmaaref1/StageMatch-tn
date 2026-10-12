"""
routers/students.py — Endpoints for managing student profiles
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    """
    Create a new student profile, or update existing one if email already exists.
    """
    existing_student = db.query(Student).filter(Student.email == student_data.email).first()

    if existing_student:
        # Update existing profile
        for key, value in student_data.model_dump().items():
            setattr(existing_student, key, value)
        db.commit()
        db.refresh(existing_student)
        return existing_student

    # Create new profile
    new_student = Student(**student_data.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Get student profile by ID.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student