from app.models import Module
from app import db

class ModuleService:
    def get_all_modules(self):
        modules = Module.query.order_by(Module.order).all()
        return [self._serialize_module(module) for module in modules]

    def create_module(self, data):
        new_module = Module(
            name=data['name'],
            parent_id=data.get('parent_id'),
            order=self._get_next_order(data.get('parent_id'))
        )
        db.session.add(new_module)
        db.session.commit()
        return self._serialize_module(new_module)

    def update_module(self, module_id, data):
        module = Module.query.get(module_id)
        if not module:
            return {'success': False, 'message': 'Module not found'}
        
        module.name = data.get('name', module.name)
        module.parent_id = data.get('parent_id', module.parent_id)
        db.session.commit()
        return self._serialize_module(module)

    def delete_module(self, module_id):
        module = Module.query.get(module_id)
        if not module:
            return {'success': False, 'message': 'Module not found'}
        
        db.session.delete(module)
        db.session.commit()
        return {'success': True, 'message': 'Module deleted successfully'}

    def reorder_modules(self, data):
        for item in data:
            module = Module.query.get(item['id'])
            if module:
                module.parent_id = item.get('parent_id')
                module.order = item['order']
        db.session.commit()
        return {'success': True, 'message': 'Modules reordered successfully'}

    def _serialize_module(self, module):
        return {
            'id': module.id,
            'name': module.name,
            'parent_id': module.parent_id,
            'order': module.order
        }

    def _get_next_order(self, parent_id):
        last_module = Module.query.filter_by(parent_id=parent_id).order_by(Module.order.desc()).first()
        return (last_module.order + 1) if last_module else 1