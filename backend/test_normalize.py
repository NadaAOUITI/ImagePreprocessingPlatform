#!/usr/bin/env python3
"""
Test spécifique pour la normalisation des pixels
"""
import cv2
import numpy as np
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_normalize():
    """Test technique de la normalisation des pixels"""
    print("🧪 TEST TECHNIQUE NORMALISATION DES PIXELS")
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
    
    # Analyser les valeurs originales
    orig_min = np.min(original_img)
    orig_max = np.max(original_img)
    orig_mean = np.mean(original_img)
    orig_std = np.std(original_img)
    
    print(f"📈 Valeurs originales:")
    print(f"   Min: {orig_min}")
    print(f"   Max: {orig_max}")
    print(f"   Moyenne: {orig_mean:.2f}")
    print(f"   Écart-type: {orig_std:.2f}")
    print(f"   Plage: [{orig_min}, {orig_max}]")
    
    # Test de normalisation
    print(f"\n🔧 TEST: Normalisation")
    print("-" * 25)
    
    payload = {
        "filename": filename,
        "operation": "normalize"
    }
    
    print("📋 Paramètres: Aucun (normalisation automatique)")
    
    try:
        response = requests.post(f"{BASE_URL}/process", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            output_filename = result["output_file"]
            print(f"✅ Traitement réussi: {output_filename}")
            
            # Analyser l'image normalisée
            processed_path = os.path.join("../processed", output_filename)
            
            if os.path.exists(processed_path):
                processed_img = cv2.imread(processed_path)
                
                print(f"📊 Image normalisée:")
                print(f"   Dimensions: {processed_img.shape}")
                
                # Validation technique des dimensions
                if original_img.shape == processed_img.shape:
                    print("✅ Dimensions conservées")
                else:
                    print("❌ Dimensions modifiées")
                
                # Analyser les nouvelles valeurs
                norm_min = np.min(processed_img)
                norm_max = np.max(processed_img)
                norm_mean = np.mean(processed_img)
                norm_std = np.std(processed_img)
                
                print(f"📈 Valeurs normalisées:")
                print(f"   Min: {norm_min}")
                print(f"   Max: {norm_max}")
                print(f"   Moyenne: {norm_mean:.2f}")
                print(f"   Écart-type: {norm_std:.2f}")
                print(f"   Plage: [{norm_min}, {norm_max}]")
                
                # Validation de la normalisation
                print(f"\n🔍 VALIDATION TECHNIQUE:")
                
                # Vérifier que la plage est [0, 255] (OpenCV normalise vers cette plage)
                if norm_min == 0 and norm_max == 255:
                    print("✅ Normalisation réussie: Plage [0, 255]")
                elif norm_min >= 0 and norm_max <= 255:
                    print(f"✅ Normalisation partielle: Plage [{norm_min}, {norm_max}]")
                else:
                    print(f"❌ Normalisation échouée: Plage [{norm_min}, {norm_max}]")
                
                # Vérifier l'utilisation complète de la plage
                range_utilization = (norm_max - norm_min) / 255.0 * 100
                print(f"📊 Utilisation de la plage: {range_utilization:.1f}%")
                
                if range_utilization > 95:
                    print("✅ Excellente utilisation de la plage dynamique")
                elif range_utilization > 80:
                    print("✅ Bonne utilisation de la plage dynamique")
                else:
                    print("⚠️ Utilisation limitée de la plage dynamique")
                
                # Calculer le gain de contraste
                orig_range = orig_max - orig_min
                norm_range = norm_max - norm_min
                contrast_gain = (norm_range / orig_range) if orig_range > 0 else 1
                
                print(f"📈 Gain de contraste: {contrast_gain:.2f}x")
                
                if contrast_gain > 1.1:
                    print("✅ Contraste amélioré")
                elif contrast_gain > 0.9:
                    print("✅ Contraste maintenu")
                else:
                    print("⚠️ Contraste réduit")
                
                # Analyser la distribution des pixels
                print(f"\n📊 ANALYSE DE DISTRIBUTION:")
                
                # Histogramme par canal
                for i, color in enumerate(['Bleu', 'Vert', 'Rouge']):
                    orig_channel = original_img[:,:,i]
                    norm_channel = processed_img[:,:,i]
                    
                    orig_ch_min, orig_ch_max = np.min(orig_channel), np.max(orig_channel)
                    norm_ch_min, norm_ch_max = np.min(norm_channel), np.max(norm_channel)
                    
                    print(f"   {color}: [{orig_ch_min}, {orig_ch_max}] → [{norm_ch_min}, {norm_ch_max}]")
                
                # Vérifier la préservation des relations
                correlation = np.corrcoef(original_img.flatten(), processed_img.flatten())[0,1]
                print(f"📈 Corrélation avec original: {correlation:.4f}")
                
                if correlation > 0.95:
                    print("✅ Relations entre pixels préservées")
                elif correlation > 0.8:
                    print("✅ Relations largement préservées")
                else:
                    print("⚠️ Relations partiellement modifiées")
                
                # Calculer la différence visuelle
                diff = cv2.absdiff(original_img, processed_img)
                mean_diff = np.mean(diff)
                print(f"📈 Différence moyenne: {mean_diff:.2f}")
                
                # Vérifier les couleurs
                if processed_img.shape[2] == 3:
                    print("✅ Couleurs conservées (3 canaux)")
                else:
                    print("❌ Couleurs modifiées")
                
                print(f"\n📁 FICHIERS POUR VÉRIFICATION VISUELLE:")
                print(f"   Original: {original_path}")
                print(f"   Normalisé: {processed_path}")
                
                print(f"\n🎯 ATTENDU VISUELLEMENT:")
                print(f"   ✅ Couleurs identiques mais contraste amélioré")
                print(f"   ✅ Détails plus visibles dans les zones sombres/claires")
                print(f"   ✅ Pas de changement de teinte")
                print(f"   ✅ Image plus équilibrée en luminosité")
                
            else:
                print("❌ Fichier traité non trouvé")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_normalize()