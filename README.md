# Image Preprocessing Platform

## Project Structure
```
ImagePreprocessingPlatform/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── frontend/               # React app (to be created by frontend team)
├── uploads/               # Original uploaded images
└── processed/            # Processed images
```

## Backend API Endpoints

### POST /upload
Upload an image file
- **Body**: FormData with 'file' field
- **Response**: `{'message': 'Upload successful', 'filename': 'image.jpg'}`

### POST /process
Process an uploaded image
- **Body**: `{'filename': 'image.jpg', 'operation': 'grayscale'}`
- **Response**: `{'message': 'Processing complete', 'output_file': 'processed_image.jpg'}`

### GET /operations
Get available processing operations
- **Response**: Array of operations with name and label

### GET /download/<filename>
Download processed image file

## Available Operations
- `grayscale`: Convert to grayscale
- `blur`: Gaussian blur
- `threshold`: Binary threshold
- `edge_detection`: Canny edge detection (to implement)
- `histogram_eq`: Histogram equalization (to implement)

## Setup Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

Server runs on http://localhost:5000

## Frontend Requirements
The React frontend should:
1. Upload images via /upload endpoint
2. Display original and processed images side by side
3. Provide UI controls for different operations
4. Allow downloading processed images
5. Handle errors gracefully