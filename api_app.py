import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from util import check
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend to call backend

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH, 'static/upload/')

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_PATH, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'TumorTrace API is running'})

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_PATH, filename)
        file.save(filepath)
        
        # Get prediction
        result = check(filepath)
        classification = np.where(result == np.amax(result))[1][0]
        confidence = float(result[0][classification] * 100)
        
        # Determine result text
        if classification == 0:
            result_text = 'a Tumor'
        else:
            result_text = 'Not a Tumor'
        
        return jsonify({
            'success': True,
            'confidence': round(confidence, 2),
            'result': result_text,
            'message': f'{confidence:.2f}% Confidence - This is {result_text}'
        })
    
    return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, or JPEG'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
