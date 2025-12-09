# 1. IMPORTANTE: Agregamos 'render_template' a la importación
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def pagina_inicio():
    # 2. En lugar de devolver una cadena de texto...
    # Le pedimos a Flask que busque 'index.html' en la carpeta templates
    # y lo procese para enviarlo al usuario.
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)