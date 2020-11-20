Llegue a integrar bootstrap, lo unico que me faltaria seria Blueprints. Sobre este ultimo no prometo llegar a integrarlo pero me gustaria (aprovecho a llorar la mona y comento que tengo que entregar una monografia en facultad del Viernes y estoy con parciales)

Repaso las funcionalidades:
- Login y register con flask login y forms.
- Modelos con alchemy (vas a ver que mis datos son para un server MySQL privado).
- Control de autorizacion para el Flask Admin mediante Permissions con Flask Principal.
- Almaceno mejor tiempo por user.
- Comenta si es el mejor tiempo del usuario.
- Ranking de los 10 mejores tiempos.
- Use migrations para reacomodar la BD (estan los script de flask migrate en el repo).
- Bootstrap para diseño (Algunas cosas las edite a mano y otras las copie de tu base alternativa, esta base.html.oroginal que era mi base sin boots).
- Script para popular la BD (uno popula usuarios, categorias, preguntas, y el otro solo roles, ya que fue lo que "migre").

No integre:
- Blueprints
- Con bootstrap podria hacer las cosas mas prolijas.

Breve descipcion del flujo de datos:
- Al precionar Home o ingresar a /trivia (o index.html) se muestra el ranking y mensajes iniciales.
- Cualquiera de las rutas protegidas redirigen a login si el usuario no se logeo.
- Para iniciar la trivia debe precionar el boton conrrespondiente(hay texto que indica el procedimiento en el baner inferior de la pagina)
- Al marcar una respuesta hay un boton de volver a categorias (puedo redireccionarlo automaticamente con un sleep pero me gusto el boton para seguir mis debug).
- Una ves se contesta una respuesta correctamente por categoria se redirige a ganador marcando si fue su mejor tiempo o cual fue el mejor previo.
- Para reiniciar se preciona el mismo boton que al iniciar.
- Los user logeados tienen boton de logout.


