from flask import Flask, request,Blueprint
from ventaDulces.model import classVentaDulces 
ventaDulcesBP=Blueprint('ventaDulcesBP',__name__)


@ventaDulcesBP.route('/ventaDulces', methods=['GET'])
def ConsultaGeneral():
    conexion=classVentaDulces()
    respuesta=conexion.consultaGeneral()
    return respuesta

@ventaDulcesBP.route('/ventaDulces/<id>', methods=['GET'])
def ConsultaIndividual(id):
    conexion=classVentaDulces()
    respuesta=conexion.consultaIndividual(id)
    return respuesta

@ventaDulcesBP.route('/ventaDulces', methods=['POST'])
def Insertar():
    datos=request.get_json()
    conexion=classVentaDulces()
    respuesta=conexion.insertar(datos)
    return respuesta

@ventaDulcesBP.route('/ventaDulces/<id>', methods=['PUT'])
def Actualizar(id):
    datos=request.get_json()
    conexion=classVentaDulces()
    respuesta=conexion.actualizar(id,datos)
    return respuesta

@ventaDulcesBP.route('/ventaDulces/<id>', methods=['DELETE'])
def Eliminar(id):
    conexion=classVentaDulces()
    respuesta=conexion.eliminar(id)
    return respuesta