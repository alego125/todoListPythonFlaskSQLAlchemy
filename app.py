#Importamos flask, render template(con el cual renderizamos plantillas html), importamos tambien request para hacer el llamado con este modulo de la informacion de un formulario, importamos redirect para redireccionar a otro template, importamos url_for para inficar la url donde redireccionaremos por ejemplo
from flask import Flask, render_template, request, redirect, url_for
#Importamos sql alchemy
from flask_sqlalchemy import SQLAlchemy

#Le pasamos el name a la funcion de Flask para inicializarla y la guardamos en una variable app con la cual iniciamos el servidor
app = Flask(__name__)
#Indicamos a la aplicacion mediante config un parametro mediante el cual le vamos a indicar el lugar donde se encuentra la base de datos, para esto igualamos al string donde usaremos el protocolo de sqlite donde indicamos mediante sqlite:///, las tres barras indican que usaremos el protocolo de sqlite, seguidamente indicamos la carpeta donde esta la base de datos y luego la base de datos
#Si quisieramos usar una base de datos en mysql simplemente loq ue debemos hacer es en la lsiguiente linea apuntar en vez de a sqlite a mysql e indicar la url de la base de datos mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/task.db'
#Con este comando de arriba sqlalchemy va a saber donde buscar la base de datos para ejecutar los comandos en ella

#Ejecutamos el modulo de sqlalchemy 
#La funcion sqlalchemy recibe un parametro que es app es decir la palicacion 
#Con esta funcion creamos un cursor de la base de datos el cual lo guardamos en una variable llamada db la cual usaremos despues para realizar las acciones sobre la base de datos, es decir las consultas
db = SQLAlchemy(app)

#Creamos una clase para realizar le modelado de los datos recibidos por sqlalchemy
#Dentro ed task creamos una instancia de db con la cual le diremos que de db queremos crear un modelo de datos para esto usamos el metodo Model
class Task(db.Model):
    #Del modelo de datos lo que haremos aqui es colocar todos los datos que estan relacionados con una tarea
    #Ejemplo queremos guardar un id de la tarea, la tarea o su contenido y tambien una propiedad llamada done o hecho para indicar que ya fue realizada esa tarea
    #Primero indicamos el id para esto igualamos a db.column y le decimos que esta columna sera de tipo integer y tendra una llave primaria por lo cual colocamos primary_key en True
    id = db.Column(db.Integer, primary_key=True)
    #Tambien tendremos un contenido de la tarea, y la columna sera de tipo string y tendra 200 caracteres
    content = db.Column(db.String(200))
    #Propiedad done para indicar si la tarea fue hecha o no y sera tipo boolean
    done = db.Column(db.Boolean)


#Creamos la ruta inicial de la palicacion 
@app.route('/')
def home():
    #Creamos una nueva consulta a la base de datos para traer la informacion de esta y poder mostrar la lista de tareas dentro de la pantalla principal
    #Usamos la clase Task y de esta usamos query_all para trae toda la informacion de la base de datos y a esta informacion la guardamos dentro de una variable llamada task
    tasks = Task.query.all()
    #Renderizamos el template index.html y ademas le pasamos en una variable tasks la variable tasks de arriba con toda la informacion de la base de datos
    return render_template('index.html', tasks=tasks)

#Creamos una ruta especifica para agregar tareas, este utilizara el metodo POST para enviar informacion
@app.route('/create-task', methods=['POST'])
def create():
    #REcibimos los datos mediante request.form
    #Usamos la clase Task para introducir en cada campo la informacion recuperada del form
    #Luego a la instancia de la clase Task en una variable
    #Entonces a la isntancia de la clase le pasamos que el atributo content sera igual a lo que recuperamos del formulario del input con el name content, ademas que la propiedad done se setea en False ya que si estamos creando la tarea se supone que todavia no esta realizada
    task = Task(content=request.form['content'], done=False)
    #Ahora con nuestro objeto task creado lo que debemos hacer es guardarlo en nuestra base de datos, para estio usamos el metodo de db llamado session y de este el add, este loq ue permite es agregar un nuevo dato a la base de datos
    #Al pasarle el objeto task a la tabla lo que sucede es que estamos agregando una nueva tarea a la tabla
    db.session.add(task)
    #HAora hacemos un commit de esta sesion para indicar que terminamos lo que estamos haciendo y ahora lo que debemos es guardar esos datos
    db.session.commit()
    #Retornamos la redireccion hacia la pagina principal home, le pasamos mediante url_for el nombre de la funcion de la ruta de inicio
    #Con esto al guardar automaticamente se redirecciona nuevamente a la pagina principal o sea recarga la pagina y muestra el nuevo task agregado ya que al recargar la pagina esta va nuevamente a la base ed datos y trae nuevamente toda la info
    return redirect(url_for('home'))

#Creamos la ruta para done es decir la ruta que nos va a colocar la tarea como hecha
#A esta tarea le debemos pasar el id tambien por que queremos saber a que tarea de la lista queremos cambiar la propiedad done a true
@app.route('/done/<id>')
def done(id):
    #Realizamos la consulta para traer el task que coincida con el id que le pasamos 
    task = Task.query.filter_by(id=int(id)).first()
    #ahora lo que hacemos es cambiar al contrario la propiedad done de ese tas simplemente con la funcion not es decir si esta en true lo pone en false y si esta en false lo pone en true, y ese valor nuevo lo guardamos en la propiedad task.done
    #Entonces lo que hacemos es que el valor que teniamos lo estamos invirtiendo y lo estamos reasignando nuevamente a la misma propiedad
    task.done = not(task.done)
    #Terminado esto hacemos un commit para que los cambios se gurden
    db.session.commit()
    #Y para finalizar volvemos a redireccionar a la ruta home para que se recargue la pagina haga la consulta a la base de datos y se vuelvan a mostrar los datos de la base ded atos pero ahora con los cambios
    return redirect(url_for('home'))


#Creamos la ruta la cual vamos a usar para eliminar el id especificado
#Usamos la ruta delete y seguido le indicamos el id que va a ser especificado segun el task que seleccionemos por esto lo colocamos entre < > para indicar que sera un parametro 
@app.route('/delete/<id>')
#Creamos la funcion que recibira ese parametro id 
def delete(id):
    #Para eliminar usamos la clase Task, el query para indicar que usaremos un query y luego usaremos el metodo filter_by para que nos filtre la infromacion del query por el parametro que le pasamos entre parentesis, este id lo pasamos a entero y lo asignamos a otra variable que es el parametro de la funcion id y por ultimo le decios que selecciones el primero que encuentre por medio de el metodo first() y a todo esto lo guardamos en una variable task
    """task = Task.query.filter_by(id=int(id)).first()
    Task.query.delete(task)"""
    #Esta forma que vemos arriba es una de las maneras de eliminar primero busco la primer coincidencia que tengamos y luego la eliminimo. Pero puedo hacerlo directamente tambien de la siguiente manera
    task = Task.query.filter_by(id=int(id)).delete()
    #Una vez eliminado hacemos commit de esta eliminacion para que se apliquen los cambios en la base de datos
    db.session.commit()
    #Para finalizar redireccionamos nuevamente a home para que recargue la pagina y se listen nuevamente los datos pero ahora sin esta tarea que fue eliminada
    return redirect(url_for('home'))

#Hacemos la siguiente comparacion y decimos si name es igual a main o sea si es el archivo principal el que arranca nuestra aplicacion 
if __name__ == '__main__':
    #Arrancamos el servidor y le ponemos en modo debug para que cada vez que se haga un cambio este se reinicie solo
    app.run(debug = True)
