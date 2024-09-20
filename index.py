import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def opt():
    while True:
        return    
def tarea1():
    return
def tarea2():
    return
def tarea3():
    return
def tarea4():
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

print("\n------============------\n\nIniciando Conexión...\n")
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
print("\n------============------\n")

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
    
    opt = opt()
    
    if opt == 1:
        tarea1()
    elif opt == 2:
        tarea2()
    elif opt == 3:
        tarea3()
    elif opt == 4:
        tarea4()
    elif opt == 5:
        tarea5()
    elif opt == 6:
        tarea6()
    elif opt == 7:
        tarea7()
    elif opt == 8:
        tarea8()
    elif opt == 9:
        tarea9()
    elif opt == 10:
        tarea10()
    elif opt == 0:
        exit
    else:
        print("> La opción Ingresada es INVALIDA, Reintentalo Nuevamente...")