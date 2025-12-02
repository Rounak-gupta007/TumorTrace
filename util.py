import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import os

# Check if model file exists before loading
model_path = "VGG_model.h5"
if os.path.exists(model_path):
    saved_model = load_model(model_path)
else:
    saved_model = None
    print(f"Warning: Model file '{model_path}' not found. Predictions will not work.")


def check(input_img):
    if saved_model is None:
        # Return dummy output if model is not loaded
        return np.array([[0.5, 0.5]])
    
    img = load_img(input_img, target_size=(128, 128))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    output = saved_model.predict(img)    
    return output