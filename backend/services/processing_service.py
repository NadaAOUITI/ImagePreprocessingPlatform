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

        elif operation == 'edge_canny':
            if 'low' in params and 'high' in params:
                suffix_parts.append(f"l{params['low']}h{params['high']}")
        elif operation == 'extract_channel' and 'channel' in params:
            suffix_parts.append(f"{params['channel']}")
        
        return f"_{'_'.join(suffix_parts)}" if suffix_parts else ""
        # ✨ NOUVEAU: Méthode pour les fonctionnalités avancées (preview & presets)

    @staticmethod
    def apply_contrast_brightness(image, params):
        alpha = float(params.get('contrast', 1.0))
        beta = int(params.get('brightness', 0))
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    @staticmethod
    def apply_operation(image, operation, params):
        """
        Apply a single processing operation to an image (for preview and presets)

        Args:
            image:  numpy array (cv2 image) - NOT a file path
            operation: string name of operation
            params: dict of parameters for the operation

        Returns:
            Processed image as numpy array
        """
        img = image.copy()

        try:
            # Map new operation names to implementations
            if operation == 'grayscale':
                if len(img.shape) == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # Convert back to 3 channels for consistency
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            elif operation == 'blur' or operation == 'gaussian_blur':
                kernel = params.get('kernel', 5) if params else 5
                # Ensure kernel is odd
                kernel = kernel if kernel % 2 == 1 else kernel + 1
                img = cv2.GaussianBlur(img, (kernel, kernel), 0)

            elif operation == 'sharpen':
                strength = params.get('strength', 1.0) if params else 1.0
                kernel = np.array([[-1, -1, -1],
                                   [-1, 9, -1],
                                   [-1, -1, -1]], dtype=np.float32) * strength
                img = cv2.filter2D(img, -1, kernel)

            elif operation == 'canny':
                threshold1 = params.get('threshold1', 100) if params else 100
                threshold2 = params.get('threshold2', 200) if params else 200
                if len(img.shape) == 3:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                else:
                    gray = img
                edges = cv2.Canny(gray, threshold1, threshold2)
                img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

            elif operation == 'histogram_equalization':
                if len(img.shape) == 3:
                    # Convert to YUV
                    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                    # Equalize the Y channel
                    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
                    img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
                else:
                    img = cv2.equalizeHist(img)
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            elif operation == 'bilateral_filter':
                d = params.get('d', 9) if params else 9
                sigmaColor = params.get('sigmaColor', 75) if params else 75
                sigmaSpace = params.get('sigmaSpace', 75) if params else 75
                img = cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)

            elif operation == 'adaptive_threshold':
                blockSize = params.get('blockSize', 11) if params else 11
                C = params.get('C', 2) if params else 2
                if len(img.shape) == 3:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                else:
                    gray = img
                thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY, blockSize, C)
                img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

            elif operation == 'median_blur':
                kernel = params.get('kernel', 5) if params else 5
                kernel = kernel if kernel % 2 == 1 else kernel + 1
                img = cv2.medianBlur(img, kernel)

            elif operation == 'rotate':
                angle = params.get('angle', 90) if params else 90
                if angle == 90:
                    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                elif angle == 180:
                    img = cv2.rotate(img, cv2.ROTATE_180)
                elif angle == 270:
                    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                else:
                    # Custom angle
                    h, w = img.shape[:2]
                    center = (w // 2, h // 2)
                    M = cv2.getRotationMatrix2D(center, angle, 1.0)
                    img = cv2.warpAffine(img, M, (w, h))

            elif operation == 'flip':
                direction = params.get('direction', 'horizontal') if params else 'horizontal'
                if direction == 'horizontal':
                    img = cv2.flip(img, 1)
                elif direction == 'vertical':
                    img = cv2.flip(img, 0)
                elif direction == 'both':
                    img = cv2.flip(img, -1)

            elif operation == 'resize':
                width = params.get('width') if params else None
                height = params.get('height') if params else None
                if width and height:
                    img = cv2.resize(img, (int(width), int(height)))

            elif operation == 'brightness':
                value = params.get('value', 30) if params else 30
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv)
                v = cv2.add(v, value)
                v = np.clip(v, 0, 255)
                final_hsv = cv2.merge((h, s, v))
                img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

            elif operation == 'contrast':
                value = params.get('value', 1.5) if params else 1.5
                img = cv2.convertScaleAbs(img, alpha=value, beta=0)
            elif operation == 'contrast_brightness':
                return ProcessingService.apply_contrast_brightness(image, params)
            else:
                raise ValueError(f"Unknown operation: {operation}")

            return img

        except Exception as e:
            raise Exception(f"Error applying operation '{operation}': {str(e)}")

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
        # ✨ AJOUT:  Nouvelle méthode pour les fonctionnalités avancées

    @staticmethod
    def apply_operation(image, operation, params):
        """
        Apply a single processing operation to an image (for preview and presets)

        Args:
            image: numpy array (cv2 image) - NOT a file path
            operation: string name of operation
            params: dict of parameters for the operation

        Returns:
            Processed image as numpy array
        """
        img = image.copy()

        try:
            # Map new operation names to existing methods
            if operation == 'grayscale':
                if len(img.shape) == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # Convert back to 3 channels for consistency
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            elif operation == 'blur' or operation == 'gaussian_blur':
                kernel = params.get('kernel', 5)
                # Ensure kernel is odd
                kernel = kernel if kernel % 2 == 1 else kernel + 1
                img = cv2.GaussianBlur(img, (kernel, kernel), 0)

            elif operation == 'sharpen':
                strength = params.get('strength', 1.0)
                kernel = np.array([[-1, -1, -1],
                                   [-1, 9, -1],
                                   [-1, -1, -1]]) * strength
                img = cv2.filter2D(img, -1, kernel)

            elif operation == 'canny':
                threshold1 = params.get('threshold1', 100)
                threshold2 = params.get('threshold2', 200)
                if len(img.shape) == 3:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                else:
                    gray = img
                edges = cv2.Canny(gray, threshold1, threshold2)
                img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

            elif operation == 'histogram_equalization':
                if len(img.shape) == 3:
                    # Convert to YUV
                    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                    # Equalize the Y channel
                    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
                    img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
                else:
                    img = cv2.equalizeHist(img)
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            elif operation == 'bilateral_filter':
                d = params.get('d', 9)
                sigmaColor = params.get('sigmaColor', 75)
                sigmaSpace = params.get('sigmaSpace', 75)
                img = cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)

            elif operation == 'adaptive_threshold':
                blockSize = params.get('blockSize', 11)
                C = params.get('C', 2)
                if len(img.shape) == 3:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                else:
                    gray = img
                thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY, blockSize, C)
                img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

            elif operation == 'median_blur':
                kernel = params.get('kernel', 5)
                kernel = kernel if kernel % 2 == 1 else kernel + 1
                img = cv2.medianBlur(img, kernel)
            elif operation == 'contrast_brightness':
                return ProcessingService.apply_contrast_brightness(image, params)

            else:
                raise ValueError(f"Unknown operation: {operation}")

            return img

        except Exception as e:
            raise Exception(f"Error applying operation '{operation}': {str(e)}")

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

            elif operation == 'sharpen_laplacian':
                return ProcessingService._sharpen_laplacian(input_path, output_path)

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
    def _sharpen_laplacian(input_path, output_path):
        """Laplacien + original"""
        img = cv2.imread(input_path)
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        sharpened = cv2.convertScaleAbs(img - laplacian)
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