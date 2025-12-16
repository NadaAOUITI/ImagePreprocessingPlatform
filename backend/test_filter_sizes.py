#!/usr/bin/env python3
"""
Test des filtres avec differentes tailles
"""
import sys
sys.path.append('.')
from services.processing_service import ProcessingService
import os

def test_filter_sizes():
    """Test filtres avec tailles 3, 5, 7"""
    print("TEST FILTRES AVEC DIFFERENTES TAILLES")
    print("=" * 50)
    
    input_image = "16-Flair_brain0003.png"
    input_path = os.path.join("../uploads", input_image)
    
    if not os.path.exists(input_path):
        print(f"Image non trouvee: {input_path}")
        return
    
    print(f"Image: {input_image}")
    
    # Tailles a tester
    sizes = [3, 5, 7]
    
    # 1. TEST PREWITT
    print("\n1. PREWITT - Differentes tailles")
    for size in sizes:
        output_path = os.path.join("../processed", f"brain_prewitt_{size}x{size}.png")
        params = {'kernel_size': size}
        
        success = ProcessingService._edge_prewitt(input_path, output_path, params)
        if success:
            print(f"  Prewitt {size}x{size}: brain_prewitt_{size}x{size}.png")
        else:
            print(f"  Erreur Prewitt {size}x{size}")
    
    # 2. TEST SOBEL
    print("\n2. SOBEL - Differentes tailles")
    for size in sizes:
        output_path = os.path.join("../processed", f"brain_sobel_{size}x{size}.png")
        params = {'kernel_size': size}
        
        success = ProcessingService._edge_sobel(input_path, output_path, params)
        if success:
            print(f"  Sobel {size}x{size}: brain_sobel_{size}x{size}.png")
        else:
            print(f"  Erreur Sobel {size}x{size}")
    
    # 3. TEST LAPLACIEN
    print("\n3. LAPLACIEN - Differentes tailles")
    for size in sizes:
        output_path = os.path.join("../processed", f"brain_laplacian_{size}x{size}.png")
        params = {'kernel_size': size}
        
        success = ProcessingService._edge_laplacian(input_path, output_path, params)
        if success:
            print(f"  Laplacien {size}x{size}: brain_laplacian_{size}x{size}.png")
        else:
            print(f"  Erreur Laplacien {size}x{size}")
    
    print("\nRESULTATS:")
    print("- Taille 3x3: Detection precise, sensible au bruit")
    print("- Taille 5x5: Detection equilibree, moins de bruit")
    print("- Taille 7x7: Detection robuste, contours plus epais")
    
    print(f"\nFichiers generes dans ../processed/:")
    for filter_name in ['prewitt', 'sobel', 'laplacian']:
        for size in sizes:
            print(f"- brain_{filter_name}_{size}x{size}.png")

if __name__ == "__main__":
    test_filter_sizes()