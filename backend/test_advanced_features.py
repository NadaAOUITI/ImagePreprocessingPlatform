import requests
import json
import os
from pathlib import Path

BASE_URL = "http://localhost:5000/api"


def print_header(title):
    print("\n" + "=" * 60)
    print(f"🧪 {title}")
    print("=" * 60)


def test_server_status():
    """Test if server is running"""
    print_header("Testing Server Status")
    try:
        response = requests.get("http://localhost:5000/")
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Server not responding: {e}")
        return False


def test_health_check():
    """Test health check endpoint"""
    print_header("Testing Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error:  {e}")


def test_upload_image():
    """Test image upload"""
    print_header("Testing Image Upload")

    # Create a test image if it doesn't exist
    test_image_path = "test_image.jpg"

    if not os.path.exists(test_image_path):
        print("📝 Creating test image...")
        import cv2
        import numpy as np

        # Create a simple test image (blue square)
        img = np.zeros((300, 300, 3), dtype=np.uint8)
        img[:, :] = (255, 0, 0)  # Blue
        cv2.rectangle(img, (50, 50), (250, 250), (0, 255, 0), -1)  # Green square
        cv2.circle(img, (150, 150), 50, (0, 0, 255), -1)  # Red circle
        cv2.imwrite(test_image_path, img)
        print(f"✅ Test image created: {test_image_path}")

    try:
        with open(test_image_path, 'rb') as f:
            files = {'files': (test_image_path, f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/upload", files=files)

        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            data = response.json()

            # ✨ FIX: Extraire le nom de fichier depuis successful_uploads
            if data.get('successful_uploads') and len(data['successful_uploads']) > 0:
                filename = data['successful_uploads'][0].get('filename')
                print(f"✅ Uploaded filename: {filename}")
                return filename
            elif data.get('filename'):
                return data.get('filename')

    except Exception as e:
        print(f"❌ Error:  {e}")

    return None
def test_gallery():
    """Test gallery endpoint"""
    print_header("Testing Gallery")
    try:
        response = requests.get(f"{BASE_URL}/gallery")
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"📄 Found {len(data.get('images', []))} images")
        if data.get('images'):
            print(f"   First image: {data['images'][0]}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_histogram(filename):
    """Test histogram generation"""
    print_header("Testing Histogram Generation")

    if not filename:
        print("⚠️  No filename provided, skipping test")
        return

    channels = ['all', 'r', 'g', 'b', 'gray']

    for channel in channels:
        try:
            response = requests.get(f"{BASE_URL}/histogram/{filename}?channel={channel}")
            print(f"\n📊 Channel: {channel}")
            print(f"✅ Status Code:  {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   Width: {data.get('width')}")
                print(f"   Height: {data.get('height')}")
                print(f"   Channels: {data.get('channels')}")
                print(f"   Histogram keys: {list(data.get('histogram', {}).keys())}")
        except Exception as e:
            print(f"❌ Error for channel {channel}: {e}")


def test_preview(filename):
    """Test real-time preview"""
    print_header("Testing Real-time Preview")

    if not filename:
        print("⚠️  No filename provided, skipping test")
        return

    operations = [
        {
            'operation': 'grayscale',
            'params': {}
        },
        {
            'operation': 'blur',
            'params': {'kernel': 5}
        },
        {
            'operation': 'sharpen',
            'params': {'strength': 1.5}
        }
    ]

    for op in operations:
        try:
            payload = {
                'filename': filename,
                'operation': op['operation'],
                'params': op['params']
            }
            response = requests.post(f"{BASE_URL}/preview", json=payload)
            print(f"\n🔍 Operation: {op['operation']}")
            print(f"✅ Status Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                preview_length = len(data.get('preview', ''))
                print(f"   Preview data length: {preview_length} characters")
                print(f"   Success: {data.get('success')}")
        except Exception as e:
            print(f"❌ Error for {op['operation']}: {e}")


def test_roi_detection(filename):
    """Test ROI detection"""
    print_header("Testing ROI Detection")

    if not filename:
        print("⚠️  No filename provided, skipping test")
        return

    roi_types = ['faces', 'contours']

    for roi_type in roi_types:
        try:
            payload = {
                'filename': filename,
                'type': roi_type
            }
            response = requests.post(f"{BASE_URL}/roi/detect", json=payload)
            print(f"\n🎯 ROI Type: {roi_type}")
            print(f"✅ Status Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                regions = data.get('regions', [])
                print(f"   Found {len(regions)} regions")
                for i, region in enumerate(regions[: 3]):  # Show first 3
                    print(f"   Region {i + 1}: {region}")
        except Exception as e:
            print(f"❌ Error for {roi_type}: {e}")


def test_presets():
    """Test preset listing"""
    print_header("Testing Presets List")
    try:
        response = requests.get(f"{BASE_URL}/presets")
        print(f"✅ Status Code: {response.status_code}")

        if response.status_code == 200:
            presets = response.json()
            print(f"📄 Available presets: {len(presets)}")
            for key, preset in presets.items():
                print(f"\n   🎨 {key}:")
                print(f"      Name: {preset['name']}")
                print(f"      Operations: {len(preset['operations'])}")
                for op in preset['operations']:
                    print(f"         - {op['type']}:  {op['params']}")
    except Exception as e:
        print(f"❌ Error:  {e}")


def test_apply_preset(filename):
    """Test applying a preset"""
    print_header("Testing Apply Preset")

    if not filename:
        print("⚠️  No filename provided, skipping test")
        return

    presets_to_test = ['enhance_contrast', 'edge_detection', 'denoise', 'black_white']

    for preset in presets_to_test:
        try:
            payload = {
                'filename': filename,
                'preset': preset
            }
            response = requests.post(f"{BASE_URL}/preset/apply", json=payload)
            print(f"\n🎨 Preset:  {preset}")
            print(f"✅ Status Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   Processed image:  {data.get('processed_image')}")
                print(f"   Success: {data.get('success')}")
        except Exception as e:
            print(f"❌ Error for {preset}:  {e}")
def test_contrast_brightness_preview(filename):
    """Test contrast & brightness preview"""
    print_header("Testing Contrast & Brightness Preview")

    if not filename:
        print("⚠️  No filename provided, skipping test")
        return

    payload = {
        'filename': filename,
        'operation': 'contrast_brightness',
        'params': {
            'contrast': 1.4,
            'brightness': 30
        }
    }

    try:
        response = requests.post(f"{BASE_URL}/preview", json=payload)
        print(f"✅ Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"   Preview length: {len(data.get('preview', ''))}")
            print(f"   Success: {data.get('success')}")
        else:
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


def run_all_tests():
    """Run all tests"""
    print("\n" + "🚀" * 30)
    print("STARTING COMPREHENSIVE BACKEND TESTS")
    print("🚀" * 30)

    # Test server status
    if not test_server_status():
        print("\n❌ Server is not running. Please start the server first!")
        print("   Run: python backend/app.py")
        return

    # Test health check
    test_health_check()

    # Test gallery
    test_gallery()

    # Test upload and get filename
    filename = test_upload_image()

    if filename:
        # Test advanced features with uploaded image
        test_histogram(filename)
        test_preview(filename)
        test_roi_detection(filename)
        test_presets()
        test_apply_preset(filename)
        test_contrast_brightness_preview(filename)

    else:
        print("\n⚠️  Upload failed, skipping tests that require an image")

    print("\n" + "✅" * 30)
    print("ALL TESTS COMPLETED")
    print("✅" * 30 + "\n")


if __name__ == "__main__":
    run_all_tests()