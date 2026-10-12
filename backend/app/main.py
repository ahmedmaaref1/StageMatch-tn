"""
main.py — FastAPI Application Entry Point

FEATURES:
- Automatic OpenAPI documentation at /docs
- CORS Middleware enabled so React (localhost:5173) can communicate with API
- Modular Routers for /offers and /students
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import offers, students

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Smart PFE Internship Recommender for Tunisian Students",
    version="1.0.0",
)

# ── CORS CONFIGURATION ────────────────────────────────────────────────────────
# WHY: Browsers block web requests made between different ports
# (e.g. React on 5173 calling FastAPI on 8000). CORS allows this communication!
origins = [
    "http://localhost:5173",  # React Vite dev server
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "*",                      # Open during development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── INCLUDE ROUTERS ───────────────────────────────────────────────────────────
app.include_router(offers.router)
app.include_router(students.router)


@app.get("/")
def root():
    return {
        "app": "StageMatch TN",
        "status": "online",
        "docs_url": "/docs"
    }