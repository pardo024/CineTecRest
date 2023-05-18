from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://titulatec_soa:Hola.123@localhost/TitulaTEC_SOA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#importa tus clases
from funciones.funcionesBP import funcionesBP
from ventaBoletos.ventaBoletosBP import ventaBoletosBP
from funciones.funcionesBP import funcionesBP
from empleados.empleadosBP import empleadosBP
from inventario.inventarioBP import inventarioBP
from peliculas.peliculaBP import peliculaBP
from ventaDulces.ventaDulcesBP import ventaDulcesBP

#importa los blueprints
app.register_blueprint(funcionesBP)
app.register_blueprint(ventaBoletosBP)
app.register_blueprint(empleadosBP)
app.register_blueprint(inventarioBP)
app.register_blueprint(peliculaBP)
app.register_blueprint(ventaDulcesBP)
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def init():
    return "Escuchando el Servicio REST de Cinetec"

if __name__ == '__main__':
    app.run(debug=True)
        