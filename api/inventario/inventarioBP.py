from urllib.request import HTTPBasicAuthHandler
from flask import Flask, request,Blueprint
from inventario.model import classInventario
inventarioBP=Blueprint('inventarioBP',__name__)
from flask_httpauth import HTTPBasicAuth


auth=HTTPBasicAuth()

@auth.verify_password
def login(username,password):
    cn=classInventario()
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

@inventarioBP.route('/inventario', methods=['GET'])
def ConsultaGeneral():
    conexion=classInventario()
    respuesta=conexion.consultaGeneral()
    return respuesta

@inventarioBP.route('/inventario/<id>', methods=['GET'])
@auth.login_required
def ConsultaIndividual(id):
    conexion=classInventario()
    respuesta=conexion.consultaIndividual(id)
    return respuesta

@inventarioBP.route('/inventario', methods=['POST'])
@auth.login_required(role="supervisor")
def Insertar():
    datos=request.get_json()
    conexion=classInventario()
    respuesta=conexion.insertar(datos)
    return respuesta

@inventarioBP.route('/inventario/<id>', methods=['PUT'])
@auth.login_required(role="gerente")
def Actualizar(id):
    datos=request.get_json()
    conexion=classInventario()
    respuesta=conexion.actualizar(id,datos)
    return respuesta

@inventarioBP.route('/inventario/<id>', methods=['DELETE'])
@auth.login_required(role="gerente")
def Eliminar(id):
    conexion=classInventario()
    respuesta=conexion.eliminar(id)
    return respuesta

