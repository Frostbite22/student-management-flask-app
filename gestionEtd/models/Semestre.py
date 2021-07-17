from gestionEtd import app, db 

class Semestre(db.Model):
    __table_args__ = {'extend_existing': True} 
    __table__name = 'semestre'
    id = db.Column(db.Integer, primary_key=True)
    num_semestre = db.Column(db.Integer, nullable=False)
    coef_semestre = db.Column(db.Float, nullable=False)
    id_niv = db.Column(db.Integer, db.ForeignKey('niveau.id'),
        nullable=False)
    modules = db.relationship('Module',backref='semestre', lazy='dynamic')

    
    def __repr__(self):
        return f"Semestre('{self.num_semestre}','{self.niveau}')"
    ## static method moyenne generale 

    
