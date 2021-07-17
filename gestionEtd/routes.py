import secrets
import os
import pandas as pd
from PIL import Image
from flask import  render_template, url_for, flash, redirect,request,abort
from gestionEtd import app, db, bcrypt, mail
from gestionEtd.forms import (RegistrationForm,LoginForm, UpdateAccountForm, 
                             RequestResetForm, RestPasswordForm,UpdateEtudiantForm,
                             NiveauForm, SpecForm,NoteForm,SemestreForm,ModuleForm,
                             MatiereForm)

from gestionEtd.models.User import User, Role
from gestionEtd.models.Niveau import Niveau
from gestionEtd.models.Specialite import Specialite
from gestionEtd.models.Administrateur import Administrateur
from gestionEtd.models.Etudiant import Etudiant
from gestionEtd.models.Note import Note
from gestionEtd.models.Semestre import Semestre
from gestionEtd.models.Matiere import Matiere
from gestionEtd.models.Module import Module
from sqlalchemy import exc

from functools import partial, reduce



from flask_mail import Message  
from flask_login import login_user, current_user, logout_user, login_required 



# ## initialization 

# db.create_all()

# #create admin role : 
# admin_role = Role(name='admin')
# db.session.add(admin_role)
# db.session.commit()

# #create etudiant role ! 
# etudiant_role = Role(name='etudiant')
# db.session.add(etudiant_role)
# db.session.commit()


# # create Admin User 
# hashed_password = bcrypt.generate_password_hash("admin").decode('utf-8')
# admin = Administrateur(nom="admin",prenom="admin",email="admin@gmail.com",password=hashed_password)
# adminRole = Role.query.filter_by(name="admin").first()
# admin.role_id = adminRole.id
# db.session.add(admin)
# db.session.commit()


@app.route('/')
@app.route('/home')
@login_required
def home():
    if current_user.role.name =="admin":
        listeNiveau = Niveau.query.all()
        listeSpecialite = Specialite.query.all()
        listeSemestre = Semestre.query.all()
        return render_template('home.html',listeNiveau=listeNiveau,\
        listeSpecialite=listeSpecialite,listeSemestre=listeSemestre)
    return redirect(url_for('mesNotes'))

       
@app.route('/mesNotes')
@login_required
def mesNotes():
    etd_notes = (db.session.query(Etudiant,Niveau,Semestre,Module,Matiere,Note)\
    .join(Etudiant)\
    .join(Semestre)\
    .join(Module)\
    .join(Matiere)\
    .join(Note)\
    .filter(current_user.id==Etudiant.id)\
    ).all()

    my_columns = ["nom","prenom","matiere","nom_note","valeur_note","module","niveau","semestre"]
    datalist = []
    dataframe = pd.DataFrame(columns=my_columns)
    for i in range(0,len(etd_notes)):
        datalist.append([etd_notes[i]['Etudiant'].nom,
        etd_notes[i]['Etudiant'].prenom,
        etd_notes[i]['Matiere'].nom_matiere,
        etd_notes[i]['Note'].nom,
        etd_notes[i]['Note'].valeur,
        etd_notes[i]['Module'].nom_module,
        etd_notes[i]['Niveau'].nom_niv,
        etd_notes[i]['Semestre'].num_semestre])

    dataframe = pd.DataFrame(datalist,columns=my_columns)
    dataframe = dataframe.pivot(values=['valeur_note'],index=['nom','prenom','niveau'], columns=['semestre','module','matiere','nom_note'])
    return render_template('mes_notes.html',etd_record=dataframe)




@app.route('/about')
def about():
    return render_template('about.html',title='about')


