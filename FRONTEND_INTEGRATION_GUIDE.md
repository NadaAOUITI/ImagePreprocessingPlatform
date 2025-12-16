# Frontend Integration Guide - Image Preprocessing Platform

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python start_server.py
```
**Server runs on:** `http://localhost:5000`

### Important Notes
- ⚠️ **Ignore all test files** (`test_*.py`) - they are for backend testing only
- 📁 **Folder Structure**: `uploads/` (original images), `processed/` (processed images)
- 🔧 **Content-Type**: Use `multipart/form-data` for file uploads, `application/json` for processing requests

---

## 📋 API Endpoints Reference

### 🔼 Image Upload & Management

#### 1. Upload Images
```http
POST /api/upload
Content-Type: multipart/form-data
```

**Request:**
```javascript
const formData = new FormData();
formData.append('files', file1);
formData.append('files', file2); // Multiple files supported

fetch('http://localhost:5000/api/upload', {
    method: 'POST',
    body: formData
})
```

**Response:**
```json
{
    "message": "2 fichier(s) uploadé(s) avec succès",
    "successful_uploads": [
        {
            "filename": "image1.jpg",
            "size": 245760,
            "success": true
        }
    ],
    "failed_uploads": [],
    "total_uploaded": 2
}
```

#### 2. Get Gallery (List All Images)
```http
GET /api/gallery
```

**Response:**
```json
{
    "images": [
        {
            "filename": "image1.jpg",
            "size": 245760,
            "upload_date": "2024-01-15T10:30:00"
        }
    ],
    "total": 1
}
```

#### 3. Get Specific Image
```http
GET /api/image/{filename}
```
Returns the actual image file (for display in `<img>` tags)

#### 4. Delete Image
```http
DELETE /api/image/{filename}
```

**Response:**
```json
{
    "message": "Image supprimée avec succès"
}
```

#### 5. Get Image Information
```http
GET /api/image/{filename}/info
```

**Response:**
```json
{
    "filename": "image1.jpg",
    "size": 245760,
    "dimensions": [1920, 1080],
    "format": "JPEG",
    "upload_date": "2024-01-15T10:30:00"
}
```

---

### ⚙️ Image Processing

#### 3. Process Image
```http
POST /api/process
Content-Type: application/json
```

**Request:**
```json
{
    "filename": "image1.jpg",
    "operation": "grayscale",
    "parameters": {}
}
```

**Response:**
```json
{
    "message": "Traitement terminé avec succès",
    "input_file": "image1.jpg",
    "output_file": "image1_grayscale.jpg",
    "operation": "grayscale",
    "parameters": {}
}
```

#### 5. Get Available Operations
```http
GET /api/operations
```

**Response:**
```json
{
    "operations": [
        {
            "name": "grayscale",
            "description": "Convert to grayscale",
            "parameters": []
        },
        {
            "name": "blur_gaussian",
            "description": "Gaussian blur",
            "parameters": [
                {
                    "name": "kernel_size",
                    "type": "integer",
                    "default": 5,
                    "min": 3,
                    "max": 31
                }
            ]
        }
    ]
}
```

#### 7. Get Processed Image
```http
GET /api/processed/{filename}
```
Returns the processed image file

---

## 🛠️ Available Processing Operations

### Basic Operations
- **`grayscale`** - Convert to grayscale
- **`normalize`** - Normalize pixel values
- **`histogram_eq`** - Histogram equalization
- **`histogram_stretch`** - Histogram stretching

### Filters & Blur
- **`blur_gaussian`** - Gaussian blur
  - Parameters: `kernel_size` (3-31, odd numbers)

### Edge Detection
- **`edge_canny`** - Canny edge detection
  - Parameters: `threshold1` (50-150), `threshold2` (100-300)
- **`edge_sobel`** - Sobel edge detection
- **`edge_prewitt`** - Prewitt edge detection
- **`edge_laplacian`** - Laplacian edge detection

### Geometric Transformations
- **`resize`** - Resize image
  - Parameters: `width` (pixels), `height` (pixels)
- **`rotate`** - Rotate image
  - Parameters: `angle` (degrees, -360 to 360)
- **`flip`** - Flip image
  - Parameters: `direction` ("horizontal", "vertical", "both")

### Advanced
- **`threshold`** - Binary thresholding
  - Parameters: `threshold` (0-255), `type` ("binary", "adaptive")
- **`extract_channel`** - Extract RGB channel
  - Parameters: `channel` ("red", "green", "blue")

---

## 🏗️ Backend Architecture

The backend follows a clean architecture pattern:

**Request Flow:** `Frontend → Routes → Services → Response`

**Example Use Case - Image Processing:**
1. Frontend sends POST to `/api/process`
2. `processing_routes.py` receives request
3. Route calls `ProcessingService.process_image()`
4. Service applies operation using OpenCV
5. Processed image saved to `processed/` folder
6. Response sent back with new filename

