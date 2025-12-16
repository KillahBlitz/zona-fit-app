# Tutorial: Configurar MySQL con DBeaver para Smart Fit App

## 📋 Índice
1. [Instalar MySQL](#1-instalar-mysql)
2. [Instalar DBeaver](#2-instalar-dbeaver)
3. [Conectar DBeaver a MySQL](#3-conectar-dbeaver-a-mysql)
4. [Crear Base de Datos](#4-crear-base-de-datos)
5. [Crear Tabla](#5-crear-tabla)
6. [Configurar Conexión Python](#6-configurar-conexión-python)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Instalar MySQL

### macOS:
```bash
# Opción 1: Homebrew (recomendado)
brew install mysql

# Iniciar servicio MySQL
brew services start mysql

# Configurar usuario root (primera vez)
mysql_secure_installation
```

### Verificar que MySQL está corriendo:
```bash
# Ver status del servicio
brew services list

# Debería mostrar:
# mysql started
```

### Conectar por primera vez:
```bash
mysql -u root -p
# Presiona Enter si no configuraste contraseña
# O ingresa la contraseña que configuraste
```

---

## 2. Instalar DBeaver

### Descargar:
1. Ve a: https://dbeaver.io/download/
2. Descarga **DBeaver Community Edition** (gratis)
3. Instala siguiendo el wizard

### Abrir DBeaver:
- En macOS: Busca "DBeaver" en Spotlight o Launchpad

---

## 3. Conectar DBeaver a MySQL

### Paso 1: Nueva Conexión
1. Abre DBeaver
2. Click en el icono de **"Plug"** (Nueva Conexión) en la barra superior
   - O menú: `Database > New Database Connection`

### Paso 2: Seleccionar MySQL
1. En la ventana que aparece, selecciona **MySQL**
2. Click en **Next**

### Paso 3: Configurar Conexión
Completa los campos:

```
Host:       localhost
Port:       3306
Database:   (dejar vacío por ahora)
Username:   root
Password:   (tu contraseña de MySQL, o vacío si no configuraste)
```

### Paso 4: Test Connection
1. Click en **Test Connection**
2. Si es primera vez, DBeaver descargará el driver MySQL automáticamente
3. Deberías ver: ✅ **"Connected"**

### Paso 5: Finish
1. Click en **Finish**
2. Ahora verás la conexión en el panel izquierdo

---

## 4. Crear Base de Datos

### Opción A: Usando interfaz DBeaver
1. En el panel izquierdo, expande tu conexión MySQL
2. Click derecho en **"Databases"**
3. Selecciona **Create New Database**
4. Nombre: `zona_fit_db`
5. Click **OK**

### Opción B: Usando SQL Editor
1. Click derecho en tu conexión > **SQL Editor > Open SQL Script**
2. Escribe:
```sql
CREATE DATABASE zona_fit_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```
3. Click en el botón **Execute** (▶️) o presiona `Ctrl+Enter` (Mac: `Cmd+Return`)

### Verificar:
1. Expande **Databases** en el panel izquierdo
2. Deberías ver `zona_fit_db`

---

## 5. Crear Tabla

### Paso 1: Seleccionar Base de Datos
1. En el panel izquierdo, click derecho en `zona_fit_db`
2. Selecciona **Set Active Database**

### Paso 2: Abrir SQL Editor
1. Click derecho en `zona_fit_db`
2. Selecciona **SQL Editor > Open SQL Script**

### Paso 3: Ejecutar Script de Tabla
Copia y pega este código:

```sql
USE zona_fit_db;

CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    membresia INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insertar datos de prueba
INSERT INTO cliente (nombre, apellido, membresia) VALUES
('Juan', 'Pérez', 1),
('María', 'García', 2),
('Carlos', 'López', 1);

-- Verificar
SELECT * FROM cliente;
```

### Paso 4: Ejecutar
1. Selecciona todo el código (Cmd+A / Ctrl+A)
2. Click en **Execute SQL Statement** (▶️)
3. Deberías ver los 3 registros insertados

---

## 6. Configurar Conexión Python

### Verificar credenciales de MySQL:
1. En DBeaver, click derecho en tu conexión
2. **Edit Connection**
3. Anota:
   - Host: `localhost`
   - Port: `3306`
   - Username: `root`
   - Password: (la que configuraste)

### Crear archivo de configuración:
Crea el archivo `src/zona_fit_db/conexion.py`:

```python
from mysql.connector import pooling
from mysql.connector import Error

class Conexion:
    DATABASE = 'zona_fit_db'
    USERNAME = 'root'          # ⬅️ Tu usuario MySQL
    PASSWORD = ''              # ⬅️ Tu contraseña MySQL (o vacío)
    HOST = 'localhost'
    PORT = '3306'
    POOL_SIZE = 5
    POOL_NAME = 'zona_fit_pool'
    pool = None

    @classmethod
    def obtener_pool(cls):
        if cls.pool is None:
            try:
                cls.pool = pooling.MySQLConnectionPool(
                    pool_name=cls.POOL_NAME,
                    pool_size=cls.POOL_SIZE,
                    host=cls.HOST,
                    port=cls.PORT,
                    database=cls.DATABASE,
                    user=cls.USERNAME,
                    password=cls.PASSWORD
                )
                print(f'✓ Pool de conexiones creado: {cls.POOL_NAME}')
                return cls.pool
            except Error as e:
                print(f'✗ Error al obtener pool: {e}')
                return None
        else:
            return cls.pool

    @classmethod
    def obtener_conexion(cls):
        try:
            pool = cls.obtener_pool()
            if pool:
                return pool.get_connection()
            return None
        except Error as e:
            print(f'✗ Error al obtener conexión: {e}')
            return None

    @classmethod
    def liberar_conexion(cls, conexion):
        try:
            conexion.close()
        except Error as e:
            print(f'✗ Error al liberar conexión: {e}')

    @classmethod
    def cerrar_conexiones(cls):
        try:
            if cls.pool:
                cls.pool = None
                print('✓ Pool de conexiones cerrado')
        except Error as e:
            print(f'✗ Error al cerrar pool: {e}')


if __name__ == '__main__':
    # Prueba de conexión
    conexion1 = Conexion.obtener_conexion()
    if conexion1:
        print('✓ Conexión 1 exitosa')
        Conexion.liberar_conexion(conexion1)
    
    conexion2 = Conexion.obtener_conexion()
    if conexion2:
        print('✓ Conexión 2 exitosa')
        Conexion.liberar_conexion(conexion2)
```

### Probar conexión:
```bash
cd src/zona_fit_db
python conexion.py
```

Deberías ver:
```
✓ Pool de conexiones creado: zona_fit_pool
✓ Conexión 1 exitosa
✓ Conexión 2 exitosa
```

---

## 7. Troubleshooting

### ❌ Error: Can't connect to MySQL server

**Causa:** MySQL no está corriendo

**Solución:**
```bash
# Verificar status
brew services list

# Si no está corriendo, iniciar
brew services start mysql

# Verificar puerto
sudo lsof -i :3306
```

---

### ❌ Error: Access denied for user 'root'

**Causa:** Contraseña incorrecta

**Solución:**
```bash
# Resetear contraseña de root
mysql.server stop
sudo mysqld_safe --skip-grant-tables &
mysql -u root

# En MySQL:
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nueva_contraseña';
quit;

# Reiniciar MySQL
brew services restart mysql
```

---

### ❌ Error: Unknown database 'zona_fit_db'

**Causa:** Base de datos no existe

**Solución:** Ve a [Paso 4](#4-crear-base-de-datos)

---

### ❌ Python no encuentra el módulo mysql.connector

**Solución:**
```bash
pip install mysql-connector-python
```

---

## 📊 Visualizar Datos en DBeaver

### Ver tabla:
1. Expande `zona_fit_db > Tables`
2. Doble click en `cliente`
3. Click en la pestaña **Data**
4. Verás todos los registros

### Ejecutar consultas:
1. Click derecho en `zona_fit_db`
2. **SQL Editor > Open SQL Script**
3. Escribe tu query:
```sql
SELECT * FROM cliente WHERE membresia = 1;
```
4. Execute (▶️)

---

## ✅ Checklist Final

Antes de ejecutar la app Python:

- [ ] MySQL está corriendo: `brew services list`
- [ ] Base de datos `zona_fit_db` existe en DBeaver
- [ ] Tabla `cliente` existe con datos de prueba
- [ ] Archivo `conexion.py` tiene credenciales correctas
- [ ] Test de conexión funciona: `python zona_fit_db/conexion.py`
- [ ] Módulo instalado: `pip install mysql-connector-python`

---

## 🚀 Ejecutar App

```bash
cd src
python main.py
```

Deberías ver:
```
Iniciando Sistema de Gestión de Clientes...

    *** Sistema de Gestión de Clientes - Smart Fit ***
    1. Listar clientes
    2. Agregar cliente
    3. Actualizar cliente
    4. Eliminar cliente
    5. Salir
```

---

## 📚 Recursos Adicionales

- DBeaver Docs: https://dbeaver.com/docs/
- MySQL Docs: https://dev.mysql.com/doc/
- MySQL Python Connector: https://dev.mysql.com/doc/connector-python/

---

¡Listo! 🎉 Ahora tienes MySQL configurado con DBeaver y listo para usar con Python.