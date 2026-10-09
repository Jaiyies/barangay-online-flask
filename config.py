import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SECRET_KEY = 'dev-secret-key-change-in-production'
    
    # MySQL Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'bsit2026@123'  # ✅ Your root password
    MYSQL_DB = 'barangay_online_services'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

    import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SECRET_KEY = 'dev-secret-key-change-in-production'
    
    # MySQL Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'bsit2026@123'
    MYSQL_DB = 'barangay_online_services'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    # ============ AI ASSISTANT CONFIGURATION ============
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # ============ GOOGLE OAUTH CONFIGURATION ============
    GOOGLE_CLIENT_ID = '1024740089887-r3bguo33a5ecs4ltuf1fiubqr19c8jgv.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'
    
    # ============ AI ASSISTANT CONFIGURATION ============
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')