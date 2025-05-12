import os
from dotenv import load_dotenv

# Load environment variables from a .env file into the environment
load_dotenv()

class Config:
    # API key for Gemini model access
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    # Database URI - defaulting to a local SQLite file if not provided
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URI', 'sqlite:///nsdevil.db')
    # Prevents SQLAlchemy from tracking object changes (which consumes memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() == "true"
