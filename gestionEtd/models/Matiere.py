from gestionEtd import app, db 

class Matiere(db.Model):
    __table__name = 'matiere'

    id = db.Column(db.Integer, primary_key=True)
    nom_matiere = db.Column(db.String(120), nullable=False)
    coef_matiere = db.Column(db.Integer,nullable=False)
    id_module = db.Column(db.Integer, db.ForeignKey('module.id'),
        nullable=False)
    notes = db.relationship('Note',backref='matiere', lazy='dynamic')


    ## static method moyenne module 

    
