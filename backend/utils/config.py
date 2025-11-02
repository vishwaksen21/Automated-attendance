"""
Configuration management module for the attendance system.
Centralizes all configuration in one place for easy management.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class"""

    # Project root directory
    BASE_DIR = Path(__file__).parent.parent.parent

    # ==================== FILE PATHS ====================
    TRAINING_IMAGE_PATH = Path(
        os.getenv("TRAINING_IMAGE_PATH", BASE_DIR / "TrainingImage")
    )
    TRAINING_LABEL_PATH = Path(
        os.getenv("TRAINING_LABEL_PATH", BASE_DIR / "TrainingImageLabel/Trainner.yml")
    )
    STUDENT_DETAILS_PATH = Path(
        os.getenv("STUDENT_DETAILS_PATH", BASE_DIR / "StudentDetails/studentdetails.csv")
    )
    ATTENDANCE_PATH = Path(os.getenv("ATTENDANCE_PATH", BASE_DIR / "Attendance"))
    FACE_CASCADE_PATH = Path(
        os.getenv("FACE_CASCADE_PATH", BASE_DIR / "haarcascade_frontalface_default.xml")
    )

    # ==================== FACE RECOGNITION ====================
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "90"))
    NUM_SAMPLES = int(os.getenv("NUM_SAMPLES", "50"))
    FACE_DETECTION_SCALE = float(os.getenv("FACE_DETECTION_SCALE", "1.2"))
    FACE_DETECTION_NEIGHBORS = int(os.getenv("FACE_DETECTION_NEIGHBORS", "5"))

    # ==================== DATABASE ====================
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "attendance_system")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "students")

    # ==================== API ====================
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "5000"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # ==================== SECURITY ====================
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    JWT_EXPIRY = int(os.getenv("JWT_EXPIRY", "3600"))  # 1 hour
    BCRYPT_LOG_ROUNDS = int(os.getenv("BCRYPT_LOG_ROUNDS", "12"))

    # ==================== LOGGING ====================
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = Path(os.getenv("LOG_DIR", BASE_DIR / "logs"))

    @classmethod
    def init_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.TRAINING_IMAGE_PATH,
            cls.ATTENDANCE_PATH,
            cls.LOG_DIR,
            cls.TRAINING_LABEL_PATH.parent,
            cls.STUDENT_DETAILS_PATH.parent,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Development environment configuration"""

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration"""

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration"""

    DEBUG = True
    TESTING = True
    MONGODB_URI = "mongodb://localhost:27017/test_attendance"
    DATABASE_NAME = "test_attendance_system"


# Select configuration based on environment
config_env = os.getenv("FLASK_ENV", "development").lower()

if config_env == "production":
    config = ProductionConfig()
elif config_env == "testing":
    config = TestingConfig()
else:
    config = DevelopmentConfig()

# Initialize directories
config.init_directories()
