from flask import Blueprint, jsonify, request, url_for, current_app, redirect, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db, oauth
import urllib.parse
import json
import secrets

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login')
def login():
    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    session['oauth_nonce'] = nonce
    
    print("Session after setting state and nonce:", session)  # Debugging line
    
    redirect_uri = url_for('auth.authorized', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, state=state, nonce=nonce)

@bp.route('/logout')
@jwt_required()
def logout():
    session.pop('user', None)
    return jsonify({"message": "Successfully logged out"}), 200

@bp.route('/authorized')
def authorized():
    try:
        if request.args.get('state') != session.pop('oauth_state', None):
            return jsonify({"error": "Invalid state parameter"}), 401

        token = oauth.google.authorize_access_token()
        nonce = session.pop('oauth_nonce', None)
        user_info = oauth.google.parse_id_token(token, nonce=nonce)
    except Exception as e:
        return jsonify({"error": str(e)}), 401

    google_email = user_info['email']

    if not google_email.endswith('@gmail.com'):
        return jsonify({"error": "Only Gmail accounts are allowed"}), 401

    user = User.query.filter_by(email=google_email).first()
    if not user:
        user = User(email=google_email, name=user_info['name'])
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(identity=user.id)
    user_data = {"id": user.id, "name": user.name, "email": user.email}
    
    session['user'] = user_data

    print("Session after setting user data:", session)
    
    redirect_url = f"{current_app.config['FRONTEND_URL']}/login?token={access_token}&user={urllib.parse.quote(json.dumps(user_data))}"
    return redirect(redirect_url)

@bp.route('/user')
def get_user():
    print("Current session:", session)  # Debugging line
    user = session.get('user')
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User  not found"}), 404