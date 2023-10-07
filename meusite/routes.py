from meusite import app2, database, bcrypt

from meusite.models import Usuario, Post, Seguindo
from flask import render_template, request, flash, redirect, url_for
from meusite.forms import form_login, form_criarconta, form_editar_perfil, form_post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app2.route('/', methods=['GET', 'POST'])
def login():
    campo_login = form_login()

    if campo_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=campo_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, campo_login.senha.data):
            login_user(usuario)
            flash(f'login feito com sucesso no email {campo_login.email.data}')
            return redirect(url_for('home'))
        else:
            flash(f'email ou senha incorretos')

    return render_template('login.html', campo_login=campo_login)


@app2.route('/home')
@login_required
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)





@app2.route('/usuarios', methods=['POST', 'GET'])
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()



    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app2.route('/usuarios/<int:usuario>', methods=['POST', 'GET'])
@login_required
def seguir(usuario):
    seguidor_alvo = Usuario.query.filter_by(id=usuario).first()
    if seguidor_alvo not in current_user.seguidores:
        current_user.seguidores.append(seguidor_alvo)
        database.session.commit()
    return redirect(url_for('usuarios'))

@app2.route('/usuarios/<int:usuario>/deixar_seguir', methods=['POST', 'GET'])
@login_required
def deixar_seguir(usuario):
    seguidor_alvo = Usuario.query.filter_by(id=usuario).first()
    if seguidor_alvo in current_user.seguidores:
        current_user.seguidores.remove(seguidor_alvo)
    database.session.commit()
    return redirect(url_for('usuarios'))





@app2.route('/criar_conta', methods=['POST','GET'])
def criar_conta():
    campo_criarconta = form_criarconta()

    if campo_criarconta.validate_on_submit():
        senha_cript = bcrypt.generate_password_hash(campo_criarconta.senha.data)
        usuario = Usuario(username=campo_criarconta.username.data, email=campo_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'conta criada  com sucesso no email {campo_criarconta.email.data}')
        return redirect(url_for('home'))

    return render_template('criar_conta.html', campo_criarconta=campo_criarconta)


@app2.route('/sair')
def sair():
    logout_user()
    flash(f'logout feito com sucesso ')
    return redirect(url_for('login'))


@app2.route('/perfil', methods=['POST', 'GET'])
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')

    return render_template('perfil.html', foto_perfil=foto_perfil)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_completo = os.path.join(nome, codigo, extensao)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app2.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (130, 130)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app2.route('/perfil/editar', methods=['POST', 'GET'])
@login_required
def editar_perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    form = form_editar_perfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.editar_foto.data:
            nome_imagem = salvar_imagem(form.editar_foto.data)
            current_user.foto_perfil = nome_imagem

        database.session.commit()
        flash(f'nome de email mudado com sucesso para, {current_user.email},nome de usuario mudado com sucesso para {current_user.username}')
        return redirect(url_for('perfil'))
    return render_template('editar_perfil.html', form=form, foto_perfil=foto_perfil)


@app2.route('/perfil/criar_post', methods=['POST', 'GET'])
@login_required
def post():
    form = form_post()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso')
        return redirect(url_for('home'))
    return render_template('criar_post.html', form=form)


@app2.route('/post/<post_id>')
def exibir_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)
@app2.route('/post/<post_id>/excluir')
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('post excluido com sucesso')
    return redirect(url_for('home'))

@app2.route('/seguindo/<int:usuario_id>')
@login_required
def seguindo(usuario_id):
    usuario = Usuario.query.filter_by(id=usuario_id).first()
    lista_seguindo = usuario.seguidores

    return render_template('seguindo.html',lista_seguindo=lista_seguindo)

@app2.route('/seguidores/<int:usuario_id>')
@login_required
def seguidores(usuario_id):
    usuario = Usuario.query.filter_by(id=usuario_id).first()
    lista_seguidores =  Usuario.query.filter(Usuario.seguidores.contains(usuario)).all()
    return render_template('seguidores.html',seguidores=lista_seguidores)

