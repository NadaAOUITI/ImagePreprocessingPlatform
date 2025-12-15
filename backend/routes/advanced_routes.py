from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import base64
import os
from config.settings import Config
from services.processing_service import ProcessingService  # ✨ Déplacé en haut

advanced_bp = Blueprint('advanced', __name__)


@advanced_bp.route('/preview', methods=['POST'])
def preview_transformation():
    """Real-time preview of transformations without saving"""
    try:
        data = request.json
        filename = data.get('filename')
        operation = data.get('operation')
        params = data.get('params', {})

        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        img = cv2.imread(filepath)
        if img is None:
            return jsonify({'error': 'Failed to read image'}), 400

        # ✅ FIX: Méthode statique directe (pas d'instanciation)
        result = ProcessingService.apply_operation(img, operation, params)

        # Convert to base64 for preview
        _, buffer = cv2.imencode('.png', result)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'preview': f'data:image/png;base64,{img_base64}',
            'success': True
        })
    except Exception as e:
        return jsonify({'error':  str(e)}), 500


@advanced_bp.route('/histogram/<filename>', methods=['GET'])
def get_histogram(filename):
    """Generate histogram data for an image"""
    try:
        from services.histogram_service import generate_histogram

        channel = request.args.get('channel', 'all')

        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        histogram_data = generate_histogram(filepath, channel)
        return jsonify(histogram_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/roi/detect', methods=['POST'])
def detect_roi():
    """Detect regions of interest (faces, contours)"""
    try:
        from services.roi_service import detect_faces, detect_contours

        data = request. json
        filename = data.get('filename')
        roi_type = data.get('type', 'faces')

        filepath = os.path.join(Config. UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        if roi_type == 'faces':
            regions = detect_faces(filepath)
        else:
            regions = detect_contours(filepath)

        return jsonify({'regions':  regions, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@advanced_bp.route('/presets', methods=['GET'])
def get_presets():
    """Get available preprocessing presets"""
    presets = {
        'enhance_contrast': {
            'name':  'Enhance Contrast',
            'operations': [
                {'type': 'histogram_equalization', 'params': {}},
                {'type': 'sharpen', 'params': {'strength':  1.5}}
            ]
        },
        'edge_detection': {
            'name':  'Edge Detection',
            'operations': [
                {'type':  'grayscale', 'params': {}},
                {'type': 'gaussian_blur', 'params': {'kernel': 5}},
                {'type': 'canny', 'params':  {'threshold1': 100, 'threshold2': 200}}
            ]
        },
        'denoise': {
            'name': 'Denoise',
            'operations': [
                {'type': 'bilateral_filter', 'params': {'d': 9, 'sigmaColor':  75, 'sigmaSpace': 75}}
            ]
        },
        'black_white': {
            'name': 'Black & White',
            'operations': [
                {'type':  'grayscale', 'params': {}},
                {'type': 'adaptive_threshold', 'params': {'blockSize': 11, 'C': 2}}
            ]
        }
    }
    return jsonify(presets)


@advanced_bp.route('/preset/apply', methods=['POST'])
def apply_preset():
    """Apply a preset to an image"""
    try:
        from services.preset_service import apply_preset_operations

        data = request.json
        filename = data.get('filename')
        preset_name = data.get('preset')

        filepath = os. path.join(Config.UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        result_path = apply_preset_operations(filepath, preset_name)

        return jsonify({'processed_image': os.path.basename(result_path), 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500