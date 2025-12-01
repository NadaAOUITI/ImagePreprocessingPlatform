from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Démarrage du serveur Image Preprocessing Platform")
    print("📍 URL: http://localhost:5000")
    print("📋 Endpoints disponibles:")
    print("   - GET  /                    : Info API")
    print("   - POST /api/upload          : Upload d'images")
    print("   - GET  /api/gallery         : Liste des images")
    print("   - GET  /api/image/<filename>: Récupérer une image")
    print("   - DEL  /api/image/<filename>: Supprimer une image")
    print("-" * 50)
    
    app.run(debug=True, port=5000, host='0.0.0.0')