### creating the application Factory 
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail 
from flask_login import LoginManager,current_user
from functools import wraps

import os


app = Flask(__name__) 
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category ='info'
app.config['MAIL_SERVER'] =  'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'landoulsiferes@gmail.com'
app.config['MAIL_PASSWORD'] = 'orenda2019'
mail = Mail(app)


# def login_required(role="ANY"):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorated_view(*args, **kwargs):
#             if not current_user.is_authenticated:
#               return login_manager.unauthorized()
#             if ((str(current_user.role_id) != role) and (role != "ANY")):
#                 return login_manager.unauthorized()
#             return fn(*args, **kwargs)
#         return decorated_view
#     return wrapper



from gestionEtd import routes
