from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
class classInventario():
    def __init__(self):
        self.cliente=MongoClient()
        self.bd=self.cliente.CineTec
        self.coleccion=self.bd.inventario

    def consultaGeneral(self):
        respuesta={"estatus":"","mensaje":""}
        resultado=self.coleccion.find()
        lista=[]
        for documento in resultado:
            documento["_id"]=str(documento["_id"])
            lista.append(documento)
        
        if len(lista)>0:
            respuesta["estatus"]="ok"
            respuesta["mensaje"]="Consulta exitosa"
            respuesta["inventario"]=lista
        else:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="No hay inventario"
            respuesta["inventario"]=[]
        return respuesta

    def consultaIndividual(self,id):
        respuesta={"estatus":"","mensaje":""}
        res=self.coleccion.find_one({"_id":int(id)})
        if res:
         respuesta["estatus"]="ok"
         respuesta["mensaje"]="Consulta individual exitosa"
         respuesta["solicitudes"]=res
        else:
            respuesta["estatus"]="Error"
            respuesta["mensaje"]="No hay solicitudes registradas con el id proporcionado"
        return respuesta
    
    def insertar(self,datos):
        respuesta={"estatus":"","mensaje":""}
        try:
            idIncrementado=self.coleccion.find().sort([("_id",-1)]).limit(1) 
            for elemento in idIncrementado:
                idIncrementado=elemento["_id"]
                datos["_id"]=int(idIncrementado)+1
            formato={
                "_id":datos.get("_id"),
                "categoria":datos.get("categoria"),
                "disponibilidad":datos.get("disponibilidad"),
                "fecha_vencimiento": datos.get("fecha_vencimiento"),
                "nombre": datos.get("nombre"),
                "precio": datos.get("precio"),
                "presentacion": datos.get("presentacion")}
            if formato["_id"] and formato["categoria"] and formato["disponibilidad"] and formato["fecha_vencimiento"] and formato["nombre"] and formato["precio"] and formato["presentacion"]:

                    if datetime.strptime(formato["fecha_vencimiento"], "%Y-%m-%d") > datetime.now():
                        self.coleccion.insert_one(datos)
                        respuesta["estatus"]="ok"
                        respuesta["mensaje"]="Se ha registrado el producto con id "+str(formato["_id"])
                    else: 
                        respuesta["estatus"]="error"
                        respuesta["mensaje"]="No se pudo registrar el producto por fecha de vencimiento"
            else:
                respuesta["estatus"]="error"
                respuesta["mensaje"]="No se pudo registrar el inventario por falta de datos"
        except:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="fallo desconocido al insertar el inventario"
        return respuesta
    
    def actualizar(self,id,datos):
        respuesta={"estatus":"","mensaje":""}
        updatedata= {
            "disponibilidad": datos.get("disponibilidad"),
            "precio": datos.get("precio"),
            }
        try:
            self.coleccion.update_one({"_id":int(id)},{'$set':updatedata})
            respuesta["estatus"]="ok"
            respuesta["mensaje"]="Se ha actualizado el inventario"
        except:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="No se pudo actualizar el inventario"
        return respuesta
    
    def eliminar(self,id):
        respuesta={"estatus":"","mensaje":""}
        try:
            self.coleccion.delete_one({"_id":int(id)})
            respuesta["estatus"]="ok"
            respuesta["mensaje"]="Se ha eliminado el inventario"
        except:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="No se pudo eliminar el inventario"
        return respuesta