import requests

BASE_URL = "http://localhost:5000/api"

def test_image_info():
    """Test de l'endpoint /info"""
    print("📋 Test de l'endpoint /info")
    
    # Récupérer la liste des images
    response = requests.get(f"{BASE_URL}/gallery")
    if response.status_code != 200:
        print("❌ Impossible de récupérer la galerie")
        return
    
    images = response.json().get('images', [])
    if not images:
        print("❌ Aucune image disponible pour tester")
        return
    
    filename = images[0]['filename']
    print(f"📸 Test avec: {filename}")
    
    # Test endpoint /info
    try:
        response = requests.get(f"{BASE_URL}/image/{filename}/info")
        if response.status_code == 200:
            info = response.json()
            print("✅ Endpoint /info fonctionne:")
            print(f"   Fichier: {info['filename']}")
            print(f"   Dimensions: {info['width']}x{info['height']}")
            print(f"   Format: {info['format']}")
            print(f"   Taille: {info['size_bytes']} bytes")
            print(f"   Ratio: {info['aspect_ratio']}")
            print(f"   Transparence: {info['has_transparency']}")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_image_info()