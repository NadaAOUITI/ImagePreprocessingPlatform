# Complete API Integration Guide - Image Preprocessing Platform

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
**Server runs on:** `http://localhost:5000`

### Important Notes
- ⚠️ **Test Files**: Ignore all `test_*.py` files - they are for backend testing only
- 📁 **Folder Structure**: 
  - `uploads/` - Original uploaded images
  - `processed/` - Processed/transformed images
- 🔧 **Content-Type**: 
  - Use `multipart/form-data` for file uploads
  - Use `application/json` for processing requests




#### 3. Get Processed Image
```http
GET /api/processed/{filename}
```

**Usage:**
```javascript
<img src="http://localhost:5000/api/processed/image1_grayscale.jpg" alt="Processed" />
```

---

### 🔬 Advanced Processing Features

#### 1. Real-time Preview (Without Saving)
```http
POST /api/preview
Content-Type: application/json
```

**Request:**
```json
{
    "filename": "image1.jpg",
    "operation": "blur",
    "params": {
        "kernel": 15
    }
}
```

**Response:**
```json
{
    "preview": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "success": true
}
```

**Frontend Example:**
```javascript
const previewTransform = async (filename, operation, params) => {
    const response = await fetch('http://localhost:5000/api/preview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            filename,
            operation,
            params
        })
    });
    
    const data = await response.json();
    // Display base64 image
    document.getElementById('preview').src = data.preview;
};
```

#### 2. Get Image Histogram
```http
GET /api/histogram/{filename}?channel=all
```

**Query Parameters:**
- `channel`: `all`, `red`, `green`, `blue`

**Response:**
```json
{
    "red": [120, 145, 178, ...],
    "green": [98, 132, 165, ...],
    "blue": [87, 115, 142, ...],
    "success": true
}
```

**Frontend Example:**
```javascript
const getHistogram = async (filename, channel = 'all') => {
    const response = await fetch(
        `http://localhost:5000/api/histogram/${filename}?channel=${channel}`
    );
    return await response.json();
};
```

#### 3. Detect ROI (Region of Interest)
```http
POST /api/roi/detect
Content-Type: application/json
```

**Request:**
```json
{
    "filename": "photo.jpg",
    "type": "faces"
}
```

**Types:** `faces`, `contours`

**Response:**
```json
{
    "regions": [
        {
            "x": 120,
            "y": 80,
            "width": 200,
            "height": 200,
            "type": "face"
        }
    ],
    "success": true
}
```

#### 4. Get Available Presets
```http
GET /api/presets
```

**Response:**
```json
{
    "enhance_contrast": {
        "name": "Enhance Contrast",
        "operations": [
            {"type": "histogram_equalization", "params": {}},
            {"type": "sharpen", "params": {"strength": 1.5}}
        ]
    },
    "edge_detection": {
        "name": "Edge Detection",
        "operations": [
            {"type": "grayscale", "params": {}},
            {"type": "gaussian_blur", "params": {"kernel": 5}},
            {"type": "canny", "params": {"threshold1": 100, "threshold2": 200}}
        ]
    },
    "denoise": {
        "name": "Denoise",
        "operations": [
            {"type": "bilateral_filter", "params": {"d": 9, "sigmaColor": 75, "sigmaSpace": 75}}
        ]
    },
    "black_white": {
        "name": "Black & White",
        "operations": [
            {"type": "grayscale", "params": {}},
            {"type": "adaptive_threshold", "params": {"blockSize": 11, "C": 2}}
        ]
    }
}
```

#### 5. Apply Preset
```http
POST /api/preset/apply
Content-Type: application/json
```

**Request:**
```json
{
    "filename": "image1.jpg",
    "preset": "enhance_contrast"
}
```

**Response:**
```json
{
    "processed_image": "image1_enhanced.jpg",
    "success": true
}
```

---

### 📥 Download Endpoints

#### 1. Download Single File
```http
GET /api/download/single/{filename}
```

**Frontend Example:**
```javascript
const downloadSingle = (filename) => {
    window.location.href = `http://localhost:5000/api/download/single/${filename}`;
};
```

#### 2. Batch Download (ZIP)
```http
GET /api/download/batch?files=file1.jpg,file2.jpg,file3.jpg
```

**Frontend Example:**
```javascript
const downloadBatch = (filenames) => {
    const files = filenames.join(',');
    window.location.href = `http://localhost:5000/api/download/batch?files=${files}`;
};

