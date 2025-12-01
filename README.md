# Image Preprocessing Platform

## Project Structure
```
ImagePreprocessingPlatform/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   ├── start_server.py     # Server startup script
│   ├── test_upload.py      # Upload testing script
│   ├── TESTING.md          # Testing documentation
│   ├── config/
│   │   └── settings.py      # Configuration
│   ├── services/
│   │   ├── upload_service.py   # Upload logic
│   │   └── validation_service.py # File validation
│   ├── routes/
│   │   └── upload_routes.py    # Upload endpoints
│   └── utils/
│       ├── file_utils.py       # File utilities
│       └── error_handlers.py   # Error handling
├── frontend/               # React app
├── uploads/               # Original uploaded images
└── processed/            # Processed images
```

## Backend API Endpoints

### POST /api/upload
Upload multiple image files
- **Body**: FormData with 'files' field (multiple files supported)
- **Response**: 
```json
{
  "message": "2 fichier(s) uploadé(s) avec succès",
  "successful_uploads": [...],
  "failed_uploads": [...],
  "total_uploaded": 2
}
```

### GET /api/gallery
Get uploaded images with metadata
- **Response**: `{'images': [...], 'total': 5}`

### GET /api/image/<filename>
Retrieve specific uploaded image

### DELETE /api/image/<filename>
Delete uploaded image

### POST /process (TODO)
Process an uploaded image
- **Body**: `{'filename': 'image.jpg', 'operation': 'grayscale'}`
- **Response**: `{'message': 'Processing complete', 'output_file': 'processed_image.jpg'}`

### GET /operations (TODO)
Get available processing operations
- **Response**: Array of operations with name and label

### GET /download/<filename> (TODO)
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
python start_server.py
```

Server runs on http://localhost:5000

## Testing Upload Functionality
```bash
# Run automated tests
python test_upload.py

# Manual API testing
curl http://localhost:5000/api/gallery
curl -X POST -F "files=@image.jpg" http://localhost:5000/api/upload
```

See `TESTING.md` for detailed testing instructions.

## Frontend Requirements
The React frontend should:
1. Upload images via /upload endpoint
2. Display original and processed images side by side
3. Provide UI controls for different operations
4. Allow downloading processed images
5. Handle errors gracefully

## **Actors**

1. **User** – uploads, processes, visualizes, and downloads images.
2. **System / Backend** – handles image processing, storage, and serves the web interface.
3. **Admin (Optional)** – monitors usage or manages system settings.

---

## **Use Cases & Tasks**

### **1. Image Upload**

**Use Case:** Allow users to upload images

**Tasks:**

- ✅ Implement file input for uploading images (support multiple formats: PNG, JPG, etc.).
- ✅ Validate uploaded files (file type, size limits).
- ✅ Display error messages for invalid files.
- ✅ Support multiple images upload and gallery view.

**Backend Implementation Status:** ✅ COMPLETED
- Modular architecture with services, routes, and utilities
- Multiple file upload support (max 10 files, 16MB each)
- Strict validation (format, size, image integrity)
- Comprehensive error handling
- Gallery endpoint with metadata
- RESTful API endpoints

---

### **2. Image Display & Visualization**

**Use Case:** Show original and processed images

**Tasks:**

- Display uploaded image immediately.
- Implement side-by-side comparison: original vs processed image.
- Add **zoom functionality** for detailed viewing.
- Optionally implement **split-view drag comparison**.

---

### **3. Basic Preprocessing**

**Use Case:** Apply standard image preprocessing transformations

**Tasks:**

- Convert to grayscale.
- Apply binary thresholding (fixed/adaptive/mean-based).
- Apply filters (blur, sharpen, edge detection).
- Redimension/rescale images.
- Geometric transformations (rotation, flipping).
- Normalize pixel values to a standard range (e.g., [0, 1]).
- Equalize histograms to enhance contrast.
- Segment image channels (RGB).

---

### **4. Advanced & Innovative Features**

**Use Case:** Provide enhanced preprocessing and interactivity

**Tasks:**

- Real-time preview of transformations before applying.
- Undo/Redo functionality for each operation.
- Interactive histogram display (grayscale or per RGB channel).
- Region of interest selection (e.g., faces, simple object contours).
- Bonus: automated region detection or pre-processing presets.

---

### **5. Image Download**

**Use Case:** Let users save processed images

**Tasks:**

- Implement a download button for processed images.
- Ensure image format and quality are preserved.
- Optionally, allow batch downloads for multiple images.

---

### **6. Error Handling**

**Use Case:** Prevent and handle user or system errors

**Tasks:**

- Validate input formats and sizes.
- Handle processing errors gracefully with user-friendly messages.
- Log errors for debugging.

---

### **7. Backend & Technical Tasks**

**Use Case:** Build robust and maintainable system

**Tasks:**

- Choose backend framework (e.g., Flask, Django, Node.js).
- Integrate Python image processing libraries (OpenCV, PIL).
- Store images temporarily for processing (or permanent if needed).
- Implement a clean API for frontend-backend communication.

---

### **8. Presentation & Documentation**

**Use Case:** Showcase the project

**Tasks:**

- Prepare 10-minute demo highlighting functionality.
- Document architecture, preprocessing methods, and innovative features.
- Include screenshots or live demo of interface and transformations.