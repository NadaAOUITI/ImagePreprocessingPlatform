from flask import Flask, jsonify
from flask_cors import CORS
import os
from config.settings import Config
from routes.upload_routes import upload_bp
from routes.processing_routes import processing_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configuration CORS
    CORS(app)
    
    # Créer les dossiers nécessaires
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.PROCESSED_FOLDER, exist_ok=True)
    
    # Enregistrer les blueprints
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(processing_bp, url_prefix='/api')
    
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Image Preprocessing Platform API',
            'version': '1.0',
            'endpoints': {
                'upload': '/api/upload',
                'gallery': '/api/gallery',
                'image': '/api/image/<filename>',
                'process': '/api/process',
                'operations': '/api/operations'
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)