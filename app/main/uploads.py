import os
from flask import request, current_app
from werkzeug.utils import secure_filename
from app.errors import bad_request
from app.main import main

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_FILE_EXTENSIONS']

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return bad_request('No file part')
    file = request.files['file']
    if file.filename == '':
        return bad_request('No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return {'success': 'your file is uploaded'}, 201