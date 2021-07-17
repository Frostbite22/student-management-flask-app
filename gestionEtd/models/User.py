from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from gestionEtd import db, app,login_manager
from flask_login import UserMixin, current_user
from functools import wraps
# from flask_user import roles_required, UserMixin, current_user

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User',backref='role', lazy='dynamic')
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model,UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    type = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        "polymorphic_on": type
    }




    def __repr__(self):
        return '<User %r>' % self.nom

