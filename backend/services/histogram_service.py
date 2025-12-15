import cv2
import numpy as np


def generate_histogram(image_path, channel='all'):
    """Generate histogram data for visualization"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to read image")

    histogram_data = {}

    if channel == 'gray':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        histogram_data['gray'] = hist.flatten().tolist()
    elif channel == 'all':
        # Calculate for each RGB channel
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            histogram_data[color] = hist.flatten().tolist()
    else:
        # Single channel
        channel_map = {'r': 2, 'g': 1, 'b': 0}
        if channel in channel_map:
            hist = cv2.calcHist([img], [channel_map[channel]], None, [256], [0, 256])
            histogram_data[channel] = hist.flatten().tolist()

    return {
        'histogram': histogram_data,
        'width': img.shape[1],
        'height': img.shape[0],
        'channels': img.shape[2] if len(img.shape) == 3 else 1
    }