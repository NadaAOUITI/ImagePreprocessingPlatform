class OperationsService:
    @staticmethod
    def get_available_operations():
        """Retourne la liste des opérations disponibles avec leurs paramètres"""
        return {
            'grayscale': {
                'name': 'Niveaux de gris',
                'description': 'Convertit l\'image en niveaux de gris',
                'parameters': {}
            },
            'threshold': {
                'name': 'Seuillage binaire',
                'description': 'Applique un seuillage binaire',
                'parameters': {
                    'threshold': {'type': 'int', 'default': 127, 'min': 0, 'max': 255},
                    'type': {'type': 'select', 'default': 'binary', 'options': ['binary', 'adaptive']}
                }
            },
            # === FILTRES DE FLOU ===
            'blur_gaussian': {
                'name': 'Flou Gaussien',
                'description': 'Applique un flou gaussien',
                'parameters': {
                    'kernel_size': {'type': 'int', 'default': 5, 'min': 3, 'max': 31, 'step': 2}
                }
            },
            'blur_median': {
                'name': 'Flou Médian',
                'description': 'Applique un flou médian (réduit le bruit)',
                'parameters': {
                    'kernel_size': {'type': 'int', 'default': 5, 'min': 3, 'max': 31, 'step': 2}
                }
            },
            'blur_average': {
                'name': 'Flou Moyenneur',
                'description': 'Applique un flou moyenneur',
                'parameters': {
                    'kernel_size': {'type': 'int', 'default': 5, 'min': 3, 'max': 31, 'step': 2}
                }
            },
            # === FILTRES DE SHARPENING ===
            'sharpen_kernel': {
                'name': 'Accentuation Kernel',
                'description': 'Accentue avec kernel classique',
                'parameters': {}
            },
            'sharpen_unsharp': {
                'name': 'Unsharp Mask',
                'description': 'Accentuation par masque flou',
                'parameters': {
                    'strength': {'type': 'float', 'default': 1.5, 'min': 0.5, 'max': 3.0}
                }
            },
            'sharpen_laplacian': {
                'name': 'Laplacien + Original',
                'description': 'Accentuation par Laplacien',
                'parameters': {}
            },
            'sharpen_highboost': {
                'name': 'High-Boost Filter',
                'description': 'Filtre d\'amplification des hautes fréquences',
                'parameters': {
                    'boost_factor': {'type': 'float', 'default': 2.0, 'min': 1.0, 'max': 5.0}
                }
            },
            # === FILTRES DE DÉTECTION DE CONTOURS ===
            'edge_canny': {
                'name': 'Détection Canny',
                'description': 'Détecte les contours avec Canny',
                'parameters': {
                    'low': {'type': 'int', 'default': 50, 'min': 0, 'max': 255},
                    'high': {'type': 'int', 'default': 150, 'min': 0, 'max': 255}
                }
            },
            'edge_roberts': {
                'name': 'Filtre de Roberts',
                'description': 'Détection de contours avec Roberts',
                'parameters': {}
            },
            'edge_sobel': {
                'name': 'Filtre de Sobel',
                'description': 'Détection de contours avec Sobel',
                'parameters': {}
            },
            'edge_prewitt': {
                'name': 'Filtre de Prewitt',
                'description': 'Détection de contours avec Prewitt',
                'parameters': {}
            },
            'edge_laplacian': {
                'name': 'Filtre Laplacien',
                'description': 'Détection de contours avec Laplacien',
                'parameters': {}
            },
            'resize': {
                'name': 'Redimensionnement',
                'description': 'Redimensionne l\'image',
                'parameters': {
                    'width': {'type': 'int', 'default': 300, 'min': 50, 'max': 2000},
                    'height': {'type': 'int', 'default': 300, 'min': 50, 'max': 2000}
                }
            },
            'rotate': {
                'name': 'Rotation',
                'description': 'Fait tourner l\'image',
                'parameters': {
                    'angle': {'type': 'int', 'default': 90, 'min': -360, 'max': 360}
                }
            },
            'flip': {
                'name': 'Retournement',
                'description': 'Retourne l\'image',
                'parameters': {
                    'direction': {'type': 'select', 'default': 'horizontal', 'options': ['horizontal', 'vertical', 'both']}
                }
            },
            'normalize': {
                'name': 'Normalisation',
                'description': 'Normalise les valeurs des pixels',
                'parameters': {}
            },
            'histogram_eq': {
                'name': 'Égalisation d\'histogramme',
                'description': 'Améliore le contraste',
                'parameters': {}
            },
            'histogram_stretch': {
                'name': 'Étirement d\'histogramme',
                'description': 'Étire l\'histogramme pour utiliser toute la plage dynamique',
                'parameters': {}
            },
            'extract_channel': {
                'name': 'Extraction de canal',
                'description': 'Extrait un canal RGB',
                'parameters': {
                    'channel': {'type': 'select', 'default': 'red', 'options': ['red', 'green', 'blue']}
                }
            }
        }