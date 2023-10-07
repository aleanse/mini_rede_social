from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app2 =  Flask(__name__)
app2.config["SECRET_KEY"] = '7510a8915fd7f850ba4b37384cc4f8573bdfab44731e6d44cb711542364df399'

#cria um banco de dados
app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meusite.db'

#cria uma instancia do banco de dados
database = SQLAlchemy(app2)
bcrypt = Bcrypt(app2)
login_manager = LoginManager(app2)
login_manager.login_view = 'login'
login_manager.login_message = 'por favor faça o login para acessar essa pagina'

from meusite import routes