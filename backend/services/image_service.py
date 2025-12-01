import os
from PIL import Image
from config.settings import Config
from services.upload_service import UploadService

class ImageService:
    @staticmethod
    def get_image_info(filename):
        """Récupère les informations détaillées d'une image"""
        try:
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            
            if not os.path.exists(filepath):
                return None
            
            # Réutiliser la méthode existante (DRY)
            base_metadata = UploadService._extract_metadata(filepath)
            
            if not base_metadata:
                return None
            
            # Ajouter les informations supplémentaires
            with Image.open(filepath) as img:
                base_metadata.update({
                    'filename': filename,
                    'aspect_ratio': round(img.width / img.height, 2),
                    'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                })
            
            return base_metadata
                
        except Exception as e:
            print(f"Erreur info image: {e}")
            return None