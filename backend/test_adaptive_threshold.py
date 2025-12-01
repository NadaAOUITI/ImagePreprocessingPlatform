#!/usr/bin/env python3
"""
Test spécifique pour le seuillage adaptatif
"""
import cv2
import numpy as np
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_adaptive_threshold():
    """Test technique du seuillage adaptatif"""
    print("🧪 TEST TECHNIQUE SEUILLAGE ADAPTATIF")
    print("=" * 50)
    
    filename = "img.png"
    
    # Vérifier que img.png existe
    original_path = os.path.join("../uploads", filename)
    if not os.path.exists(original_path):
        print(f"❌ {filename} non trouvé dans uploads/")
        return
    
    print(f"📸 Image de test: {filename}")
    
    # Vérifier image originale
    original_img = cv2.imread(original_path)
    print(f"📊 Image originale:")
    print(f"   Dimensions: {original_img.shape}")
    print(f"   Type: Couleur ({original_img.shape[2]} canaux)")
    
    # Test 1: Seuillage adaptatif
    print(f"\n🔧 TEST 1: SEUILLAGE ADAPTATIF")
    print("-" * 30)
    
    payload1 = {
        "filename": filename, 
        "operation": "threshold",
        "parameters": {
            "type": "adaptive"
        }
    }
    
    response1 = requests.post(f"{BASE_URL}/process", json=payload1)
    
    if response1.status_code == 200:
        result1 = response1.json()
        output_filename1 = result1["output_file"]
        print(f"✅ Traitement adaptatif réussi: {output_filename1}")
        
        # Analyser résultat adaptatif
        processed_path1 = os.path.join("../processed", output_filename1)
        if os.path.exists(processed_path1):
            processed_img1 = cv2.imread(processed_path1, cv2.IMREAD_UNCHANGED)
            
            print(f"📊 Image adaptative:")
            print(f"   Dimensions: {processed_img1.shape}")
            
            # Vérifier valeurs binaires
            unique_values1 = np.unique(processed_img1)
            print(f"📈 Valeurs uniques: {unique_values1}")
            
            if len(unique_values1) <= 2 and all(val in [0, 255] for val in unique_values1):
                print("✅ Seuillage adaptatif binaire réussi")
            else:
                print("❌ Seuillage adaptatif échoué")
            
            # Statistiques
            total_pixels = processed_img1.size
            white_pixels1 = np.sum(processed_img1 == 255)
            black_pixels1 = np.sum(processed_img1 == 0)
            
            print(f"📊 Statistiques adaptatives:")
            print(f"   Pixels blancs: {white_pixels1} ({white_pixels1/total_pixels*100:.1f}%)")
            print(f"   Pixels noirs: {black_pixels1} ({black_pixels1/total_pixels*100:.1f}%)")
            
            print(f"📁 Fichier adaptatif: {processed_path1}")
    else:
        print(f"❌ Erreur seuillage adaptatif: {response1.text}")
    
    # Test 2: Seuillage basé sur la moyenne (simulé avec seuil calculé)
    print(f"\n🔧 TEST 2: SEUILLAGE BASÉ SUR LA MOYENNE")
    print("-" * 40)
    
    # Calculer la moyenne de l'image originale en grayscale
    gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    mean_value = int(np.mean(gray_img))
    print(f"📊 Valeur moyenne calculée: {mean_value}")
    
    payload2 = {
        "filename": filename, 
        "operation": "threshold",
        "parameters": {
            "threshold": mean_value,
            "type": "binary"
        }
    }
    
    response2 = requests.post(f"{BASE_URL}/process", json=payload2)
    
    if response2.status_code == 200:
        result2 = response2.json()
        output_filename2 = result2["output_file"]
        print(f"✅ Traitement basé sur moyenne réussi: {output_filename2}")
        
        # Analyser résultat basé sur moyenne
        processed_path2 = os.path.join("../processed", output_filename2)
        if os.path.exists(processed_path2):
            processed_img2 = cv2.imread(processed_path2, cv2.IMREAD_UNCHANGED)
            
            print(f"📊 Image basée sur moyenne:")
            print(f"   Dimensions: {processed_img2.shape}")
            print(f"   Seuil utilisé: {mean_value}")
            
            # Vérifier valeurs binaires
            unique_values2 = np.unique(processed_img2)
            print(f"📈 Valeurs uniques: {unique_values2}")
            
            if len(unique_values2) <= 2 and all(val in [0, 255] for val in unique_values2):
                print("✅ Seuillage basé sur moyenne réussi")
            else:
                print("❌ Seuillage basé sur moyenne échoué")
            
            # Statistiques
            white_pixels2 = np.sum(processed_img2 == 255)
            black_pixels2 = np.sum(processed_img2 == 0)
            
            print(f"📊 Statistiques basées sur moyenne:")
            print(f"   Pixels blancs: {white_pixels2} ({white_pixels2/total_pixels*100:.1f}%)")
            print(f"   Pixels noirs: {black_pixels2} ({black_pixels2/total_pixels*100:.1f}%)")
            
            print(f"📁 Fichier basé sur moyenne: {processed_path2}")
    else:
        print(f"❌ Erreur seuillage basé sur moyenne: {response2.text}")
    
    print(f"\n💡 COMPARAISON VISUELLE:")
    print(f"   Original: {original_path}")
    if 'processed_path1' in locals():
        print(f"   Adaptatif: {processed_path1}")
    if 'processed_path2' in locals():
        print(f"   Basé sur moyenne: {processed_path2}")

if __name__ == "__main__":
    test_adaptive_threshold()