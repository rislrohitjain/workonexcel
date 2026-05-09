from flask import Flask, render_template, request, jsonify, send_from_directory
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
    # Get the file path from the URL query string
    file_path = request.args.get('path')
    if not file_path or not os.path.exists(file_path):
        return "File not found", 404
    
    # Send the file to the user's computer
    return send_file(os.path.abspath(file_path), as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000, debug=True)