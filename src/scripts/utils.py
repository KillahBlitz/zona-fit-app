
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.DAOClass import ClienteDAO
from src.models.ClienteClass import Cliente

def add_client(data):
    id = data.get("id", None)
    name = data["name"]
    last_name = data["last_name"]
    membership = data["membership"]
    type_action = None
    if id is None:
        cliente = Cliente(nombre=name, apellido=last_name, membresia=membership)
        dao = ClienteDAO()
        dao.insertar(cliente)
        type_action = "add"
    else:
        cliente = Cliente(id=id, nombre=name, apellido=last_name, membresia=membership)
        dao = ClienteDAO()
        dao.actualizar(cliente)
        type_action = "update"
    return True, type_action

def delete_client(data):
    id = data.get("id", None)
    name = data["name"]
    last_name = data["last_name"]
    membership = data["membership"]
    if id is not None:
        cliente = Cliente(id=id, nombre=name, apellido=last_name, membresia=membership)
        dao = ClienteDAO()
        dao.eliminar(cliente)
        return True, "delete"
    return False, "delete"

def clean_form(data):
    pass
