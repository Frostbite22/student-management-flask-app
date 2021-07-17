from gestionEtd import app, db 

class Note(db.Model):
    __table__name = 'note'

    id_Note = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    valeur = db.Column(db.Float, nullable=False)
    coef_note = db.Column(db.Float, nullable=False)
    id_matiere = db.Column(db.Integer, db.ForeignKey('matiere.id'),
        nullable=False)

    ## static method moyenne matiere 

    
