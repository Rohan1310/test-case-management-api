from app.models import User
from app import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

class AuthService:
    def login(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return {'success': True, 'access_token': access_token, 'user': {'id': user.id, 'name': user.name, 'email': user.email}}
        return {'success': False, 'message': 'Invalid email or password'}

    @jwt_required
    def logout(self):
        # In a real-world scenario, you might want to blacklist the token
        return {'success': True, 'message': 'Logged out successfully'}