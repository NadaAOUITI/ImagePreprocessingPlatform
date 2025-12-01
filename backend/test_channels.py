#!/usr/bin/env python3
"""
Test pour l'extraction de canaux RGB
"""
import cv2
import numpy as np
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_extract_channels():
    """Test technique de l'extraction de canaux RGB"""
    print("🧪 TEST TECHNIQUE EXTRACTION DE CANAUX RGB")
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
    
    # Tester l'extraction de chaque canal
    channels_to_test = ['red', 'green', 'blue']
    results = []
    
    for channel in channels_to_test:
        print(f"\n🔧 TEST: Extraction Canal {channel.upper()}")
        print("-" * 35)
        
        payload = {
            "filename": filename,
            "operation": "extract_channel",
            "parameters": {"channel": channel}
        }
        
        print(f"📋 Paramètres: channel = {channel}")
        
        try:
            response = requests.post(f"{BASE_URL}/process", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                output_filename = result["output_file"]
                print(f"✅ Traitement réussi: {output_filename}")
                
                # Analyser l'image extraite
                processed_path = os.path.join("../processed", output_filename)
                
                if os.path.exists(processed_path):
                    processed_img = cv2.imread(processed_path)
                    
                    print(f"📊 Canal {channel} extrait:")
                    print(f"   Dimensions: {processed_img.shape}")
                    
                    # Validation technique des dimensions
                    if original_img.shape == processed_img.shape:
                        print("✅ Dimensions conservées")
                    else:
                        print("❌ Dimensions modifiées")
                    
                    # Vérifier que c'est toujours en couleur (3 canaux)
                    if processed_img.shape[2] == 3:
                        print("✅ Format couleur conservé (3 canaux)")
                    else:
                        print("❌ Format couleur modifié")
                    
                    # Analyser les canaux de l'image extraite
                    b_proc, g_proc, r_proc = cv2.split(processed_img)
                    
                    print(f"📈 Analyse des canaux extraits:")
                    
                    # Vérifier quel canal est actif
                    if channel == 'red':
                        active_channel = r_proc
                        inactive_channels = [b_proc, g_proc]
                        inactive_names = ['Bleu', 'Vert']
                    elif channel == 'green':
                        active_channel = g_proc
                        inactive_channels = [b_proc, r_proc]
                        inactive_names = ['Bleu', 'Rouge']
                    else:  # blue
                        active_channel = b_proc
                        inactive_channels = [g_proc, r_proc]
                        inactive_names = ['Vert', 'Rouge']
                    
                    # Vérifier le canal actif
                    active_mean = np.mean(active_channel)
                    active_nonzero = np.count_nonzero(active_channel)
                    
                    print(f"   Canal {channel.upper()} (actif): moyenne={active_mean:.1f}, pixels non-zéro={active_nonzero}")
                    
                    # Vérifier les canaux inactifs (doivent être à zéro)
                    all_inactive_zero = True
                    for i, inactive_channel in enumerate(inactive_channels):
                        inactive_max = np.max(inactive_channel)
                        inactive_nonzero = np.count_nonzero(inactive_channel)
                        
                        print(f"   Canal {inactive_names[i]} (inactif): max={inactive_max}, non-zéro={inactive_nonzero}")
                        
                        if inactive_max > 0:
                            all_inactive_zero = False
                    
                    # Validation de l'extraction
                    print(f"\n🔍 VALIDATION TECHNIQUE:")
                    
                    if all_inactive_zero:
                        print("✅ Canaux inactifs correctement mis à zéro")
                    else:
                        print("❌ Canaux inactifs non mis à zéro")
                    
                    if active_nonzero > 0:
                        print("✅ Canal actif contient des données")
                    else:
                        print("❌ Canal actif vide")
                    
                    # Comparer avec le canal original
                    b_orig, g_orig, r_orig = cv2.split(original_img)
                    if channel == 'red':
                        original_channel = r_orig
                    elif channel == 'green':
                        original_channel = g_orig
                    else:
                        original_channel = b_orig
                    
                    correlation = np.corrcoef(original_channel.flatten(), active_channel.flatten())[0,1]
                    print(f"📈 Corrélation avec canal original: {correlation:.4f}")
                    
                    if correlation > 0.99:
                        print("✅ Canal parfaitement préservé")
                    elif correlation > 0.95:
                        print("✅ Canal bien préservé")
                    else:
                        print("⚠️ Canal partiellement modifié")
                    
                    results.append({
                        'channel': channel,
                        'file': output_filename,
                        'path': processed_path,
                        'active_mean': active_mean,
                        'inactive_zero': all_inactive_zero,
                        'correlation': correlation
                    })
                    
                    print(f"📁 Fichier: {processed_path}")
                else:
                    print("❌ Fichier traité non trouvé")
            else:
                print(f"❌ Erreur {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    # Résumé des résultats
    if results:
        print(f"\n📊 COMPARAISON DES EXTRACTIONS:")
        print("=" * 50)
        
        print(f"\n{'Canal':<8} {'Corrélation':<12} {'Moyenne':<10} {'Inactifs=0':<12}")
        print("-" * 50)
        
        for result in results:
            inactive_status = "✅ Oui" if result['inactive_zero'] else "❌ Non"
            print(f"{result['channel'].upper():<8} {result['correlation']:<12.4f} {result['active_mean']:<10.1f} {inactive_status:<12}")
        
        # Vérifier que tous les canaux ont été extraits correctement
        all_successful = all(r['correlation'] > 0.95 and r['inactive_zero'] for r in results)
        
        if all_successful:
            print("\n✅ Toutes les extractions de canaux réussies")
        else:
            print("\n⚠️ Certaines extractions ont des problèmes")
        
        print(f"\n💡 FICHIERS POUR VÉRIFICATION VISUELLE:")
        print(f"   Original (couleur): {original_path}")
        for result in results:
            color_name = {'red': 'Rouge', 'green': 'Vert', 'blue': 'Bleu'}[result['channel']]
            print(f"   Canal {color_name}: {result['path']}")
        
        print(f"\n🎯 ATTENDU VISUELLEMENT:")
        print(f"   ✅ Canal Rouge: Image avec dominante rouge")
        print(f"   ✅ Canal Vert: Image avec dominante verte") 
        print(f"   ✅ Canal Bleu: Image avec dominante bleue")
        print(f"   ✅ Zones sombres: Peu de couleur dans ce canal")
        print(f"   ✅ Zones claires: Beaucoup de couleur dans ce canal")

if __name__ == "__main__":
    test_extract_channels()