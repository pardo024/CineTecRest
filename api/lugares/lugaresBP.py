from flask import Flask, request,Blueprint
from lugares.model import classLugares 
from flask_httpauth import HTTPBasicAuth

lugaresBP=Blueprint('lugaresBP',__name__)



auth=HTTPBasicAuth()
@auth.verify_password
def login(username,password):
    cn=classLugares()
    user=cn.validarCredenciales(username,password)
    if user!=None:
        return user
    else:
        return False

@auth.get_user_roles
def get_user_roles(user):
    return user["puesto"]


@auth.error_handler
def error_hander():
    return {"estatus":"Error","mensaje":"Notiene aturizacion para la ejecucion  de la operacion"}


@lugaresBP.route('/Lugar', methods=['POST'])
def insertar_inventario():
    datos=request.get_json()
    conexion=classLugares()
    respuesta=conexion.insertar_lugar(datos)
    return respuesta


@lugaresBP.route('/Lugar/<int:id>', methods=['GET'])
def consulta_individual(id):
    conexion=classLugares()
    respuesta=conexion.consultar_Lugar(id)
    return respuesta


@lugaresBP.route('/Lugar', methods=['GET'])
def consulta_general():
    conexion=classLugares()
    respuesta=conexion.consulta_general()
    return respuesta


@lugaresBP.route('/Lugar/<int:id>', methods=['DELETE'])
@auth.login_required(role=['supervisor','general'])
def eliminar_lugar(id):
    conexion=classLugares()
    respuesta=conexion.eliminar_Lugar(id)
    return respuesta


@lugaresBP.route('/Lugar/<int:id>', methods=['PUT'])
def Actualizar_lugar(id):
    datos=request.get_json()
    conexion=classLugares()
    respuesta=conexion.actualizar_Lugar(id,datos)
    return respuesta

@lugaresBP.route('/Lugar/<id>', methods=['PUT'])
def Actualizar_empleado(id):
    datos=request.get_json()
    conexion=classLugares()
    respuesta=conexion.actualizar_Lugar(id,datos)
    return respuesta