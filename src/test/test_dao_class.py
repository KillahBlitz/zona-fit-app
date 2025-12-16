import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

from models.ClienteClass import Cliente
from models.DAOClass import ClienteDAO


class TestClienteDAO(unittest.TestCase):

    @patch('models.DAOClass.Conexion')
    def test_seleccionar_clientes_exitoso(self, mock_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = [
            (1, "Juan", "Pérez", 1),
            (2, "María", "García", 2)
        ]
        
        clientes = ClienteDAO.seleccionar()
        
        self.assertEqual(len(clientes), 2)
        self.assertEqual(clientes[0].nombre, "Juan")
        self.assertEqual(clientes[1].nombre, "María")
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    @patch('models.DAOClass.Conexion')
    def test_seleccionar_sin_clientes(self, mock_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        clientes = ClienteDAO.seleccionar()
        
        self.assertEqual(len(clientes), 0)
    
    @patch('models.DAOClass.Conexion')
    def test_insertar_cliente_exitoso(self, mock_conexion):

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1
        
        cliente = Cliente(nombre="Test", apellido="User", membresia=1)
        
        registros = ClienteDAO.insertar(cliente)
        
        self.assertEqual(registros, 1)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    @patch('models.DAOClass.Conexion')
    def test_insertar_cliente_con_error(self, mock_conexion):

        mock_conexion.obtener_conexion.side_effect = Exception("Error de conexión")
        
        cliente = Cliente(nombre="Test", apellido="User", membresia=1)
        
        registros = ClienteDAO.insertar(cliente)
        
        self.assertIsNone(registros)
    
    @patch('models.DAOClass.Conexion')
    def test_actualizar_cliente_exitoso(self, mock_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1
        
        cliente = Cliente(1, "Actualizado", "Test", 2)
        
        registros = ClienteDAO.actualizar(cliente)

        self.assertEqual(registros, 1)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        
        call_args = mock_cursor.execute.call_args[0]
        valores = call_args[1]
        self.assertEqual(valores[0], "Actualizado")
        self.assertEqual(valores[1], "Test")
        self.assertEqual(valores[2], 2)
        self.assertEqual(valores[3], 1)
    
    @patch('models.DAOClass.Conexion')
    def test_actualizar_cliente_no_existente(self, mock_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 0  
        
        cliente = Cliente(999, "NoExiste", "Test", 1)
        registros = ClienteDAO.actualizar(cliente)
        
        self.assertEqual(registros, 0)
    
    @patch('models.DAOClass.Conexion')
    def test_eliminar_cliente_exitoso(self, mock_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1
        
        cliente = Cliente(id_cliente=1)
        registros = ClienteDAO.eliminar(cliente)
        self.assertEqual(registros, 1)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    @patch('models.DAOClass.Conexion')
    def test_eliminar_cliente_no_existente(self, mock_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 0
        
        cliente = Cliente(id_cliente=999)
        
        registros = ClienteDAO.eliminar(cliente)
        
        self.assertEqual(registros, 0)
    
    @patch('models.DAOClass.Conexion')
    def test_conexion_se_cierra_correctamente(self, mock_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        ClienteDAO.seleccionar()
        
        mock_cursor.close.assert_called_once()
        mock_conexion.liberar_conexion.assert_called_once_with(mock_conn)
    
    @patch('models.DAOClass.Conexion')
    def test_multiples_inserciones(self, mock_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1
        
        clientes = [
            Cliente(nombre="Cliente1", apellido="Test1", membresia=1),
            Cliente(nombre="Cliente2", apellido="Test2", membresia=2),
            Cliente(nombre="Cliente3", apellido="Test3", membresia=3),
        ]
        
        resultados = [ClienteDAO.insertar(c) for c in clientes]
        
        self.assertEqual(len(resultados), 3)
        self.assertTrue(all(r == 1 for r in resultados))
        self.assertEqual(mock_cursor.execute.call_count, 3)


class TestClienteDAOIntegration(unittest.TestCase):
    @patch('models.DAOClass.Conexion')
    def test_crud_completo_mockeado(self, mock_conexion):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.obtener_conexion.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.rowcount = 1
        cliente = Cliente(nombre="Test", apellido="CRUD", membresia=1)
        registros_insert = ClienteDAO.insertar(cliente)
        self.assertEqual(registros_insert, 1)
        
        mock_cursor.fetchall.return_value = [(1, "Test", "CRUD", 1)]
        clientes = ClienteDAO.seleccionar()
        self.assertEqual(len(clientes), 1)
        
        cliente_actualizar = clientes[0]
        cliente_actualizar.nombre = "Test Actualizado"
        registros_update = ClienteDAO.actualizar(cliente_actualizar)
        self.assertEqual(registros_update, 1)
        
        registros_delete = ClienteDAO.eliminar(cliente_actualizar)
        self.assertEqual(registros_delete, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
