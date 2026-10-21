"""
routers/students.py — Endpoints for managing student profiles
"""



import io
import re
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pypdf import PdfReader

from app.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse, ParsedCVResponse
from app.scraper.skills_registry import extract_skills_from_text, detect_tech_track, INSTITUTIONS

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



@router.post("/parse-cv", response_model=ParsedCVResponse)
async def parse_student_cv(file: UploadFile = File(...)):
    """
    Parses an uploaded PDF CV:
    - Extracts text with pypdf
    - Automatically extracts technical skills using skills_registry
    - Detects university from the official Tunisian tech directory
    - Detects best-fitting tech track
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés.")

    content = await file.read()
    try:
        reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Impossible de lire le fichier PDF: {str(e)}")

    if not text.strip():
        raise HTTPException(status_code=400, detail="Le fichier PDF semble vide ou est un scan image sans texte.")

    # 1. Extract Technical Skills
    skills = extract_skills_from_text(text)

    # 2. Detect Tech Track
    detected_domain = detect_tech_track(text[:300], text)

    # 3. Detect University from Tunisian Institutions Directory
    detected_university = None
    text_lower = text.lower()
    for inst in INSTITUTIONS:
        name = inst[0]
        # Check acronym with strict word boundary (avoids false substring matches like 'isi' in 'classification')
        acronym = name.split("(")[0].strip().lower()
        pattern = r'\b' + re.escape(acronym) + r'\b'
        if len(acronym) >= 3 and re.search(pattern, text_lower):
            detected_university = name
            break
        # Check clean institutional name
        clean_name = re.sub(r'\(.*?\)', '', name).strip().lower()
        if len(clean_name) > 6 and re.search(r'\b' + re.escape(clean_name) + r'\b', text_lower):
            detected_university = name
            break

    # 4. Extract Email (if present)
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    email = email_match.group(0) if email_match else None

    # 5. Extract Candidate Name (first readable line of CV)
    lines = [line.strip() for line in text.split("\n") if len(line.strip()) > 2]
    candidate_name = lines[0] if lines else None
    if candidate_name and len(candidate_name) > 40:
        candidate_name = None

    return ParsedCVResponse(
        full_name=candidate_name,
        email=email,
        university=detected_university,
        domain=detected_domain,
        skills=skills,
        raw_text_snippet=text[:300]
    )