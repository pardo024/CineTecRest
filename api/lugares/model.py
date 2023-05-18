from pymongo import MongoClient
from bson import ObjectId

class classLugares():
  def __init__(self):
    self.cliente=MongoClient()
    self.bd=self.cliente.CineTec
    self.coleccion=self.bd.lugares


  def validarCredenciales(self, usuario, password):
      users=self.bd.empleados.find_one({"nombre":usuario,"password":password})
      if users:
          return users
      else:
          return None

    

  def insertar_lugar(self, solicitud):
    lugarId = solicitud.get("_id", "")

    if self.coleccion.find_one({"_id":lugarId}):
      return "El lugar {lugarId} ya existe en la base de datos"
    else:
      self.coleccion.insert_one(solicitud)
      return "El lugar {lugarId} fue insertado en la base de datos"




  def consultar_Lugar(self, id):
    resp = {"estatus": "", "mensaje": ""}
    res=self.bd.lugares.find_one({"_id":(id)})

    if res:

      resp["estatus"] = "ok"
      resp["mensaje"] = "Se encontro el lugar"
      resp["data"] = res
      return resp
    
    else:
      resp["estatus"] = "error"
      resp["mensaje"] = "No se encontro el lugar"
      return resp

    


  def consulta_general(self):
        respuesta={"estatus":"","mensaje":""}
        res=self.bd.lugares.find()
        lista=[]
        for documento in res:
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


  def eliminar_Lugar(self, id):

    res=self.bd.lugares.delete_one({"_id":(id)})
    if res.deleted_count==0:
      return "No se encontro el lugar con el ID Introducido"
    else:
      return "Se elimino el lugar con el ID Introducido"
    

#def actualuzar
#sacar asiento con pop y actualizar numero de aciento

  def actualizar_Lugar(self, id, info):

        try:
            respuesta={"estatus":"","mensaje":""}
            data=self.bd.lugares.find_one({"_id":int(id)})
            if data:
                lugares=data.get("lugares")
                if "indice_lugar_eliminar" in info:
                        indice_lugar_eliminar=info["indice_lugar_eliminar"]
                        if 0<= indice_lugar_eliminar < len(lugares):
                            lugares = lugares.pop(indice_lugar_eliminar)
                            del info["indice_lugar_eliminar"]
                            data.update(info)
                            self.bd.lugares.update_one({"_id":int(id)}, {"$set":data})
                            
                            respuesta["estatus"]="ok"
                            respuesta["mensaje"]=lugares
                            
            else: 
                
                respuesta["estatus"]="error"
                respuesta["mensaje"]="No se encontro el id"    
        except:
            respuesta["estatus"]="error"
            respuesta["mensaje"]="ERROR INEXPLICABLE FUERA DEL ALCANCE DEL PROGRAMADOR"
            
        return respuesta
   
    