#!/usr/bin/env python3
"""
Test spécifique pour les filtres de détection de contours
"""
import cv2
import numpy as np
import os
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_edge_filters():
    """Test technique des filtres de détection de contours"""
    print("🧪 TEST TECHNIQUE FILTRES DE DÉTECTION DE CONTOURS")
    print("=" * 65)
    
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
    
    # Liste des filtres d'edge detection à tester
    edge_filters = [
        {
            'operation': 'edge_canny',
            'name': 'Canny',
            'params': {'low': 50, 'high': 150}
        },
        {
            'operation': 'edge_roberts', 
            'name': 'Roberts',
            'params': {}
        },
        {
            'operation': 'edge_sobel',
            'name': 'Sobel', 
            'params': {}
        },
        {
            'operation': 'edge_prewitt',
            'name': 'Prewitt', 
            'params': {}
        },
        {
            'operation': 'edge_laplacian',
            'name': 'Laplacien', 
            'params': {}
        }
    ]
    
    results = []
    
    for filter_config in edge_filters:
        print(f"\n🔧 TEST: {filter_config['name']}")
        print("-" * 25)
        
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
                    processed_img = cv2.imread(processed_path, cv2.IMREAD_UNCHANGED)
                    
                    print(f"📊 Image traitée:")
                    print(f"   Dimensions: {processed_img.shape}")
                    
                    # Vérifier si c'est en grayscale
                    is_grayscale = len(processed_img.shape) == 2
                    print(f"   Type: {'Grayscale' if is_grayscale else 'Couleur'}")
                    
                    # Validation technique
                    expected_dims = original_img.shape[:2]
                    actual_dims = processed_img.shape[:2]
                    
                    if expected_dims == actual_dims:
                        print("✅ Dimensions conservées")
                    else:
                        print("❌ Dimensions modifiées")
                    
                    # Analyser les contours détectés
                    if is_grayscale:
                        edge_img = processed_img
                    else:
                        edge_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
                    
                    # Compter les pixels de contours (non-zéro)
                    edge_pixels = np.count_nonzero(edge_img)
                    total_pixels = edge_img.size
                    edge_percentage = (edge_pixels / total_pixels) * 100
                    
                    print(f"📈 Pixels de contours: {edge_pixels} ({edge_percentage:.1f}%)")
                    
                    # Analyser l'intensité des contours
                    mean_intensity = np.mean(edge_img[edge_img > 0]) if edge_pixels > 0 else 0
                    max_intensity = np.max(edge_img)
                    
                    print(f"📈 Intensité moyenne contours: {mean_intensity:.2f}")
                    print(f"📈 Intensité maximale: {max_intensity}")
                    
                    # Analyser la continuité des contours
                    # Utiliser la connectivité pour mesurer la qualité
                    _, labels, stats, _ = cv2.connectedComponentsWithStats(edge_img, connectivity=8)
                    num_components = labels.max()
                    
                    print(f"📈 Composantes connectées: {num_components}")
                    
                    # Calculer la variance (mesure de la distribution des contours)
                    edge_variance = np.var(edge_img.astype(np.float64))
                    print(f"📈 Variance des contours: {edge_variance:.2f}")
                    
                    # Vérifier les valeurs de pixels
                    unique_values = np.unique(edge_img)
                    print(f"📈 Valeurs uniques: {len(unique_values)} valeurs")
                    
                    # Déterminer si c'est binaire ou en niveaux de gris
                    is_binary = len(unique_values) <= 2 and all(val in [0, 255] for val in unique_values)
                    print(f"📈 Type de sortie: {'Binaire' if is_binary else 'Niveaux de gris'}")
                    
                    results.append({
                        'name': filter_config['name'],
                        'file': output_filename,
                        'path': processed_path,
                        'edge_percentage': edge_percentage,
                        'mean_intensity': mean_intensity,
                        'max_intensity': max_intensity,
                        'components': num_components,
                        'variance': edge_variance,
                        'is_binary': is_binary,
                        'is_grayscale': is_grayscale
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
        print(f"\n📊 COMPARAISON DES FILTRES DE DÉTECTION DE CONTOURS:")
        print("=" * 70)
        
        print(f"\n{'Filtre':<12} {'Contours%':<10} {'Intensité':<10} {'Composantes':<12} {'Type':<10}")
        print("-" * 70)
        
        for result in results:
            output_type = "Binaire" if result['is_binary'] else "Niveaux"
            print(f"{result['name']:<12} {result['edge_percentage']:<10.1f} {result['mean_intensity']:<10.1f} {result['components']:<12} {output_type:<10}")
        
        # Analyse comparative
        print(f"\n🔍 ANALYSE COMPARATIVE:")
        
        # Filtre avec le plus de contours détectés
        max_edges = max(results, key=lambda x: x['edge_percentage'])
        print(f"   Plus de contours: {max_edges['name']} ({max_edges['edge_percentage']:.1f}%)")
        
        # Filtre avec la meilleure intensité
        max_intensity = max(results, key=lambda x: x['mean_intensity'])
        print(f"   Meilleure intensité: {max_intensity['name']} ({max_intensity['mean_intensity']:.1f})")
        
        # Filtre avec moins de fragmentation
        min_components = min(results, key=lambda x: x['components'])
        print(f"   Moins fragmenté: {min_components['name']} ({min_components['components']} composantes)")
        
        print(f"\n💡 FICHIERS POUR VÉRIFICATION VISUELLE:")
        print(f"   Original: {original_path}")
        for result in results:
            print(f"   {result['name']}: {result['path']}")

if __name__ == "__main__":
    test_edge_filters()