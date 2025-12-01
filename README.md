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
│   │   ├── validation_service.py # File validation
│   │   └── image_service.py    # Image processing (thumbnails, resize)
│   ├── routes/
│   │   └── upload_routes.py    # Upload & display endpoints
│   └── utils/
│       ├── file_utils.py       # File utilities
│       └── error_handlers.py   # Error handling
├── frontend/               # React app
├── uploads/               # Original uploaded images
└── processed/            # Processed images
```



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

## Testing Display Functionality
```bash
# Run display tests (info endpoint)
python test_display.py

# Manual info testing
curl http://localhost:5000/api/image/filename.jpg/info
```

See `TESTING.md` for detailed testing instructions.



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

**Backend Endpoints:**
- `POST /api/upload` - Upload multiple images
- `GET /api/gallery` - Get list of uploaded images with metadata
- `GET /api/image/<filename>` - Retrieve specific image
- `DELETE /api/image/<filename>` - Delete image

---

### **2. Image Display & Visualization**

**Use Case:** Show original and processed images

**Tasks:**

- Display uploaded image immediately.
- Implement side-by-side comparison: original vs processed image.
- Add **zoom functionality** for detailed viewing.
- Optionally implement **split-view drag comparison**.

**Backend Implementation Status:** ✅ COMPLETED (Minimal backend support)
- Image serving and metadata endpoints
- **Note:** This task is primarily FRONTEND work - thumbnails and resizing handled by frontend

**Backend Endpoints:**
- `GET /api/image/<filename>` - Get full resolution image
- `GET /api/image/<filename>/info` - Get detailed image information



---

### **3. Basic Preprocessing**

**Use Case:** Apply standard image preprocessing transformations

**Tasks:**

- ✅ Convert to grayscale.
- ✅ Apply binary thresholding (fixed/adaptive/mean-based).
- ✅ Apply filters (blur, sharpen, edge detection).
- ✅ Redimension/rescale images.
- ✅ Geometric transformations (rotation, flipping).
- ✅ Normalize pixel values to a standard range (e.g., [0, 1]).
- ✅ Equalize histograms to enhance contrast.
- ✅ Segment image channels (RGB).

**Backend Implementation Status:** ✅ COMPLETED

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