# importamos la instancia de Flask (app)
from apptrivia import app,admin_permission
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from forms.login import LoginForm
from forms.register import RegisterForm
import os, random, datetime
from flask_sqlalchemy import SQLAlchemy

# importamos los modelos a usar
from apptrivia import db
from models.models import Categoria, Pregunta, Respuesta, User
from flask import render_template, session, redirect, url_for, request, url_for, flash, jsonify, abort
from werkzeug.urls import url_parse
from werkzeug.exceptions import HTTPException
from flask_principal import AnonymousIdentity, RoleNeed, UserNeed, identity_loaded, identity_changed

# para poder usar Flask-Login
login_manager = LoginManager(app)
login_manager.init_app(app)

@app.route('/inicio')
@login_required
def inicio():
    session['tiempo'] = datetime.datetime.now()
    session['categorias'] = {"1":1,"2":1,"3":1,"4":1}
    return redirect(url_for('mostrarcategorias'))


@app.route('/trivia')
def index():
    contador = 1
    ranking_list = []
    ranking = User.query.order_by(User.tiempo).all()
    for user in ranking:
        ranking_list.append({"nombre":user.name,"tiempo":user.tiempo,"posicion":contador})
        contador = contador + 1
        if contador >= 10:
            break
    return render_template('index.html', ranking = ranking_list)


@app.route('/trivia/categorias', methods=['GET'])
@login_required
def mostrarcategorias():
    print(session['categorias'].values())
    suma = []
    categorias = Categoria.query.all()
    categoriasf =[]
    for categoria in categorias:
        if session['categorias'][str(categoria.id)] == 1:
            categoriasf.append(categoria)
    for valor in session['categorias'].values():
        suma.append(int(valor))
    if sum(suma) == 0:
        session['tiempo2'] = datetime.datetime.now()
        tiempo = session['tiempo2'] - session['tiempo']
        tiempo = tiempo.total_seconds()
        mensaje = "Que sos, el campeon de las trivias? Tardaste en segundos:"
        if current_user.tiempo == None:
            mensaje2 = "Es tu mejor tiempo!"
            mejor_tiempo(tiempo)
        elif tiempo < current_user.tiempo:
            mensaje2 = "Es tu mejor tiempo!"
            mejor_tiempo(tiempo)
        else:
            mensaje2 = "Tu mejor tiempo Fue:{}".format(current_user.tiempo)
        return render_template('ganador.html', tiempo=tiempo,mensaje=mensaje,mensaje2=mensaje2)
    else:
        print(session['categorias'].values())
        return render_template('categorias.html', categorias=categoriasf)


@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    respuestas = Respuesta.query.filter_by(pregunta_id =pregunta.id).all()
    session['categoria_actual'] = str(id_categoria)
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta,respuestas=respuestas)


@app.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
@login_required
def mostrarrespuesta(id_pregunta,id_respuesta):
    pregunta = Pregunta.query.filter_by(id= id_pregunta).all()
    respuesta = Respuesta.query.filter_by(id=id_respuesta).all()
    if respuesta[0].resultado == True:
        resultado = "Respuesta Correcta"
        session['categorias'][session['categoria_actual']] = 0
        session.modified = True
    else:
        resultado = "Respuesta Incorrecta"
    return render_template('respuesta.html', resultado=resultado, pregunta=pregunta[0],respuesta=respuesta[0])


#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@app.route('/trivia/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #get by email valida
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)


@app.route("/trivia/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            flash('El email {} ya está siendo utilizado por otro usuario'.format(email))
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=username, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template("register.html", form=form)


@app.route('/trivia/logout')
def logout():
    logout_user()
    # Flask-Principal: Remove session keys
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Flask-Principal: the user is now anonymous
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('index'))

def mejor_tiempo(tiempo):
    usuario = User.query.filter_by(id=current_user.id).first()
    usuario.tiempo = tiempo
    return db.session.commit()


""" manejo de errores """

@app.errorhandler(404)
def page_not_found(e):
    #return jsonify(error=str(e)), 404
    return render_template('404.html')

@app.errorhandler(401)
def unathorized(e):
    return redirect(url_for('login'))

@app.errorhandler(403)
def unathorized(e):
    return render_template('403.html')

@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=str(e)), e.code

""" Flask-Principal"""

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Seteamos la identidad al usuario
    identity.user = current_user

    # Agregamos una UserNeed a la identidad, con el id del usuario actual.
    if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

    # Agregamos a la identidad la lista de roles que posee el usuario actual.
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))



@app.route('/test')
@login_required
@admin_permission.require(http_exception=403)
def test_principal():
    return render_template('test.html')