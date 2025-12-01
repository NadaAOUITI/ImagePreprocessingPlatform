import os
import json
from datetime import datetime
from PIL import Image
from config.settings import Config

class FileUtils:
    @staticmethod
    def get_uploaded_images():
        """Récupère la liste des images uploadées avec métadonnées"""
        images = []
        
        if not os.path.exists(Config.UPLOAD_FOLDER):
            return images
        
        for filename in os.listdir(Config.UPLOAD_FOLDER):
            if FileUtils._is_image_file(filename):
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                metadata = FileUtils._get_file_metadata(filepath)
                images.append({
                    'filename': filename,
                    'metadata': metadata
                })
        
        return sorted(images, key=lambda x: x['metadata']['upload_time'], reverse=True)
    
    @staticmethod
    def delete_image(filename):
        """Supprime une image uploadée"""
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    @staticmethod
    def _is_image_file(filename):
        return ('.' in filename and 
                filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS)
    
    @staticmethod
    def _get_file_metadata(filepath):
        """Récupère les métadonnées d'un fichier"""
        try:
            stat = os.stat(filepath)
            with Image.open(filepath) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'size_bytes': stat.st_size,
                    'upload_time': datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
        except Exception:
            return {
                'size_bytes': os.path.getsize(filepath),
                'upload_time': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
            }