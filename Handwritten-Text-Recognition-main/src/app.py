from flask import Flask, render_template, request
import main
import argparse
#import urllib.request
#from app import app
from main import infer
from main import FilePaths
from Model import Model
from Model import DecoderType
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C://Users//ahari//myenv//Include//Handwritten-Text-Recognition-main//src//uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key='htrs123!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])

def hello_word():
    print("hello world called")

    return render_template('main.html',prediction='please select image file')

@app.route('/', methods=['POST'])

def upload_file():
    print("upload file called")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            #return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else :
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #parser = argparse.ArgumentParser()
            #parser.add_argument('--dump', help='dump output of NN to CSV file(s)', action='store_true')
            #args = parser.parse_args()
            decoderType = DecoderType.BestPath
            model = Model(open(FilePaths.fnCharList).read(), decoderType, mustRestore=True)
            #print('before infer method')
            f=os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
            arec=infer(model, f)
            #print('from infer prediction')
            print(f)
            print(arec[0])
            return render_template('main.html',prediction='The text is "{}"'.format(arec[0]))




if __name__ == '_main_':
     app.run(port=3000, debug=True)