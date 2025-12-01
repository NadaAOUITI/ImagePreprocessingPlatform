#!/usr/bin/env python3
"""
Test spécifique pour les filtres de flou
"""
import cv2
import numpy as np
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_blur_filters():
    """Test technique des filtres de flou"""
    print("🧪 TEST TECHNIQUE FILTRES DE FLOU")
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
    
    # Liste des filtres de flou à tester
    blur_filters = [
        {
            'operation': 'blur_gaussian',
            'name': 'Flou Gaussien',
            'params': {'kernel_size': 15}
        },
        {
            'operation': 'blur_median', 
            'name': 'Flou Médian',
            'params': {'kernel_size': 15}
        },
        {
            'operation': 'blur_average',
            'name': 'Flou Moyenneur', 
            'params': {'kernel_size': 15}
        }
    ]
    
    results = []
    
    for filter_config in blur_filters:
        print(f"\n🔧 TEST: {filter_config['name']}")
        print("-" * 30)
        
        payload = {
            "filename": filename,
            "operation": filter_config['operation'],
            "parameters": filter_config['params']
        }
        
        print(f"📋 Paramètres: {filter_config['params']}")
        
        try:
            response = requests.post(f"{BASE_URL}/process", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                output_filename = result["output_file"]
                print(f"✅ Traitement réussi: {output_filename}")
                
                # Analyser l'image traitée
                processed_path = os.path.join("../processed", output_filename)
                
                if os.path.exists(processed_path):
                    processed_img = cv2.imread(processed_path)
                    
                    print(f"📊 Image traitée:")
                    print(f"   Dimensions: {processed_img.shape}")
                    
                    # Validation technique
                    if original_img.shape == processed_img.shape:
                        print("✅ Dimensions conservées")
                    else:
                        print("❌ Dimensions modifiées")
                    
                    # Calculer la différence moyenne (mesure du flou)
                    diff = cv2.absdiff(original_img, processed_img)
                    mean_diff = np.mean(diff)
                    print(f"📈 Différence moyenne: {mean_diff:.2f}")
                    
                    # Calculer la variance (mesure de netteté)
                    gray_processed = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
                    laplacian_var = cv2.Laplacian(gray_processed, cv2.CV_64F).var()
                    print(f"📈 Variance Laplacien (netteté): {laplacian_var:.2f}")
                    
                    results.append({
                        'name': filter_config['name'],
                        'file': output_filename,
                        'path': processed_path,
                        'mean_diff': mean_diff,
                        'sharpness': laplacian_var
                    })
                    
                    print(f"📁 Fichier: {processed_path}")
                else:
                    print("❌ Fichier traité non trouvé")
            else:
                print(f"❌ Erreur {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    # Comparaison des résultats
    if results:
        print(f"\n📊 COMPARAISON DES FILTRES DE FLOU:")
        print("=" * 50)
        
        # Calculer netteté originale
        gray_original = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
        original_sharpness = cv2.Laplacian(gray_original, cv2.CV_64F).var()
        print(f"📈 Netteté originale: {original_sharpness:.2f}")
        
        print(f"\n{'Filtre':<20} {'Différence':<12} {'Netteté':<12} {'Réduction':<12}")
        print("-" * 60)
        
        for result in results:
            reduction = ((original_sharpness - result['sharpness']) / original_sharpness) * 100
            print(f"{result['name']:<20} {result['mean_diff']:<12.2f} {result['sharpness']:<12.2f} {reduction:<12.1f}%")
        
        print(f"\n💡 FICHIERS POUR VÉRIFICATION VISUELLE:")
        print(f"   Original: {original_path}")
        for result in results:
            print(f"   {result['name']}: {result['path']}")

if __name__ == "__main__":
    test_blur_filters()