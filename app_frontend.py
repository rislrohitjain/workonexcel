from flask import Flask, render_template, request, jsonify, send_from_directory,send_file
# from flask import Flask, render_template, request, jsonify, send_file
import requests
import os

app = Flask(__name__)
BACKEND_URL = "http://127.0.0.1:8000"

@app.route('/')
def index():
    return render_template('index.html')

# New route to download the template
@app.route('/download-template')
def download_template():
    return send_from_directory('static', 'sample_template.xlsx', as_attachment=True)

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