// Usage
downloadBatch(['image1_grayscale.jpg', 'image2_blur.jpg', 'image3_edges.jpg']);
```

---

## 🛠️ Available Processing Operations

### Basic Operations

| Operation | Description | Parameters |
|-----------|-------------|------------|
| `grayscale` | Convert to grayscale | None |
| `normalize` | Normalize pixel values | None |
| `histogram_eq` | Histogram equalization | None |
| `histogram_stretch` | Histogram stretching | None |

### Filters & Blur

| Operation | Description | Parameters |
|-----------|-------------|------------|
| `blur_gaussian` | Gaussian blur | `kernel_size` (3-31, odd) |
| `blur_median` | Median blur | `kernel_size` (3-31, odd) |
| `blur_average` | Average blur | `kernel_size` (3-31, odd) |

### Edge Detection

| Operation | Description | Parameters |
|-----------|-------------|------------|
| `edge_canny` | Canny edge detection | `low` (50-150), `high` (100-300) |
| `edge_sobel` | Sobel edge detection | `kernel_size` (3, 5, 7) |
| `edge_prewitt` | Prewitt edge detection | `kernel_size` (3, 5, 7) |
| `edge_laplacian` | Laplacian edge detection | `kernel_size` (3, 5, 7) |

### Sharpening

| Operation | Description | Parameters |
|-----------|-------------|------------|
| `sharpen_kernel` | Classic sharpening kernel | None |
| `sharpen_laplacian` | Laplacian sharpening | None |

### Geometric Transformations

| Operation | Description | Parameters |
|-----------|-------------|------------|
| `resize` | Resize image | `width` (px), `height` (px) |
| `rotate` | Rotate image | `angle` (-360 to 360) |
| `flip` | Flip image | `direction` ("horizontal", "vertical", "both") |

### Advanced

| Operation | Description | Parameters |
|-----------|-------------|------------|
| `threshold` | Binary thresholding | `threshold` (0-255), `type` ("binary", "adaptive") |
| `extract_channel` | Extract RGB channel | `channel` ("red", "green", "blue") |
| `contrast_brightness` | Adjust contrast/brightness | `contrast` (float), `brightness` (int) |

---

## 💻 Complete React Integration Examples

### 1. Image Upload Component

```javascript
import React, { useState } from 'react';

function ImageUpload({ onUploadSuccess }) {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);

    const handleFileSelect = (e) => {
        const files = Array.from(e.target.files);
        setSelectedFiles(files);
    };

    const handleUpload = async () => {
        if (selectedFiles.length === 0) {
            alert('Please select files first');
            return;
        }

        setUploading(true);
        setProgress(0);

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
            
            if (result.successful_uploads && result.successful_uploads.length > 0) {
                alert(`✅ ${result.total_uploaded} images uploaded successfully!`);
                setSelectedFiles([]);
                if (onUploadSuccess) onUploadSuccess();
            }
            
            if (result.failed_uploads && result.failed_uploads.length > 0) {
                console.error('Failed uploads:', result.failed_uploads);
            }
        } catch (error) {
            console.error('Upload error:', error);
            alert('❌ Upload failed. Please try again.');
        } finally {
            setUploading(false);
            setProgress(0);
        }
    };

    return (
        <div className="upload-container">
            <input 
                type="file" 
                multiple 
                accept="image/*"
                onChange={handleFileSelect}
                disabled={uploading}
            />
            
            {selectedFiles.length > 0 && (
                <div className="file-list">
                    <p>{selectedFiles.length} file(s) selected:</p>
                    <ul>
                        {selectedFiles.map((file, idx) => (
                            <li key={idx}>{file.name} ({(file.size / 1024).toFixed(2)} KB)</li>
                        ))}
                    </ul>
                </div>
            )}
            
            <button 
                onClick={handleUpload} 
                disabled={uploading || selectedFiles.length === 0}
            >
                {uploading ? `Uploading... ${progress}%` : 'Upload Images'}
            </button>
        </div>
    );
}

