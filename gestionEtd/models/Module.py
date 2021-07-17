from gestionEtd import app, db 

class Module(db.Model):
    __table__name = 'module'

    id = db.Column(db.Integer, primary_key=True)
    nom_module = db.Column(db.String(120), nullable=False)
    coef_module = db.Column(db.Integer, nullable=False)
    id_semestre = db.Column(db.Integer, db.ForeignKey('semestre.id'),
        nullable=False)
    matieres = db.relationship('Matiere',backref='module', lazy='dynamic')

    ## static method moyenne semestre
    
