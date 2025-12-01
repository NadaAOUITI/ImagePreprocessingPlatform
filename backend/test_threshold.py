#!/usr/bin/env python3
"""
Test spécifique pour le seuillage binaire fixe
"""
import cv2
import numpy as np
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_threshold_technical():
    """Test technique du seuillage binaire fixe"""
    print("🧪 TEST TECHNIQUE SEUILLAGE BINAIRE")
    print("=" * 45)
    
    # 1. Utiliser img.png spécifiquement
    filename = "img.png"
    
    # Vérifier que img.png existe
    original_path = os.path.join("../uploads", filename)
    if not os.path.exists(original_path):
        print(f"❌ {filename} non trouvé dans uploads/")
        return
    print(f"📸 Image de test: {filename}")
    
    # 2. Vérifier image originale
    original_img = cv2.imread(original_path)
    
    print(f"📊 Image originale:")
    print(f"   Dimensions: {original_img.shape}")
    print(f"   Type: Couleur ({original_img.shape[2]} canaux)")
    
    # 3. Appliquer seuillage binaire fixe via API
    threshold_value = 127  # Valeur de seuil fixe
    payload = {
        "filename": filename, 
        "operation": "threshold",
        "parameters": {
            "threshold": threshold_value,
            "type": "binary"
        }
    }
    
    print(f"🔧 Paramètres: seuil = {threshold_value}, type = binaire")
    
    response = requests.post(f"{BASE_URL}/process", json=payload)
    
    if response.status_code != 200:
        print(f"❌ Erreur API: {response.text}")
        return
    
    result = response.json()
    output_filename = result["output_file"]
    print(f"✅ Traitement réussi: {output_filename}")
    
    # 4. Vérifier image traitée
    processed_path = os.path.join("../processed", output_filename)
    
    if not os.path.exists(processed_path):
        print("❌ Fichier traité non trouvé")
        return
    
    processed_img = cv2.imread(processed_path, cv2.IMREAD_UNCHANGED)
    
    print(f"📊 Image traitée:")
    print(f"   Dimensions: {processed_img.shape}")
    print(f"   Type: {'Grayscale' if len(processed_img.shape) == 2 else 'Couleur'}")
    
    # 5. Validation technique
    print(f"\n🔍 VALIDATION TECHNIQUE:")
    
    # Vérifier dimensions
    if original_img.shape[:2] == processed_img.shape[:2]:
        print("✅ Dimensions conservées")
    else:
        print("❌ Dimensions modifiées")
    
    # Vérifier conversion en grayscale
    if len(processed_img.shape) == 2:
        print("✅ Conversion en grayscale réussie")
    else:
        print("❌ Image toujours en couleur")
    
    # Vérifier valeurs binaires (0 ou 255 seulement)
    unique_values = np.unique(processed_img)
    print(f"📈 Valeurs uniques dans l'image: {unique_values}")
    
    if len(unique_values) <= 2 and all(val in [0, 255] for val in unique_values):
        print("✅ Seuillage binaire réussi (valeurs 0 et 255 seulement)")
    else:
        print("❌ Seuillage binaire échoué (valeurs non binaires)")
    
    # Statistiques
    total_pixels = processed_img.size
    white_pixels = np.sum(processed_img == 255)
    black_pixels = np.sum(processed_img == 0)
    
    print(f"\n📊 STATISTIQUES:")
    print(f"   Pixels totaux: {total_pixels}")
    print(f"   Pixels blancs (255): {white_pixels} ({white_pixels/total_pixels*100:.1f}%)")
    print(f"   Pixels noirs (0): {black_pixels} ({black_pixels/total_pixels*100:.1f}%)")
    
    print(f"\n📁 FICHIERS POUR VÉRIFICATION VISUELLE:")
    print(f"   Original: {original_path}")
    print(f"   Seuillé: {processed_path}")
    print(f"\n💡 Ouvre ces deux images pour comparer visuellement")

if __name__ == "__main__":
    test_threshold_technical()