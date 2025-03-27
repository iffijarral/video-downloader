import os
from flask import Flask, request, jsonify
import yt_dlp as youtube_dl

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return "Video download app is running"

@app.before_request
def check_api_key():
    if request.endpoint == "download_video":
        key = request.headers.get("X-API-KEY")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 403

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Use /tmp directory for downloads
    download_dir = "/tmp"
    output_path = os.path.join(download_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'message': 'Download completed!', 'path': output_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
