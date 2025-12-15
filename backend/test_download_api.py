import requests
import os
import zipfile
import io

API_URL = "http://localhost:5000/api"
SAVE_DIR = "./test_downloads/"
os.makedirs(SAVE_DIR, exist_ok=True)


def test_single_download(filename):
    print(f"\n{'=' * 80}")
    print(f"TEST 1: Downloading single image: {filename}")
    print('=' * 80)

    # ✅ CORRECT URL: /api/download/single/<filename>
    url = f"{API_URL}/download/single/{filename}"
    print(f"GET {url}")

    try:
        resp = requests.get(url)
        print(f"Status code: {resp.status_code}")

        if resp.status_code == 200:
            outpath = os.path.join(SAVE_DIR, filename)
            with open(outpath, "wb") as f:
                f.write(resp.content)
            file_size = len(resp.content)
            print(f"✅ SUCCESS: Saved to {outpath} ({file_size} bytes)")
        else:
            print(f"❌ FAILED: {resp.status_code}")
            try:
                error = resp.json()
                print(f"   Error: {error}")
            except:
                print(f"   Response: {resp.text[:200]}")
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")


def test_batch_download(filenames):
    print(f"\n{'=' * 80}")
    print(f"TEST 2: Batch downloading {len(filenames)} files")
    print('=' * 80)
    print(f"Files: {filenames}")

    param = ",".join(filenames)
    # ✅ UPDATED: Changed to /download/batch endpoint
    url = f"{API_URL}/download/batch?files={param}"
    print(f"GET {url}")

    try:
        resp = requests.get(url)
        print(f"Status code: {resp.status_code}")

        if resp.status_code == 200:
            content_type = resp.headers.get("Content-Type", "")
            print(f"Content-Type: {content_type}")

            if content_type.startswith("application/zip"):
                z = zipfile.ZipFile(io.BytesIO(resp.content))
                members = z.namelist()
                z.extractall(SAVE_DIR)
                print(f"✅ SUCCESS: Extracted {len(members)} files to {SAVE_DIR}")
                for member in members:
                    print(f"   - {member}")
            else:
                print(f"❌ FAILED: Expected ZIP but got {content_type}")
                try:
                    error = resp.json()
                    print(f"   Error: {error}")
                except:
                    print(f"   Response: {resp.text[:200]}")
        else:
            print(f"❌ FAILED: {resp.status_code}")
            try:
                error = resp.json()
                print(f"   Error: {error}")
            except:
                print(f"   Response: {resp.text[:200]}")
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("IMAGE DOWNLOAD API TEST")
    print("=" * 80)

    # Use exact filenames from your 'processed' directory:
    single_filename = "test_image_89c5caa2_preset_black_white.jpg"
    batch_filenames = [
        "test_image_62ba43af_preset_black_white.jpg",
        "test_image_62ba43af_preset_denoise.jpg",
        "test_image_89c5caa2_preset_edge_detection.jpg"
    ]

    test_single_download(single_filename)
    test_batch_download(batch_filenames)

    print("\n" + "=" * 80)
    print("TESTS COMPLETED")
    print("=" * 80)