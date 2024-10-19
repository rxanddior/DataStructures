import random as rd
import sys
import datetime
import sqlite3
from sqlite3 import Error
from datetime import date, datetime, timedelta
import openpyxl

# Crea una tabla en SQLite3
def Crear_tabla():
    try:
        with sqlite3.connect("34.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios (clave INTEGER PRIMARY KEY, nombre TEXT NOT NULL);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS Salas (clave INTEGER PRIMARY KEY, nombre TEXT NOT NULL, capacidad INTEGER NOT NULL);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS Reservaciones (folio INTEGER PRIMARY KEY, nombre TEXT NOT NULL, horario TEXT NOT NULL, fecha TIMESTAMP);")
            print("Tablas creadas exitosamente")
    except Error as e:
        print(e)
    except Exception as e:
        print(f"Se produjo el siguiente error: {e}")

Crear_tabla()

# Opción 1: Registrar Reservación
def Registrar_Reservacion():
    while True:
        valor_clave = int(input("¿Cuál es tu clave de cliente: "))
        try:
            with sqlite3.connect("34.db") as conn:
                mi_cursor = conn.cursor()
                valores = {"clave": valor_clave}
                mi_cursor.execute("SELECT * FROM Usuarios WHERE clave = :clave", valores)
                registro = mi_cursor.fetchall()

                if registro:
                    for clave, nombre in registro:
                        print(f"{clave}\t{nombre}")
                else:
                    print(f"No se encontró un cliente asociado con la clave {valor_clave}")
                    continue
        except Error as e:
            print(e)
        except Exception as e:
            print(f"Se produjo el siguiente error: {e}")
            continue

        Nombre = input("Ingresa el nombre de la reservación (Escribe SALIR para regresar al menú): ")
        if Nombre == 'SALIR':
            return

        Horario = input("¿Cuál es el horario que quieres? [M, V, N]: ")
        Fecha_Ingresada = input("Ingresa la fecha de reservación (dd/mm/aaaa): ")

        # Validar formato de fecha
        try:
            Fecha_dt = datetime.strptime(Fecha_Ingresada, '%d/%m/%Y')
        except ValueError:
            print("Formato de fecha no válido. Por favor, ingresa la fecha en el formato correcto (dd/mm/aaaa).")
            continue

        fecha_permitida = datetime.now() + timedelta(days=2)
        if Fecha_dt < fecha_permitida:
            print("Debes hacer la reservación con 2 días de anticipación.")
            continue

        nivel = rd.randint(1, 99)
        try:
            with sqlite3.connect("34.db") as conn:
                mi_cursor = conn.cursor()
                Miami = {"folio": nivel, "nombre": Nombre, "horario": Horario, "fecha": Fecha_dt}
                mi_cursor.execute("INSERT INTO Reservaciones VALUES (:folio, :nombre, :horario, :fecha)", Miami)
                conn.commit()  # Guardar los cambios insertados
                print("¡Reservación Realizada con éxito!")
        except Error as e:
            print(e)
        except Exception as e:
            print(f"Surgió una falla siendo esta la causa: {e}")

# Opción 2: Modificar descripciones de la reservación
def modificar_descripciones():
    while True:
        llave = input("¿Cuál es el nombre de tu reservación: ")
        try:
            with sqlite3.connect("34.db") as conn:
                mi_cursor = conn.cursor()
                valores1 = {"nombre": llave}
                mi_cursor.execute("SELECT * FROM Reservaciones WHERE nombre = :nombre", valores1)
                registro = mi_cursor.fetchall()

                if registro:
                    for folio, nombre, horario, fecha in registro:
                        print("Clave\tNombre\tTurno\tFecha")
                        print(f"{folio}\t{nombre}\t{horario}\t{fecha}")
                else:
                    print(f"No se encontró una reservación asociada con el nombre {llave}")
                    continue
        except Error as e:
            print(e)
        except Exception as e:
            print(f"Se produjo el siguiente error: {e}")
            continue

        nuevo_nombre = input("¿A qué nombre lo quieres cambiar?: ")
        id_number = folio
        Turno = horario
        fecha_dt = fecha
        try:
            with sqlite3.connect("34.db") as conn:
                mi_cursor = conn.cursor()
                Sydney = {"folio": id_number, "nombre": nuevo_nombre, "turno": Turno, "fecha": fecha_dt}
                mi_cursor.execute("UPDATE Reservaciones SET nombre = :nombre WHERE folio = :folio;", Sydney)
                conn.commit()  # Guardar los cambios insertados
                print("Modificación realizada con éxito.")
                return
        except Error as e:
            print(e)
        except Exception as e:
            print(f"Surgió una falla siendo esta la causa: {e}")

