from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
BACKEND_URL = "http://127.0.0.1:8000"

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(port=5000, debug=True)