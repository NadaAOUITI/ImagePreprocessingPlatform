#!/usr/bin/env python3
"""
Test spécifique pour l'étirement d'histogramme
"""
import cv2
import numpy as np
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_histogram_stretch():
    """Test technique de l'étirement d'histogramme"""
    print("🧪 TEST TECHNIQUE ÉTIREMENT D'HISTOGRAMME")
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
    
    # Analyser chaque canal
    orig_stats = {}
    for i, color in enumerate(['Bleu', 'Vert', 'Rouge']):
        channel = original_img[:,:,i]
        min_val = np.min(channel)
        max_val = np.max(channel)
        mean_val = np.mean(channel)
        std_val = np.std(channel)
        
        orig_stats[color] = {
            'min': min_val,
            'max': max_val,
            'mean': mean_val,
            'std': std_val,
            'range': max_val - min_val
        }
        
        print(f"   {color}: [{min_val}, {max_val}] (plage: {max_val - min_val})")
    
    # Calculer utilisation globale de la plage
    global_min = np.min(original_img)
    global_max = np.max(original_img)
    global_range = global_max - global_min
    range_utilization = (global_range / 255.0) * 100
    
    print(f"   Plage globale: [{global_min}, {global_max}]")
    print(f"   Utilisation plage: {range_utilization:.1f}%")
    
    # Test d'étirement d'histogramme
    print(f"\n🔧 TEST: Étirement d'Histogramme")
    print("-" * 35)
    
    payload = {
        "filename": filename,
        "operation": "histogram_stretch"
    }
    
    print("📋 Paramètres: Aucun (étirement automatique)")
    
    try:
        response = requests.post(f"{BASE_URL}/process", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            output_filename = result["output_file"]
            print(f"✅ Traitement réussi: {output_filename}")
            
            # Analyser l'image étirée
            processed_path = os.path.join("../processed", output_filename)
            
            if os.path.exists(processed_path):
                processed_img = cv2.imread(processed_path)
                
                print(f"📊 Image étirée:")
                print(f"   Dimensions: {processed_img.shape}")
                
                # Validation technique des dimensions
                if original_img.shape == processed_img.shape:
                    print("✅ Dimensions conservées")
                else:
                    print("❌ Dimensions modifiées")
                
                # Analyser l'histogramme étiré
                print(f"\n📈 ANALYSE HISTOGRAMME ÉTIRÉ:")
                
                # Analyser chaque canal après étirement
                stretch_stats = {}
                for i, color in enumerate(['Bleu', 'Vert', 'Rouge']):
                    channel = processed_img[:,:,i]
                    min_val = np.min(channel)
                    max_val = np.max(channel)
                    mean_val = np.mean(channel)
                    std_val = np.std(channel)
                    
                    stretch_stats[color] = {
                        'min': min_val,
                        'max': max_val,
                        'mean': mean_val,
                        'std': std_val,
                        'range': max_val - min_val
                    }
                    
                    print(f"   {color}: [{min_val}, {max_val}] (plage: {max_val - min_val})")
                
                # Calculer nouvelle utilisation de la plage
                stretch_global_min = np.min(processed_img)
                stretch_global_max = np.max(processed_img)
                stretch_global_range = stretch_global_max - stretch_global_min
                stretch_range_utilization = (stretch_global_range / 255.0) * 100
                
                print(f"   Plage globale: [{stretch_global_min}, {stretch_global_max}]")
                print(f"   Utilisation plage: {stretch_range_utilization:.1f}%")
                
                # Validation de l'étirement
                print(f"\n🔍 VALIDATION TECHNIQUE:")
                
                # Vérifier l'amélioration de la plage dynamique
                range_improvement = stretch_range_utilization / range_utilization if range_utilization > 0 else 1
                print(f"📈 Amélioration plage dynamique: {range_improvement:.2f}x")
                
                if range_improvement > 1.2:
                    print("✅ Plage dynamique significativement étendue")
                elif range_improvement > 1.05:
                    print("✅ Plage dynamique légèrement étendue")
                else:
                    print("⚠️ Plage dynamique peu ou pas étendue")
                
                # Vérifier l'étirement par canal
                print(f"\n📊 ÉTIREMENT PAR CANAL:")
                all_channels_stretched = True
                
                for color in ['Bleu', 'Vert', 'Rouge']:
                    orig = orig_stats[color]
                    stretch = stretch_stats[color]
                    
                    range_gain = stretch['range'] / orig['range'] if orig['range'] > 0 else 1
                    contrast_gain = stretch['std'] / orig['std'] if orig['std'] > 0 else 1
                    
                    print(f"   {color}:")
                    print(f"     Plage: {orig['range']} → {stretch['range']} ({range_gain:.2f}x)")
                    print(f"     Contraste: {orig['std']:.1f} → {stretch['std']:.1f} ({contrast_gain:.2f}x)")
                    
                    # Vérifier si le canal utilise toute la plage [0, 255]
                    if stretch['min'] == 0 and stretch['max'] == 255:
                        print(f"     ✅ Plage complète [0, 255] utilisée")
                    else:
                        print(f"     ⚠️ Plage partielle [{stretch['min']}, {stretch['max']}]")
                        all_channels_stretched = False
                
                if all_channels_stretched:
                    print("✅ Tous les canaux utilisent la plage complète")
                else:
                    print("⚠️ Certains canaux n'utilisent pas la plage complète")
                
                # Calculer la différence visuelle
                diff = cv2.absdiff(original_img, processed_img)
                mean_diff = np.mean(diff)
                print(f"\n📈 Différence moyenne: {mean_diff:.2f}")
                
                if mean_diff > 15:
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
                
                if correlation > 0.9:
                    print("✅ Structure de l'image très bien préservée")
                elif correlation > 0.8:
                    print("✅ Structure de l'image préservée")
                else:
                    print("⚠️ Structure partiellement modifiée")
                
                # Comparer avec l'égalisation d'histogramme
                print(f"\n🔄 COMPARAISON ÉTIREMENT vs ÉGALISATION:")
                print(f"   Étirement: Préserve la forme de l'histogramme")
                print(f"   Égalisation: Redistribue uniformément les pixels")
                print(f"   Étirement: Plus naturel, moins agressif")
                
                print(f"\n📁 FICHIERS POUR VÉRIFICATION VISUELLE:")
                print(f"   Original: {original_path}")
                print(f"   Étiré: {processed_path}")
                
                print(f"\n🎯 ATTENDU VISUELLEMENT:")
                print(f"   ✅ Contraste amélioré de façon naturelle")
                print(f"   ✅ Couleurs plus vives sans sur-saturation")
                print(f"   ✅ Détails mieux définis dans toutes les zones")
                print(f"   ✅ Aspect plus naturel que l'égalisation")
                print(f"   ✅ Pas de changement de teinte")
                
            else:
                print("❌ Fichier traité non trouvé")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_histogram_stretch()