import os

class Config:
    # Get the backend directory (where this config file is located)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Get the project root (parent of backend)
    PROJECT_ROOT = os.path.dirname(BASE_DIR)

    # Dossiers
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')
    PROCESSED_FOLDER = os.path.join(PROJECT_ROOT, 'processed')

    # Limites de fichiers
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    MAX_FILES_PER_UPLOAD = 10
    
    # Formats supportés
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
    ALLOWED_MIME_TYPES = {
        'image/png', 'image/jpeg', 'image/gif', 
        'image/bmp', 'image/tiff', 'image/webp'
    }
    
    # Configuration Flask
    SECRET_KEY = 'dev-key-change-in-production'
    DEBUG = True
    
    # Configuration thumbnails
    THUMBNAIL_SIZES = {
        'small': (100, 100),
        'medium': (200, 200),
        'large': (400, 400)
    }
    DEFAULT_THUMBNAIL_SIZE = (200, 200)