@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("error login. Check email and password","danger")
    return render_template('login.html',title="Login",form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/addEtd',methods=['POST','GET'])
@login_required
def addEtudiant():
    if current_user.role.name =="admin":
        form = RegistrationForm()
        if form.validate_on_submit():
            try :
                niv = Niveau.query.filter_by(nom_niv=form.niv.data).first()
                print(niv.id)
            except:
                niv = Niveau(nom_niv=form.niv.data)
                db.session.add(niv)
                db.session.commit()
                print(niv.id)
            try :
                spec = Specialite.query.filter_by(nom_specialite=form.spec.data).first()
                print(spec.id)
            except:
                spec = Specialite(nom_specialite=form.spec.data)
                db.session.add(spec)
                db.session.commit()
                print(spec.id)
            random_hex = secrets.token_hex(8)
            hashed_password = bcrypt.generate_password_hash(random_hex).decode('utf-8')
            newEtd = Etudiant(nom=form.nom.data,prenom=form.prenom.data,cin=form.cin.data,email=form.email.data,id_niv=niv.id,id_specialite=spec.id,password=hashed_password)
            etudiantRole = Role.query.filter_by(name="etudiant").first()
            newEtd.role_id = etudiantRole.id
            db.session.add(newEtd)
            db.session.commit()
            send_reset_email(newEtd)
            flash(f'Student Account has been Created successfully!',"success")
            return redirect(url_for('etudiants'))
        return render_template('addEtd.html',title="Add student",form=form)
    return redirect(url_for('login'))


@app.route('/etudiants',methods=['POST','GET'])
@login_required
def etudiants():
    if current_user.role.name =="admin":
        if request.method == 'POST':
            dataframe = pd.read_excel(request.files.get('file'))
            for index,row in dataframe.iterrows():
                random_hex = secrets.token_hex(8)
                hashed_password = bcrypt.generate_password_hash(random_hex).decode('utf-8')
                try :
                    niv = Niveau.query.filter_by(nom_niveau=row['niveau']).first()
                    print(niv.nom_niv)
                except:
                    niv = Niveau(nom_niv=row['niveau'])
                    db.session.add(niv)
                    db.session.commit()
                    print(niv.nom_niv)
                try :
                    spec = Specialite.query.filter_by(nom_specialite=row['specialite']).first()
                    print(spec.nom_specialite)
                except:
                    spec = Specialite(nom_specialite=row['specialite'])
                    db.session.add(spec)
                    db.session.commit()
                    print(spec.nom_specialite)
                newEtd = Etudiant(nom=row['nom'],prenom=row['prenom'],email=row['email'],cin=row['cin'],id_niv=niv.id,id_specialite=spec.id,password=hashed_password)
                etudiantRole = Role.query.filter_by(name="etudiant").first()
                newEtd.role_id = etudiantRole.id
                db.session.add(newEtd)
                db.session.commit()
                send_reset_email(newEtd)
        listeEtudiants = Etudiant.query.all()
        return render_template('etudiants.html',title="Etudiants",listeEtudiants=listeEtudiants)
    return redirect(url_for('login'))

@app.route('/notes',methods=['POST','GET'])
@login_required
def addNotesEtudiant():
    if current_user.role.name =="admin":
        form = NoteForm()
        return render_template('add_note_etudiant.html',form=form)
    return redirect(url_for('login'))

    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext 
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account',methods=['POST','GET'])
@login_required
def account():
    if current_user.role.name =="etudiant":
        form = UpdateAccountForm() 
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.nom = form.nom.data 
            current_user.prenom = form.prenom.data 
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated','success')
            return redirect(url_for('account'))
        elif request.method=="GET":
            form.nom.data = current_user.nom 
            form.prenom.data = current_user.prenom 
            form.email.data =current_user.email 
        image_file = url_for('static',filename='profile_pics/'+ current_user.image_file )
        return render_template('account.html',title="Account",image_file=image_file,form=form)
    return redirect(url_for('login'))



@app.route("/niveau/new",methods=['POST','GET'])
@login_required
def addNiveau(): 
    if current_user.role.name =="admin":
        form = NiveauForm()
        if form.validate_on_submit():
            niv = Niveau(nom_niv=form.name.data)
            db.session.add(niv)
            db.session.commit()
            flash('Niveau has been created','success')
            return redirect(url_for('home'))
        return render_template('create_niv_spec.html',title="New Niveau",form=form)
    return redirect(url_for('login'))



@app.route("/niveau/<int:niveau_id>/delete",methods=['POST','GET'])
@login_required
def delete_niveau(niveau_id):
    if current_user.role.name =="admin":
        niv = Niveau.query.get_or_404(niveau_id)
        print(niv.etudiants)
        try :
            db.session.delete(niv)
            db.session.commit()
            flash('Niveau has been deleted','success')
        except:
            flash('Ce niveau admet des étudiants','danger')
            return redirect(url_for('home'))
        return redirect(url_for('home'))
    return redirect(url_for('login'))
  

@app.route("/semestre/new",methods=['POST','GET'])
@login_required
def addSemestre(): 
    if current_user.role.name =="admin":
        form = SemestreForm()
        if form.validate_on_submit():
            semestre = Semestre(num_semestre=form.num.data,coef_semestre=form.coef.data,id_niv=form.niveau.data.id)
            db.session.add(semestre)
            db.session.commit()
            flash('Semestre has been created','success')
            return redirect(url_for('home'))
        return render_template('create_semestre.html',title="New Semestre",form=form)
    return redirect(url_for('login'))

@app.route("/semestre/<int:semestre_id>/delete",methods=['POST','GET'])
@login_required
def delete_semestre(semestre_id):
    if current_user.role.name =="admin":
        semestre = Semestre.query.get_or_404(semestre_id)
        try :
            db.session.delete(semestre)
            db.session.commit()
            flash('Semestre has been deleted','success')
        except:
            flash('Ce semestre admet des modules','danger')
            return redirect(url_for('home'))
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/semestre/<int:semestre_id>",methods=['POST','GET'])
@login_required
def semestre(semestre_id):
    if current_user.role.name =="admin":
        semestre = Semestre.query.get_or_404(semestre_id)
        return render_template('semestre.html',title=semestre.niveau,listeModule=semestre.modules,semestre_id=semestre_id)
    return redirect(url_for('login'))


@app.route("/semestre/<int:semestre_id>/module/new",methods=['POST','GET'])
@login_required
def addModule(semestre_id): 
    if current_user.role.name =="admin":
        form = ModuleForm()
        if form.validate_on_submit():
            module = Module(nom_module=form.nom.data,coef_module=form.coef.data,id_semestre=semestre_id)
            db.session.add(module)
            db.session.commit()
            flash('Module has been created','success')
            return redirect(url_for('home'))
        return render_template('create_module.html',title="New Module",form=form)
    return redirect(url_for('login'))

@app.route("/module/<int:module_id>/delete",methods=['POST','GET'])
@login_required
def delete_module(module_id):
    if current_user.role.name =="admin":
        module = Module.query.get_or_404(module_id)
        try :
            db.session.delete(module)
            db.session.commit()
            flash('module has been deleted','success')
        except:
            flash('Ce module admet des matières','danger')
            return redirect(url_for('home'))
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/module/<int:module_id>",methods=['POST','GET'])
@login_required
def module(module_id):
    if current_user.role.name =="admin":
        module = Module.query.get_or_404(module_id)
        return render_template('module.html',title=module.semestre,listeMatiere=module.matieres,module_id=module_id)
    return redirect(url_for('login'))



@app.route("/module/<int:module_id>/matiere/new",methods=['POST','GET'])
@login_required
def addMatiere(module_id): 
    if current_user.role.name =="admin":
        form = MatiereForm()
        if form.validate_on_submit():
            matiere = Matiere(nom_matiere=form.nom.data,coef_matiere=form.coef.data,id_module=module_id)
            db.session.add(matiere)
            db.session.commit()
            flash('Matiere has been created','success')
            return redirect(url_for('module',module_id=module_id))
        return render_template('create_module.html',title="New Matiere",form=form)
    return redirect(url_for('login'))

@app.route("/matiere/<int:matiere_id>/delete",methods=['POST','GET'])
@login_required
def delete_matiere(matiere_id):
    if current_user.role.name =="admin":
        matiere = Matiere.query.get_or_404(matiere_id)
        module_id= matiere.module.id
        try :
            db.session.delete(matiere)
            db.session.commit()
            flash('matiere has been deleted','success')
        except:
            flash('Cette matiere admet à des notes','danger')
            return redirect(url_for('home'))
        return redirect(url_for('module',module_id=module_id))
    return redirect(url_for('login'))

@app.route("/matiere/<int:matiere_id>",methods=['POST','GET'])
@login_required
def matiere(matiere_id):
    if current_user.role.name =="admin":
        matiere = Matiere.query.get_or_404(matiere_id)
        return render_template('matiere.html',title=matiere.module,listeNote=matiere.notes,matiere_id=matiere_id)
    return redirect(url_for('login'))

@app.route("/matiere/<int:matiere_id>/note/new",methods=['POST','GET'])
@login_required
def addNote(matiere_id): 
    if current_user.role.name =="admin":
        form = NoteForm()
        matiere = Matiere.query.filter_by(id=matiere_id).first()
        if form.validate_on_submit():
            note = Note(nom=form.nom.data,valeur=form.valeur.data,coef_note=form.coef.data,id_matiere=matiere_id)
            db.session.add(note)
            db.session.commit()
            etd = form.etudiant.data
            etd.niveau.semestre = note.matiere.module.semestre
            etd.niveau.semestre.module = note.matiere.module
            etd.niveau.semestre.module.matiere = note.matiere
            etd.niveau.semestre.module.matiere.note = note 
            db.session.commit()

            flash('Note has been created for the student','success')
            return redirect(url_for('notes'))
        return render_template('create_note.html',title="New Note",form=form,niveau=matiere.module.semestre.niveau)
    return redirect(url_for('login'))

@app.route("/note/<int:note_id>/delete",methods=['POST','GET'])
@login_required
def delete_note(note_id):
    if current_user.role.name =="admin":
        note = Note.query.get_or_404(note_id)
        matiere_id= note.matiere.id
        try :
            db.session.delete(note)
            db.session.commit()
            flash('Note has been deleted','success')
        except:
            flash('Cette Note  est linked à des étudiants','danger')
            return redirect(url_for('home'))
        return redirect(url_for('matiere',matiere_id=matiere_id))
    return redirect(url_for('login'))


@app.route("/notes/",methods=['POST','GET'])
@login_required
def notes():
    if current_user.role.name =="admin":
        if request.method == 'POST':
            dataframe1 = pd.read_excel(request.files.get('file'))
            for index,row in dataframe1.iterrows():
                try :
                    etd = (db.session.query(Etudiant,Niveau,Semestre,Module,Matiere)\
                    .join(Etudiant)\
                    .join(Semestre)\
                    .join(Module)\
                    .join(Matiere)\
                    .filter(Etudiant.cin==row['cin'])\
                    .filter(Semestre.num_semestre==row['semestre'])\
                    .filter(Module.nom_module==row['module'])\
                    .filter(Matiere.nom_matiere==row['matiere'])\
                    ).first()
                    matiere = Matiere.query.filter_by(nom_matiere=row['matiere']).first() 
                    print(matiere.id)
                    note = Note(nom=row['nom_note'],valeur=row['valeur_note'],coef_note=row['valeur_note'],id_matiere=matiere.id)
                    db.session.add(note)
                    db.session.commit()
                    print(note.valeur)
                    etd.niveau.semestre.module.matiere.note = note 
                    db.session.commit()
                except:
                    pass

        etd_notes = (db.session.query(Etudiant,Niveau,Semestre,Module,Matiere,Note)\
        .join(Etudiant)\
        .join(Semestre)\
        .join(Module)\
        .join(Matiere)\
        .join(Note)\
        ).all()
        # .filter(Niveau.nom_niv==etd.niveau.nom_niv)\
        # .filter(Note.valeur==note.valeur)\
        my_columns = ["nom","prenom","matiere","nom_note","valeur_note","module","niveau","semestre"]
        datalist = []
        dataframe = pd.DataFrame(columns=my_columns)
        for i in range(0,len(etd_notes)):
            datalist.append([etd_notes[i]['Etudiant'].nom,
            etd_notes[i]['Etudiant'].prenom,
            etd_notes[i]['Matiere'].nom_matiere,
            etd_notes[i]['Note'].nom,
            etd_notes[i]['Note'].valeur,
            etd_notes[i]['Module'].nom_module,
            etd_notes[i]['Niveau'].nom_niv,
            etd_notes[i]['Semestre'].num_semestre])

        dataframe = pd.DataFrame(datalist,columns=my_columns)
        dataframe = dataframe.pivot(values=['valeur_note'],index=['nom','prenom','niveau'], columns=['semestre','module','matiere','nom_note'])

        return render_template('notes.html',dataframe=dataframe)
    return redirect(url_for('login'))


# @app.route('/etudiants',methods=['POST','GET'])
# @login_required
# def etudiants():
#     if current_user.role.name =="admin":
#         if request.method == 'POST':
            # dataframe = pd.read_excel(request.files.get('file'))
            # for index,row in dataframe.iterrows():
                # random_hex = secrets.token_hex(8)
                # hashed_password = bcrypt.generate_password_hash(random_hex).decode('utf-8')
                # try :
                #     niv = Niveau.query.filter_by(nom_niveau=row['niveau']).first()
                #     print(niv.nom_niv)
                # except:
                #     niv = Niveau(nom_niv=row['niveau'])
                #     db.session.add(niv)
                #     db.session.commit()
                #     print(niv.nom_niv)
                # try :
                #     spec = Specialite.query.filter_by(nom_specialite=row['specialite']).first()
                #     print(spec.nom_specialite)
                # except:
                #     spec = Specialite(nom_specialite=row['specialite'])
                #     db.session.add(spec)
                #     db.session.commit()
                #     print(spec.nom_specialite)
                # newEtd = Etudiant(nom=row['nom'],prenom=row['prenom'],email=row['email'],cin=row['cin'],id_niv=niv.id,id_specialite=spec.id,password=hashed_password)
                # etudiantRole = Role.query.filter_by(name="etudiant").first()
                # newEtd.role_id = etudiantRole.id
                # db.session.add(newEtd)
                # db.session.commit()
                # send_reset_email(newEtd)
#         listeEtudiants = Etudiant.query.all()
#         return render_template('etudiants.html',title="Etudiants",listeEtudiants=listeEtudiants)
#     return redirect(url_for('login'))

@app.route("/niveau/<int:niveau_id>",methods=['POST','GET'])
@login_required
def par_niveau(niveau_id):
    if current_user.role.name =="admin":
        niv = Niveau.query.get_or_404(niveau_id)
        return render_template('etudiants_par_niveau.html',title=niv.nom_niv,etudiants=niv.etudiants)
    return redirect(url_for('login'))



@app.route("/specialite/new",methods=['POST','GET'])
def addSpecialite():
    if current_user.role.name =="admin":
        form = SpecForm()
        if form.validate_on_submit():
            spec = Specialite(nom_specialite=form.name.data)
            db.session.add(spec)
            db.session.commit()
            flash('Specialite has been created','success')
            return redirect(url_for('home'))
        return render_template('create_niv_spec.html',title="New Specialite",form=form)
    return redirect(url_for('login'))


@app.route("/specialite/<int:specialite_id>/delete",methods=['POST','GET'])
@login_required
def delete_specialite(specialite_id):
    if current_user.role.name =="admin":
        spec = Specialite.query.get_or_404(specialite_id)
        try  :
            db.session.delete(spec)
            db.session.commit()
            flash('Specialite has been deleted','success')
        except :
            flash('Cette specialite admet des étudiants','danger')
            return redirect(url_for('home'))
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route("/specialite/<int:specialite_id>",methods=['POST','GET'])
@login_required
def par_specialite(specialite_id):
    if current_user.role.name =="admin":
        spec = Specialite.query.get_or_404(specialite_id)
        return render_template('etudiants_par_specialite.html',title=spec.nom_specialite,etudiants=spec.etudiants)
    return redirect(url_for('login'))


@app.route("/etudiant/<int:etudiant_id>/update",methods=['POST','GET'])
@login_required
def update_etudiant(etudiant_id):
    if current_user.role.name =="admin":
        etd = Etudiant.query.get_or_404(etudiant_id)
        form = UpdateEtudiantForm()
        if form.validate_on_submit():
            etd.nom = form.nom.data
            etd.prenom = form.prenom.data
            etd.email = form.email.data
            try :
                niv = Niveau.query.filter_by(nom_niv=form.niv.data).first()
                print(niv.id)
            except:
                niv = Niveau(nom_niv=form.niv.data)
                db.session.add(niv)
                db.session.commit()
                print(niv.id)
            try :
                spec = Specialite.query.filter_by(nom_specialite=form.spec.data).first()
                print(spec.id)
            except:
                spec = Specialite(nom_specialite=form.spec.data)
                db.session.add(spec)
                db.session.commit()
                print(spec.id)
            etd.id_specialite = spec.id 
            etd.id_niv = niv.id
            db.session.commit()
            flash('Student has been updated!','success')
        elif request.method == "GET":
            form.nom.data = etd.nom
            form.prenom.data = etd.prenom
            form.email.data = etd.email
            form.niv.data = etd.niveau.nom_niv
            form.spec.data = etd.specialite.nom_specialite
            return redirect(url_for('etudiants'))
        return render_template('addEtd.html',title="Update Student",form=form)
    return redirect(url_for('login'))

@app.route("/etudiant/<int:etudiant_id>/delete",methods=['POST'])
@login_required
def delete_etd(etudiant_id):
    etd = Etudiant.query.get_or_404(etudiant_id)
    db.session.delete(etd)
    db.session.commit()
    flash('Student has been deleted','success')
    return redirect(url_for('etudiants'))

# @app.route('/user/<string:username>')
# def user_posts(username):
#     page = request.args.get('page',1,type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = Post.query.filter_by(author=user)\
#         .order_by(Post.posted_date.desc())\
#         .paginate(page = page,per_page=5)
#     return render_template('user_posts.html',posts=posts,user=user)

def send_reset_email(newEtd):
    token = newEtd.get_reset_token()
    msg = Message('Password reset request',\
                  sender='landoulsiferes@outlook.com',\
                  recipients=[newEtd.email])
    msg.body = f'''To reset your password, visit the following link: 
{url_for('reset_token',token=token, _external= True)}

If you did not make this request than ignore all this and no changes 
will be made. 
'''
    mail.send(msg)

@app.route('/reset_password/<token>',methods=['POST','GET'])
def reset_token(token):
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    user = Etudiant.verify_reset_token(token)
    # if user is None:
    #     flash('That is an invalid or expired token','warning')
    #     return redirect(url_for('home'))
    form = RestPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your Password has been Updated! You are able to login!',"success")
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Reset Password',form=form)
