import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_operations_list():
    """Test de la liste des opérations"""
    print("📋 Test de la liste des opérations")
    
    try:
        response = requests.get(f"{BASE_URL}/operations")
        if response.status_code == 200:
            operations = response.json()['operations']
            print(f"✅ {len(operations)} opérations disponibles:")
            for op_name, op_info in operations.items():
                print(f"   - {op_name}: {op_info['name']}")
        else:
            print(f"❌ Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_grayscale_processing():
    """Test du traitement en niveaux de gris"""
    print("\n🎨 Test traitement niveaux de gris")
    
    # Récupérer une image disponible
    response = requests.get(f"{BASE_URL}/gallery")
    images = response.json().get('images', [])
    
    if not images:
        print("❌ Aucune image disponible")
        return
    
    filename = images[0]['filename']
    print(f"📸 Test avec: {filename}")
    
    # Traitement en niveaux de gris
    payload = {
        'filename': filename,
        'operation': 'grayscale'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/process", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Traitement réussi:")
            print(f"   Fichier de sortie: {result['output_file']}")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_blur_with_params():
    """Test du flou avec paramètres"""
    print("\n🌫️ Test flou avec paramètres")
    
    # Récupérer une image disponible
    response = requests.get(f"{BASE_URL}/gallery")
    images = response.json().get('images', [])
    
    if not images:
        print("❌ Aucune image disponible")
        return
    
    filename = images[0]['filename']
    
    # Traitement flou avec paramètres
    payload = {
        'filename': filename,
        'operation': 'blur',
        'parameters': {
            'kernel_size': 15
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/process", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Flou appliqué:")
            print(f"   Fichier de sortie: {result['output_file']}")
            print(f"   Paramètres: {result['parameters']}")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_threshold():
    """Test du seuillage"""
    print("\n⚫ Test seuillage binaire")
    
    # Récupérer une image disponible
    response = requests.get(f"{BASE_URL}/gallery")
    images = response.json().get('images', [])
    
    if not images:
        print("❌ Aucune image disponible")
        return
    
    filename = images[0]['filename']
    
    # Traitement seuillage
    payload = {
        'filename': filename,
        'operation': 'threshold',
        'parameters': {
            'threshold': 100,
            'type': 'binary'
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/process", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Seuillage appliqué:")
            print(f"   Fichier de sortie: {result['output_file']}")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🧪 Tests de traitement d'images")
    print("=" * 50)
    
    test_operations_list()
    test_grayscale_processing()
    test_blur_with_params()
    test_threshold()
    
    print("\n✅ Tests terminés!")