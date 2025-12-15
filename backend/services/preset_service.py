import cv2
import os
from config.settings import PROCESSED_FOLDER
from services.processing_service import ProcessingService


def apply_preset_operations(image_path, preset_name):
    """Apply a series of operations defined by a preset"""
    presets = {
        'enhance_contrast': [
            ('histogram_equalization', {}),
            ('sharpen', {'strength': 1.5})
        ],
        'edge_detection': [
            ('grayscale', {}),
            ('gaussian_blur', {'kernel': 5}),
            ('canny', {'threshold1': 100, 'threshold2': 200})
        ],
        'denoise': [
            ('bilateral_filter', {'d': 9, 'sigmaColor': 75, 'sigmaSpace': 75})
        ],
        'black_white': [
            ('grayscale', {}),
            ('adaptive_threshold', {'blockSize': 11, 'C': 2})
        ]
    }

    if preset_name not in presets:
        raise ValueError(f"Unknown preset: {preset_name}")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to read image")

    processor = ProcessingService()

    # Apply each operation in sequence
    for operation, params in presets[preset_name]:
        img = processor.apply_operation(img, operation, params)

    # Save result
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    output_filename = f"{name}_preset_{preset_name}{ext}"
    output_path = os.path.join(PROCESSED_FOLDER, output_filename)

    cv2.imwrite(output_path, img)
    return output_path