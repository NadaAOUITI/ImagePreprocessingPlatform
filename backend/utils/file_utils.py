import os
from datetime import datetime
from config.settings import Config
from services.upload_service import UploadService

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
                # Réutiliser la méthode existante (DRY)
                metadata = UploadService._extract_metadata(filepath)
                if metadata:
                    # Ajouter le timestamp
                    metadata['upload_time'] = datetime.fromtimestamp(
                        os.path.getmtime(filepath)
                    ).isoformat()
                    
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
    
