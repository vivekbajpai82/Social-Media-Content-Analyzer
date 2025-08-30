import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # OCR Configuration
    TESSERACT_CONFIG = '--oem 3 --psm 6'
    
    # Analysis Configuration
    SOCIAL_MEDIA_PLATFORMS = {
        'twitter': {'max_chars': 280, 'optimal_hashtags': 2},
        'instagram': {'max_chars': 2200, 'optimal_hashtags': 5},
        'facebook': {'max_chars': 63206, 'optimal_hashtags': 3},
        'linkedin': {'max_chars': 3000, 'optimal_hashtags': 3}
    }