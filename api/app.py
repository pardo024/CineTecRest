from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://titulatec_soa:Hola.123@localhost/TitulaTEC_SOA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#importa tus clases
from ventaDulces.ventaDulcesBP import ventaDulcesBP

#importa los blueprints
app.register_blueprint(ventaDulcesBP)

db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def init():
    return "Escuchando el Servicio REST de Cinetec"

if __name__ == '__main__':
    app.run(debug=True)
        