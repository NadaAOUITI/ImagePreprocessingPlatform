#!/usr/bin/env python3
"""
Test spécifique pour la conversion en niveaux de gris
"""
import cv2
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_grayscale_technical():
    """Test technique de la conversion grayscale"""
    print("🧪 TEST TECHNIQUE GRAYSCALE")
    print("=" * 40)
    
    # 1. Récupérer une image de test
    response = requests.get(f"{BASE_URL}/gallery")
    images = response.json().get("images", [])
    
    if not images:
        print("❌ Aucune image disponible")
        return
    
    filename = images[0]["filename"]
    print(f"📸 Image de test: {filename}")
    
    # 2. Vérifier image originale
    original_path = os.path.join("../uploads", filename)
    original_img = cv2.imread(original_path)
    
    print(f"📊 Image originale:")
    print(f"   Dimensions: {original_img.shape}")
    print(f"   Canaux: {len(original_img.shape)} ({'3 canaux RGB' if len(original_img.shape) == 3 else '1 canal'})")
    
    # 3. Appliquer grayscale via API
    payload = {"filename": filename, "operation": "grayscale"}
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
    print(f"   Canaux: {len(processed_img.shape)} ({'3 canaux RGB' if len(processed_img.shape) == 3 else '1 canal'})")
    
    # 5. Validation technique
    print(f"\n🔍 VALIDATION:")
    
    # Vérifier dimensions
    if original_img.shape[:2] == processed_img.shape[:2]:
        print("✅ Dimensions conservées")
    else:
        print("❌ Dimensions modifiées")
    
    # Vérifier conversion en grayscale
    if len(processed_img.shape) == 2:
        print("✅ Conversion en 1 canal réussie")
    elif len(processed_img.shape) == 3 and processed_img.shape[2] == 1:
        print("✅ Conversion en 1 canal réussie (format 3D)")
    else:
        print("❌ Conversion échouée - toujours en couleur")
    
    print(f"\n📁 Fichiers:")
    print(f"   Original: {original_path}")
    print(f"   Traité: {processed_path}")

if __name__ == "__main__":
    test_grayscale_technical()