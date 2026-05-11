from flask import Flask, render_template, request, jsonify, send_from_directory,send_file
import sys
# from flask import Flask, render_template, request, jsonify, send_file
import requests
import os

# This logic handles paths for both regular Python and PyInstaller EXE
def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(".")

base_dir = get_base_path()

app = Flask(__name__, 
            static_folder=os.path.join(base_dir, 'static'),
            template_folder=os.path.join(base_dir, 'templates'))

BACKEND_URL = "http://127.0.0.1:8000"

@app.route('/')
def index():
    return render_template('index.html')

# New route to download the template
@app.route('/download-template')
def download_template():
    # Force the path to the static folder
    static_path = os.path.join(base_dir, 'static')
    filename = 'sample_template.xlsx'
    
    # Create the folder and a dummy file if it doesn't exist (Self-healing)
    if not os.path.exists(static_path):
        os.makedirs(static_path)
    
    file_full_path = os.path.join(static_path, filename)
    if not os.path.exists(file_full_path):
        return f"Template file missing at {file_full_path}. Please place the file there.", 404

    return send_from_directory(static_path, filename, as_attachment=True)

@app.route('/download-installer')
def download_installer():
    # Define the directory where your EXE is stored
    output_path = os.path.join(base_dir, 'Output')
    filename = 'WorkOnExcelRohitJainPro_Setup.exe'
    
    # Self-healing: Ensure directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    file_full_path = os.path.join(output_path, filename)
    
    # Check if the installer actually exists
    if not os.path.exists(file_full_path):
        return f"Installer missing at {file_full_path}. Please place the setup file there.", 404

    return send_from_directory(output_path, filename, as_attachment=True)
    
@app.route('/proxy-upload', methods=['POST'])
def proxy_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    files = {'file': (file.filename, file.stream, file.content_type)}
    try:
        r = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=60)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": f"Backend connection failed: {str(e)}"}), 503
        
        
@app.route('/download-file')
def download_file():
    # 1. Get the path from the URL query parameter
    file_path = request.args.get('path')
    
    if not file_path:
        return "No path provided", 400

    # 2. Convert to absolute path so the OS can find it
    # This handles the "exports/2026-05-09/file.xlsx" relative path correctly
    abs_path = os.path.abspath(file_path)

    if os.path.exists(abs_path):
        # 3. Get the original filename to show in the download tray
        original_name = os.path.basename(abs_path)
        return send_file(
            abs_path, 
            as_attachment=True, 
            download_name=original_name,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        return f"File not found at: {abs_path}", 404
        
if __name__ == '__main__':
    app.run(port=5000, debug=True)