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
        opcion = input(colored("\n> Ingresa la tarea que deseas ejecutar: ", "cyan"))
        if opcion.isdigit():
            opcion = int(opcion)
            return opcion
        else:
            print(colored("\n----------========== Advertencia ==========----------\n", "red"))
            print(colored(f"> La opción ingresada [{opcion}] es invalida.", "yellow"))
            print(colored("\n----------=================================----------\n", "red"))
        return    
def tarea1():
    Year = datetime.datetime.today().strftime("%Y")
    Month = datetime.datetime.today().strftime("%m")
    CompleteDate = datetime.datetime.today().strftime("%Y%m%d")
    today_url = f"https://www.sismologia.cl/sismicidad/catalogo/{Year}/{Month}/{CompleteDate}.html"
    status = requests.get(today_url)
    print(colored("\n> Verificando URL...\n", "yellow"))
    if status.status_code == 200:
        print(colored("> URL Valida!", "green"))
        
        service = Service(executable_path="driver/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        
        try:
            driver.get(today_url)
            time.sleep(3)
            
            tabla_sismos = driver.find_element(By.CSS_SELECTOR, ".sismologia.detalle")
            filas = tabla_sismos.find_elements(By.TAG_NAME, 'tr')[1:]
            '''
            magnitud = []
            profundidad = []
            ubicacion = []
            fecha = []
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    magnitud_str = celdas[4].text.strip()
                    profundidad_str = celdas[3].text.strip()
                    ubicacion_str = celdas[1].text.strip()
                    fecha_str = celdas[2].text.strip()
                    
                try:
                    magnitud_str = str(magnitud_str)
                    profundidad_str = str(profundidad_str)
                    ubicacion_str = str(ubicacion_str)
                    magnitud.append(magnitud_str)
                    profundidad.append(profundidad_str)
                    ubicacion.append(ubicacion_str)
                    fecha.append(fecha_str)
                except ValueError:
                    print(colored(f">> Error: No se pudo convertir un dato. > {magnitud_str} {profundidad_str} {ubicacion_str} {fecha_str} <", "red"))
            '''
            sismos = []  # Lista para almacenar los sismos como diccionarios
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    # Extraer datos de cada columna
                    magnitud_str = celdas[4].text.strip()  # Columna de magnitud
                    profundidad_str = celdas[3].text.strip()  # Columna de profundidad
                    ubicacion_str = celdas[0].text.strip()  # Columna de ubicación
                    fecha_str = celdas[1].text.strip()  # Columna de fecha
                    
                    try:
                        # Convertimos la magnitud a float para poder ordenarla
                        magnitud_str = magnitud_str.replace("Ml", "")
                        magnitud_str = magnitud_str.replace(" ", "")
                        magnitud = float(magnitud_str)
                        profundidad_str = profundidad_str.replace("km", "")
                        profundidad_str = profundidad_str.replace(" ", "")
                        profundidad = int(profundidad_str)
                        fecha_str, ubicacion = ubicacion_str.split("\n")
                        # Guardamos los detalles del sismo en un diccionario
                        sismo = {
                            'magnitud': magnitud,
                            'profundidad': profundidad,
                            'ubicacion': ubicacion,
                            'fecha': fecha_str
                        }
                        sismos.append(sismo)
                    except ValueError:
                        print(colored(f">> Error: No se pudo convertir la magnitud o profundidad: {magnitud_str} {profundidad_str}", "red"))
            
            sismos_ordenados = sorted(sismos, key=lambda x: x['magnitud'], reverse=True)
            
            # Mostrar los 3 sismos de mayor magnitud
            print(colored("\n> Top 3 sismos de mayor magnitud:\n", "green"))
            for i, sismo in enumerate(sismos_ordenados[:3]):
                print(colored(f"{i + 1}. Fecha y Hora: {sismo['fecha']} | Ubicación: {sismo['ubicacion']} | Magnitud: {sismo['magnitud']} Ml | Profundidad: {sismo['profundidad']} Km\n", "yellow"))
            
        finally:
            driver.quit()

    else:
        print(colored("> Error: No se pudo acceder a la URL", "red"))
            
            
         
    return

def tarea2():
    Year = datetime.datetime.today().strftime("%Y")
    Month = datetime.datetime.today().strftime("%m")
    CompleteDate = datetime.datetime.today().strftime("%Y%m%d")
    today_url = f"https://www.sismologia.cl/sismicidad/catalogo/{Year}/{Month}/{CompleteDate}.html"
    status = requests.get(today_url)
    print(colored("\n> Validando URL...\n", "yellow"))
    if status.status_code == 200:
        print(colored(">> URL Valida!", "green"))
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
                 profundidad_str = celdas[3].text.strip()
                 profundidad_str = profundidad_str.replace("km", "").strip()
                 
                try:
                    profundidad = int(profundidad_str.replace(",", "."))
                    profundidades.append(profundidad)
                except ValueError:
                    print(colored(f"\n> Error al convertir profundidad: {profundidad_str}\n", "red"))
            
          
            if profundidades:
                profundidad_total = sum(profundidades)
                print(colored(f"\n> La profundidad acumulada de hoy ({fecha_actual}) es de: {profundidad_total} km.\n", "green"))
        except Exception as e:
            print(colored(f"\n> Ocurrió un error: {str(e)}\n", "red"))
        
        finally:
            driver.quit()
        
    else:
        print(colored(">> Ups!, Algo ha salido mal. La URL puede ser inválida.\n", "red"))
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
    print(colored("           > Conexión Establecida Exitosamente!\n","green"))
    print(colored("----------==========================================----------\n","light_yellow"))

    fecha_actual = datetime.datetime.today().strftime('%d/%m/%Y')

    while True:
        print("¡Bienvenido(a)!, ¿Qué deseas hacer?")
        print(f"1.- Mostrar Ranking de 3 Sismos con Mayor Magnitud")
        print(f"2.- Mostrar Profundidad Acumulada De Todos los Sismos del Día({fecha_actual})")
        print(f"3.- Mostrar Sismo De Menor Magnitud")
        print("4.- Mostrar Sismos Ocurridos En Un Intervalo De Tiempo.")
        print(f"5.- Mostrar Datos Del Ultimo Sismo.")
        print(f"6.- Mostrar Tiempo Transcurrido Desde El Ultimo Sismo")
        print("7.- Enviar Información Del Ultimo Sismo Al Correo")
        print(f"8.- Mostrar Grafico Intensidad de Sismos")
        print(f"9.- Mostrar Grafico Profundidad")
        print(f"10.- Grafico Comparativo Sismos")
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
    print(colored("     > Status: Conexión Fallida", "red"))
    print(colored("     > Detalles: No se encuentra la página que buscas...", "yellow"))
    print(colored(f"     > CODE: {respuesta.status_code}", "red"))
    print(colored("     > Finalizando Programa Debido a problemas con la conexión. <", "red"))
    print(colored("\n----------==========================================----------\n","light_yellow"))
elif respuesta.status_code == 204:
    print(colored("     > Status: Conexión Exitosa", "green"))
    print(colored("     > Detalles: No se encuentran datos para devolver.", "red"))
    print(colored(f"     > CODE: {respuesta.status_code}", "red"))
    print(colored("     > Finalizando Programa Debido a problemas con la conexión. <", "red"))
    print(colored("\n----------==========================================----------\n","light_yellow"))
elif respuesta.status_code == 403:
    print(colored("     > Status: Conexión Fallida (FORBIDDEN)", "red"))
    print(colored("     > Detalles: El servidor detecta la petición pero el servidor no cumple con esta.", "red"))
    print(colored(f"     > CODE: {respuesta.status_code}", "red"))
    print(colored("     > Finalizando Programa Debido a problemas con la conexión. <", "red"))
    print(colored("\n----------==========================================----------\n","light_yellow"))
else: 
    print(colored("     > Status: Conexión Fallida", "red"))
    print(colored(f"     >  CODE: {respuesta.status_code}", "red"))
    print(colored("     > Finalizando Programa Debido a problemas con la conexión. <", "red"))
    print(colored("\n----------==========================================----------\n","light_yellow"))