from flask import Blueprint, request, jsonify, send_from_directory
from services.processing_service import ProcessingService
from services.operations_service import OperationsService
from utils.error_handlers import handle_upload_error, handle_file_not_found
from config.settings import Config

processing_bp = Blueprint('processing', __name__)

@processing_bp.route('/process', methods=['POST'])
def process_image():
    """Traite une image avec l'opération spécifiée"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données JSON requises'}), 400
        
        filename = data.get('filename')
        operation = data.get('operation')
        params = data.get('parameters', {})
        
        if not filename or not operation:
            return jsonify({'error': 'filename et operation requis'}), 400
        
        # Traiter l'image
        output_filename, error = ProcessingService.process_image(filename, operation, params)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Traitement terminé avec succès',
            'input_file': filename,
            'output_file': output_filename,
            'operation': operation,
            'parameters': params
        })
        
    except Exception as e:
        return handle_upload_error(e)

@processing_bp.route('/operations', methods=['GET'])
def get_operations():
    """Récupère la liste des opérations disponibles"""
    try:
        operations = OperationsService.get_available_operations()
        return jsonify({'operations': operations})
    except Exception as e:
        return handle_upload_error(e)

@processing_bp.route('/processed/<filename>', methods=['GET'])
def get_processed_image(filename):
    """Récupère une image traitée"""
    try:
        return send_from_directory(Config.PROCESSED_FOLDER, filename)
    except FileNotFoundError:
        return handle_file_not_found()

@processing_bp.route('/download/<filename>', methods=['GET'])
def download_processed_image(filename):
    """Télécharge une image traitée"""
    try:
        return send_from_directory(
            Config.PROCESSED_FOLDER, 
            filename, 
            as_attachment=True,
            download_name=filename
        )
    except FileNotFoundError:
        return handle_file_not_found()