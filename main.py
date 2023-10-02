
import os
import json
from flask import Flask,render_template,request,send_file
from werkzeug.utils import secure_filename
import assets
from io import BytesIO

app = Flask(__name__, template_folder='./templates')

# TEMP FILE PATH
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'tmp')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home Page

@app.route('/',methods=['GET'])
def home():
    count = assets.count_files_in_directory(app.config['UPLOAD_FOLDER'])
    if count > 10:
        status = assets.delete_files_in_directory(app.config['UPLOAD_FOLDER'])

    return render_template('home.html')

# Download File

@app.route('/download/<id>')
def download(id):
    try:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], id),'rb') as file:
                        jsondata = file.read()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], id))
        return send_file(BytesIO(jsondata),download_name=id,as_attachment=True)
    
    except:
        return  render_template('error.html',fail='You can only download it once! Re Encrypt / Decrypt the file.')

# JSON

@app.route('/json', methods=['GET'])
def json():
    return render_template('json.html')

@app.route('/jsonEncrypt',methods=['GET','POST'])
def jsonEncrypt():
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
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return render_template('error.html',fail='Invalid JSON Format')
        
        enc_data = assets.encrypt(key,jsondata)
        f = request.files['jsonfile']
        if f.filename == '':
            output_file_name = 'encJSON-'+assets.string_generator()+'.json'
        else:
            output_file_name = secure_filename(f.filename)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], output_file_name),'wb') as file:
            file.write(enc_data)
        return render_template('jsonencrypt_success.html',file_name=output_file_name,key=key)
                
    return render_template('jsonencrypt.html')


@app.route('/jsonDecrypt',methods=['GET','POST'])
def jsonDecrypt():
    if request.method == 'POST':
        key = request.values.get('key')
        jsondata = request.values.get('jsonarea')
        if jsondata == '':
            if 'encfile' in request.files:
                f = request.files['encfile']
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                with open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)),'rb') as file:
                    jsondata = file.read()
        else:
            jsondata = bytes(jsondata,'utf-8')

        try:
            json.loads(jsondata)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return render_template('error.html',fail='Input is already in JSON Format!')
        except:
            
            try:
                dec_data = assets.decrypt(key,jsondata)
            except:
                return render_template('error.html',fail='Incorrect Decryption Key')
            f = request.files['encfile']
            if f.filename == '':
                output_file_name = 'decJSON-'+assets.string_generator()+'.json'
            else:
                output_file_name = secure_filename(f.filename)
            with open(os.path.join(app.config['UPLOAD_FOLDER'], output_file_name),'wb') as file:
                file.write(dec_data)
            return render_template('jsondecrypt_success.html',file_name=output_file_name,key=key)
        
    return render_template('jsondecrypt.html')


# Text


@app.route('/text', methods=['GET'])
def text():
    return render_template('text.html')

@app.route('/textEncrypt',methods=['GET','POST'])
def textEncrypt():
    if request.method == 'POST':
        key = request.values.get('key')
        textdata = request.values.get('textarea')
        if textdata == '':
            if 'textfile' in request.files:
                f = request.files['textfile']
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                with open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)),'rb') as file:
                    textdata = file.read()
        else:
            textdata = bytes(textdata,'utf-8')

        
        enc_data = assets.encrypt(key,textdata)
        f = request.files['textfile']
        if f.filename == '':
            output_file_name = 'encTxt-'+assets.string_generator()+'.txt'
        else:
            output_file_name = secure_filename(f.filename)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], output_file_name),'wb') as file:
            file.write(enc_data)
        return render_template('textencrypt_success.html',file_name=output_file_name,key=key)
                
    return render_template('textencrypt.html')


@app.route('/textDecrypt',methods=['GET','POST'])
def textDecrypt():
    if request.method == 'POST':
        key = request.values.get('key')
        textdata = request.values.get('textarea')
        if textdata == '':
            if 'encfile' in request.files:
                f = request.files['encfile']
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                with open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)),'rb') as file:
                    textdata = file.read()
        else:
            textdata = bytes(textdata,'utf-8')

            
        try:
            dec_data = assets.decrypt(key,textdata)
        except:
            return render_template('error.html',fail='Incorrect Decryption Key')
        f = request.files['encfile']
        if f.filename == '':
            output_file_name = 'decTxt-'+assets.string_generator()+'.txt'
        else:
            output_file_name = secure_filename(f.filename)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], output_file_name),'wb') as file:
            file.write(dec_data)
        return render_template('textdecrypt_success.html',file_name=output_file_name,key=key)
    
    return render_template('textdecrypt.html')




if __name__ == '__main__':
    app.run(threaded=True,port=8000)