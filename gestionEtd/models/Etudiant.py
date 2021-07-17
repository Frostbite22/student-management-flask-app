from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from gestionEtd import db, app,login_manager
from gestionEtd.models.User import User
from flask_login import UserMixin,current_user



# @login_manager.user_loader
# def load_user(user_id):
#     return Etudiant.query.get(int(user_id))

class Etudiant(User):
    __table__name = 'etudiant'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    cin = db.Column(db.Integer,unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_niv = db.Column(db.Integer, db.ForeignKey('niveau.id'),
        nullable=False)
    id_specialite = db.Column(db.Integer, db.ForeignKey('specialite.id'),
        nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    __mapper_args__ = {
        'polymorphic_identity': 'etudiant'
    }



    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'etudiant_id':self.id}).decode('utf-8')
        
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['etudiant_id']
            print(user_id)
        except:
            return None
        return Etudiant.query.get(user_id)

    def __repr__(self):
        return f"Etudiant('{self.nom}','{self.email}','{self.id}','{self.role}','{self.image_file}')"



