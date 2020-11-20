import os
from flask import g, Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_principal import Principal, Permission, RoleNeed
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_bootstrap import Bootstrap

# instancia Flask
app = Flask(__name__)

#Bootstrap
bootstrap = Bootstrap(app)
# sesiones
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

# lee la config desde el archivo config.py
app.config.from_pyfile('config.py')
    
# inicializa la base de datos con la config leida
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate()
# Se inicializa el objeto migrate
migrate.init_app(app, db)

# Flask-Principal: ---  Setup ------------------------------------
principal = Principal()
principal.init_app(app)

# Flask-Principal: Creamos un permiso con una sola necesidad que debe ser satisfecho para entrar al admin.
admin_permission = Permission(RoleNeed('admin'))


class MyModelView(ModelView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

admin = Admin(app, index_view=MyAdminIndexView())



# rutas disponibles
from routes import *
from models.models import Categoria, Pregunta, User, Respuesta, Role

# Los modelos que queremos mostrar en el admin
admin.add_view(ModelView(Categoria, db.session))
admin.add_view(ModelView(Pregunta, db.session))
admin.add_view(ModelView(Respuesta, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))

# subimos el server (solo cuando se llama directamente a este archivo)
if __name__ == '__main__':
    app.run(debug=True)