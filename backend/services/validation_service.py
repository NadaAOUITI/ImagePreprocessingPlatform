import os
from PIL import Image
from config.settings import Config

class ValidationService:
    @staticmethod
    def validate_file(file):
        """Valide un fichier uploadé"""
        errors = []
        
        if not ValidationService._is_allowed_extension(file.filename):
            errors.append("Format de fichier non supporté")
        
        if not ValidationService._is_valid_size(file):
            errors.append(f"Fichier trop volumineux (max {Config.MAX_FILE_SIZE // (1024*1024)}MB)")
        
        if not ValidationService._is_valid_image(file):
            errors.append("Le fichier n'est pas une image valide")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _is_allowed_extension(filename):
        return ('.' in filename and 
                filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS)
    
    @staticmethod
    def _is_valid_size(file):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        return size <= Config.MAX_FILE_SIZE
    
    @staticmethod
    def _is_valid_image(file):
        try:
            file.seek(0)
            with Image.open(file) as img:
                img.verify()
            file.seek(0)
            return True
        except Exception:
            return False