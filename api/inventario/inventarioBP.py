from flask import Flask, request,Blueprint
from inventario.model import classInventario
inventarioBP=Blueprint('inventarioBP',__name__)
 

@inventarioBP.route('/inventario', methods=['GET'])
def ConsultaGeneral():
    conexion=classInventario()
    respuesta=conexion.consultaGeneral()
    return respuesta

@inventarioBP.route('/inventario/<id>', methods=['GET'])
def ConsultaIndividual(id):
    conexion=classInventario()
    respuesta=conexion.consultaIndividual(id)
    return respuesta

@inventarioBP.route('/inventario', methods=['POST'])
def Insertar():
    datos=request.get_json()
    conexion=classInventario()
    respuesta=conexion.insertar(datos)
    return respuesta

@inventarioBP.route('/inventario/<id>', methods=['PUT'])
def Actualizar(id):
    datos=request.get_json()
    conexion=classInventario()
    respuesta=conexion.actualizar(id,datos)
    return respuesta

@inventarioBP.route('/inventario/<id>', methods=['DELETE'])
def Eliminar(id):
    conexion=classInventario()
    respuesta=conexion.eliminar(id)
    return respuesta