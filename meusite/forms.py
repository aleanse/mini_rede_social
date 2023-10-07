from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,PasswordField,SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from meusite.models import Usuario
from flask_login import current_user
class form_login(FlaskForm):
    email = StringField('email',validators=[DataRequired(),Email()])
    senha = PasswordField('senha',validators=[DataRequired(),Length(6,10)])
    submit_login = SubmitField('fazer login')

class form_criarconta(FlaskForm):
    username = StringField('nome de usuario', validators=[DataRequired(), Length(6,20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    senha = PasswordField('senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('confirmação de senha', validators=[DataRequired(), EqualTo('senha', message='as senhas tem que ser iguais')])
    submit_criarconta = SubmitField('criar conta')

    #validador personalizado que verifica se ja existe email e usuario no banco de dados
    def validate_email(self,email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email ja cadastrado, cadastre outro email para continuar')

    def validate_username(self,username):
        usuario2 = Usuario.query.filter_by(username=username.data).first()
        if usuario2:
            raise ValidationError('ja existe um usuario com esse nome, cadastre outro nome para continuar')


class form_editar_perfil(FlaskForm):
    username = StringField('novo nome de usuario', validators=[DataRequired(), Length(6, 20)])
    email = StringField('novo email', validators=[DataRequired(), Email()])
    editar_foto = FileField('editar foto de perfil',validators=[FileAllowed(['jpg', 'png'])])
    submit_editar_perfil = SubmitField('Editar Perfil')
    def validate_email(self,email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('ja existe esse email, cadastre outro email para continuar')


class form_post(FlaskForm):
    titulo = StringField('titulo do post',validators=[DataRequired()])
    corpo = TextAreaField('escreva seu post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')

