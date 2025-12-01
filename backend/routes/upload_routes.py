from flask import Blueprint, request, jsonify, send_from_directory
from services.upload_service import UploadService
from utils.file_utils import FileUtils
from utils.error_handlers import handle_upload_error, handle_file_not_found
from config.settings import Config

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_files():
    """Upload multiple files"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'Aucun fichier fourni'}), 400
        
        files = request.files.getlist('files')
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        success, results = UploadService.upload_files(files)
        
        if success:
            successful = [r for r in results if r.get('success')]
            failed = [r for r in results if not r.get('success')]
            
            return jsonify({
                'message': f'{len(successful)} fichier(s) uploadé(s) avec succès',
                'successful_uploads': successful,
                'failed_uploads': failed,
                'total_uploaded': len(successful)
            })
        else:
            return jsonify({'error': results}), 400
            
    except Exception as e:
        return handle_upload_error(e)

@upload_bp.route('/gallery', methods=['GET'])
def get_gallery():
    """Récupérer la galerie d'images"""
    try:
        images = FileUtils.get_uploaded_images()
        return jsonify({
            'images': images,
            'total': len(images)
        })
    except Exception as e:
        return handle_upload_error(e)

@upload_bp.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    """Récupérer une image spécifique"""
    try:
        return send_from_directory(Config.UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return handle_file_not_found()

@upload_bp.route('/image/<filename>', methods=['DELETE'])
def delete_image(filename):
    """Supprimer une image"""
    try:
        if FileUtils.delete_image(filename):
            return jsonify({'message': 'Image supprimée avec succès'})
        else:
            return handle_file_not_found()
    except Exception as e:
        return handle_upload_error(e)