import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import datetime
from termcolor import colored

def opt():
    while True:
        opcion = input("> Ingresa la tarea que deseas ejecutar: ")
        if opcion.isdigit():
            opcion = int(opcion)
            return opcion
        else:
            print(colored("\n----------========== Advertencia ==========----------\n", "red"))
            print(colored(f"> La opción ingresada [{opcion}] es invalida.", "yellow"))
            print(colored("\n----------=================================----------\n", "red"))
        return    
def tarea1():
    return
def tarea2():
    Year = datetime.datetime.today().strftime("%Y")
    Month = datetime.datetime.today().strftime("%m")
    CompleteDate = datetime.datetime.today().strftime("%Y%m%d")
    today_url = f"https://www.sismologia.cl/sismicidad/catalogo/{Year}/{Month}/{CompleteDate}.html"
    status = requests.get(today_url)
    print(colored("\n> Validando URL...\n", "yellow"))
    if status.status_code == 200:
        print(colored(">> URL Valida!\n", "green"))
        #Funcionalidad del Codigo
        
        service = Service(executable_path="driver/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        
        try :
            driver.get(today_url)
            time.sleep(3)
            
            tabla_sismos = driver.find_element(By.CSS_SELECTOR, ".sismologia.detalle")
            filas = tabla_sismos.find_elements(By.TAG_NAME, 'tr')[1:]
            
            profundidades = []
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    # Suponemos que la profundidad está en la columna 5 (índice 4)
                 profundidad_str = celdas[3].text.strip()  # Elimina espacios adicionales
                 profundidad_str = profundidad_str.replace("km", "").strip()  # Elimina 'km' y espacios
                 
                try:
                    profundidad = float(profundidad_str.replace(",", "."))  # Convierte a float
                    profundidades.append(profundidad)
                except ValueError:
                    print(colored(f"\n> Error al convertir profundidad: {profundidad_str}\n", "red"))
            
            # Sumar todas las profundidades recolectadas
            if profundidades:
                profundidad_total = sum(profundidades)
                print(colored(f"\n> La profundidad acumulada de hoy ({fecha_actual}) es de: {profundidad_total} km.\n", "green"))
        except Exception as e:
            print(colored(f"\n> Ocurrió un error: {str(e)}\n", "red"))
        
        finally:
            driver.quit()
        
    else:
        print(colored(">> Ups!, Algo ha salido mal. La URL puede ser inválida.", "red"))
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

url = "https://www.sismologia.cl/"


respuesta = requests.get(url)

print(colored("\n----------========== Verificando Conexión ==========----------\n","light_yellow"))
if respuesta.status_code == 200:
    print(colored("> Conexión Establecida Exitosamente!\n","green"))
    print(colored("----------========================================----------\n","light_yellow"))

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
            print(colored("\n> Finalizando programa, ¡Hasta la Proxima!\n","red"))
            break
            
elif respuesta.status_code == 404:
    print(colored(f">Conexión Fallida, No se encuentra la página que buscas...\nCODE: {respuesta.status_code}", "red"))
    print(colored("\n----------==========================================----------\n","light_yellow"))
elif respuesta.status_code == 204:
    print(colored(f"Conexión Exitosa, Lamentablemente no se encuentran datos para devolver.\nCODE: {respuesta.status_code}", "yellow"))
    print(colored("\n----------==========================================----------\n","light_yellow"))
elif respuesta.status_code == 403:
    print(colored(f"Conexión Fallida (FORBIDDEN), El servidor detecta la petición pero el servidor no cumple con esta.\nCODE: {respuesta.status_code}", "red"))
    print(colored("\n----------==========================================----------\n","light_yellow"))
else: 
    print(colored(f"Conexión Fallida: {respuesta.status_code}.", "red"))
    print(colored("\n----------==========================================----------\n","light_yellow"))