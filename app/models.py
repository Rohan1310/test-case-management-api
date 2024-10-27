from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    order = db.Column(db.Integer, nullable=False)

    parent = db.relationship('Module', remote_side=[id], backref='children')

    # Add the to_dict method
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "order": self.order,
        }

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    attachment = db.Column(db.String(255))

    module = db.relationship('Module', backref='test_cases')