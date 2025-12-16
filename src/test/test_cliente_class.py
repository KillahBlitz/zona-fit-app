import unittest
import sys
import os

from models.ClienteClass import Cliente


class TestCliente(unittest.TestCase):
    
    def test_crear_cliente_con_todos_los_parametros(self):
        cliente = Cliente(
            id_cliente=1,
            nombre="Juan",
            apellido="Pérez",
            membresia=2
        )
        
        self.assertEqual(cliente.id, 1)
        self.assertEqual(cliente.nombre, "Juan")
        self.assertEqual(cliente.apellido, "Pérez")
        self.assertEqual(cliente.membresia, 2)
    
    def test_crear_cliente_sin_id(self):
        cliente = Cliente(
            nombre="María",
            apellido="García",
            membresia=1
        )
        
        self.assertIsNone(cliente.id)
        self.assertEqual(cliente.nombre, "María")
        self.assertEqual(cliente.apellido, "García")
        self.assertEqual(cliente.membresia, 1)
    
    def test_crear_cliente_con_parametros_nombrados(self):
        cliente = Cliente(
            id_cliente=5,
            nombre="Carlos",
            apellido="López",
            membresia=3
        )
        
        self.assertEqual(cliente.id, 5)
        self.assertEqual(cliente.nombre, "Carlos")
    
    def test_str_representacion(self):
        cliente = Cliente(1, "Ana", "Martínez", 2)
        resultado = str(cliente)
        
        self.assertIn("1", resultado)
        self.assertIn("Ana", resultado)
        self.assertIn("Martínez", resultado)
        self.assertIn("2", resultado)
    
    def test_cliente_con_nombre_vacio(self):
        cliente = Cliente(nombre="", apellido="Test", membresia=1)
        
        self.assertEqual(cliente.nombre, "")
        self.assertEqual(cliente.apellido, "Test")
    
    def test_cliente_con_membresia_cero(self):
        cliente = Cliente(nombre="Test", apellido="User", membresia=0)
        
        self.assertEqual(cliente.membresia, 0)
    
    def test_modificar_atributos_cliente(self):
        cliente = Cliente(1, "Original", "Nombre", 1)
        
        cliente.nombre = "Modificado"
        cliente.apellido = "Actualizado"
        cliente.membresia = 3
        
        self.assertEqual(cliente.nombre, "Modificado")
        self.assertEqual(cliente.apellido, "Actualizado")
        self.assertEqual(cliente.membresia, 3)


if __name__ == '__main__':
    unittest.main()
