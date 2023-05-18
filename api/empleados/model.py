from pymongo import MongoClient


class classEmpleados():
  def __init__(self):
    self.cliente=MongoClient()
    self.bd=self.cliente.CineTec
    self.coleccion=self.bd.empleados


  def validarCredenciales(self, usuario, password):
      users=self.bd.empleados.find_one({"nombre":usuario,"password":password})
      if users:
          return users
      else:
          return None


  def insertar_empleado(self, solicitud):
    UsuarioId = solicitud.get("_id", "")
    puesto = solicitud.get("puesto", "")
    campos = ["_id", "direccion", "fechaIngreso", "fechaNacimiento", "nombre", "nss", "puesto", "rfc", "sexo", "telefono", "password"]

    # Validación de campos vacíos
    for campo in campos:
        if not solicitud.get(campo):
            return "El campo {campo} no puede estar vacío"

    # Validación de puesto
    puestos_validos = ["gerente", "supervisor", "general"]
    if puesto.lower() not in puestos_validos:
        return "El puesto {puesto} no es válido. Los puestos válidos son {', '.join(puestos_validos)}"

    if self.coleccion.find_one({"_id": UsuarioId}):
        return "El usuario {UsuarioId} ya existe en la base de datos"
    else:
        self.coleccion.insert_one(solicitud)
        return "se ingreso el trabajador correctamente"


  def consultar_Empleado(self, id):
    resp = {"estatus": "", "mensaje": ""}
    res=self.bd.empleados.find_one({"_id":(id)})

    if res:

      resp["estatus"] = "ok"
      resp["mensaje"] = "Se encontro el empleado {id}"
      resp["data"] = res
      return resp
    
    else:
      resp["estatus"] = "error"
      resp["mensaje"] = "No se encontro el empleado"
      return resp
    


  def consulta_generalEmp(self):
        respuesta={"estatus":"","mensaje":""}
        res=self.bd.empleados.find()
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
  
  def eliminar_empleado(self, id):

    res=self.bd.empleados.delete_one({"_id":(id)})
    if res.deleted_count==0:
      return "No se encontro el empleado con el ID Introducido"
    else:
      return "Se elimino el empleado con el ID Introducido"
    
    
  def actualizar_empleado(self, id, info):
     resp={"estatus":"","mensaje":""}

     actualisacion={
        "direccion": info.get("direccion"),
        "telefono": info.get("telefono"),
        "puesto": info.get("puesto"),
        }

     try:
        self.coleccion.update_one({"_id":(id)},{'$set':actualisacion})
        resp["estatus"]="ok"
        resp["mensaje"]="Se actualizo el empleado"
     except:
        resp["estatus"]="error"
        resp["mensaje"]="No se encontro el empleado"
     return resp
  


