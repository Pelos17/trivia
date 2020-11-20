import os

# configuraciones. True para que el servidor pueda ser levantado en modo debug
DEBUG = True

# configuracion BD

MYSQL = {
    'user': 'reportes',
    'pw': 'antel2020',
    'db': 'trivia',
    'host': '192.168.211.4',
    'port': '3306',
}


SECRET_KEY =  'A SECRET KEY'

SQLALCHEMY_TRACK_MODIFICATIONS = False

#postgresql://username:password@hostname/database
SQLALCHEMY_DATABASE_URI = "mysql://reportes:antel2020@192.168.211.4:3306/trivia"
"""
SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL['user']}:" \
                          f"{MYSQL['pw']}@{MYSQL['host']}:" \
                          f"{MYSQL['port']}/{MYSQL['db']}"
"""
