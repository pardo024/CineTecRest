from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

class classVentaBoletos():
    def __init__(self):
        self.cliente=MongoClient()
        self.bd=self.cliente.CineTecRest
        self.coleccion=self.bd.ventaBoletos

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
            respuesta["mensaje"]="No hay ventas"
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
    
    def insertar (self,datos):
        respuesta={"estatus":"","mensaje":""}
        try:
            print("insertando")
            idincrementado=self.coleccion.find().sort([("_id",-1)]).limit(1)
            for elemento in idincrementado:
                idincrementado=elemento["_id"]
                datos["_id"]=int(idincrementado)+1    
            data={
                "_id": datos.get("_id"),
                "Lugares": datos.get("Lugares"),
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "id_funcion": datos.get("id_funcion"),
                "id_empleado": datos.get("id_empleado"),
                "numBoletosVendidos": len(datos.get("Lugares")),
                "total": len(datos.get("Lugares")) * 50,
            }
            funcion=self.bd.funciones.find_one({"_id": data.get("id_funcion")})
            if funcion:

                empleado=self.bd.Empleados.find_one({"_id": data.get("id_empleado")})

                if empleado:  

                   if len(data.get("Lugares")) > 0:
                        
                            
                        self.coleccion.insert_one(data)
                        respuesta["estatus"]="ok"
                        respuesta["mensaje"]="Se inserto correctamente"

                   else:
                        respuesta["estatus"]="error"
                        respuesta["mensaje"]="No se puede insertar una venta sin boletos"    

                else:
                    respuesta["estatus"]="error"
                    respuesta["mensaje"]="No existe el empleado insertado"    
            else:
                respuesta["estatus"]="error"
                respuesta["mensaje"]="No existe la funcion insertada" 

        except:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="No se pudo insertar"
        return respuesta
    
    def eliminar(self,id):
        respuesta={"estatus":"","mensaje":""}
        try:
            res=self.coleccion.delete_one({"_id":int(id)})
            if res.deleted_count==1:
                respuesta["estatus"]="ok"
                respuesta["mensaje"]="Se elimino correctamente"
            else:
                respuesta["estatus"]="error"
                respuesta["mensaje"]="No se pudo eliminar"
        except:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="No se pudo eliminar"
        return respuesta
    
    def actualizar(self, id_venta, datos):
        respuesta = {"estatus": "", "mensaje": ""}
        
        try:
            venta = self.coleccion.find_one({"_id": int(id_venta)})
            if venta:
                lugares = venta.get("Lugares")
                if lugares:
                    # Verificar si se proporciona el índice del lugar a eliminar
                    if "indice_lugar_eliminar" in datos:
                        indice_lugar_eliminar = datos["indice_lugar_eliminar"]
                        if 0 <= indice_lugar_eliminar < len(lugares):
                            # Eliminar el lugar del arreglo Lugares
                            lugar_eliminado = lugares.pop(indice_lugar_eliminar)
                            
                            # Actualizar el campo numBoletosVendidos y total de la venta
                            venta["numBoletosVendidos"] -= 1
                            venta["total"] = venta["numBoletosVendidos"] * 50
                            
                            # Actualizar el resto de los datos proporcionados
                            del datos["indice_lugar_eliminar"]
                            venta.update(datos)
                            
                            # Actualizar la venta en la base de datos
                            self.coleccion.update_one({"_id": int(id_venta)}, {"$set": venta})
                            
                            respuesta["estatus"] = "ok"
                            respuesta["mensaje"] = "Se ha eliminado el lugar de la venta y actualizado los campos correspondientes"
                        else:
                            respuesta["estatus"] = "error"
                            respuesta["mensaje"] = "El índice del lugar a eliminar no es válido"
                    else:
                        respuesta["estatus"] = "error"
                        respuesta["mensaje"] = "No se proporcionó el índice del lugar a eliminar"
                else:
                    respuesta["estatus"] = "error"
                    respuesta["mensaje"] = "No hay lugares en la venta"
            else:
                respuesta["estatus"] = "error"
                respuesta["mensaje"] = "No se encontró la venta con el ID proporcionado"
        except:
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "No se pudo actualizar la venta"
        
        return respuesta

    def validarCredenciales(self, usuario, password):
        users=self.bd.Empleados.find_one({"nombre":usuario,"password":password})
        if users:
            return users
        else:
            return None
        

        
    