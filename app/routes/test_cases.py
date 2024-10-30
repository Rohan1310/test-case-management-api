from flask import Blueprint, abort, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from app.services.test_case_service import TestCaseService
import os
import time
import uuid

bp = Blueprint('test_cases', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/test-cases', methods=['GET'])
def get_test_cases():
    module_id = request.args.get('module_id')
    test_case_service = TestCaseService()
    test_cases = test_case_service.get_test_cases(module_id)
    return jsonify(test_cases), 200

@bp.route('/test-cases', methods=['POST'])
def create_test_case():
    data = request.form.to_dict()
    files = request.files.getlist('attachments')

    attachment_filenames = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{uuid.uuid4().hex}{ext}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            file.save(file_path)
            attachment_filenames.append(filename)

    data['attachments'] = attachment_filenames 
    data['description'] = data.get('description') or 'N/A'

    test_case_service = TestCaseService()
    result = test_case_service.create_test_case(data)
    return jsonify(result), 201

@bp.route('/test-cases/<int:test_case_id>', methods=['PUT'])
def update_test_case(test_case_id):
    existing_attachments = request.form.getlist('existing_attachments') or []
    files = request.files.getlist('attachments')
    
    attachment_filenames = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{uuid.uuid4().hex}{ext}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            file.save(file_path)
            attachment_filenames.append(filename)

    data = {
        'module_id': request.form.get('module_id'),
        'summary': request.form.get('summary'),
        'description': request.form.get('description') or 'N/A',
        'attachments': existing_attachments + attachment_filenames 
    }

    test_case_service = TestCaseService()
    result = test_case_service.update_test_case(test_case_id, data)
    return jsonify(result), 200

@bp.route('/test-cases/<int:test_case_id>', methods=['DELETE'])
def delete_test_case(test_case_id):
    test_case_service = TestCaseService()
    result = test_case_service.delete_test_case(test_case_id)
    return jsonify(result), 200

@bp.route('/test-cases/attachments/<filename>', methods=['GET'])
def get_attachments(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(file_path):
        abort(404)  # Return a 404 error if the file does not exist
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)