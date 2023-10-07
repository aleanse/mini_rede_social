

from meusite import database ,login_manager
from datetime import datetime
from flask_login import UserMixin
#configuração para usar o login_manager
@login_manager.user_loader
def load_usuario(id_usuario):

        return Usuario.query.get(int(id_usuario))



class Seguindo(database.Model):
    id = database.Column(database.Integer,primary_key=True)
    id_seguidor = database.Column(database.Integer, database.ForeignKey('usuario.id'))
    id_seguindo = database.Column(database.Integer, database.ForeignKey('usuario.id'))


class Usuario(database.Model,UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, unique=True, nullable=False)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, nullable=False, default='Default.jpg')
    posts = database.relationship('Post',backref='autor', lazy=True)
    seguidores = database.relationship('Usuario',
                                       secondary=Seguindo.__table__,
                                       primaryjoin=(Seguindo.id_seguindo == id),
                                       secondaryjoin=(Seguindo.id_seguidor == id),
                                       backref='seguidos',
                                       lazy='dynamic')
    def contar_posts(self):
        return len(self.posts)

    def contar_seguidores(self):
        return Usuario.query.filter(Usuario.seguidores.contains(self)).count()

    def contar_seguindo(self):

        return self.seguidores.count()






class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'),nullable=False)