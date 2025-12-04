import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import os
import gdown

# Model configuration
MODEL_PATH = "VGG_model.h5"
MODEL_URL = "https://drive.google.com/uc?id=1tlhLq5mckwAfvjxedOIjEnx21eUjX7MJ"

def download_model():
    """Download model from Google Drive if it doesn't exist"""
    if not os.path.exists(MODEL_PATH):
        print(f"Model file not found. Downloading from Google Drive...")
        try:
            gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
            print(f"Model downloaded successfully to {MODEL_PATH}")
        except Exception as e:
            print(f"Error downloading model: {e}")
            return False
    return True

# Download model if needed
download_model()

# Load the model
if os.path.exists(MODEL_PATH):
    print(f"Loading model from {MODEL_PATH}...")
    saved_model = load_model(MODEL_PATH)
    print("Model loaded successfully!")
else:
    saved_model = None
    print(f"Warning: Model file '{MODEL_PATH}' not found. Predictions will not work.")


def check(input_img):
    if saved_model is None:
        # Return dummy output if model is not loaded
        print("Warning: Model not loaded, returning dummy prediction")
        return np.array([[0.5, 0.5]])
    
    img = load_img(input_img, target_size=(128, 128))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    output = saved_model.predict(img)    
    return output
