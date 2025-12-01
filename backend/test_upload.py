import requests
import os

# Configuration
BASE_URL = "http://localhost:5000/api"

def test_home_endpoint():
    """Test de l'endpoint home"""
    try:
        response = requests.get("http://localhost:5000/")
        print("✅ Home endpoint:", response.json())
    except Exception as e:
        print("❌ Erreur home:", str(e))

def test_upload_single_file():
    """Test upload d'un seul fichier"""
    # Créer une image de test simple
    from PIL import Image
    test_image = Image.new('RGB', (100, 100), color='red')
    test_image.save('test_image.jpg')
    
    try:
        with open('test_image.jpg', 'rb') as f:
            files = {'files': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            print("✅ Upload single file:", response.json())
    except Exception as e:
        print("❌ Erreur upload:", str(e))
    finally:
        if os.path.exists('test_image.jpg'):
            os.remove('test_image.jpg')

def test_upload_multiple_files():
    """Test upload de plusieurs fichiers"""
    from PIL import Image
    
    # Créer plusieurs images de test
    test_files = []
    for i in range(3):
        filename = f'test_image_{i}.png'
        img = Image.new('RGB', (50, 50), color=['red', 'green', 'blue'][i])
        img.save(filename)
        test_files.append(filename)
    
    try:
        files = []
        for filename in test_files:
            files.append(('files', open(filename, 'rb')))
        
        response = requests.post(f"{BASE_URL}/upload", files=files)
        print("✅ Upload multiple files:", response.json())
        
        # Fermer les fichiers
        for _, f in files:
            f.close()
            
    except Exception as e:
        print("❌ Erreur upload multiple:", str(e))
    finally:
        for filename in test_files:
            if os.path.exists(filename):
                os.remove(filename)

def test_gallery():
    """Test de l'endpoint galerie"""
    try:
        response = requests.get(f"{BASE_URL}/gallery")
        print("✅ Gallery endpoint:", response.json())
    except Exception as e:
        print("❌ Erreur gallery:", str(e))

def test_invalid_file():
    """Test avec un fichier invalide"""
    # Créer un fichier texte
    with open('test.txt', 'w') as f:
        f.write('This is not an image')
    
    try:
        with open('test.txt', 'rb') as f:
            files = {'files': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            print("✅ Invalid file test:", response.json())
    except Exception as e:
        print("❌ Erreur invalid file:", str(e))
    finally:
        if os.path.exists('test.txt'):
            os.remove('test.txt')

if __name__ == "__main__":
    print("🧪 Tests des endpoints d'upload")
    print("=" * 40)
    
    test_home_endpoint()
    test_upload_single_file()
    test_upload_multiple_files()
    test_gallery()
    test_invalid_file()
    
    print("\n✅ Tests terminés!")