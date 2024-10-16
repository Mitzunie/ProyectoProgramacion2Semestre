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
    tlink = "https://sismologia.cl/"
    status = requests.get(tlink)
    print(colored("\n> Verificando URL...\n", "yellow"))
    if status.status_code == 200:
        print(colored("> URL Valida!", "green"))
        
        service = Service(executable_path="driver/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        
        try:
            driver.get(tlink)
            time.sleep(3)
            
            tabla_sismologia = driver.find_element(By.CLASS_NAME, "sismologia")
            filas = tabla_sismologia.find_elements(By.TAG_NAME, 'tr')[1:]
                       # Listas para almacenar magnitudes y detalles de los sismos
            sismos = []

            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if len(celdas) >= 6:  # Asegurarse de que hay al menos 6 columnas
                    magnitud_str = celdas[5].text.strip()  # Extrae la magnitud

                    try:
                        magnitud = float(magnitud_str.replace(",", "."))
                        # Almacena un diccionario con la información relevante
                        sismos.append({
                            "fecha": celdas[0].text.strip(),
                            "lugar": celdas[1].text.strip(),
                            "profundidad": celdas[2].text.strip(),
                            "magnitud": magnitud
                        })

                    except ValueError:
                        print(colored(f"Error al convertir magnitud: {magnitud_str}", "red"))

            # Ordenar los sismos por magnitud de mayor a menor
            sismos_ordenados = sorted(sismos, key=lambda x: x['magnitud'], reverse=True)

            # Mostrar el top 3
            print(colored("\n> Top 3 sismos de mayor magnitud:\n", "green"))
            for i, sismo in enumerate(sismos_ordenados[:3]):
                print(colored(f"{i+1}. Fecha: {sismo['fecha']} | Lugar: {sismo['lugar']} | Magnitud: {sismo['magnitud']} | Profundidad: {sismo['profundidad']}", "cyan"))

        except Exception as e:
            print(colored(f"\n> Ocurrió un error: {str(e)}\n", "red"))

        finally:
            driver.quit()

    else:
        print(colored(">> Ups!, Algo ha salido mal. La URL puede ser inválida.", "red"))

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

#url = "https://www.sismologia.cl/"
url = "https://www.sismologia.cl/sismicidad/catalogo/2024/10/20241015.html"

respuesta = requests.get(url)

print(colored("\n----------========== Verificando Conexión ==========----------\n","light_yellow"))
if respuesta.status_code == 200:
    print(colored("           > Conexión Establecida Exitosamente!\n","green"))
    print(colored("----------==========================================----------\n","light_yellow"))

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