"""
Configuration settings for the Job Board Flask application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Database configuration
    # Default to PostgreSQL, fallback to SQLite for development
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/jobboard')
    
    # For local development, you can use SQLite:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///jobboard.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # CORS settings for frontend integration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Pagination settings
    JOBS_PER_PAGE = int(os.getenv('JOBS_PER_PAGE', '20'))
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    # Use SQLite for easier development setup
    SQLALCHEMY_DATABASE_URI = 'sqlite:///jobboard_dev.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Use environment variable for production database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///jobboard_test.db'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}