**Key Components:**
- **Routes** (`routes/`) - Handle HTTP requests/responses
- **Services** (`services/`) - Business logic and image processing
- **Utils** (`utils/`) - File operations and error handling
- **Config** (`config/`) - Settings and folder paths

---

## 💻 React Integration Examples

### Image Upload Component
```jsx
import React, { useState } from 'react';

function ImageUpload() {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [uploading, setUploading] = useState(false);

    const handleUpload = async () => {
        if (selectedFiles.length === 0) return;

        setUploading(true);
        const formData = new FormData();
        
        selectedFiles.forEach(file => {
            formData.append('files', file);
        });

        try {
            const response = await fetch('http://localhost:5000/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.successful_uploads) {
                alert(`${result.total_uploaded} images uploaded successfully!`);
            }
        } catch (error) {
            console.error('Upload error:', error);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div>
            <input 
                type="file" 
                multiple 
                accept="image/*"
                onChange={(e) => setSelectedFiles([...e.target.files])}
            />
            <button onClick={handleUpload} disabled={uploading}>
                {uploading ? 'Uploading...' : 'Upload Images'}
            </button>
        </div>
    );
}
```

### Image Processing Component
```jsx
import React, { useState } from 'react';

function ImageProcessor({ filename }) {
    const [processing, setProcessing] = useState(false);
    const [processedImage, setProcessedImage] = useState(null);

    const processImage = async (operation, parameters = {}) => {
        setProcessing(true);
        
        try {
            const response = await fetch('http://localhost:5000/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: filename,
                    operation: operation,
                    parameters: parameters
                })
            });
            
            const result = await response.json();
            
            if (result.output_file) {
                setProcessedImage(result.output_file);
            }
        } catch (error) {
            console.error('Processing error:', error);
        } finally {
            setProcessing(false);
        }
    };

    return (
        <div>
            <div>
                <h3>Original Image</h3>
                <img 
                    src={`http://localhost:5000/api/image/${filename}`}
                    alt="Original"
                    style={{ maxWidth: '300px' }}
                />
            </div>
            
            {processedImage && (
                <div>
                    <h3>Processed Image</h3>
                    <img 
                        src={`http://localhost:5000/api/processed/${processedImage}`}
                        alt="Processed"
                        style={{ maxWidth: '300px' }}
                    />
                </div>
            )}
            
            <div>
                <button 
                    onClick={() => processImage('grayscale')}
                    disabled={processing}
                >
                    Convert to Grayscale
                </button>
                
                <button 
                    onClick={() => processImage('blur_gaussian', { kernel_size: 15 })}
                    disabled={processing}
                >
                    Apply Blur
                </button>
                
                <button 
                    onClick={() => processImage('edge_canny', { threshold1: 100, threshold2: 200 })}
                    disabled={processing}
                >
                    Edge Detection
                </button>
            </div>
        </div>
    );
}
```

### Gallery Component
```jsx
import React, { useState, useEffect } from 'react';

function ImageGallery() {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadGallery();
    }, []);

    const loadGallery = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/gallery');
            const data = await response.json();
            setImages(data.images);
        } catch (error) {
            console.error('Error loading gallery:', error);
        } finally {
            setLoading(false);
        }
    };

    const deleteImage = async (filename) => {
        try {
            await fetch(`http://localhost:5000/api/image/${filename}`, {
                method: 'DELETE'
            });
            loadGallery(); // Refresh gallery
        } catch (error) {
            console.error('Error deleting image:', error);
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <h2>Image Gallery ({images.length})</h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '16px' }}>
                {images.map((image) => (
                    <div key={image.filename} style={{ border: '1px solid #ccc', padding: '8px' }}>
                        <img 
                            src={`http://localhost:5000/api/image/${image.filename}`}
                            alt={image.filename}
                            style={{ width: '100%', height: '150px', objectFit: 'cover' }}
                        />
                        <p>{image.filename}</p>
                        <button onClick={() => deleteImage(image.filename)}>
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}d={processing}
                >
                    Edge Detection
                </button>
            </div>
        </div>
    );
}
```



```

---

## 🚨 Error Handling

### Common Error Responses
```json
// File not found
{
    "error": "File not found: image.jpg"
}

// Invalid operation
{
    "error": "Unknown operation: invalid_op"
}

// Processing failed
{
    "error": "Erreur lors du traitement grayscale"
}
```

### Frontend Error Handling
```javascript
try {
    const response = await fetch('/api/process', { /* ... */ });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Processing failed');
    }
    
    const result = await response.json();
    // Handle success
} catch (error) {
    // Show user-friendly error message
    alert(`Error: ${error.message}`);
}
```

---

## 🔧 Development Tips

1. **CORS**: Backend handles CORS automatically
2. **File Validation**: Backend validates file types and sizes
3. **Image Formats**: Supports JPG, PNG, BMP, TIFF
4. **File Naming**: Processed files get automatic suffixes (e.g., `image_grayscale.jpg`)
5. **Cleanup**: Original and processed images are stored separately
6. **Testing**: Use browser dev tools to inspect API responses