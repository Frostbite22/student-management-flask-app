from gestionEtd import app, db 

class Niveau(db.Model):
    __table__name = 'niveau'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    nom_niv = db.Column(db.String(120),unique=True, nullable=False)
    etudiants = db.relationship('Etudiant',backref='niveau', lazy='dynamic')
    semestres = db.relationship('Semestre',backref='niveau', lazy='dynamic')

    
    def __repr__(self):
        return f"Niveau('{self.nom_niv}')"
