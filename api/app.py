from flask import Flask, request
app = Flask(__name__)


#importa tus clases
from ventaDulces.ventaDulcesBP import ventaDulcesBP
from inventario.inventarioBP import inventarioBP
<<<<<<< Updated upstream

from lugares.lugaresBP import lugaresBP
from empleados.empleadosBP import empleadosBP
#importa los blueprints
app.register_blueprint(ventaDulcesBP)
app.register_blueprint(inventarioBP)
app.register_blueprint(lugaresBP)
app.register_blueprint(empleadosBP)
=======
from peliculas.peliculaBP import peliculaBP
#importa los blueprints
app.register_blueprint(ventaDulcesBP)
app.register_blueprint(inventarioBP)
app.register_blueprint(peliculaBP)
db = SQLAlchemy(app)
>>>>>>> Stashed changes

@app.route('/', methods=['GET'])
def init():
    return "Escuchando el Servicio REST de Cinetec"

if __name__ == '__main__':
    app.run(debug=True)
        