export default ImageUpload;
```

### 2. Image Gallery Component

```javascript
import React, { useState, useEffect } from 'react';

function ImageGallery({ onImageSelect }) {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedImage, setSelectedImage] = useState(null);

    useEffect(() => {
        loadGallery();
    }, []);

    const loadGallery = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:5000/api/gallery');
            const data = await response.json();
            setImages(data.images || []);
        } catch (error) {
            console.error('Error loading gallery:', error);
            alert('Failed to load gallery');
        } finally {
            setLoading(false);
        }
    };

    const deleteImage = async (filename) => {
        if (!confirm(`Delete ${filename}?`)) return;
        
        try {
            await fetch(`http://localhost:5000/api/image/${filename}`, {
                method: 'DELETE'
            });
            loadGallery(); // Refresh gallery
            alert('✅ Image deleted successfully');
        } catch (error) {
            console.error('Error deleting image:', error);
            alert('❌ Failed to delete image');
        }
    };

    const getImageInfo = async (filename) => {
        try {
            const response = await fetch(`http://localhost:5000/api/image/${filename}/info`);
            const info = await response.json();
            alert(`
                Filename: ${info.filename}
                Size: ${(info.size / 1024).toFixed(2)} KB
                Dimensions: ${info.dimensions[0]} x ${info.dimensions[1]}
                Format: ${info.format}
                Upload Date: ${new Date(info.upload_date).toLocaleString()}
            `);
        } catch (error) {
            console.error('Error getting image info:', error);
        }
    };

    const selectImage = (image) => {
        setSelectedImage(image);
        if (onImageSelect) onImageSelect(image);
    };

    if (loading) return <div>Loading gallery...</div>;

    if (images.length === 0) {
        return <div>No images uploaded yet. Upload some images to get started!</div>;
    }

    return (
        <div className="gallery-container">
            <h2>Image Gallery ({images.length})</h2>
            
            <div className="gallery-grid">
                {images.map((image) => (
                    <div 
                        key={image.filename} 
                        className={`gallery-item ${selectedImage?.filename === image.filename ? 'selected' : ''}`}
                        onClick={() => selectImage(image)}
                    >
                        <img 
                            src={`http://localhost:5000/api/image/${image.filename}`}
                            alt={image.filename}
                            loading="lazy"
                        />
                        
                        <div className="image-info">
                            <p className="filename">{image.filename}</p>
                            <p className="filesize">{(image.size / 1024).toFixed(2)} KB</p>
                        </div>
                        
                        <div className="image-actions">
                            <button onClick={(e) => {
                                e.stopPropagation();
                                getImageInfo(image.filename);
                            }}>ℹ️ Info</button>
                            
                            <button onClick={(e) => {
                                e.stopPropagation();
                                deleteImage(image.filename);
                            }}>🗑️ Delete</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ImageGallery;
```

### 3. Image Processor Component

```javascript
import React, { useState, useEffect } from 'react';

function ImageProcessor({ filename }) {
    const [operations, setOperations] = useState([]);
    const [selectedOperation, setSelectedOperation] = useState('');
    const [parameters, setParameters] = useState({});
    const [processing, setProcessing] = useState(false);
    const [processedImage, setProcessedImage] = useState(null);
    const [previewMode, setPreviewMode] = useState(false);
    const [previewImage, setPreviewImage] = useState(null);

    useEffect(() => {
        loadOperations();
    }, []);

    const loadOperations = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/operations');
            const data = await response.json();
            setOperations(data.operations || []);
        } catch (error) {
            console.error('Error loading operations:', error);
        }
    };

    const handleOperationChange = (operation) => {
        setSelectedOperation(operation);
        // Reset parameters
        const op = operations.find(o => o.name === operation);
        if (op && op.parameters) {
            const defaultParams = {};
            op.parameters.forEach(param => {
                defaultParams[param.name] = param.default;
            });
            setParameters(defaultParams);
        } else {
            setParameters({});
        }
    };

    const handleParameterChange = (paramName, value) => {
        setParameters(prev => ({
            ...prev,
            [paramName]: value
        }));
    };

    const previewTransformation = async () => {
        if (!selectedOperation) return;
        
        setPreviewMode(true);
        try {
            const response = await fetch('http://localhost:5000/api/preview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: filename,
                    operation: selectedOperation,
                    params: parameters
                })
            });
            
            const data = await response.json();
            if (data.success) {
                setPreviewImage(data.preview);
            }
        } catch (error) {
            console.error('Preview error:', error);
            alert('Failed to generate preview');
        }
    };

    const processImage = async () => {
        if (!selectedOperation) {
            alert('Please select an operation');
            return;
        }

        setProcessing(true);
        try {
            const response = await fetch('http://localhost:5000/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: filename,
                    operation: selectedOperation,
                    parameters: parameters
                })
            });
            
            const result = await response.json();
            
            if (result.output_file) {
                setProcessedImage(result.output_file);
                setPreviewMode(false);
                alert(`✅ Processing complete! File: ${result.output_file}`);
            } else {
                alert('❌ Processing failed');
            }
        } catch (error) {
            console.error('Processing error:', error);
            alert('❌ Processing error occurred');
        } finally {
            setProcessing(false);
        }
    };

    const currentOperation = operations.find(op => op.name === selectedOperation);

    return (
        <div className="processor-container">
            <div className="images-section">
                <div className="image-box">
                    <h3>Original Image</h3>
                    <img 
                        src={`http://localhost:5000/api/image/${filename}`}
                        alt="Original"
                    />
                </div>
                
                {previewMode && previewImage && (
                    <div className="image-box">
                        <h3>Preview (Not Saved)</h3>
                        <img src={previewImage} alt="Preview" />
                    </div>
                )}
                
                {processedImage && !previewMode && (
                    <div className="image-box">
                        <h3>Processed Image</h3>
                        <img 
                            src={`http://localhost:5000/api/processed/${processedImage}`}
                            alt="Processed"
                        />
                        <button onClick={() => {
                            window.location.href = `http://localhost:5000/api/download/single/${processedImage}`;
                        }}>
                            📥 Download
                        </button>
                    </div>
                )}
            </div>
            
            <div className="controls-section">
                <h3>Processing Controls</h3>
                
                <div className="operation-select">
                    <label>Select Operation:</label>
                    <select 
                        value={selectedOperation}
                        onChange={(e) => handleOperationChange(e.target.value)}
                        disabled={processing}
                    >
                        <option value="">-- Choose Operation --</option>
                        {operations.map(op => (
                            <option key={op.name} value={op.name}>
                                {op.description || op.name}
                            </option>
                        ))}
                    </select>
                </div>
                
                {currentOperation && currentOperation.parameters && currentOperation.parameters.length > 0 && (
                    <div className="parameters-section">
                        <h4>Parameters:</h4>
                        {currentOperation.parameters.map(param => (
                            <div key={param.name} className="parameter-control">
                                <label>{param.name}:</label>
                                {param.type === 'integer' ? (
                                    <input 
                                        type="number"
                                        value={parameters[param.name] || param.default}
                                        onChange={(e) => handleParameterChange(param.name, parseInt(e.target.value))}
                                        min={param.min}
                                        max={param.max}
                                        disabled={processing}
                                    />
                                ) : (
                                    <input 
                                        type="text"
                                        value={parameters[param.name] || param.default}
                                        onChange={(e) => handleParameterChange(param.name, e.target.value)}
                                        disabled={processing}
                                    />
                                )}
                                <span className="param-info">
                                    (default: {param.default})
                                </span>
                            </div>
                        ))}
                    </div>
                )}
                
                <div className="action-buttons">
                    <button 
                        onClick={previewTransformation}
                        disabled={!selectedOperation || processing}
                    >
                        👁️ Preview
                    </button>
                    
                    <button 
                        onClick={processImage}
                        disabled={!selectedOperation || processing}
                        className="primary-button"
                    >
                        {processing ? '⏳ Processing...' : '✨ Apply'}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default ImageProcessor;
```

### 4. Preset Processor Component

```javascript
import React, { useState, useEffect } from 'react';

function PresetProcessor({ filename }) {
    const [presets, setPresets] = useState({});
    const [selectedPreset, setSelectedPreset] = useState('');
    const [processing, setProcessing] = useState(false);
    const [result, setResult] = useState(null);

    useEffect(() => {
        loadPresets();
    }, []);

    const loadPresets = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/presets');
            const data = await response.json();
            setPresets(data);
        } catch (error) {
            console.error('Error loading presets:', error);
        }
    };

    const applyPreset = async () => {
        if (!selectedPreset) {
            alert('Please select a preset');
            return;
        }

        setProcessing(true);
        try {
            const response = await fetch('http://localhost:5000/api/preset/apply', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: filename,
                    preset: selectedPreset
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                setResult(data.processed_image);
                alert(`✅ Preset applied! File: ${data.processed_image}`);
            } else {
                alert('❌ Preset application failed');
            }
        } catch (error) {
            console.error('Preset error:', error);
            alert('❌ Error applying preset');
        } finally {
            setProcessing(false);
        }
    };

    return (
        <div className="preset-processor">
            <h3>Quick Presets</h3>
            
            <div className="preset-grid">
                {Object.entries(presets).map(([key, preset]) => (
                    <div 
                        key={key}
                        className={`preset-card ${selectedPreset === key ? 'selected' : ''}`}
                        onClick={() => setSelectedPreset(key)}
                    >
                        <h4>{preset.name}</h4>
                        <p>{preset.operations.length} operations</p>
                        <ul>
                            {preset.operations.map((op, idx) => (
                                <li key={idx}>{op.type}</li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
            
            <button 
                onClick={applyPreset}
                disabled={!selectedPreset || processing}
            >
                {processing ? 'Applying...' : 'Apply Preset'}
            </button>
            
            {result && (
                <div className="result-section">
                    <h4>Result:</h4>
                    <img 
                        src={`http://localhost:5000/api/processed/${result}`}
                        alt="Processed with preset"
                    />
                    <button onClick={() => {
                        window.location.href = `http://localhost:5000/api/download/single/${result}`;
                    }}>
                        📥 Download
                    </button>
                </div>
            )}
        </div>
    );
}

export default PresetProcessor;
```

### 5. Batch Download Component

```javascript
import React, { useState } from 'react';

function BatchDownload({ processedFiles }) {
    const [selectedFiles, setSelectedFiles] = useState([]);

    const toggleFile = (filename) => {
        setSelectedFiles(prev => {
            if (prev.includes(filename)) {
                return prev.filter(f => f !== filename);
            } else {
                return [...prev, filename];
            }
        });
    };

    const selectAll = () => {
        setSelectedFiles(processedFiles.map(f => f.filename));
    };

    const deselectAll = () => {
        setSelectedFiles([]);
    };

    const downloadSelected = () => {
        if (selectedFiles.length === 0) {
            alert('Please select files to download');
            return;
        }
        
        const files = selectedFiles.join(',');
        window.location.href = `http://localhost:5000/api/download/batch?files=${files}`;
    };

    return (
        <div className="batch-download">
            <h3>Batch Download</h3>
            
            <div className="batch-controls">
                <button onClick={selectAll}>Select All</button>
                <button onClick={deselectAll}>Deselect All</button>
                <button 
                    onClick={downloadSelected}
                    disabled={selectedFiles.length === 0}
                    className="download-button"
                >
                    📥 Download Selected ({selectedFiles.length})
                </button>
            </div>
            
            <div className="file-list">
                {processedFiles.map(file => (
                    <div key={file.filename} className="file-item">
                        <input 
                            type="checkbox"
                            checked={selectedFiles.includes(file.filename)}
                            onChange={() => toggleFile(file.filename)}
                        />
                        <span>{file.filename}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default BatchDownload;
```

### 6. Complete App Integration

```javascript
import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import ImageGallery from './components/ImageGallery';
import ImageProcessor from './components/ImageProcessor';
import PresetProcessor from './components/PresetProcessor';
import BatchDownload from './components/BatchDownload';
import './App.css';

function App() {
    const [selectedImage, setSelectedImage] = useState(null);
    const [refreshGallery, setRefreshGallery] = useState(0);
    const [processedFiles, setProcessedFiles] = useState([]);

    const handleUploadSuccess = () => {
        setRefreshGallery(prev => prev + 1);
    };

    const handleImageSelect = (image) => {
        setSelectedImage(image);
    };

    const addProcessedFile = (filename) => {
        setProcessedFiles(prev => [...prev, { filename }]);
    };

    return (
        <div className="App">
            <header className="app-header">
                <h1>🖼️ Image Preprocessing Platform</h1>
                <p>Upload, process, and download your images</p>
            </header>

            <main className="app-main">
                <section className="upload-section">
                    <h2>1. Upload Images</h2>
                    <ImageUpload onUploadSuccess={handleUploadSuccess} />
                </section>

                <section className="gallery-section">
                    <h2>2. Select Image</h2>
                    <ImageGallery 
                        key={refreshGallery}
                        onImageSelect={handleImageSelect}
                    />
                </section>

                {selectedImage && (
                    <>
                        <section className="processing-section">
                            <h2>3. Process Image</h2>
                            
                            <div className="processing-tabs">
                                <div className="tab-content">
                                    <h3>Manual Processing</h3>
                                    <ImageProcessor 
                                        filename={selectedImage.filename}
                                        onProcessComplete={addProcessedFile}
                                    />
                                </div>
                                
                                <div className="tab-content">
                                    <h3>Quick Presets</h3>
                                    <PresetProcessor 
                                        filename={selectedImage.filename}
                                        onProcessComplete={addProcessedFile}
                                    />
                                </div>
                            </div>
                        </section>

                        {processedFiles.length > 0 && (
                            <section className="download-section">
                                <h2>4. Download Results</h2>
                                <BatchDownload processedFiles={processedFiles} />
                            </section>
                        )}
                    </>
                )}
            </main>

            <footer className="app-footer">
                <p>Image Preprocessing Platform v1.0</p>
            </footer>
        </div>
    );
}

export default App;
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
    "error": "Error applying operation 'blur': kernel_size must be odd"
}

// Upload failed
{
    "error": "No files provided"
}

// Download failed
{
    "error": "None of the requested files were found",
    "missing": ["file1.jpg", "file2.jpg"]
}
```

### Frontend Error Handling Pattern

```javascript
const handleApiCall = async (url, options) => {
    try {
        const response = await fetch(url, options);
        
        // Check if response is ok
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return { success: true, data };
        
    } catch (error) {
        console.error('API Error:', error);
        
        // Show user-friendly error message
        alert(`⚠️ Error: ${error.message}`);
        
        return { success: false, error: error.message };
    }
};

// Usage
const result = await handleApiCall('http://localhost:5000/api/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ filename: 'test.jpg', operation: 'grayscale' })
});

if (result.success) {
    console.log('Processing successful:', result.data);
} else {
    console.error('Processing failed:', result.error);
}
```

---

## 🔧 Development Tips

### 1. CORS Configuration
- Backend automatically handles CORS for `http://localhost:3000`
- No additional configuration needed for local development

### 2. File Validation
- **Supported formats**: JPG, PNG, BMP, TIFF
- **Max file size**: Configurable in backend settings
- Backend validates file types automatically

### 3. File Naming Convention
- Processed files get automatic suffixes
- Format: `{original_name}_{operation}_{params}.{ext}`
- Example: `photo_blur_gaussian_k15.jpg`

### 4. Image Display
```javascript
// Always use full URL for images
const imageUrl = `http://localhost:5000/api/image/${filename}`;

// Add error handling
<img 
    src={imageUrl}
    alt={filename}
    onError={(e) => {
        e.target.src = '/placeholder.png';
        console.error('Failed to load image:', filename);
    }}
/>
```

### 5. Performance Tips
- Use `loading="lazy"` for gallery images
- Implement pagination for large galleries
- Use preview endpoint for real-time adjustments
- Cache processed images in state

### 6. Testing with cURL

```bash
# Upload image
curl -X POST http://localhost:5000/api/upload \
  -F "files=@image.jpg"

# Process image
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"filename":"image.jpg","operation":"grayscale","parameters":{}}'

# Get gallery
curl http://localhost:5000/api/gallery

# Download processed image
curl -O http://localhost:5000/api/download/single/image_grayscale.jpg
```

---

## 📊 API Response Status Codes

| Code | Meaning | When It Occurs |
|------|---------|----------------|
| 200 | Success | Operation completed successfully |
| 400 | Bad Request | Invalid parameters or missing required fields |
| 404 | Not Found | Image or resource doesn't exist |
| 500 | Server Error | Internal processing error |

---

## 🎯 Quick Reference: Common Workflows

### Workflow 1: Upload and Process
```javascript
// 1. Upload
const formData = new FormData();
formData.append('files', file);
const uploadResult = await fetch('http://localhost:5000/api/upload', {
    method: 'POST',
    body: formData
});
const { successful_uploads } = await uploadResult.json();
const filename = successful_uploads[0].filename;

// 2. Process
const processResult = await fetch('http://localhost:5000/api/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        filename,
        operation: 'grayscale',
        parameters: {}
    })
});
const { output_file } = await processResult.json();

// 3. Download
window.location.href = `http://localhost:5000/api/download/single/${output_file}`;
```

### Workflow 2: Preview Before Processing
```javascript
// 1. Get preview
const preview = await fetch('http://localhost:5000/api/preview', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        filename: 'photo.jpg',
        operation: 'blur',
        params: { kernel: 15 }
    })
});
const { preview: base64Image } = await preview.json();

// 2. Show preview to user
document.getElementById('preview').src = base64Image;

// 3. If user likes it, apply for real
const process = await fetch('http://localhost:5000/api/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        filename: 'photo.jpg',
        operation: 'blur_gaussian',
        parameters: { kernel_size: 15 }
    })
});
```

### Workflow 3: Batch Processing with Presets
```javascript
// 1. Get available presets
const presetsRes = await fetch('http://localhost:5000/api/presets');
const presets = await presetsRes.json();

