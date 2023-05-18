from flask import Flask, request,Blueprint
from empleados.model import classEmpleados 
from flask_httpauth import HTTPBasicAuth

empleadosBP=Blueprint('empleadosBP',__name__)


auth=HTTPBasicAuth()
@auth.verify_password
def login(username,password):
    cn=classEmpleados()
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

@empleadosBP.route('/Empleado', methods=['POST'])
@auth.login_required(role='general')
def insertar_empleado():
    conexion=classEmpleados()
    respuesta=request.get_json()
    return conexion.insertar_empleado(respuesta)


@empleadosBP.route('/Empleado/<string:id>', methods=['GET'])
def consulta_individual(id):
    conexion=classEmpleados()
    respuesta=conexion.consultar_Empleado(id)
    return respuesta


@empleadosBP.route('/Empleado', methods=['GET'])
def consulta_generalEmpleados():
    conexion=classEmpleados()
    respuesta=conexion.consulta_generalEmp()
    return respuesta

@empleadosBP.route('/Empleado/<string:id>', methods=['DELETE'])
@auth.login_required(role=['supervisor','general'])
def eliminar_empleado(id):
    conexion=classEmpleados()
    respuesta=conexion.eliminar_empleado(id)
    return respuesta


@empleadosBP.route('/Empleado/<string:id>', methods=['PUT'])
@auth.login_required(role='general')
def Actualizar_empleado(id):
    datos=request.get_json()
    conexion=classEmpleados()
    respuesta=conexion.actualizar_empleado(id,datos)
    return respuesta