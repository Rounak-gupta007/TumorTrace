import os
import numpy as np
from flask import Flask , render_template  , request 
from util import check

app = Flask(__name__,template_folder='templates')
BASE_PATH = os.getcwd()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')


def names(number):
    if number==0:
        return 'Its a Tumor'
    else:
        return 'No, Its not a tumor'




@app.route('/')
def home():
        return render_template("index.html")

@app.route('/predict')
def predict():
        return render_template("predict.html")

@app.route('/about')
def about():
        return render_template("about.html")

@app.route('/success' , methods = ['GET' , 'POST'])
def success():
    if request.method == 'POST':
            upload_file = request.files['file']
            filename = upload_file.filename
            path_save = os.path.join(UPLOAD_PATH,filename)
            upload_file.save(path_save)

            # Use the check function from util.py which loads VGG_model.h5
            res = check(path_save)
            classification = np.where(res == np.amax(res))[1][0]
            confidence = res[0][classification] * 100
            result_text = names(classification)
            text = f"{confidence:.2f}% Confidence This Is {result_text}"

            return render_template('success.html',img=filename,text_h=text)
    return render_template('index.html',upload=False)

if __name__ == "__main__":
    app.run(debug = True)
