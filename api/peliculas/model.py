from pymongo import MongoClient
from bson.objectid import ObjectId

class Pelicula():


    def __init__(self):
        self.cliente = MongoClient()
        self.bd = self.cliente.CineTecRest
        self.coleccion = self.bd.peliculas

    def validarCredenciales(self, usuario, password):
        users = self.bd.empleados.find_one({"nombre": usuario, "password": password})
        if users:
            return users
        else:
            return None

    def consultaGeneral(self):
        respuesta = {"estatus": "", "mensaje": ""}
        resultado = self.coleccion.find()
        lista = []
        for documento in resultado:
            documento["_id"] = str(documento["_id"])
            lista.append(documento)
        if len(lista) > 0:
            respuesta["estatus"] = "ok"
            respuesta["mensaje"] = "Consulta exitosa"
            respuesta["inventario"] = lista
        else:
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "No hay pelicula registrada"
            respuesta["inventario"] = []
        return respuesta

    def consultaIndividual(self, id):
        respuesta = {"estatus": "", "mensaje": ""}
        res = self.coleccion.find_one({"_id": int(id)})
        if res:
            respuesta["estatus"] = "ok"
            respuesta["mensaje"] = "La consulta individual se ha hecho correctamente"
            respuesta["solicitudes"] = res
        else:
            respuesta["estatus"] = "Error"
            respuesta["mensaje"] = "No hay ningun pelicula registradas con el id que se ha dado"
        return respuesta

    def eliminar(self, id):
        respuesta = {"estatus": "", "mensaje": ""}
        try:
            self.coleccion.delete_one({"_id": int(id)})
            respuesta["estatus"] = "ok"
            respuesta["mensaje"] = "Se ha eliminado la pelicula"
        except:
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "No se puede eliminar la pelicula"
        return respuesta

    def insertar(self, datos):
        respuesta = {"estatus": "", "mensaje": ""}
        try:
            idIncrementado = self.coleccion.find().sort([("_id", -1)]).limit(1)
            for elemento in idIncrementado:
                idIncrementado = elemento["_id"]
                datos["_id"] = int(idIncrementado) + 1
            formato = {
                "_id": datos.get("_id"),
                "nombre": datos.get("nombre"),
                "genero": datos.get("genero"),
                "clasificacion": datos.get("clasificacion"),
                "duracion": datos.get("duracion"),
                "nacionalidad": datos.get("nacionalidad"),
                "reparto":datos.get("reparto"),
                "sinopsis":datos.get("sinopsis")}
            if formato["_id"] and formato["nombre"] and formato["genero"] and formato["clasificacion"] and formato["duracion"] and formato["nacionalidad"] and formato["reparto"] and formato["sinopsis"]:
                self.coleccion.insert_one(formato)
                respuesta["estatus"] = "OK"
                respuesta["mensaje"] = "Se pudo registrar con exito la pelicula "
            else:
                respuesta["estatus"] = "error"
                respuesta["mensaje"] = "No se pudo registrar la pelicula por falta de datos"
        except:
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "fallo desconocido al insertar la informacion de la pelicula"
        return respuesta

    def actualizar(self,id,datos):
        respuesta = {"estatus": "", "mensaje": ""}
        updatedata = {
            "nombre": datos.get("nombre"),
            "genero": datos.get("genero"),
            "clasificacion": datos.get("clasificacion"),
            "duracion": datos.get("duracion"),
            "nacionalidad": datos.get("nacionalidad"),
            "reparto": datos.get("reparto"),
            "sinopsis": datos.get("sinopsis")
        }
        try:
            self.coleccion.update_one({"_id": int(id)}, {'$set': updatedata})
            respuesta["estatus"] = "ok"
            respuesta["mensaje"] = "Se ha actualizado la informacion de la pelicula"
        except:
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "No se pudo actualizar la informacion de la pelicula"
        return respuesta

