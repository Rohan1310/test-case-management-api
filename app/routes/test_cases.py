from flask import Blueprint, request, jsonify
from app.services.test_case_service import TestCaseService

bp = Blueprint('test_cases', __name__, url_prefix='/api')

@bp.route('/test-cases', methods=['GET'])
def get_test_cases():
    module_id = request.args.get('module_id')
    test_case_service = TestCaseService()
    test_cases = test_case_service.get_test_cases(module_id)
    return jsonify(test_cases), 200

@bp.route('/test-cases', methods=['POST'])
def create_test_case():
    data = request.json
    test_case_service = TestCaseService()
    result = test_case_service.create_test_case(data)
    return jsonify(result), 201

@bp.route('/test-cases/<int:test_case_id>', methods=['PUT'])
def update_test_case(test_case_id):
    data = request.json
    test_case_service = TestCaseService()
    result = test_case_service.update_test_case(test_case_id, data)
    return jsonify(result), 200

@bp.route('/test-cases/<int:test_case_id>', methods=['DELETE'])
def delete_test_case(test_case_id):
    test_case_service = TestCaseService()
    result = test_case_service.delete_test_case(test_case_id)
    return jsonify(result), 200