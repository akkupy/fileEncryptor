
import os
import json
from flask import Flask,render_template,request,send_file
from werkzeug.utils import secure_filename
import assets
from io import BytesIO

app = Flask(__name__, template_folder='./templates')

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'json')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/encrypt',methods=['GET','POST'])
def encrypt():
    if request.method == 'POST':
        key = request.values.get('key')
        jsondata = request.values.get('jsonarea')
        if jsondata == '':
            if 'jsonfile' in request.files:
                f = request.files['jsonfile']
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                with open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)),'rb') as file:
                    jsondata = file.read()
        else:
            jsondata = bytes(jsondata,'utf-8')

        try:
            json.loads(jsondata)
        except:
            return render_template('error.html',fail='Invalid JSON Format')
        
        enc_data = assets.encrypt(key,jsondata)
        f = request.files['jsonfile']
        if f.filename == '':
            output_file_name = 'encJSON-'+assets.string_generator()+'.json'
        else:
            output_file_name = f.filename
        with open(os.path.join(app.config['UPLOAD_FOLDER'], output_file_name),'wb') as file:
            file.write(enc_data)
        return render_template('encrypt_success.html',file_name=output_file_name,key=key)
                
    return render_template('encrypt.html')

@app.route('/download/<id>')
def download(id):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], id),'rb') as file:
                    jsondata = file.read()
    return send_file(BytesIO(jsondata),download_name=id,as_attachment=True)

@app.route('/decrypt',methods=['GET'])
def decrypt():
    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(threaded=True,port=8000)