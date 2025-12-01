#!/usr/bin/env python3
"""
Test spécifique pour les filtres de sharpening
"""
import cv2
import numpy as np
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_sharpen_filters():
    """Test technique des filtres de sharpening"""
    print("🧪 TEST TECHNIQUE FILTRES DE SHARPENING")
    print("=" * 55)
    
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
    
    # Liste des filtres de sharpening à tester
    sharpen_filters = [
        {
            'operation': 'sharpen_kernel',
            'name': 'Sharpen Kernel',
            'params': {}
        },
        {
            'operation': 'sharpen_unsharp', 
            'name': 'Unsharp Mask',
            'params': {'strength': 2.0}
        },
        {
            'operation': 'sharpen_laplacian',
            'name': 'Laplacien + Original', 
            'params': {}
        },
        {
            'operation': 'sharpen_highboost',
            'name': 'High-Boost Filter', 
            'params': {'boost_factor': 3.0}
        }
    ]
    
    results = []
    
    for filter_config in sharpen_filters:
        print(f"\n🔧 TEST: {filter_config['name']}")
        print("-" * 35)
        
        payload = {
            "filename": filename,
            "operation": filter_config['operation'],
            "parameters": filter_config['params']
        }
        
        if filter_config['params']:
            print(f"📋 Paramètres: {filter_config['params']}")
        else:
            print("📋 Paramètres: Aucun")
        
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
                    
                    # Calculer la différence moyenne (mesure de l'accentuation)
                    diff = cv2.absdiff(original_img, processed_img)
                    mean_diff = np.mean(diff)
                    print(f"📈 Différence moyenne: {mean_diff:.2f}")
                    
                    # Calculer la variance Laplacien (mesure de netteté)
                    gray_processed = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
                    laplacian_var = cv2.Laplacian(gray_processed, cv2.CV_64F).var()
                    print(f"📈 Variance Laplacien (netteté): {laplacian_var:.2f}")
                    
                    # Calculer le gradient moyen (mesure des contours)
                    sobel_x = cv2.Sobel(gray_processed, cv2.CV_64F, 1, 0, ksize=3)
                    sobel_y = cv2.Sobel(gray_processed, cv2.CV_64F, 0, 1, ksize=3)
                    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
                    mean_gradient = np.mean(gradient_magnitude)
                    print(f"📈 Gradient moyen (contours): {mean_gradient:.2f}")
                    
                    # Vérifier les valeurs de pixels (pas de saturation)
                    max_val = np.max(processed_img)
                    min_val = np.min(processed_img)
                    saturated_pixels = np.sum((processed_img == 0) | (processed_img == 255))
                    total_pixels = processed_img.size
                    saturation_percent = (saturated_pixels / total_pixels) * 100
                    
                    print(f"📈 Valeurs pixels: [{min_val}, {max_val}]")
                    print(f"📈 Saturation: {saturation_percent:.1f}%")
                    
                    results.append({
                        'name': filter_config['name'],
                        'file': output_filename,
                        'path': processed_path,
                        'mean_diff': mean_diff,
                        'sharpness': laplacian_var,
                        'gradient': mean_gradient,
                        'saturation': saturation_percent
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
        print(f"\n📊 COMPARAISON DES FILTRES DE SHARPENING:")
        print("=" * 60)
        
        # Calculer métriques originales
        gray_original = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
        original_sharpness = cv2.Laplacian(gray_original, cv2.CV_64F).var()
        
        sobel_x_orig = cv2.Sobel(gray_original, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y_orig = cv2.Sobel(gray_original, cv2.CV_64F, 0, 1, ksize=3)
        gradient_orig = np.sqrt(sobel_x_orig**2 + sobel_y_orig**2)
        original_gradient = np.mean(gradient_orig)
        
        print(f"📈 Netteté originale: {original_sharpness:.2f}")
        print(f"📈 Gradient original: {original_gradient:.2f}")
        
        print(f"\n{'Filtre':<20} {'Différence':<12} {'Netteté':<12} {'Gradient':<12} {'Saturation':<12}")
        print("-" * 75)
        
        for result in results:
            sharpness_gain = ((result['sharpness'] - original_sharpness) / original_sharpness) * 100
            gradient_gain = ((result['gradient'] - original_gradient) / original_gradient) * 100
            
            print(f"{result['name']:<20} {result['mean_diff']:<12.2f} {result['sharpness']:<12.2f} {result['gradient']:<12.2f} {result['saturation']:<12.1f}%")
            print(f"{'Gain:':<20} {'':<12} {sharpness_gain:+12.1f}% {gradient_gain:+12.1f}% {'':<12}")
        
        print(f"\n💡 FICHIERS POUR VÉRIFICATION VISUELLE:")
        print(f"   Original: {original_path}")
        for result in results:
            print(f"   {result['name']}: {result['path']}")

if __name__ == "__main__":
    test_sharpen_filters()