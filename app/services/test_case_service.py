from app.models import TestCase
from app import db
import os
from flask import current_app

class TestCaseService:
    def get_test_cases(self, module_id=None):
        query = TestCase.query
        if module_id:
            query = query.filter_by(module_id=module_id)
        test_cases = query.all()
        return [self._serialize_test_case(test_case) for test_case in test_cases]

    def create_test_case(self, data):
        new_test_case = TestCase(
            module_id=data['module_id'],
            summary=data['summary'],
            description=data.get('description', 'N/A'),
            attachments=data.get('attachments', []) 
        )
        db.session.add(new_test_case)
        db.session.commit()
        return self._serialize_test_case(new_test_case)

    def update_test_case(self, test_case_id, data):
        test_case = TestCase.query.get(test_case_id)
        if not test_case:
            return {'success': False, 'message': 'Test case not found'}
        
        test_case.module_id = data.get('module_id', test_case.module_id)
        test_case.summary = data.get('summary', test_case.summary)
        test_case.description = data.get('description', 'N/A')
        test_case.attachments = data['attachments']
        
        db.session.commit()
        return self._serialize_test_case(test_case)

    def delete_test_case(self, test_case_id):
        test_case = TestCase.query.get(test_case_id)
        if not test_case:
            return {'success': False, 'message': 'Test case not found'}
        
        if test_case.attachments:
            self._delete_attachments(test_case.attachments)
        
        db.session.delete(test_case)
        db.session.commit()
        return {'success': True, 'message': 'Test case deleted successfully'}

    def _serialize_test_case(self, test_case):
        return {
            'id': test_case.id,
            'module_id': test_case.module_id,
            'summary': test_case.summary,
            'description': test_case.description or 'N/A',
            'attachments': test_case.attachments
        }

    def _delete_attachments(self, attachments):
        for filename in attachments:
            if isinstance(filename, str):  # Ensure filename is a string
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(file_path):
                    os.remove(file_path)