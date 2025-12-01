#!/usr/bin/env python3
"""
Test spécifique pour les transformations géométriques
"""
import cv2
import numpy as np
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_geometric_transforms():
    """Test technique des transformations géométriques"""
    print("🧪 TEST TECHNIQUE TRANSFORMATIONS GÉOMÉTRIQUES")
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
    
    # Liste des transformations géométriques à tester
    geometric_transforms = [
        {
            'operation': 'rotate',
            'name': 'Rotation 90°',
            'params': {'angle': 90}
        },
        {
            'operation': 'rotate',
            'name': 'Rotation 180°',
            'params': {'angle': 180}
        },
        {
            'operation': 'rotate',
            'name': 'Rotation 45°',
            'params': {'angle': 45}
        },
        {
            'operation': 'flip', 
            'name': 'Miroir Horizontal',
            'params': {'direction': 'horizontal'}
        },
        {
            'operation': 'flip',
            'name': 'Miroir Vertical', 
            'params': {'direction': 'vertical'}
        },
        {
            'operation': 'flip',
            'name': 'Miroir Both (180°)', 
            'params': {'direction': 'both'}
        }
    ]
    
    results = []
    
    for transform_config in geometric_transforms:
        print(f"\n🔧 TEST: {transform_config['name']}")
        print("-" * 35)
        
        payload = {
            "filename": filename,
            "operation": transform_config['operation'],
            "parameters": transform_config['params']
        }
        
        print(f"📋 Paramètres: {transform_config['params']}")
        
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
                    
                    # Vérifier conservation des couleurs
                    if processed_img.shape[2] == original_img.shape[2]:
                        print("✅ Couleurs conservées (3 canaux)")
                    else:
                        print("❌ Couleurs modifiées")
                    
                    # Analyser les changements de dimensions
                    orig_h, orig_w = original_img.shape[:2]
                    proc_h, proc_w = processed_img.shape[:2]
                    
                    print(f"📏 Dimensions: {orig_w}x{orig_h} → {proc_w}x{proc_h}")
                    
                    if transform_config['operation'] == 'rotate':
                        angle = transform_config['params']['angle']
                        
                        # Vérifier les rotations spéciales
                        if angle == 90 or angle == 270:
                            if proc_w == orig_h and proc_h == orig_w:
                                print("✅ Rotation 90°: Dimensions échangées correctement")
                            else:
                                print("❌ Rotation 90°: Dimensions incorrectes")
                        elif angle == 180:
                            if proc_w == orig_w and proc_h == orig_h:
                                print("✅ Rotation 180°: Dimensions conservées")
                            else:
                                print("❌ Rotation 180°: Dimensions incorrectes")
                        else:
                            print(f"📐 Rotation {angle}°: Nouvelles dimensions calculées")
                    
                    elif transform_config['operation'] == 'flip':
                        if proc_w == orig_w and proc_h == orig_h:
                            print("✅ Miroir: Dimensions conservées")
                        else:
                            print("❌ Miroir: Dimensions modifiées")
                    
                    # Calculer la différence pour vérifier la transformation
                    if processed_img.shape == original_img.shape:
                        diff = cv2.absdiff(original_img, processed_img)
                        mean_diff = np.mean(diff)
                        print(f"📈 Différence moyenne: {mean_diff:.2f}")
                        
                        if mean_diff > 0:
                            print("✅ Transformation appliquée (image modifiée)")
                        else:
                            print("❌ Aucune transformation détectée")
                    else:
                        print("📈 Dimensions différentes - transformation confirmée")
                    
                    # Vérifier la conservation des pixels (même histogramme)
                    orig_hist = cv2.calcHist([original_img], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
                    proc_hist = cv2.calcHist([processed_img], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
                    
                    # Comparer les histogrammes (doivent être identiques pour les transformations géométriques)
                    hist_correlation = cv2.compareHist(orig_hist, proc_hist, cv2.HISTCMP_CORREL)
                    print(f"📊 Corrélation histogramme: {hist_correlation:.4f}")
                    
                    if hist_correlation > 0.99:
                        print("✅ Pixels conservés (transformation géométrique pure)")
                    else:
                        print("⚠️ Pixels légèrement modifiés (interpolation)")
                    
                    results.append({
                        'name': transform_config['name'],
                        'operation': transform_config['operation'],
                        'file': output_filename,
                        'path': processed_path,
                        'orig_dims': (orig_w, orig_h),
                        'new_dims': (proc_w, proc_h),
                        'hist_corr': hist_correlation,
                        'params': transform_config['params']
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
        print(f"\n📊 COMPARAISON DES TRANSFORMATIONS GÉOMÉTRIQUES:")
        print("=" * 70)
        
        print(f"\n{'Transformation':<20} {'Dimensions':<15} {'Corrélation':<12} {'Statut':<15}")
        print("-" * 70)
        
        for result in results:
            orig_dims = f"{result['orig_dims'][0]}x{result['orig_dims'][1]}"
            new_dims = f"{result['new_dims'][0]}x{result['new_dims'][1]}"
            dims_str = f"{orig_dims}→{new_dims}"
            
            status = "✅ Parfait" if result['hist_corr'] > 0.99 else "⚠️ Interpolé"
            
            print(f"{result['name']:<20} {dims_str:<15} {result['hist_corr']:<12.4f} {status:<15}")
        
        # Grouper par type
        rotations = [r for r in results if r['operation'] == 'rotate']
        flips = [r for r in results if r['operation'] == 'flip']
        
        print(f"\n🔄 ROTATIONS ({len(rotations)} testées):")
        for rot in rotations:
            angle = rot['params']['angle']
            print(f"   {angle}° : {rot['file']}")
        
        print(f"\n🪞 MIROIRS ({len(flips)} testés):")
        for flip in flips:
            direction = flip['params']['direction']
            print(f"   {direction} : {flip['file']}")
        
        print(f"\n💡 FICHIERS POUR VÉRIFICATION VISUELLE:")
        print(f"   Original: {original_path}")
        for result in results:
            print(f"   {result['name']}: {result['path']}")
        
        print(f"\n🎯 ATTENDU VISUELLEMENT:")
        print(f"   ✅ Couleurs identiques à l'original")
        print(f"   ✅ Rotations: Image tournée selon l'angle")
        print(f"   ✅ Miroirs: Image retournée selon la direction")
        print(f"   ✅ Aucun changement de couleur ou de contraste")

if __name__ == "__main__":
    test_geometric_transforms()