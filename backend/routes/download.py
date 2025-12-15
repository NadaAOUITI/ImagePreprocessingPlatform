from flask import Blueprint, send_file, request, jsonify
import os
import zipfile
import io
from config.settings import Config

download_bp = Blueprint("download", __name__)

# Use the same PROCESSED_FOLDER path as defined in Config
PROCESSED_FOLDER = Config.PROCESSED_FOLDER

# Add this to verify the path on startup
print(f"[DOWNLOAD] PROCESSED_FOLDER: {PROCESSED_FOLDER}")
print(f"[DOWNLOAD] Folder exists: {os.path.exists(PROCESSED_FOLDER)}")
if os.path.exists(PROCESSED_FOLDER):
    files = os.listdir(PROCESSED_FOLDER)
    print(f"[DOWNLOAD] Files in folder: {len(files)}")
    if files:
        print(f"[DOWNLOAD] First 5 files: {files[:5]}")


def safe_filename(filename):
    """Prevent directory traversal attacks"""
    return os.path.basename(filename)


@download_bp.route("/download/batch", methods=["GET"])
def batch_download():
    """Download multiple files as a ZIP archive

    Usage: GET /api/download/batch?files=file1.jpg,file2.jpg,file3.jpg
    """
    print(f"\n[BATCH DOWNLOAD] Request received")

    files_param = request.args.get("files")
    if not files_param:
        return jsonify({"error": "No files specified. Use ?files=file1.jpg,file2.jpg"}), 400

    # Parse and sanitize filenames
    files = files_param.split(",")
    files = [safe_filename(fn.strip()) for fn in files if fn.strip()]

    if not files:
        return jsonify({"error": "No valid files specified"}), 400

    print(f"[BATCH DOWNLOAD] Requested {len(files)} files: {files}")

    # Create ZIP in memory
    memory_file = io.BytesIO()
    found_files = []
    missing_files = []

    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename in files:
            filepath = os.path.join(PROCESSED_FOLDER, filename)

            if os.path.isfile(filepath):
                zf.write(filepath, arcname=filename)
                found_files.append(filename)
                print(f"[BATCH DOWNLOAD] ✅ Added: {filename}")
            else:
                missing_files.append(filename)
                print(f"[BATCH DOWNLOAD] ❌ Missing: {filename}")

    # Return error if no files found
    if not found_files:
        return jsonify({
            "error": "None of the requested files were found",
            "missing": missing_files
        }), 404

    print(f"[BATCH DOWNLOAD] Success: {len(found_files)} files, {len(missing_files)} missing")

    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype="application/zip",
        download_name="images.zip",
        as_attachment=True,
    )


@download_bp.route("/download/single/<filename>", methods=["GET"])
def download_single(filename):
    """Download a single file

    Usage: GET /api/download/single/image.jpg
    """
    print(f"\n[SINGLE DOWNLOAD] Request received")

    filename = safe_filename(filename)
    filepath = os.path.join(PROCESSED_FOLDER, filename)

    print(f"[SINGLE DOWNLOAD] Requested: {filename}")
    print(f"[SINGLE DOWNLOAD] Full path: {filepath}")
    print(f"[SINGLE DOWNLOAD] File exists: {os.path.isfile(filepath)}")

    if not os.path.isfile(filepath):
        # Show available files for debugging
        if os.path.exists(PROCESSED_FOLDER):
            available = os.listdir(PROCESSED_FOLDER)[:10]
            print(f"[SINGLE DOWNLOAD] Available files (first 10): {available}")

        return jsonify({
            "error": f"File not found: {filename}",
            "path_checked": filepath
        }), 404

    print(f"[SINGLE DOWNLOAD] ✅ Sending file: {filename}")
    return send_file(filepath, as_attachment=True, download_name=filename)