import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from config.settings import Config

class ProcessingService:
    @staticmethod
    def process_image(filename, operation, params=None):
        """Traite une image avec l'opération spécifiée"""
        try:
            input_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            if not os.path.exists(input_path):
                return None, "Image non trouvée"
            
            # Générer nom de fichier de sortie
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_{operation}{ext}"
            output_path = os.path.join(Config.PROCESSED_FOLDER, output_filename)
            
            # Appliquer l'opération
            success = ProcessingService._apply_operation(input_path, output_path, operation, params)
            
            if success:
                return output_filename, None
            else:
                return None, f"Erreur lors du traitement {operation}"
                
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def _apply_operation(input_path, output_path, operation, params):
        """Applique l'opération spécifique"""
        try:
            if operation == 'grayscale':
                return ProcessingService._grayscale(input_path, output_path)
            elif operation == 'threshold':
                return ProcessingService._threshold(input_path, output_path, params)
            elif operation == 'blur':
                return ProcessingService._blur(input_path, output_path, params)
            elif operation == 'sharpen':
                return ProcessingService._sharpen(input_path, output_path)
            elif operation == 'edge_detection':
                return ProcessingService._edge_detection(input_path, output_path, params)
            elif operation == 'resize':
                return ProcessingService._resize(input_path, output_path, params)
            elif operation == 'rotate':
                return ProcessingService._rotate(input_path, output_path, params)
            elif operation == 'flip':
                return ProcessingService._flip(input_path, output_path, params)
            elif operation == 'normalize':
                return ProcessingService._normalize(input_path, output_path)
            elif operation == 'histogram_eq':
                return ProcessingService._histogram_equalization(input_path, output_path)
            elif operation == 'extract_channel':
                return ProcessingService._extract_channel(input_path, output_path, params)
            else:
                return False
        except Exception:
            return False
    
    @staticmethod
    def _grayscale(input_path, output_path):
        """Conversion en niveaux de gris"""
        img = cv2.imread(input_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(output_path, gray)
        return True
    
    @staticmethod
    def _threshold(input_path, output_path, params):
        """Seuillage binaire"""
        threshold_value = params.get('threshold', 127) if params else 127
        threshold_type = params.get('type', 'binary') if params else 'binary'
        
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        
        if threshold_type == 'adaptive':
            result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        else:
            _, result = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)
        
        cv2.imwrite(output_path, result)
        return True
    
    @staticmethod
    def _blur(input_path, output_path, params):
        """Flou gaussien"""
        kernel_size = params.get('kernel_size', 5) if params else 5
        
        img = cv2.imread(input_path)
        blurred = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
        cv2.imwrite(output_path, blurred)
        return True
    
    @staticmethod
    def _sharpen(input_path, output_path):
        """Accentuation"""
        img = cv2.imread(input_path)
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(img, -1, kernel)
        cv2.imwrite(output_path, sharpened)
        return True
    
    @staticmethod
    def _edge_detection(input_path, output_path, params):
        """Détection de contours"""
        low_threshold = params.get('low', 50) if params else 50
        high_threshold = params.get('high', 150) if params else 150
        
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        edges = cv2.Canny(img, low_threshold, high_threshold)
        cv2.imwrite(output_path, edges)
        return True
    
    @staticmethod
    def _resize(input_path, output_path, params):
        """Redimensionnement"""
        width = params.get('width', 300) if params else 300
        height = params.get('height', 300) if params else 300
        
        img = cv2.imread(input_path)
        resized = cv2.resize(img, (width, height))
        cv2.imwrite(output_path, resized)
        return True
    
    @staticmethod
    def _rotate(input_path, output_path, params):
        """Rotation"""
        angle = params.get('angle', 90) if params else 90
        
        img = cv2.imread(input_path)
        height, width = img.shape[:2]
        center = (width // 2, height // 2)
        
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, rotation_matrix, (width, height))
        cv2.imwrite(output_path, rotated)
        return True
    
    @staticmethod
    def _flip(input_path, output_path, params):
        """Retournement"""
        direction = params.get('direction', 'horizontal') if params else 'horizontal'
        
        img = cv2.imread(input_path)
        if direction == 'horizontal':
            flipped = cv2.flip(img, 1)
        elif direction == 'vertical':
            flipped = cv2.flip(img, 0)
        else:  # both
            flipped = cv2.flip(img, -1)
        
        cv2.imwrite(output_path, flipped)
        return True
    
    @staticmethod
    def _normalize(input_path, output_path):
        """Normalisation des pixels [0,1] -> [0,255]"""
        img = cv2.imread(input_path)
        normalized = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        cv2.imwrite(output_path, normalized)
        return True
    
    @staticmethod
    def _histogram_equalization(input_path, output_path):
        """Égalisation d'histogramme"""
        img = cv2.imread(input_path)
        
        # Convertir en YUV et égaliser le canal Y
        yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
        result = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        
        cv2.imwrite(output_path, result)
        return True
    
    @staticmethod
    def _extract_channel(input_path, output_path, params):
        """Extraction de canal RGB"""
        channel = params.get('channel', 'red') if params else 'red'
        
        img = cv2.imread(input_path)
        b, g, r = cv2.split(img)
        
        if channel == 'red':
            result = cv2.merge([np.zeros_like(b), np.zeros_like(g), r])
        elif channel == 'green':
            result = cv2.merge([np.zeros_like(b), g, np.zeros_like(r)])
        else:  # blue
            result = cv2.merge([b, np.zeros_like(g), np.zeros_like(r)])
        
        cv2.imwrite(output_path, result)
        return True