from gestionEtd import app, db 
from gestionEtd.models.User import User
from gestionEtd import db, app ,login_manager
from flask_login import UserMixin,current_user


# @login_manager.user_loader
# def load_user(user_id):
#     return Administrateur.query.get(int(user_id))


class Administrateur(User):
    __table__name = 'administrateur'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }


    def __repr__(self):
        return f"Admin('{self.nom}','{self.prenom}','{self.email}')"



