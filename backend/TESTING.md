# Guide de Test - Tâche d'Upload d'Images

## 🚀 Démarrage du serveur

```bash
cd backend
python start_server.py
```

Le serveur démarre sur `http://localhost:5000`

## 🧪 Tests Automatisés

```bash
# Dans un autre terminal
python test_upload.py
```

## 📋 Tests Manuels avec curl

### 1. Test de l'API home
```bash
curl http://localhost:5000/
```

### 2. Upload d'une seule image
```bash
curl -X POST -F "files=@path/to/your/image.jpg" http://localhost:5000/api/upload
```

### 3. Upload de plusieurs images
```bash
curl -X POST -F "files=@image1.jpg" -F "files=@image2.png" http://localhost:5000/api/upload
```

### 4. Récupérer la galerie
```bash
curl http://localhost:5000/api/gallery
```

### 5. Récupérer une image spécifique
```bash
curl http://localhost:5000/api/image/filename.jpg
```

### 6. Supprimer une image
```bash
curl -X DELETE http://localhost:5000/api/image/filename.jpg
```

## 🧪 Tests avec Postman

1. **POST** `http://localhost:5000/api/upload`
   - Body: form-data
   - Key: `files` (type: File)
   - Sélectionner une ou plusieurs images

2. **GET** `http://localhost:5000/api/gallery`
   - Récupère la liste des images uploadées

## ✅ Fonctionnalités Testées

- ✅ Upload de fichiers multiples
- ✅ Validation des formats (PNG, JPG, etc.)
- ✅ Validation de la taille (max 16MB)
- ✅ Vérification que c'est une vraie image
- ✅ Gestion d'erreurs pour fichiers invalides
- ✅ Génération de noms uniques
- ✅ Extraction de métadonnées
- ✅ Galerie d'images
- ✅ Suppression d'images

## 🎯 Résultats Attendus

### Upload réussi:
```json
{
  "message": "2 fichier(s) uploadé(s) avec succès",
  "successful_uploads": [
    {
      "filename": "image_a1b2c3d4.jpg",
      "original_filename": "image.jpg",
      "success": true,
      "metadata": {
        "width": 1920,
        "height": 1080,
        "format": "JPEG",
        "mode": "RGB",
        "size_bytes": 245760
      },
      "upload_time": "2024-01-15T10:30:00"
    }
  ],
  "failed_uploads": [],
  "total_uploaded": 2
}
```

### Fichier invalide:
```json
{
  "message": "0 fichier(s) uploadé(s) avec succès",
  "successful_uploads": [],
  "failed_uploads": [
    {
      "filename": "document.txt",
      "success": false,
      "errors": [
        "Format de fichier non supporté",
        "Le fichier n'est pas une image valide"
      ]
    }
  ],
  "total_uploaded": 0
}
```