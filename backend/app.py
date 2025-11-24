from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = '../uploads'
PROCESSED_FOLDER = '../processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': 'Upload successful', 'filename': filename})
    
    return jsonify({'error': 'Invalid file'}), 400

@app.route('/process', methods=['POST'])
def process_image():
    data = request.json
    filename = data.get('filename')
    operation = data.get('operation')
    
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = cv2.imread(input_path)
    
    # Basic processing examples
    if operation == 'grayscale':
        processed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif operation == 'blur':
        processed = cv2.GaussianBlur(image, (15, 15), 0)
    elif operation == 'threshold':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, processed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    else:
        processed = image
    
    output_filename = f"processed_{filename}"
    output_path = os.path.join(PROCESSED_FOLDER, output_filename)
    cv2.imwrite(output_path, processed)
    
    return jsonify({'message': 'Processing complete', 'output_file': output_filename})

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

@app.route('/operations')
def get_operations():
    operations = [
        {'name': 'grayscale', 'label': 'Convert to Grayscale'},
        {'name': 'blur', 'label': 'Gaussian Blur'},
        {'name': 'threshold', 'label': 'Binary Threshold'},
        {'name': 'edge_detection', 'label': 'Edge Detection'},
        {'name': 'histogram_eq', 'label': 'Histogram Equalization'}
    ]
    return jsonify(operations)

if __name__ == '__main__':
    app.run(debug=True, port=5000)