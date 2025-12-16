from models.ClienteClass import Cliente
from models.DAOClass import ClienteDAO


def mostrar_menu():
    print("""
    *** Sistema de Gestión de Clientes - Smart Fit ***
    1. Listar clientes
    2. Agregar cliente
    3. Actualizar cliente
    4. Eliminar cliente
    5. Salir
    """)


def listar_clientes():
    print("\n--- Listado de Clientes ---")
    clientes = ClienteDAO.seleccionar()
    if clientes:
        for cliente in clientes:
            print(cliente)
    else:
        print("No hay clientes registrados")


def agregar_cliente():
    print("\n--- Agregar Nuevo Cliente ---")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    membresia = int(input("Membresía: "))
    
    cliente = Cliente(nombre=nombre, apellido=apellido, membresia=membresia)
    registros_insertados = ClienteDAO.insertar(cliente)
    
    if registros_insertados:
        print(f"✓ Cliente agregado exitosamente. Registros insertados: {registros_insertados}")
    else:
        print("✗ Error al agregar cliente")


def actualizar_cliente():
    print("\n--- Actualizar Cliente ---")
    id_cliente = int(input("ID del cliente a actualizar: "))
    nombre = input("Nuevo nombre: ")
    apellido = input("Nuevo apellido: ")
    membresia = int(input("Nueva membresía: "))
    
    cliente = Cliente(id_cliente, nombre, apellido, membresia)
    registros_actualizados = ClienteDAO.actualizar(cliente)
    
    if registros_actualizados:
        print(f"✓ Cliente actualizado exitosamente. Registros actualizados: {registros_actualizados}")
    else:
        print("✗ Error al actualizar cliente o cliente no encontrado")


def eliminar_cliente():
    print("\n--- Eliminar Cliente ---")
    id_cliente = int(input("ID del cliente a eliminar: "))
    
    cliente = Cliente(id_cliente=id_cliente)
    registros_eliminados = ClienteDAO.eliminar(cliente)
    
    if registros_eliminados:
        print(f"✓ Cliente eliminado exitosamente. Registros eliminados: {registros_eliminados}")
    else:
        print("✗ Error al eliminar cliente o cliente no encontrado")


def main():
    while True:
        try:
            mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                listar_clientes()
            elif opcion == "2":
                agregar_cliente()
            elif opcion == "3":
                actualizar_cliente()
            elif opcion == "4":
                eliminar_cliente()
            elif opcion == "5":
                print("\n¡Hasta luego!")
                break
            else:
                print("\n✗ Opción no válida. Por favor, seleccione una opción del 1 al 5.")
        
        except ValueError as ve:
            print(f"\n✗ Error de entrada: {ve}. Por favor ingrese valores válidos.")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    print("Iniciando Sistema de Gestión de Clientes...")
    main()
