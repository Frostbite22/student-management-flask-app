from gestionEtd import app, db 

class Specialite(db.Model):
    __table_args__ = {'extend_existing': True} 
    __table__name = 'specialite'

    id = db.Column(db.Integer, primary_key=True)
    nom_specialite = db.Column(db.String(120),unique=True, nullable=False)
    etudiants = db.relationship('Etudiant',backref='specialite', lazy='dynamic')

    