# Opción 3: Consultar si una fecha está disponible
def consulta_fecha():
    fecha_consultar = input("Dime una fecha (dd/mm/aaaa): ")
    try:
        fecha_consultar = datetime.strptime(fecha_consultar, "%d/%m/%Y")
    except ValueError:
        print("Formato de fecha no válido. Por favor, ingresa la fecha en el formato correcto (dd/mm/aaaa).")
        return

    try:
        with sqlite3.connect("34.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            criterios = {"fecha": fecha_consultar}
            mi_cursor.execute("SELECT folio, nombre, horario, fecha FROM Reservaciones WHERE fecha = :fecha", criterios)
            registros = mi_cursor.fetchall()

            if registros:
                print(f"La fecha {fecha_consultar.strftime('%d/%m/%Y')} NO está disponible.")
            else:
                print(f"La fecha {fecha_consultar.strftime('%d/%m/%Y')} está disponible.")
    except Error as e:
        print(e)
    except Exception as e:
        print(f"Se produjo el siguiente error: {e}")

# Opción 4: Reporte de reservaciones por fecha
def reporte_reservaciones_por_fecha():
    fecha_consultar = input("Dime una fecha (dd/mm/aaaa): ")
    try:
        fecha_consultar = datetime.strptime(fecha_consultar, "%d/%m/%Y")
    except ValueError:
        print("Formato de fecha no válido. Por favor, ingresa la fecha en el formato correcto (dd/mm/aaaa).")
        return

    try:
        with sqlite3.connect("34.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            criterios = {"fecha": fecha_consultar}
            mi_cursor.execute("SELECT folio, nombre, horario, fecha FROM Reservaciones WHERE fecha = :fecha", criterios)
            conn.commit()  # Guardar los cambios insertados
            registros = mi_cursor.fetchall()

            if registros:
                print(f"Reservaciones para la fecha {fecha_consultar.strftime('%d/%m/%Y')}:")
                for folio, nombre, horario, fecha in registros:
                    print(f'Folio: {folio}, Nombre: {nombre}, Horario: {horario}, Fecha: {fecha}')
            else:
                print(f"No hay reservaciones para esa fecha.")
    except Error as e:
        print(e)
    except Exception as e:
        print(f"Se produjo el siguiente error: {e}")

# Opción 5: Registrar Sala
def Registrar_Sala():
    while True:
        SALA = input("¿Cómo se va a llamar la sala? (Escribe SALIR para regresar al menú): ")
        if SALA == 'SALIR':
            return
        if not SALA:
            print("El nombre de la sala no puede estar vacío.")
            continue

        capacity = int(input("¿Cuál va a ser la capacidad?: "))
        N = rd.randint(1, 99)
        try:
            with sqlite3.connect("34.db") as conn:
                mi_cursor = conn.cursor()
                Valores5 = {"clave": N, "nombre": SALA, "capacidad": capacity}
                mi_cursor.execute("INSERT INTO Salas (clave, nombre, capacidad) VALUES(:clave, :nombre, :capacidad)", Valores5)
                conn.commit()  # Guardar los cambios insertados
                print("Sala registrada!")
                print(f"Tu clave de la sala es: {N}")
        except Error as e:
            print(e)
        except Exception as e:
            print(f"Surgió una falla siendo esta la causa: {e}")

# Opción 6: Registrar Cliente
def Registrar_Cliente():
    while True:
        Usuario = input("Ingresa al usuario. (Escribe SALIR si quieres regresar al menú principal): ")
        if Usuario == 'SALIR':
            return
        if not Usuario:
            print("El nombre del usuario no puede estar vacío.")
            continue

        N = rd.randint(1, 99)
        try:
            with sqlite3.connect("34.db") as conn:
                mi_cursor = conn.cursor()
                Valores3 = {"clave": N, "nombre": Usuario}
                mi_cursor.execute("INSERT INTO Usuarios (clave, nombre) VALUES(:clave, :nombre)", Valores3)
                conn.commit()  # Guardar los cambios insertados
                print("Usuario registrado!")
                print(f"Tu clave de usuario es: {N}")
        except Error as e:
            print(e)
        except Exception as e:
            print(f"Surgió una falla siendo esta la causa: {e}")

# Opción 8: Eliminar reservación
def eliminar_reservacion():
    folio = int(input("Introduce el folio de la reservación que deseas eliminar: "))
    try:
        with sqlite3.connect("34.db") as conn:
            mi_cursor = conn.cursor()
            valores = {"folio": folio}
            mi_cursor.execute("DELETE FROM Reservaciones WHERE folio = :folio", valores)
            conn.commit()  # Guardar los cambios insertados
            if mi_cursor.rowcount > 0:
                print(f"Reservación con folio {folio} eliminada exitosamente.")
            else:
                print(f"No se encontró una reservación con folio {folio}.")
    except Error as e:
        print(e)
    except Exception as e:
        print(f"Se produjo el siguiente error: {e}")

# Opción 9: Exportar base de datos a Excel
def exportar_base_de_datos_a_excel():
    try:
        with sqlite3.connect("34.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT * FROM Reservaciones")
            conn.commit()  # Guardar los cambios insertados
            reservaciones = mi_cursor.fetchall()

        workbook = openpyxl.Workbook()
        hoja = workbook.active
        hoja.title = "Reservaciones"

        # Encabezados
        encabezados = ['Folio', 'Nombre', 'Horario', 'Fecha']
        hoja.append(encabezados)

        # Datos
        for reservacion in reservaciones:
            hoja.append(reservacion)

        # Guardar archivo Excel
        workbook.save("Reporte_Reservaciones.xlsx")
        print("Base de datos exportada a Excel exitosamente como 'Reporte_Reservaciones.xlsx'")
    except Exception as e:
        print(f"Surgió una falla siendo esta la causa: {e}")

# Menú principal
def menu():
    while True:
        print("---- MENÚ ----")
        print("1. Registrar Reservación")
        print("2. Modificar las descripciones de la reservación")
        print("3. Consulta la fecha disponible")
        print("4. Reporte de las reservaciones de una fecha")
        print("5. Registrar Sala")
        print("6. Registrar Cliente")
        print("7. Salir del programa")
        print("8. Eliminar reservación")
        print("9. Exportar base de datos a Excel")
        try:
            opcion = int(input("Selecciona una opción (1-9): "))
            if opcion == 1:
                Registrar_Reservacion()
            elif opcion == 2:
                modificar_descripciones()
            elif opcion == 3:
                consulta_fecha()
            elif opcion == 4:
                reporte_reservaciones_por_fecha()
            elif opcion == 5:
                Registrar_Sala()
            elif opcion == 6:
                Registrar_Cliente()
            elif opcion == 7:
                print("Saliendo del programa...")
                sys.exit()
            elif opcion == 8:
                eliminar_reservacion()
            elif opcion == 9:
                exportar_base_de_datos_a_excel()
            else:
                print("Opción no válida. Por favor, selecciona un número entre 1 y 9.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número entre 1 y 9.")     
        
menu()


