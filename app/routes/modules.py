from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import Module
from app import db

bp = Blueprint('modules', __name__, url_prefix='/api/modules')

@bp.route('', methods=['GET'])
@jwt_required()
def get_modules():
    modules = Module.query.order_by(Module.order).all()
    return jsonify([module.to_dict() for module in modules]), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_module():
    data = request.json
    new_module = Module(
        name=data['name'],
        parent_id=data.get('parent_id'),
        order=Module.query.count() + 1
    )
    db.session.add(new_module)
    db.session.commit()
    return jsonify(new_module.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_module(id):
    module = Module.query.get_or_404(id)
    data = request.json
    module.name = data.get('name', module.name)
    module.parent_id = data.get('parent_id', module.parent_id)
    db.session.commit()
    return jsonify(module.to_dict()), 200

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_module(id):
    module = Module.query.get_or_404(id)
    db.session.delete(module)
    db.session.commit()
    return '', 204

@bp.route('/reorder', methods=['POST'])
@jwt_required()
def reorder_modules():
    data = request.json
    for item in data:
        module = Module.query.get(item['id'])
        if module:
            module.parent_id = item.get('parent_id')
            module.order = item['order']
    db.session.commit()
    return jsonify({"message": "Modules reordered successfully"}), 200