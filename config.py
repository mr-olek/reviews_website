import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///reviews.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
    CLAUDE_MODEL = os.environ.get('CLAUDE_MODEL', 'claude-sonnet-4-6')

    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

    SCRAPE_DELAY = float(os.environ.get('SCRAPE_DELAY', '2.0'))
    MAX_REVIEWS_PER_SCRAPE = int(os.environ.get('MAX_REVIEWS_PER_SCRAPE', '20'))

    IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images', 'generated')
    UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images', 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB upload limit
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
