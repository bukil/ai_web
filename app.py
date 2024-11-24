from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

INVOKE_URL = "https://ai.api.nvidia.com/v1/vlm/nvidia/neva-22b"
API_KEY = "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"  # Replace with your NVIDIA API key

@app.route('/')
def serve_index():
    """Serve the index.html file."""
    return send_from_directory(app.static_folder, "index.html")

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        data = request.json
        image_b64 = data['image']

        # Check image size
        if len(image_b64) >= 180_000:
            return jsonify({"error": "Image too large. Use smaller images."}), 400

        # Prepare the request to NVIDIA API
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json"
        }

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": f'Describe what you see in this image. <img src="data:image/png;base64,{image_b64}" />'
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.20,
            "top_p": 0.70,
            "seed": 0,
            "stream": False
        }

        # Make the API request
        response = requests.post(INVOKE_URL, headers=headers, json=payload)
        response.raise_for_status()

        return jsonify({"result": response.json()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)