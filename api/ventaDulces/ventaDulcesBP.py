from flask import Flask, request,Blueprint
from flask_sqlalchemy import SQLAlchemy
from ventaDulces.model import classVentaDulces 
ventaDulcesBP=Blueprint('ventaDulcesBP',__name__)


@ventaDulcesBP.route('/ventaDulces', methods=['GET'])
def ConsultaGeneral():
    conexion=classVentaDulces()
    respuesta=conexion.prueba()
    return respuesta
