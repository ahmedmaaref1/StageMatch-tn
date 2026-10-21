from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import offers, students, recommendations
from app.scheduler import start_scheduler, shutdown_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage : lance le planificateur de scraping en arrière-plan
    start_scheduler()
    yield
    # Arrêt : éteint proprement le planificateur
    shutdown_scheduler()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Smart PFE Internship Recommender for Tunisian Students",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(offers.router)
app.include_router(students.router)
app.include_router(recommendations.router)


@app.get("/")
def root():
    return {
        "app": "StageMatch TN",
        "status": "online",
        "docs_url": "/docs",
    }