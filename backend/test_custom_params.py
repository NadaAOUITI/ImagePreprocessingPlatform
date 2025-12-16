import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_rotation_with_custom_angle():
    """Test rotation avec angle personnalisé"""
    print("🔄 Test rotation avec angle personnalisé")
    
    # Récupérer une image disponible
    response = requests.get(f"{BASE_URL}/gallery")
    images = response.json().get('images', [])
    
    if not images:
        print("❌ Aucune image disponible")
        return
    
    filename = images[0]['filename']
    print(f"📸 Test avec: {filename}")
    
    # Test rotation 45 degrés
    payload = {
        'filename': filename,
        'operation': 'rotate',
        'parameters': {
            'angle': 45
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/process", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Rotation 45° réussie:")
            print(f"   Fichier de sortie: {result['output_file']}")
            print(f"   Angle appliqué: {result['parameters']['angle']}°")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_blur_with_custom_kernel():
    """Test flou avec taille de kernel personnalisée"""
    print("\n🌫️ Test flou avec kernel personnalisé")
    
    # Récupérer une image disponible
    response = requests.get(f"{BASE_URL}/gallery")
    images = response.json().get('images', [])
    
    if not images:
        print("❌ Aucune image disponible")
        return
    
    filename = images[0]['filename']
    
    # Test flou gaussien avec kernel 21x21
    payload = {
        'filename': filename,
        'operation': 'blur_gaussian',
        'parameters': {
            'kernel_size': 21
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/process", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Flou gaussien 21x21 réussi:")
            print(f"   Fichier de sortie: {result['output_file']}")
            print(f"   Taille kernel: {result['parameters']['kernel_size']}x{result['parameters']['kernel_size']}")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_threshold_with_custom_value():
    """Test seuillage avec valeur personnalisée"""
    print("\n⚫ Test seuillage avec valeur personnalisée")
    
    # Récupérer une image disponible
    response = requests.get(f"{BASE_URL}/gallery")
    images = response.json().get('images', [])
    
    if not images:
        print("❌ Aucune image disponible")
        return
    
    filename = images[0]['filename']
    
    # Test seuillage avec valeur 80
    payload = {
        'filename': filename,
        'operation': 'threshold',
        'parameters': {
            'threshold': 80,
            'type': 'binary'
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/process", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("✅ Seuillage à 80 réussi:")
            print(f"   Fichier de sortie: {result['output_file']}")
            print(f"   Seuil appliqué: {result['parameters']['threshold']}")
            print(f"   Type: {result['parameters']['type']}")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_multiple_filters_with_params():
    """Test plusieurs filtres avec paramètres différents"""
    print("\n🎛️ Test filtres multiples avec paramètres")
    
    # Récupérer une image disponible
    response = requests.get(f"{BASE_URL}/gallery")
    images = response.json().get('images', [])
    
    if not images:
        print("❌ Aucune image disponible")
        return
    
    filename = images[0]['filename']
    
    # Tests multiples
    tests = [
        {
            'operation': 'blur_median',
            'parameters': {'kernel_size': 15},
            'description': 'Flou médian 15x15'
        },
        {
            'operation': 'rotate',
            'parameters': {'angle': -30},
            'description': 'Rotation -30°'
        },
        {
            'operation': 'edge_canny',
            'parameters': {'low': 30, 'high': 100},
            'description': 'Canny (30-100)'
        }
    ]
    
    for test in tests:
        payload = {
            'filename': filename,
            'operation': test['operation'],
            'parameters': test['parameters']
        }
        
        try:
            response = requests.post(f"{BASE_URL}/process", json=payload)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {test['description']}: {result['output_file']}")
            else:
                print(f"❌ {test['description']}: Erreur {response.status_code}")
        except Exception as e:
            print(f"❌ {test['description']}: {e}")

def test_operations_list():
    """Test de la liste des opérations avec paramètres"""
    print("\n📋 Test liste des opérations avec paramètres")
    
    try:
        response = requests.get(f"{BASE_URL}/operations")
        if response.status_code == 200:
            operations = response.json()['operations']
            
            # Vérifier les opérations avec paramètres
            param_ops = {k: v for k, v in operations.items() if v.get('parameters')}
            
            print(f"✅ {len(param_ops)} opérations avec paramètres:")
            for op_name, op_info in param_ops.items():
                params = op_info['parameters']
                param_names = list(params.keys())
                print(f"   - {op_name}: {param_names}")
        else:
            print(f"❌ Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🧪 Tests des paramètres personnalisés")
    print("=" * 60)
    
    test_operations_list()
    test_rotation_with_custom_angle()
    test_blur_with_custom_kernel()
    test_threshold_with_custom_value()
    test_multiple_filters_with_params()
    
    print("\n✅ Tests terminés!")