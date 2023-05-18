from flask import Flask, request,Blueprint
from ventaDulces.model import classVentaDulces 
ventaDulcesBP=Blueprint('ventaDulcesBP',__name__)
from flask_httpauth import HTTPBasicAuth

auth=HTTPBasicAuth()
@auth.verify_password
def login(username,password):
    cn=classVentaDulces()
    user=cn.validarCredenciales(username,password)
    if user!=None:
        return user
    else:
        return False

@auth.get_user_roles
def get_user_roles(user):
    return user["puesto"]

@auth.error_handler
def errr_handler():
    return{"estatus":"ERROR","mensaje":"No tiene autorizacion para realizar esta accion"}

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
@auth.login_required(role="gerente")
def Eliminar(id):
    conexion=classVentaDulces()
    respuesta=conexion.eliminar(id)
    return respuesta