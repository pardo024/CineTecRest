from flask import Flask, request,Blueprint
from funciones.model import classfunciones
funcionesBP=Blueprint('funcionesBP',__name__)
from flask_httpauth import HTTPBasicAuth
import json

auth=HTTPBasicAuth()

@auth.verify_password
def login(username,password):
    cn=classfunciones()
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

@funcionesBP.route('/funciones', methods=['GET'])
def ConsultaGeneral():
    conexion=classfunciones()
    respuesta=conexion.consultaGeneral()
    return respuesta

@funcionesBP.route('/funciones/<id>', methods=['GET'])
def ConsultaIndividual(id):
    conexion=classfunciones()
    respuesta=conexion.consultaIndividual(id)
    return respuesta

@funcionesBP.route('/Funciones', methods=['POST'])
@auth.login_required(role="supervisor")
def insertar():
    datos=request.get_json()
    conexion=classfunciones()
    respuesta=conexion.insertar(datos)
    print(respuesta)
    return respuesta

@funcionesBP.route('/funciones/<id>', methods=['PUT'])
@auth.login_required(role="gerente")
def actualizar(id):
    datos=request.get_json()
    conexion=classfunciones()
    respuesta=conexion.actualizar(id,datos)
    return respuesta

@funcionesBP.route('/funciones/<id>', methods=['DELETE'])
@auth.login_required(role="gerente")
def eliminar(id):
    conexion=classfunciones()
    respuesta=conexion.eliminar(id)
    return respuesta
