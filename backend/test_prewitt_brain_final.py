#!/usr/bin/env python3
"""
Test Prewitt sur image cerveau:
- Combine: utilise la methode existante _edge_prewitt
- Vertical/Horizontal: implementation directe
"""
import cv2
import numpy as np
import os
import sys
sys.path.append('.')
from services.processing_service import ProcessingService

def test_prewitt_brain():
    """Test Prewitt: vertical, horizontal, combine"""
    print("TEST PREWITT SUR IMAGE CERVEAU")
    print("=" * 40)
    
    input_image = "16-Flair_brain0003.png"
    input_path = os.path.join("../uploads", input_image)
    
    if not os.path.exists(input_path):
        print(f"Image non trouvee: {input_path}")
        return
    
    print(f"Image: {input_image}")
    
    # 1. PREWITT VERTICAL (Gx seulement)
    print("\n1. PREWITT VERTICAL (Gx)")
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    edges_x = cv2.filter2D(img, cv2.CV_64F, prewitt_x)
    result_x = cv2.convertScaleAbs(edges_x)
    
    output_vertical = os.path.join("../processed", "brain_prewitt_vertical.png")
    cv2.imwrite(output_vertical, result_x)
    print(f"Sauvegarde: brain_prewitt_vertical.png")
    
    # 2. PREWITT HORIZONTAL (Gy seulement)
    print("\n2. PREWITT HORIZONTAL (Gy)")
    prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    edges_y = cv2.filter2D(img, cv2.CV_64F, prewitt_y)
    result_y = cv2.convertScaleAbs(edges_y)
    
    output_horizontal = os.path.join("../processed", "brain_prewitt_horizontal.png")
    cv2.imwrite(output_horizontal, result_y)
    print(f"Sauvegarde: brain_prewitt_horizontal.png")
    
    # 3. PREWITT COMBINE (utilise la methode existante)
    print("\n3. PREWITT COMBINE (methode existante)")
    output_combined = os.path.join("../processed", "brain_prewitt_combined.png")
    success = ProcessingService._edge_prewitt(input_path, output_combined)
    
    if success:
        print(f"Sauvegarde: brain_prewitt_combined.png")
    else:
        print("Erreur avec la methode existante")
    
    # Statistiques
    print("\nSTATISTIQUES:")
    print(f"Vertical   - Min: {result_x.min():3d}, Max: {result_x.max():3d}")
    print(f"Horizontal - Min: {result_y.min():3d}, Max: {result_y.max():3d}")
    
    if success:
        combined_img = cv2.imread(output_combined, cv2.IMREAD_GRAYSCALE)
        print(f"Combine    - Min: {combined_img.min():3d}, Max: {combined_img.max():3d}")
    
    print("\nRESULTATS:")
    print("- Vertical: Detecte contours verticaux (Gx)")
    print("- Horizontal: Detecte contours horizontaux (Gy)")
    print("- Combine: Detecte tous contours (sqrt(Gx² + Gy²))")

if __name__ == "__main__":
    test_prewitt_brain()