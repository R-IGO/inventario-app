# 1. ACTUALIZAR IMPORTACIONES: Agregamos request y redirect
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    calificacion = db.Column(db.Integer)

    def __repr__(self):
        return f'<Libro {self.titulo}>'

# 2. ACTUALIZAR LA RUTA: Ahora aceptamos GET y POST
@app.route('/', methods=['GET', 'POST'])
def pagina_inicio():
    
    # LOGICA PARA GUARDAR (Si el método es POST)
    if request.method == 'POST':
        # a. Obtenemos los datos del formulario usando los 'name' del HTML
        titulo_form = request.form.get('titulo_libro')
        autor_form = request.form.get('autor_libro')
        calif_form = request.form.get('calificacion_libro')
        
        # b. Creamos el objeto Libro con esos datos
        nuevo_libro = Libro(titulo=titulo_form, autor=autor_form, calificacion=calif_form)
        
        # c. Lo guardamos en la base de datos
        db.session.add(nuevo_libro)
        db.session.commit()
        
        # d. Redireccionamos a la misma página para ver el cambio (evita duplicados al recargar)
        return redirect('/')

    # LOGICA PARA MOSTRAR (Si es GET o después del redirect)
    lista_libros = Libro.query.all()
    return render_template('index.html', libros=lista_libros)

# Ruta para borrar un libro específico
@app.route('/borrar/<int:id_libro>')
def borrar_libro(id_libro):
    # 1. Buscamos el libro por su ID
    # Si no existe, devuelve error 404 automáticamente (muy útil)
    libro_a_borrar = db.get_or_404(Libro, id_libro)
    
    # 2. Lo borramos de la sesión
    db.session.delete(libro_a_borrar)
    
    # 3. Confirmamos el cambio en la base de datos
    db.session.commit()
    
    # 4. Regresamos a la página principal
    return redirect('/')

# Ruta para editar (Maneja tanto mostrar el formulario como guardar los cambios)
@app.route('/editar/<int:id_libro>', methods=['GET', 'POST'])
def editar_libro(id_libro):
    # 1. Buscamos el libro (igual que para borrar)
    libro_a_editar = db.get_or_404(Libro, id_libro)

    # 2. Si el usuario envió el formulario (POST)
    if request.method == 'POST':
        # Actualizamos los campos del objeto con los nuevos datos del formulario
        libro_a_editar.titulo = request.form.get('titulo_libro')
        libro_a_editar.autor = request.form.get('autor_libro')
        libro_a_editar.calificacion = request.form.get('calificacion_libro')

        # Guardamos en la BD
        db.session.commit()

        # Nos vamos al inicio
        return redirect('/')

    # 3. Si el usuario solo entró a la página (GET)
    # Le enviamos el libro encontrado para que el HTML pueda rellenar los datos
    return render_template('editar.html', libro=libro_a_editar)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)