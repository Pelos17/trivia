# importamos la instancia de la BD
from apptrivia import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(64), index=True, unique=True)

    preguntas = db.relationship('Pregunta', backref='categoria', lazy='dynamic')

    def __repr__(self):
        return f'<Categoria: {self.descripcion}>'


class Pregunta(db.Model):
    __tablename__ = 'pregunta'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False, unique=True)

    respuestas = db.relationship('Respuesta', backref='pregunta', lazy='dynamic')

    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    
    def __repr__(self):
        return f'<Pregunta {self.text}>'


class Respuesta(db.Model):
    __tablename__ = 'respuesta'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False, unique=True)
    resultado = db.Column(db.Boolean, nullable=False,default=False)
    
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'))

    def __repr__(self):
        return f'<Respuesta {self.text} {self.resultado}>'


class User(db.Model, UserMixin):
    __tablename__ = 'trivia_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    tiempo = db.Column(db.Float, nullable=True)
    roles = db.relationship('Role', backref='user', lazy='dynamic')

    def set_password(self,password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return f'<Usuario {self.name} Email: {self.email}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('trivia_user.id'))

    def __repr__(self):
        return f'<Role {self.rolename}>'