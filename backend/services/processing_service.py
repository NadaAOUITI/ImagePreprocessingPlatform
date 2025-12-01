import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from config.settings import Config

class ProcessingService:
    @staticmethod
    def _generate_param_suffix(operation, params):
        """Génère un suffixe basé sur les paramètres"""
        if not params:
            return ""
        
        suffix_parts = []
        
        if operation == 'rotate' and 'angle' in params:
            suffix_parts.append(f"{params['angle']}deg")
        elif operation == 'flip' and 'direction' in params:
            suffix_parts.append(f"{params['direction']}")
        elif operation in ['blur_gaussian', 'blur_median', 'blur_average'] and 'kernel_size' in params:
            suffix_parts.append(f"k{params['kernel_size']}")
        elif operation == 'threshold':
            if 'threshold' in params:
                suffix_parts.append(f"t{params['threshold']}")
            if 'type' in params:
                suffix_parts.append(f"{params['type']}")
        elif operation == 'resize':
            if 'width' in params and 'height' in params:
                suffix_parts.append(f"{params['width']}x{params['height']}")
        elif operation == 'sharpen_unsharp' and 'strength' in params:
            suffix_parts.append(f"s{params['strength']}")
        elif operation == 'sharpen_highboost' and 'boost_factor' in params:
            suffix_parts.append(f"b{params['boost_factor']}")
        elif operation == 'edge_canny':
            if 'low' in params and 'high' in params:
                suffix_parts.append(f"l{params['low']}h{params['high']}")
        elif operation == 'extract_channel' and 'channel' in params:
            suffix_parts.append(f"{params['channel']}")
        
        return f"_{'_'.join(suffix_parts)}" if suffix_parts else ""
    
    @staticmethod
    def process_image(filename, operation, params=None):
        """Traite une image avec l'opération spécifiée"""
        try:
            input_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            if not os.path.exists(input_path):
                return None, "Image non trouvée"
            
            # Générer nom de fichier de sortie avec paramètres
            name, ext = os.path.splitext(filename)
            param_suffix = ProcessingService._generate_param_suffix(operation, params)
            output_filename = f"{name}_{operation}{param_suffix}{ext}"
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
            # Filtres de flou
            elif operation == 'blur_gaussian':
                return ProcessingService._blur_gaussian(input_path, output_path, params)
            elif operation == 'blur_median':
                return ProcessingService._blur_median(input_path, output_path, params)
            elif operation == 'blur_average':
                return ProcessingService._blur_average(input_path, output_path, params)
            # Filtres de sharpening
            elif operation == 'sharpen_kernel':
                return ProcessingService._sharpen_kernel(input_path, output_path)
            elif operation == 'sharpen_unsharp':
                return ProcessingService._sharpen_unsharp(input_path, output_path, params)
            elif operation == 'sharpen_laplacian':
                return ProcessingService._sharpen_laplacian(input_path, output_path)
            elif operation == 'sharpen_highboost':
                return ProcessingService._sharpen_highboost(input_path, output_path, params)
            # Filtres de détection de contours
            elif operation == 'edge_canny':
                return ProcessingService._edge_canny(input_path, output_path, params)
            elif operation == 'edge_roberts':
                return ProcessingService._edge_roberts(input_path, output_path)
            elif operation == 'edge_sobel':
                return ProcessingService._edge_sobel(input_path, output_path)
            elif operation == 'edge_prewitt':
                return ProcessingService._edge_prewitt(input_path, output_path)
            elif operation == 'edge_laplacian':
                return ProcessingService._edge_laplacian(input_path, output_path)
            # Autres opérations
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
            elif operation == 'histogram_stretch':
                return ProcessingService._histogram_stretch(input_path, output_path)
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
    
    # ===== FILTRES DE FLOU =====
    @staticmethod
    def _blur_gaussian(input_path, output_path, params):
        """Flou gaussien"""
        kernel_size = params.get('kernel_size', 5) if params else 5
        img = cv2.imread(input_path)
        blurred = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
        cv2.imwrite(output_path, blurred)
        return True
    
    @staticmethod
    def _blur_median(input_path, output_path, params):
        """Flou médian"""
        kernel_size = params.get('kernel_size', 5) if params else 5
        img = cv2.imread(input_path)
        blurred = cv2.medianBlur(img, kernel_size)
        cv2.imwrite(output_path, blurred)
        return True
    
    @staticmethod
    def _blur_average(input_path, output_path, params):
        """Flou moyenneur"""
        kernel_size = params.get('kernel_size', 5) if params else 5
        img = cv2.imread(input_path)
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
        blurred = cv2.filter2D(img, -1, kernel)
        cv2.imwrite(output_path, blurred)
        return True
    
    # ===== FILTRES DE SHARPENING =====
    @staticmethod
    def _sharpen_kernel(input_path, output_path):
        """Accentuation avec kernel classique"""
        img = cv2.imread(input_path)
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(img, -1, kernel)
        cv2.imwrite(output_path, sharpened)
        return True
    
    @staticmethod
    def _sharpen_unsharp(input_path, output_path, params):
        """Unsharp mask"""
        strength = params.get('strength', 1.5) if params else 1.5
        img = cv2.imread(input_path)
        blurred = cv2.GaussianBlur(img, (9, 9), 0)
        sharpened = cv2.addWeighted(img, 1 + strength, blurred, -strength, 0)
        cv2.imwrite(output_path, sharpened)
        return True
    
    @staticmethod
    def _sharpen_laplacian(input_path, output_path):
        """Laplacien + original"""
        img = cv2.imread(input_path)
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        sharpened = cv2.convertScaleAbs(img - laplacian)
        cv2.imwrite(output_path, sharpened)
        return True
    
    @staticmethod
    def _sharpen_highboost(input_path, output_path, params):
        """High-boost filter"""
        boost_factor = params.get('boost_factor', 2.0) if params else 2.0
        img = cv2.imread(input_path)
        blurred = cv2.GaussianBlur(img, (5, 5), 0)
        high_freq = cv2.subtract(img, blurred)
        sharpened = cv2.addWeighted(img, 1.0, high_freq, boost_factor, 0)
        cv2.imwrite(output_path, sharpened)
        return True
    
    # ===== FILTRES DE DÉTECTION DE CONTOURS =====
    @staticmethod
    def _edge_canny(input_path, output_path, params):
        """Détection de contours Canny"""
        low_threshold = params.get('low', 50) if params else 50
        high_threshold = params.get('high', 150) if params else 150
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        edges = cv2.Canny(img, low_threshold, high_threshold)
        cv2.imwrite(output_path, edges)
        return True
    
    @staticmethod
    def _edge_roberts(input_path, output_path):
        """Filtre de Roberts"""
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        roberts_x = np.array([[1, 0], [0, -1]])
        roberts_y = np.array([[0, 1], [-1, 0]])
        edges_x = cv2.filter2D(img, cv2.CV_64F, roberts_x)
        edges_y = cv2.filter2D(img, cv2.CV_64F, roberts_y)
        edges = np.sqrt(edges_x**2 + edges_y**2)
        edges = cv2.convertScaleAbs(edges)
        cv2.imwrite(output_path, edges)
        return True
    
    @staticmethod
    def _edge_sobel(input_path, output_path):
        """Filtre de Sobel"""
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        edges = np.sqrt(sobel_x**2 + sobel_y**2)
        edges = cv2.convertScaleAbs(edges)
        cv2.imwrite(output_path, edges)
        return True
    
    @staticmethod
    def _edge_prewitt(input_path, output_path):
        """Filtre de Prewitt"""
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        edges_x = cv2.filter2D(img, cv2.CV_64F, prewitt_x)
        edges_y = cv2.filter2D(img, cv2.CV_64F, prewitt_y)
        edges = np.sqrt(edges_x**2 + edges_y**2)
        edges = cv2.convertScaleAbs(edges)
        cv2.imwrite(output_path, edges)
        return True
    
    @staticmethod
    def _edge_laplacian(input_path, output_path):
        """Filtre Laplacien"""
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        edges = cv2.convertScaleAbs(laplacian)
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
    def _histogram_stretch(input_path, output_path):
        """Étirement d'histogramme (contrast stretching)"""
        img = cv2.imread(input_path)
        
        # Étirer chaque canal séparément
        result = np.zeros_like(img)
        
        for i in range(img.shape[2]):
            channel = img[:,:,i]
            
            # Trouver min et max du canal
            min_val = np.min(channel)
            max_val = np.max(channel)
            
            # Éviter la division par zéro
            if max_val > min_val:
                # Étirer vers [0, 255]
                stretched = ((channel - min_val) / (max_val - min_val) * 255).astype(np.uint8)
                result[:,:,i] = stretched
            else:
                result[:,:,i] = channel
        
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