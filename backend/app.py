from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from config.settings import Config
from routes.upload_routes import upload_bp
from routes.processing_routes import processing_bp
from routes.advanced_routes import advanced_bp
from routes.download import download_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS pour ton frontend
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.PROCESSED_FOLDER, exist_ok=True)

    # Enregistrement des blueprints
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(processing_bp, url_prefix='/api')
    app.register_blueprint(advanced_bp, url_prefix='/api')
    app.register_blueprint(download_bp, url_prefix='/api')

    # Endpoint test/health
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'upload_folder': os.path.exists(Config.UPLOAD_FOLDER),
            'processed_folder': os.path.exists(Config.PROCESSED_FOLDER)
        })

    # Endpoint temporaire pour le processing
    @app.route("/api/processing/process", methods=["POST", "OPTIONS"])
    def process_image():
        if request.method == "OPTIONS":
            return "", 200  # réponse preflight
        data = request.get_json()
        filename = data.get("filename")
        operation = data.get("operation")
        parameters = data.get("parameters", {})

        # Exemple de traitement fictif
        output_file = "image_floutee.png"
        return jsonify({"output_file": output_file}), 200




    # Endpoint racine
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Image Preprocessing Platform API',
            'version': '1.0'
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
