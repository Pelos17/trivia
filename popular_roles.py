from apptrivia import db
from models.models import  User, Role

from apptrivia import db
from models.models import  User, Role

db.session.add_all(
         [Role(rolename='admin', user_id=1),
          Role(rolename='user', user_id=2),  # multiples roles
          Role(rolename='user', user_id=3)])
db.session.commit()