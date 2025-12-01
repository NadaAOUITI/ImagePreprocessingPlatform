from flask import jsonify
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_upload_error(error):
    """Gestionnaire d'erreurs pour les uploads"""
    logger.error(f"Erreur d'upload: {str(error)}")
    return jsonify({
        'error': 'Erreur lors de l\'upload',
        'message': 'Une erreur inattendue s\'est produite'
    }), 500

def handle_validation_error(errors):
    """Gestionnaire d'erreurs de validation"""
    return jsonify({
        'error': 'Erreur de validation',
        'details': errors
    }), 400

def handle_file_not_found():
    """Gestionnaire pour fichier non trouvé"""
    return jsonify({
        'error': 'Fichier non trouvé'
    }), 404