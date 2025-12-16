#!/usr/bin/env python3
"""
Test du filtre de Prewitt sur l'image cerveau
Teste: vertical, horizontal et combiné
"""
import cv2
import numpy as np
import os

def test_prewitt_brain():
    """Test Prewitt sur image cerveau"""
    print("🧠 TEST PREWITT SUR IMAGE CERVEAU")
    print("=" * 50)
    
    # Chemin de l'image
    input_image = "16-Flair_brain0003.png"
    input_path = os.path.join("../uploads", input_image)
    
    # Vérifier si l'image existe
    if not os.path.exists(input_path):
        print(f"❌ Image non trouvée: {input_path}")
        print("📁 Fichiers disponibles dans uploads:")
        if os.path.exists("../uploads"):
            files = os.listdir("../uploads")
            for f in files:
                print(f"   - {f}")
        return
    
    print(f"📸 Image trouvée: {input_image}")
    
    # Charger l'image en grayscale
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    print(f"📊 Dimensions: {img.shape}")
    
    # Masques de Prewitt
    prewitt_x = np.array([[-1, 0, 1], 
                          [-1, 0, 1], 
                          [-1, 0, 1]], dtype=np.float32)
    
    prewitt_y = np.array([[-1, -1, -1], 
                          [ 0,  0,  0], 
                          [ 1,  1,  1]], dtype=np.float32)
    
    print("\n🔍 MASQUES PREWITT:")
    print("Masque X (détection verticale):")
    print(prewitt_x)
    print("\nMasque Y (détection horizontale):")
    print(prewitt_y)
    
    # 1. PREWITT VERTICAL (Gx seulement)
    print("\n1️⃣ PREWITT VERTICAL (contours verticaux)")
    edges_x = cv2.filter2D(img, cv2.CV_64F, prewitt_x)
    edges_x_abs = cv2.convertScaleAbs(edges_x)
    
    output_vertical = os.path.join("../processed", "brain_prewitt_vertical.png")
    cv2.imwrite(output_vertical, edges_x_abs)
    print(f"✅ Sauvegardé: {output_vertical}")
    
    # 2. PREWITT HORIZONTAL (Gy seulement)
    print("\n2️⃣ PREWITT HORIZONTAL (contours horizontaux)")
    edges_y = cv2.filter2D(img, cv2.CV_64F, prewitt_y)
    edges_y_abs = cv2.convertScaleAbs(edges_y)
    
    output_horizontal = os.path.join("../processed", "brain_prewitt_horizontal.png")
    cv2.imwrite(output_horizontal, edges_y_abs)
    print(f"✅ Sauvegardé: {output_horizontal}")
    
    # 3. PREWITT COMBINÉ (magnitude)
    print("\n3️⃣ PREWITT COMBINÉ (magnitude)")
    edges_combined = np.sqrt(edges_x**2 + edges_y**2)
    edges_combined_abs = cv2.convertScaleAbs(edges_combined)
    
    output_combined = os.path.join("../processed", "brain_prewitt_combined.png")
    cv2.imwrite(output_combined, edges_combined_abs)
    print(f"✅ Sauvegardé: {output_combined}")
    
    # Statistiques
    print("\n📊 STATISTIQUES:")
    print(f"Vertical   - Min: {edges_x_abs.min():3d}, Max: {edges_x_abs.max():3d}, Moyenne: {edges_x_abs.mean():.1f}")
    print(f"Horizontal - Min: {edges_y_abs.min():3d}, Max: {edges_y_abs.max():3d}, Moyenne: {edges_y_abs.mean():.1f}")
    print(f"Combiné    - Min: {edges_combined_abs.min():3d}, Max: {edges_combined_abs.max():3d}, Moyenne: {edges_combined_abs.mean():.1f}")
    
    print("\n🎯 RÉSULTATS:")
    print("- Vertical: Détecte les contours verticaux (structures gauche-droite)")
    print("- Horizontal: Détecte les contours horizontaux (structures haut-bas)")
    print("- Combiné: Détecte tous les contours (magnitude totale)")
    
    print(f"\n📁 Fichiers générés dans ../processed/:")
    print("- brain_prewitt_vertical.png")
    print("- brain_prewitt_horizontal.png") 
    print("- brain_prewitt_combined.png")

if __name__ == "__main__":
    test_prewitt_brain()