import sys 
import os 

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import Base, engine  
import app.models.offer

def init_database():
    print("Initializing the database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_database()