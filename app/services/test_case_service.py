from app.models import TestCase
from app import db

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
            description=data.get('description'),
            attachment=data.get('attachment')
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
        test_case.description = data.get('description', test_case.description)
        test_case.attachment = data.get('attachment', test_case.attachment)
        db.session.commit()
        return self._serialize_test_case(test_case)

    def delete_test_case(self, test_case_id):
        test_case = TestCase.query.get(test_case_id)
        if not test_case:
            return {'success': False, 'message': 'Test case not found'}
        
        db.session.delete(test_case)
        db.session.commit()
        return {'success': True, 'message': 'Test case deleted successfully'}

    def _serialize_test_case(self, test_case):
        return {
            'id': test_case.id,
            'module_id': test_case.module_id,
            'summary': test_case.summary,
            'description': test_case.description,
            'attachment': test_case.attachment
        }