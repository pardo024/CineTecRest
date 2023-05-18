from flask import Flask, request,Blueprint
from ventaBoletos.model import classVentaBoletos
ventaBoletosBP=Blueprint('ventaBoletosBP',__name__)
 
from flask_httpauth import HTTPBasicAuth


auth=HTTPBasicAuth()

@auth.verify_password
def login(username,password):
    cn=classVentaBoletos()
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
@ventaBoletosBP.route('/ventaBoletos', methods=['GET'])
def ConsultaGeneral():
    conexion=classVentaBoletos()
    respuesta=conexion.consultaGeneral()
    return respuesta

@ventaBoletosBP.route('/ventaBoletos/<id>', methods=['GET'])
def ConsultaIndividual(id):
    conexion=classVentaBoletos()
    respuesta=conexion.consultaIndividual(id)
    return respuesta

@ventaBoletosBP.route('/ventaBoletos', methods=['POST'])
def Insertar():
    datos=request.json
    conexion=classVentaBoletos()
    respuesta=conexion.insertar(datos)
    return respuesta

@ventaBoletosBP.route('/ventaBoletos/<id>', methods=['PUT'])
def Actualizar(id):
    datos=request.json
    conexion=classVentaBoletos()
    respuesta=conexion.actualizar(id,datos)
    return respuesta

@ventaBoletosBP.route('/ventaBoletos/<id>', methods=['DELETE'])
@auth.login_required(role="gerente")
def Eliminar(id):
    conexion=classVentaBoletos()
    respuesta=conexion.eliminar(id)
    return respuesta
