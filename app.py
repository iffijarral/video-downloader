from flask import Flask, request, jsonify
import yt_dlp as youtube_dl

import os

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.getenv("API_KEY")
PORT = 3000

@app.route("/")
def home():
    return "Video download app is running"

@app.before_request
def check_api_key():
    # Check the route path to apply the API key validation only for /download
    if request.path == "/download":
        key = request.headers.get("X-API-KEY")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 403

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()

    # Extract URL from request body
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Define the output path
    output_path = os.path.join(os.getcwd(), 'downloads', '%(title)s.%(ext)s')

    # Create the download directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    # Define youtube-dl options
    ydl_opts = {
        'outtmpl': output_path,  # Set output template
        'format': 'best',  # Download the best available format
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # Start downloading the video
        return jsonify({'message': 'Download started successfully!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=False)
