# student-management-flask-app
A student management app built with Flask micro-framework, Flask-Login, WTForms

# E-manual:
## note :
This tutorial is for linux user, you can find the equivalent commands for
windows or mac
## 0-installing pip and virtualenv:
You have to install pip and virtualenv
type : ``` sudo apt install python3-pip ``` <br>
type:  ``` pip install virtualenv ```<br> 
## 1-Setting up python virtual environment:
## Creating virtual environment: <br>
Go to any directory you desire to put your environments on. For my case, I chose the Environments folder than I have created specifically for python virtual environments. <br>
Then, make another directory for the python environment that you are going to use. <br>
Finally create the environment with the last command:
## Activate the virtual Environment:
To activate the environment, type the following command.
``` python3 -m venv <env_name_you_chose> ```  <br>
``` source bin/activate/<env_name_you_chose> ``` <br>

Now you are on <env_name_you_chose> virtual environment. <br>
To deactivate the virtual environment <br>
Type: ``` deactivate ```
Now you can proceed by installing the dependencies of the web application.
All the dependencies are available on requirements.txt <br> 
Just type: ```pip install -r requirements.txt ``` <br>
So that all the requirements of the application would be installed
To check that all the dependencies are installed
Type : ```pip freeze ``` <br>
## 2-Getting started with the App:
For sure, you have to have your virtual environment ON.
Go to the folder wherein the getionEtd App is location and start with exporting the environment
variables
Type : ```export FLASK_APP=run.py ``` <br>
Then : ```export FLASK_ENV=development``` <br> 
(we will set it to development mode since we want to see the log on the terminal. But when this app is in
production, we should set it to production mode) .
Before running the app, we have to initialize our database by creating an administrator, since our
application will not contain a sign-up feature for security reasons ( you don’t want to create an
administrator from a web page !!).
So to do that, go to file routes.py in the directory gestionEtd/routes.py and uncomment the code
initialization. <br> 
Now, run the application so that tables will be created and the administrator would be added.<br>
Type : ```flask run ```(then ctrl +C to stop it) <br>
Put again the initialization code into comment (to avoid having creating another database and
trying to create an administrator with the same name).
Now re-run the app and everything should be working fine : <br>
Type : ```flask run ``` <br>
run the application on : http://127.0.0.1:5000/
