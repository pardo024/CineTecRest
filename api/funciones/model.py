from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

class classfunciones():
    def __init__(self):
        self.cliente=MongoClient()
        self.bd=self.cliente.CineTecRest
        self.coleccion=self.bd.funciones

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
            respuesta["funciones"]=lista
        else:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="No hay ventas"
            respuesta["funciones"]=[]
        return respuesta
    
    def consultaIndividual(self,id):
        respuesta={"estatus":"","mensaje":""}
        res=self.coleccion.find_one({"_id":int(id)})
        if res:
         respuesta["estatus"]="ok"
         respuesta["mensaje"]="Consulta individual exitosa"
         respuesta["funciones"]=res
        else:
            respuesta["estatus"]="Error"
            respuesta["mensaje"]="No hayfunciones registradas con el id proporcionado"
        return respuesta
    
    def insertar (self,datos):
        respuesta={"estatus":"","mensaje":""}
        try:
            idincrementado=self.coleccion.find().sort([("_id",-1)]).limit(1)
            for elemento in idincrementado:
                idincrementado=elemento["_id"]
                datos["_id"]=int(idincrementado)+1

            formato={
                "_id": datos.get("_id"),
                "fecha": datos.get("fecha"),
                "horaFin": datos.get("horaFin"),
                "horaInicio": datos.get("horaInicio"),
                "id_pelicula": datos.get("id_pelicula"),
                "id_sala": datos.get("id_sala"),
            }    
            pelicula=self.bd.peliculas.find_one({"_id": formato.get("id_pelicula")})
            if pelicula:

                if datos.get("fecha")> datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
                    if formato["_id"] and formato["fecha"] and formato["horaFin"] and formato["horaInicio"] and formato["id_pelicula"] and formato["id_sala"]:
                        self.coleccion.insert_one(formato)
                        respuesta["estatus"]="ok"
                        respuesta["mensaje"]="Se inserto correctamente"
                    else:
                        respuesta["estatus"]="error"
                        respuesta["mensaje"]="No se pudo insertar faltan datos"
                else :
                    respuesta["estatus"]="error"
                    respuesta["mensaje"]="No se pudo insertar la fecha de la funcion es menor a la actual"

            else:
                respuesta["estatus"]="error"
                respuesta["mensaje"]="No se pudo insertar la pelicula no existe"        
        except:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="No se pudo insertar"
        return respuesta
    
    def eliminar(self,id):
        respuesta={"estatus":"","mensaje":""}
        try:
            res=self.coleccion.delete_one({"_id":int(id)})
            if res.deleted_count>0:
                respuesta["estatus"]="ok"
                respuesta["mensaje"]="Se elimino correctamente"
            else:
                respuesta["estatus"]="error"
                respuesta["mensaje"]="No se pudo eliminar"
        except:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="No se pudo eliminar"
        return respuesta
    
    def actualizar(self,id,datos):
        respuesta={"estatus":"","mensaje":""}
        try:
            formato={
                "_id": int(id),
                "fecha": datos.get("fecha"),
                "horaFin": datos.get("horaFin"),
                "horaInicio": datos.get("horaInicio"),
                "id_pelicula": datos.get("id_pelicula"),
                "id_sala": datos.get("id_sala"),
            }
            pelicula=self.bd.peliculas.find_one({"_id": formato.get("id_pelicula")})
            if pelicula:
                if datos.get("fecha")> datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
                    if formato["_id"] and formato["fecha"] and formato["horaFin"] and formato["horaInicio"] and formato["id_pelicula"] and formato["id_sala"]:
                        res=self.coleccion.update_one({"_id":int(id)},{"$set":formato})
                        if res.modified_count>0:
                            respuesta["estatus"]="ok"
                            respuesta["mensaje"]="Se actualizo correctamente"
                        else:
                            respuesta["estatus"]="error"
                            respuesta["mensaje"]="No se pudo actualizar"
                    else:
                        respuesta["estatus"]="error"
                        respuesta["mensaje"]="No se pudo actualizar faltan datos"
                else :
                    respuesta["estatus"]="error"
                    respuesta["mensaje"]="No se pudo insertar la fecha de la funcion es menor a la actual"
            else:
                respuesta["estatus"]="error"
                respuesta["mensaje"]="No se pudo insertar la pelicula no existe"
        except:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="No se pudo actualizar"
        return respuesta

    def validarCredenciales(self, usuario, password):
        users=self.bd.Empleados.find_one({"nombre":usuario,"password":password})
        if users:
            return users
        else:
            return None