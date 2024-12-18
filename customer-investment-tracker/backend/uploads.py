from flask import Blueprint, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import os

uploads = Blueprint('uploads', __name__)

photos = UploadSet('photos', IMAGES)
configure_uploads(uploads, photos)

@uploads.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join('static/uploads', filename))

    return jsonify({"msg": "File uploaded successfully", "filename": filename}), 200
