from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from flask_user import current_user
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,TextAreaField,
                    IntegerField,FloatField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,NumberRange
from gestionEtd.models.Etudiant import Etudiant
from gestionEtd.models.Niveau import Niveau
from gestionEtd.models.Semestre import Semestre
from gestionEtd.models.Module import Module
from gestionEtd.models.Matiere import Matiere


def etudiant_niveau_choices():      
    return Etudiant.query

def niveau_choices():      
    return Niveau.query

def semestre_choices():      
    return Semestre.query

def module_choices():      
    return Module.query


def matiere_choices():      
    return Matiere.query


class RegistrationForm(FlaskForm):
    nom = StringField('Nom',validators=[DataRequired(),Length(min=2,max=50)])
    prenom = StringField('Prenom',validators=[DataRequired(),Length(min=2,max=50)])
    cin = IntegerField('Cin', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    spec = StringField('Specialite',validators=[DataRequired(),Length(min=2,max=20)])
    niv = StringField('Niveau',validators=[DataRequired(),Length(min=2,max=20)])
    submit = SubmitField('Add student')


    def validate_email(self,email):
        email = Etudiant.query.filter_by(email=email.data).first()
        if email: 
            raise ValidationError('That email is taken, please choose another email!')
    
    def validate_cin(self,cin):
        if not ( len(str(cin.data)) == 8):    
            raise ValidationError('Cin must be 8 digits')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    nom = StringField('Nom',validators=[DataRequired(),Length(min=2,max=20)])
    prenom = StringField('Prenom',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Update')
    picture = FileField('Update Profile picture',validators=[FileAllowed(['jpg','png'])])

    def validate_email(self,email):
        if email.data != current_user.email:
            email = Etudiant.query.filter_by(email=email.data).first()
            if email: 
                raise ValidationError('That email is taken, please choose another email!')


class UpdateEtudiantForm(FlaskForm):
    nom = StringField('Nom',validators=[DataRequired(),Length(min=2,max=50)])
    prenom = StringField('Prenom',validators=[DataRequired(),Length(min=2,max=50)])
    cin = IntegerField('Cin', validators=[DataRequired(),NumberRange(min=8, max=8)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    spec = StringField('Specialite',validators=[DataRequired(),Length(min=2,max=20)])
    niv = StringField('Niveau',validators=[DataRequired(),Length(min=2,max=20)])
    submit = SubmitField('Update Etudiant')

    def validate_email_check(self,email,cin):
        etd = Etudiant.query.filter_by(cin=cin.data).first()
        if email.data != etd.email:
            email = Etudiant.query.filter_by(email=email.data).first()
            if email: 
                raise ValidationError('That email is taken, please choose another email!')

class RequestResetForm(FlaskForm):   
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')


    def validate_email(self,email):
        etudiant = Etudiant.query.filter_by(email=email.data).first()
        if etudiant is None: 
            raise ValidationError('There is no account with that email')

class RestPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset password')

class NiveauForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    submit = SubmitField('Add Niveau')


class SpecForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    submit = SubmitField('Add Specialite')

class SemestreForm(FlaskForm):
    num = IntegerField('Numero Semestre', validators=[DataRequired()])
    coef = FloatField('Coefficient Semestre', validators=[DataRequired()])
    niveau = QuerySelectField('Niveau',validators=[DataRequired()],query_factory=niveau_choices)
    submit = SubmitField('Add Semestre')

class ModuleForm(FlaskForm):
    nom = StringField('Nom Module', validators=[DataRequired()])
    coef = FloatField('Coefficient Module', validators=[DataRequired()])
    # semestre = QuerySelectField('Semestre',validators=[DataRequired()],query_factory=semestre_choices)
    submit = SubmitField('Add Module')

class MatiereForm(FlaskForm):
    nom = StringField('Nom Matiere', validators=[DataRequired()])
    coef = FloatField('Coefficient Matiere', validators=[DataRequired()])
    # module = QuerySelectField('Module',validators=[DataRequired()],query_factory=module_choices)
    submit = SubmitField('Add Matiere')




class NoteForm(FlaskForm):
    nom = StringField('Name',validators=[DataRequired()])
    valeur = FloatField('Valeur', validators=[DataRequired()])
    coef = FloatField('Coefficient Note', validators=[DataRequired()])
    etudiant = QuerySelectField('Etudiant',validators=[DataRequired()],query_factory=etudiant_niveau_choices)

    ## only matiere is necessary 
    # niveau = QuerySelectField('Niveau',validators=[DataRequired()],query_factory=niveau_choices)
    # semestre = QuerySelectField('Niveau',validators=[DataRequired()],query_factory=semestre_choices)
    submit = SubmitField('Add Note')



