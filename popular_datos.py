#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apptrivia import db
from models.models import Categoria, Pregunta,User,Respuesta

db.drop_all()
db.create_all()

#Usuarios
q_u1 = User(name = "Juan", email = "jvignolo@antel.com.uy", is_admin = True)
# el pass lo seteamos con el método set_password para que se guarde con hash
q_u1.set_password("1234");
# por defecto, el usuario no es admin
q_u2 = User(name = "Pedrito", email = "pedrito@antel.com.uy")
q_u2.set_password("12345");

# categorias
c_geogra = Categoria(descripcion="Geografía")
c_deporte = Categoria(descripcion="Deportes")
c_entrete = Categoria(descripcion="Entretenimiento")
c_historia = Categoria(descripcion="Historia")

# preguntas
q_Laos = Pregunta(text="¿Cuál es la capital de Laos?",categoria=c_geogra)
q_Armenia = Pregunta(text="¿Cuál es la población aproximada de Armenia?",categoria=c_geogra)
q_mundial = Pregunta(text="¿En qué país se jugó la Copa del Mundo de 1962?",categoria=c_deporte)
q_formula = Pregunta(text="¿Que corredor gano el campeonato mundial de la F1 2013?",categoria=c_deporte)
q_hank = Pregunta(text="¿Como se llama el cuñado del Walter White en Breaking Bad?",categoria=c_entrete)
q_oscar = Pregunta(text="¿Quien gano el premio a mejor Actris en los Oscars 2015?",categoria=c_entrete)
q_diad = Pregunta(text="¿En que fecha sucedio el Dia D en la Segunda Guerra Mundial?",categoria=c_historia)
q_muro = Pregunta(text="¿En que fecha se derribo el Muro de Berlin?",categoria=c_historia)

# respuestas
r_Laos_1 = Respuesta(text="Vientián",resultado=True,pregunta=q_Laos)
r_Laos_2 = Respuesta(text="Montevideo",resultado=False,pregunta=q_Laos)
r_Laos_3 = Respuesta(text="Shensen",resultado=False,pregunta=q_Laos)

r_Armenia_1 = Respuesta(text="3.587.523",resultado=False,pregunta=q_Armenia)
r_Armenia_2 = Respuesta(text="2.965.000",resultado=True,pregunta=q_Armenia)
r_Armenia_3 = Respuesta(text="1.254.248",resultado=False,pregunta=q_Armenia)

r_mundial_1 = Respuesta(text="Chile",resultado=True,pregunta=q_mundial)
r_mundial_2 = Respuesta(text="Inglaterra",resultado=False,pregunta=q_mundial)
r_mundial_3 = Respuesta(text="Suecia",resultado=False,pregunta=q_mundial)

r_formula_1 = Respuesta(text="Sebastian Vettel",resultado=True,pregunta=q_formula)
r_formula_2 = Respuesta(text="Lewis Hamilton",resultado=False,pregunta=q_formula)
r_formula_3 = Respuesta(text="Michael Schumacher",resultado=False,pregunta=q_formula)

r_hank_1 = Respuesta(text="Jhon",resultado=False,pregunta=q_hank)
r_hank_2 = Respuesta(text="Saul",resultado=False,pregunta=q_hank)
r_hank_3= Respuesta(text="Hank",resultado=True,pregunta=q_hank)

r_oscar_1 = Respuesta(text="Brie Larson",resultado=False,pregunta=q_oscar)
r_oscar_2 = Respuesta(text="Julianne Moore",resultado=True,pregunta=q_oscar)
r_oscar_3 = Respuesta(text="Emma Stone",resultado=False,pregunta=q_oscar)

r_diad_1 = Respuesta(text="4/06/1994",resultado=False,pregunta=q_diad)
r_diad_2 = Respuesta(text="4/05/1994",resultado=False,pregunta=q_diad)
r_diad_3 = Respuesta(text="6/06/1994",resultado=True,pregunta=q_diad)

r_muro_1 = Respuesta(text="9/11/1989",resultado=True,pregunta=q_muro)
r_muro_2 = Respuesta(text="9/10/1989",resultado=False,pregunta=q_muro)
r_muro_3 = Respuesta(text="10/10/1989",resultado=False,pregunta=q_muro)

#Carga Usuarios
db.session.add(q_u1)
db.session.add(q_u2)

#Carga cateogrias
db.session.add(c_geogra)
db.session.add(c_deporte)
db.session.add(c_entrete)
db.session.add(c_historia)

#Carga preguntas
db.session.add(q_Laos)
db.session.add(q_Armenia)
db.session.add(q_mundial)
db.session.add(q_formula)
db.session.add(q_hank)
db.session.add(q_oscar)
db.session.add(q_diad)
db.session.add(q_muro)

#carga respuestas
db.session.add(r_Laos_1)
db.session.add(r_Laos_2)
db.session.add(r_Laos_3)
db.session.add(r_Armenia_1)
db.session.add(r_Armenia_2)
db.session.add(r_Armenia_3)
db.session.add(r_mundial_1)
db.session.add(r_mundial_2)
db.session.add(r_mundial_3)
db.session.add(r_formula_1)
db.session.add(r_formula_2)
db.session.add(r_formula_3)
db.session.add(r_hank_1)
db.session.add(r_hank_2)
db.session.add(r_hank_3)
db.session.add(r_oscar_1)
db.session.add(r_oscar_2)
db.session.add(r_oscar_3)
db.session.add(r_diad_1)
db.session.add(r_diad_2)
db.session.add(r_diad_3)
db.session.add(r_muro_1)
db.session.add(r_muro_2)
db.session.add(r_muro_3)

db.session.commit()

# creamos otros usuarios (…) y los recorremos
categorias = Categoria.query.all()
for c in categorias:
    print(c.id, c.descripcion)
    # para cada categoria, obtenemos sus preguntas y las recorremos
    for p in c.preguntas:
        print(p.id, p.text)


cat = Categoria.query.get(1)
print(cat)
