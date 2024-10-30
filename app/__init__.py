from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_session import Session
from config import UPLOAD_FOLDER, Config
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
oauth = OAuth()
server_session = Session()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Configure server-side session
    app.config['SESSION_TYPE'] = 'filesystem'
    server_session.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True)
    jwt.init_app(app)
    oauth.init_app(app)

    # Set up Google OAuth
    oauth.register(
        name='google',
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

    from app.routes import auth, modules, test_cases
    app.register_blueprint(auth.bp)
    app.register_blueprint(modules.bp)
    app.register_blueprint(test_cases.bp)

    return app