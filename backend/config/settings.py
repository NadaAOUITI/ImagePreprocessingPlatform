import os

class Config:
    # Dossiers
    UPLOAD_FOLDER = os.path.abspath('../uploads')
    PROCESSED_FOLDER = os.path.abspath('../processed')
    
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