import cv2
import os
from config.settings import Config  # ✨ FIX: Import Config, pas PROCESSED_FOLDER
from services.processing_service import ProcessingService


def apply_preset_operations(image_path, preset_name):
    """Apply a series of operations defined by a preset"""
    presets = {
        'enhance_contrast': [
            {'type': 'histogram_equalization', 'params': {}},  # ✨ FIX: Dict au lieu de tuple
            {'type': 'sharpen', 'params': {'strength': 1.5}}
        ],
        'edge_detection': [
            {'type': 'grayscale', 'params': {}},
            {'type': 'gaussian_blur', 'params': {'kernel':  5}},
            {'type': 'canny', 'params': {'threshold1': 100, 'threshold2': 200}}
        ],
        'denoise': [
            {'type':  'bilateral_filter', 'params': {'d': 9, 'sigmaColor': 75, 'sigmaSpace': 75}}
        ],
        'black_white': [
            {'type': 'grayscale', 'params': {}},
            {'type': 'adaptive_threshold', 'params': {'blockSize': 11, 'C':  2}}
        ]
    }

    if preset_name not in presets:
        raise ValueError(f"Unknown preset: {preset_name}")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to read image")

    # ✨ FIX:  Pas d'instanciation, méthode statique directe
    # Apply each operation in sequence
    for operation in presets[preset_name]:
        img = ProcessingService. apply_operation(img, operation['type'], operation['params'])

    # Save result
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    output_filename = f"{name}_preset_{preset_name}{ext}"
    output_path = os.path.join(Config. PROCESSED_FOLDER, output_filename)  # ✨ FIX: Config.PROCESSED_FOLDER

    cv2.imwrite(output_path, img)
    return output_path