# Smart Fit App - Sistema de Gestión de Clientes

Sistema CRUD completo para gestión de clientes de gimnasio usando Python y MySQL.

## 📋 Características

- ✅ Listar todos los clientes
- ✅ Agregar nuevos clientes
- ✅ Actualizar información de clientes
- ✅ Eliminar clientes
- ✅ Pool de conexiones a base de datos
- ✅ Manejo de errores robusto
- ✅ Suite de pruebas automatizadas

## 🗄️ Estructura del Proyecto

```
smart_fit_app/
├── src/
│   ├── models/
│   │   ├── ClienteClass.py      # Modelo de Cliente
│   │   └── DAOClass.py           # Data Access Object
│   ├── zona_fit_db/
│   │   └── conexion.py           # Pool de conexiones
│   ├── main.py                   # Aplicación principal (menú)
│   └── test_app.py               # Suite de pruebas
└── README.md
```

## 🚀 Instalación

1. **Instalar dependencias:**
```bash
pip install mysql-connector-python
```

2. **Configurar base de datos:**
```sql
CREATE DATABASE zona_fit_db;

USE zona_fit_db;

CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    membresia INT NOT NULL
);
```

3. **Configurar conexión:**
Edita `zona_fit_db/conexion.py` con tus credenciales de MySQL.

## 💻 Uso

### Ejecutar aplicación principal:
```bash
cd src
python main.py
```

### Menú interactivo:
```
*** Sistema de Gestión de Clientes - Smart Fit ***
1. Listar clientes
2. Agregar cliente
3. Actualizar cliente
4. Eliminar cliente
5. Salir
```

### Ejecutar pruebas automatizadas:
```bash
cd src
python test_app.py
```

## 🧪 Suite de Pruebas

El archivo `test_app.py` incluye:

1. ✅ Test de inserción de cliente
2. ✅ Test de listado de clientes
3. ✅ Test de actualización de cliente
4. ✅ Test de eliminación de cliente
5. ✅ Test de inserción múltiple

### Salida esperada:
```
############################################################
INICIANDO SUITE DE PRUEBAS - SMART FIT APP
############################################################

============================================================
TEST 1: Insertar Cliente
============================================================
✓ TEST PASSED: Cliente insertado correctamente. Registros: 1

...

############################################################
RESUMEN DE PRUEBAS
############################################################
✓ Insertar Cliente: PASSED
✓ Listar Clientes: PASSED
✓ Actualizar Cliente: PASSED
✓ Eliminar Cliente: PASSED
✓ Insertar Múltiples Clientes: PASSED

Total: 5/5 pruebas exitosas
############################################################
```

## 📦 Componentes Principales

### ClienteClass.py
Modelo de dominio para representar un cliente:
```python
Cliente(id_cliente, nombre, apellido, membresia)
```

### DAOClass.py
Patrón DAO con operaciones CRUD:
- `seleccionar()` - Obtener todos los clientes
- `insertar(cliente)` - Agregar nuevo cliente
- `actualizar(cliente)` - Modificar cliente existente
- `eliminar(cliente)` - Eliminar cliente

### conexion.py
Pool de conexiones a MySQL para optimizar rendimiento y gestionar recursos.

## 🔧 Troubleshooting

**Error de conexión a base de datos:**
- Verifica que MySQL esté corriendo
- Revisa credenciales en `conexion.py`
- Asegúrate que la base de datos `zona_fit_db` exista

**Error al importar módulos:**
- Ejecuta los scripts desde la carpeta `src/`
- Verifica que la estructura de carpetas sea correcta

## 📝 Notas

- El sistema usa un pool de conexiones para mejor rendimiento
- Todas las operaciones incluyen manejo de excepciones
- Las pruebas son no destructivas (limpian datos de prueba)

## 🤝 Contribuciones

Este es un proyecto educativo del curso "Python 93 horas".
