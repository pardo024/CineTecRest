from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
class classVentaDulces():
    def __init__(self):
        self.cliente=MongoClient()
        self.bd=self.cliente.CineTec
        self.coleccion=self.bd.ventadulceria

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
            respuesta["mensaje"]="No hay ventas registradas con el id proporcionado"
        return respuesta
    
    def insertar(self, datos):
        respuesta = {"estatus": "", "mensaje": ""}
        
        try:
            idincrementado = self.coleccion.find().sort([("_id", -1)]).limit(1)
            for elemento in idincrementado:
                idincrementado = elemento["_id"]
                datos["_id"] = int(idincrementado) + 1
            
            # Buscar el nombre del empleado utilizando el id_empleado en la colección "Empleados"
            empleado = self.bd.Empleados.find_one({"_id": datos.get("id_empleado")})
            if empleado:
                nombre_empleado = empleado.get("nombre")
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formato = {
                    "_id": datos.get("_id"),
                    "fecha_venta": fecha_actual,
                    "id_empleado": datos.get("id_empleado"),
                    "nombre_empleado": nombre_empleado,  # Asignar el nombre del empleado encontrado
                    "productos_vendidos": datos.get("productos_vendidos"),
                    "total_venta": 0  # Se inicializa con 0
                }

                if formato["_id"] and formato["fecha_venta"] and formato["id_empleado"] and formato["nombre_empleado"] and formato["productos_vendidos"]:
                    productos_validos = True
                    for producto in formato["productos_vendidos"]:
                        producto_id = producto["producto_id"]
                        producto_inventario = self.bd.inventario.find_one({"_id": producto_id})
                        if producto_inventario:
                            producto["precio_unitario"] = producto_inventario.get("precio")
                            total_producto = producto["cantidad"] * producto["precio_unitario"]
                            formato["total_venta"] += total_producto  # Se actualiza el total_venta

                            # Se agrega el campo "total_producto" para referencia
                            producto["total_producto"] = total_producto
                        else:
                            productos_validos = False
                            break

                    if productos_validos:
                        self.coleccion.insert_one(formato)  
                        respuesta["estatus"] = "ok"
                        respuesta["mensaje"] = "Se ha registrado la venta de dulces"
                    else:
                        respuesta["estatus"] = "error"
                        respuesta["mensaje"] = "Uno o más productos no existen en el inventario"
                else:
                    respuesta["estatus"] = "error"
                    respuesta["mensaje"] = "No se pudo registrar la venta porque no se proporcionaron todos los datos"
            else:
                respuesta["estatus"] = "error"
                respuesta["mensaje"] = "El id de empleado no existe en la base de datos"
        except:
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "No se pudo registrar el inventario"
        return respuesta

    
    def actualizar(self, id_venta, datos):
        respuesta = {"estatus": "", "mensaje": ""}
        
        try:
            venta = self.coleccion.find_one({"_id": int(id_venta)})
            if venta:
                productos_vendidos = venta.get("productos_vendidos")
                if productos_vendidos:
                    # Verificar si se proporciona el índice del producto a eliminar
                    if "indice_producto_eliminar" in datos:
                        indice_producto_eliminar = datos["indice_producto_eliminar"]
                        if 0 <= indice_producto_eliminar < len(productos_vendidos):
                            # Eliminar el producto del arreglo productos_vendidos
                            producto_eliminado = productos_vendidos.pop(indice_producto_eliminar)
                            
                            # Actualizar el campo total_venta restando el total del producto eliminado
                            total_eliminado = producto_eliminado.get("total_producto", 0)
                            venta["total_venta"] -= total_eliminado
                            
                            # Actualizar el resto de los datos proporcionados
                            del datos["indice_producto_eliminar"]
                            venta.update(datos)
                            
                            # Actualizar la venta en la base de datos
                            self.coleccion.update_one({"_id": int(id_venta)}, {"$set": venta})
                            
                            respuesta["estatus"] = "ok"
                            respuesta["mensaje"] = "Se ha eliminado el producto de la venta y actualizado el total de la venta"
                        else:
                            respuesta["estatus"] = "error"
                            respuesta["mensaje"] = "El índice de producto a eliminar no es válido"
                    else:
                        respuesta["estatus"] = "error"
                        respuesta["mensaje"] = "No se proporcionó el índice del producto a eliminar"
                else:
                    respuesta["estatus"] = "error"
                    respuesta["mensaje"] = "No hay productos vendidos en la venta"
            else:
                respuesta["estatus"] = "error"
                respuesta["mensaje"] = "No se encontró la venta con el ID proporcionado"
        except:
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "No se pudo actualizar la venta"
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