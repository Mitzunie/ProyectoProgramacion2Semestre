import requests
import selenium
import pandas as pd
import datetime

def opt():
    while True:
        opcion = input("> Ingresa la tarea que deseas ejecutar: ")
        if opcion.isdigit():
            opcion = int(opcion)
            return opcion
        else:
            print("\n----------========== Advertencia ==========----------\n> Opción Invalida, Vuelve a intentarlo...\n----------=================================----------")
        return    
def tarea1():
    return
def tarea2():
    return
def tarea3():
    return
def tarea4():
    print("\n> Debes ingresar el intervalo de tiempo para buscar los sismos.\n")
    print("\n>> Fecha de Inicio Intervalo <<\n")
    año1 = input("> Ingresa el año:")
    mes1 = input("> Ingresa el mes:")
    dia1 = input("> Ingresa el día:")
    print("\n>> Fecha de Finalización Intervalo <<\n")
    año2 = input("> Ingresa el año:")
    mes2 = input("> Ingresa el mes:")
    dia2 = input("> Ingresa el día:")
    
    fecha_inicio = datetime.datetime(int(año1), int(mes1), int(dia1))
    fecha_fin = datetime.datetime(int(año2), int(mes2), int(dia2))
    
    while fecha_inicio > fecha_actual or fecha_fin > fecha_actual:
        print("\n> Fecha invalida, no puedes ver el futuro...\n")
        print("\n>> Fecha de Inicio Intervalo <<\n")
        año1 = input("> Ingresa el año:")
        mes1 = input("> Ingresa el mes:")
        dia1 = input("> Ingresa el día:")
        print("\n>> Fecha de Finalización Intervalo <<\n")
        año2 = input("> Ingresa el año:")
        mes2 = input("> Ingresa el mes:")
        dia2 = input("> Ingresa el día:")
    
    return
def tarea5():
    return
def tarea6():
    return
def tarea7():
    return
def tarea8():
    return
def tarea9():
    return
def tarea10():
    return

url = "https://www.sismologia.cl/sismicidad/catalogo/2024/09/20240920.html"

respuesta = requests.get(url)

print("\n------====== Verificación de Conexión ======------\n\nIniciando Conexión...\n")
if respuesta.status_code == 200:
    print("Conexión Exitosa...")
elif respuesta.status_code == 404:
    print(f"Conexión Fallida, No se encuentra la página que buscas...\nCODE: {respuesta.status_code}")
elif respuesta.status_code == 204:
    print(f"Conexión Exitosa, Lamentablemente no se encuentran datos para devolver.\nCODE: {respuesta.status_code}")
elif respuesta.status_code == 403:
    print(f"Conexión Fallida (FORBIDDEN), El servidor detecta la petición pero el servidor no cumple con esta.\nCODE: {respuesta.status_code}")
else: 
    print(f"Conexión Fallida: {respuesta.status_code}.")
print("\n------======================================------\n")

fecha_actual = datetime.datetime.today().strftime('%d/%m/%Y')

while True:
    print("¡Bienvenido(a)!, ¿Qué deseas hacer?")
    print("1.- Mostrar Ranking de 3 Sismos con Mayor Magnitud")
    print(f"2.- Mostrar Profundidad Acumulada De Todos los Sismos del Día({fecha_actual}).")
    print("3.- Mostrar Sismo De Menor Magnitud")
    print("4.- Mostrar Sismos Ocurridos En Un Intervalo De Tiempo.")
    print("5.- Mostrar Datos Del Ultimo Sismo.")
    print("6.- Mostrar Tiempo Transcurrido Desde El Ultimo Sismo")
    print("7.- Enviar Información Del Ultimo Sismo Al Correo")
    print("8.- Mostrar Grafico Intensidad de Sismos")
    print("9.- Mostrar Grafico Profundidad")
    print("10.- Grafico Comparativo Sismos")
    print("0.- Salir del Programa")
    
    opcion = opt()
    
    if opcion == 1:
        tarea1()
    elif opcion == 2:
        tarea2()
    elif opcion == 3:
        tarea3()
    elif opcion == 4:
        tarea4()
    elif opcion == 5:
        tarea5()
    elif opcion == 6:
        tarea6()
    elif opcion == 7:
        tarea7()
    elif opcion == 8:
        tarea8()
    elif opcion == 9:
        tarea9()
    elif opcion == 10:
        tarea10()
    elif opcion == 0:
        print("\nFinalizando Programa, ¡Adiós!\n")
        break
    else:
        print("\n> La opción Ingresada es INVALIDA, Reintentalo Nuevamente...\n")