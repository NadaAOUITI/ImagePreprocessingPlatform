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
            'blur': {
                'name': 'Flou gaussien',
                'description': 'Applique un flou gaussien',
                'parameters': {
                    'kernel_size': {'type': 'int', 'default': 5, 'min': 3, 'max': 31, 'step': 2}
                }
            },
            'sharpen': {
                'name': 'Accentuation',
                'description': 'Accentue les détails de l\'image',
                'parameters': {}
            },
            'edge_detection': {
                'name': 'Détection de contours',
                'description': 'Détecte les contours avec Canny',
                'parameters': {
                    'low': {'type': 'int', 'default': 50, 'min': 0, 'max': 255},
                    'high': {'type': 'int', 'default': 150, 'min': 0, 'max': 255}
                }
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
            'extract_channel': {
                'name': 'Extraction de canal',
                'description': 'Extrait un canal RGB',
                'parameters': {
                    'channel': {'type': 'select', 'default': 'red', 'options': ['red', 'green', 'blue']}
                }
            }
        }