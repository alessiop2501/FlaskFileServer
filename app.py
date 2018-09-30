import os
from os import listdir
from os.path import isfile, join
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = dir_path + '\\downloads'

@app.route('/', methods=['GET'])
def index():
	files = [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]
	return render_template('index.html', files=files)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
	return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename, as_attachment=True)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
		return redirect(url_for('index'))
	else:
		return render_template('upload.html')

if __name__ == '__main__':
	app.run(debug=True)