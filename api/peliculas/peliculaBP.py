from flask import Flask, request,Blueprint
from peliculas.model import Pelicula
peliculaBP=Blueprint('peliculaBP',__name__)
from flask_httpauth import HTTPBasicAuth

auth=HTTPBasicAuth()
@auth.verify_password
def login(username,password):
    cn=Pelicula()
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
    return {"estatus":"Error","mensaje":"No tiene aturizacion para la ejecucion  de la operacion"}

@peliculaBP.route('/peliculas',methods=['GET'])
def ConsultGeneral():
    conexion=Pelicula()
    respuesta=conexion.consultaGeneral()
    return respuesta
@peliculaBP.route('/peliculas/<id>', methods=['GET'])
def consultaIndividual(id):
    conexion=Pelicula()
    respuesta=conexion.consultaIndividual(id)
    return respuesta
@peliculaBP.route('/peliculas/<id>', methods=['DELETE'])
@auth.login_required(role=['supervisor','gerente'])
def eliminar(id):
    conexion=Pelicula()
    respuesta=conexion.eliminar(id)
    return respuesta
@peliculaBP.route('/peliculas/<id>', methods=['PUT'])
@auth.login_required(role=['supervisor','gerente'])
def actualizar(id):
    datos=request.get_json()
    conexion=Pelicula()
    respuesta=conexion.actualizar(id,datos)
    return respuesta
@peliculaBP.route('/peliculas', methods=['POST'])
@auth.login_required(role=['supervisor','gerente'])
def insertar():
    datos=request.get_json()
    conexion=Pelicula()
    respuesta=conexion.insertar(datos)
    return respuesta

