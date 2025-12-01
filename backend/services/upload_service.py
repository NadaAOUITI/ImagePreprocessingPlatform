import os
import uuid
from datetime import datetime
from PIL import Image
from werkzeug.utils import secure_filename
from config.settings import Config
from services.validation_service import ValidationService

class UploadService:
    @staticmethod
    def upload_files(files):
        """Upload multiple files avec validation"""
        if len(files) > Config.MAX_FILES_PER_UPLOAD:
            return False, f"Trop de fichiers (max {Config.MAX_FILES_PER_UPLOAD})"
        
        results = []
        for file in files:
            if file and file.filename:
                is_valid, errors = ValidationService.validate_file(file)
                
                if is_valid:
                    result = UploadService._save_file(file)
                    results.append(result)
                else:
                    results.append({
                        'filename': file.filename,
                        'success': False,
                        'errors': errors
                    })
        
        return True, results
    
    @staticmethod
    def _save_file(file):
        """Sauvegarde sécurisée du fichier"""
        try:
            # Générer nom unique
            original_filename = secure_filename(file.filename)
            name, ext = os.path.splitext(original_filename)
            unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
            
            filepath = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
            file.save(filepath)
            
            # Extraire métadonnées
            metadata = UploadService._extract_metadata(filepath)
            
            return {
                'filename': unique_filename,
                'original_filename': original_filename,
                'success': True,
                'metadata': metadata,
                'upload_time': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'filename': file.filename,
                'success': False,
                'errors': [str(e)]
            }
    
    @staticmethod
    def _extract_metadata(filepath):
        """Extraire métadonnées de l'image"""
        try:
            with Image.open(filepath) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'size_bytes': os.path.getsize(filepath)
                }
        except Exception:
            return {}