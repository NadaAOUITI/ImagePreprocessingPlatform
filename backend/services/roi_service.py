import cv2
import numpy as np
import os


def detect_faces(image_path):
    """Detect faces in the image using Haar Cascades"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to read image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load Haar Cascade (you may need to download this)
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    regions = []
    for (x, y, w, h) in faces:
        regions.append({
            'x': int(x),
            'y': int(y),
            'width': int(w),
            'height': int(h),
            'type': 'face'
        })

    return regions


def detect_contours(image_path, min_area=500):
    """Detect object contours in the image"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to read image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            regions.append({
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h),
                'type': 'contour',
                'area': float(area)
            })

    return regions