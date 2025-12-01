#!/usr/bin/env python3
"""
Test spécifique pour l'égalisation d'histogramme
"""
import cv2
import numpy as np
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_histogram_equalization():
    """Test technique de l'égalisation d'histogramme"""
    print("🧪 TEST TECHNIQUE ÉGALISATION D'HISTOGRAMME")
    print("=" * 60)
    
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
    
    # Analyser l'histogramme original
    print(f"\n📈 ANALYSE HISTOGRAMME ORIGINAL:")
    
    # Convertir en YUV pour analyser la luminance
    yuv_orig = cv2.cvtColor(original_img, cv2.COLOR_BGR2YUV)
    y_channel_orig = yuv_orig[:,:,0]
    
    # Calculer statistiques de luminance
    orig_mean_lum = np.mean(y_channel_orig)
    orig_std_lum = np.std(y_channel_orig)
    orig_min_lum = np.min(y_channel_orig)
    orig_max_lum = np.max(y_channel_orig)
    
    print(f"   Luminance moyenne: {orig_mean_lum:.2f}")
    print(f"   Écart-type luminance: {orig_std_lum:.2f}")
    print(f"   Plage luminance: [{orig_min_lum}, {orig_max_lum}]")
    
    # Test d'égalisation d'histogramme
    print(f"\n🔧 TEST: Égalisation d'Histogramme")
    print("-" * 35)
    
    payload = {
        "filename": filename,
        "operation": "histogram_eq"
    }
    
    print("📋 Paramètres: Aucun (égalisation automatique)")
    
    try:
        response = requests.post(f"{BASE_URL}/process", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            output_filename = result["output_file"]
            print(f"✅ Traitement réussi: {output_filename}")
            
            # Analyser l'image égalisée
            processed_path = os.path.join("../processed", output_filename)
            
            if os.path.exists(processed_path):
                processed_img = cv2.imread(processed_path)
                
                print(f"📊 Image égalisée:")
                print(f"   Dimensions: {processed_img.shape}")
                
                # Validation technique des dimensions
                if original_img.shape == processed_img.shape:
                    print("✅ Dimensions conservées")
                else:
                    print("❌ Dimensions modifiées")
                
                # Analyser l'histogramme égalisé
                print(f"\n📈 ANALYSE HISTOGRAMME ÉGALISÉ:")
                
                # Convertir en YUV pour analyser la luminance
                yuv_proc = cv2.cvtColor(processed_img, cv2.COLOR_BGR2YUV)
                y_channel_proc = yuv_proc[:,:,0]
                
                # Calculer nouvelles statistiques
                proc_mean_lum = np.mean(y_channel_proc)
                proc_std_lum = np.std(y_channel_proc)
                proc_min_lum = np.min(y_channel_proc)
                proc_max_lum = np.max(y_channel_proc)
                
                print(f"   Luminance moyenne: {proc_mean_lum:.2f}")
                print(f"   Écart-type luminance: {proc_std_lum:.2f}")
                print(f"   Plage luminance: [{proc_min_lum}, {proc_max_lum}]")
                
                # Validation de l'égalisation
                print(f"\n🔍 VALIDATION TECHNIQUE:")
                
                # Vérifier l'amélioration du contraste
                contrast_improvement = proc_std_lum / orig_std_lum if orig_std_lum > 0 else 1
                print(f"📈 Amélioration contraste: {contrast_improvement:.2f}x")
                
                if contrast_improvement > 1.1:
                    print("✅ Contraste significativement amélioré")
                elif contrast_improvement > 1.05:
                    print("✅ Contraste légèrement amélioré")
                else:
                    print("⚠️ Contraste peu ou pas amélioré")
                
                # Calculer la différence visuelle
                diff = cv2.absdiff(original_img, processed_img)
                mean_diff = np.mean(diff)
                print(f"📈 Différence moyenne: {mean_diff:.2f}")
                
                if mean_diff > 10:
                    print("✅ Changement visuel significatif")
                elif mean_diff > 5:
                    print("✅ Changement visuel modéré")
                else:
                    print("⚠️ Changement visuel minimal")
                
                # Vérifier les couleurs
                if processed_img.shape[2] == 3:
                    print("✅ Couleurs conservées (3 canaux)")
                else:
                    print("❌ Couleurs modifiées")
                
                # Calculer la corrélation
                correlation = np.corrcoef(original_img.flatten(), processed_img.flatten())[0,1]
                print(f"📈 Corrélation avec original: {correlation:.4f}")
                
                if correlation > 0.8:
                    print("✅ Structure de l'image préservée")
                else:
                    print("⚠️ Structure partiellement modifiée")
                
                print(f"\n📁 FICHIERS POUR VÉRIFICATION VISUELLE:")
                print(f"   Original: {original_path}")
                print(f"   Égalisé: {processed_path}")
                
                print(f"\n🎯 ATTENDU VISUELLEMENT:")
                print(f"   ✅ Contraste amélioré (zones sombres plus claires)")
                print(f"   ✅ Détails plus visibles dans toutes les zones")
                print(f"   ✅ Couleurs plus vives et équilibrées")
                print(f"   ✅ Image globalement plus lumineuse")
                
            else:
                print("❌ Fichier traité non trouvé")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_histogram_equalization()