// 2. Apply preset
const result = await fetch('http://localhost:5000/api/preset/apply', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        filename: 'photo.jpg',
        preset: 'enhance_contrast'
    })
});

// 3. Download result
const { processed_image } = await result.json();
window.location.href = `http://localhost:5000/api/download/single/${processed_image}`;
```

---

## 🐛 Troubleshooting

### Issue: "File not found" error
**Solution:** Verify the filename exactly matches what's in the gallery. Use `/api/gallery` to get the correct filename.

### Issue: Preview not showing
**Solution:** Check that the response contains `success: true` and a valid base64 string starting with `data:image/png;base64,`

### Issue: CORS errors
**Solution:** Ensure backend is running and CORS is enabled. Check backend console for CORS configuration.

### Issue: Processing takes too long
**Solution:** Use the preview endpoint for quick feedback. Only process when user confirms they want to save.

### Issue: Download not starting
**Solution:** Use `window.location.href` for downloads, not `fetch()`. Fetch doesn't trigger browser downloads.

---

## 📚 Additional Resources

- **Backend Architecture**: Clean separation of routes, services, and utilities
- **Folder Structure**: `uploads/` for originals, `processed/` for results
- **Extensibility**: Easy to add new operations in `ProcessingService`
- **State Management**: Consider using Redux or Context API for complex apps

---

## ✅ Checklist for Frontend Integration

- [ ] Backend running on port 5000
- [ ] CORS enabled for your frontend URL
- [ ] File upload component with multi-file support
- [ ] Gallery component with image list
- [ ] Processing component with operation selection
- [ ] Parameter controls for operations
- [ ] Preview functionality
- [ ] Download buttons (single and batch)
- [ ] Error handling for all API calls
- [ ] Loading states during async operations
- [ ] Responsive design for mobile devices

---

**Happy coding! 🚀**
