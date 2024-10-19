import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import datetime
from termcolor import colored
import smtplib
import email_validator
import matplotlib.pyplot as plt
import numpy as np

def opt():
    while True:
        opcion = input(colored("\n> Ingresa la tarea que deseas ejecutar: ", "cyan"))
        if str(opcion).isdigit():
            opcion = int(opcion)
            return opcion
        else:
            print(colored("\n----------========== Advertencia ==========----------\n", "red"))
            print(colored(f"> La opción ingresada [{opcion}] es invalida.", "yellow"))
            print(colored("\n----------=================================----------\n", "red"))
        return    
    
def validate_gmail(correo):
    try:
        validator = email_validator.validate_email(correo)
        print(colored(f"\n>> El correo: {correo} es valido!", "green"))
        return True
    except email_validator.EmailNotValidError:
        return False
    
def send_gmail(gmail, magnitud, profundidad, ubicacion, fecha):
    
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        email = "sismologiafinis@gmail.com"
        password = "pwmcsetzvjwlwfbn"
    
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email, password)

        from_email = email
        to_email = gmail
        subject = "Reporte Último Sismo Registrado"
        
        body = f"""
        <html>
        <body>
            <h2 style="color: #2E86C1;">Reporte del Último Sismo Registrado</h2>
            <p><strong>Datos del sismo:</strong></p>
            <ul>
                <li><strong>Ubicación:</strong> {ubicacion}</li>
                <li><strong>Magnitud:</strong> <span style="color: red;">{magnitud} Ml</span></li>
                <li><strong>Profundidad:</strong> {profundidad} Km</li>
                <li><strong>Fecha y Hora:</strong> {fecha}</li>
            </ul>
            <p>Este reporte fue generado por el sistema de <strong>Sismología Finis</strong>.</p>
            <p style="color: #5D6D7E;">Gracias por usar nuestro servicio.</p>
            <p style="color: #5D6D7E;">Fuente de la Información: https://www.sismologia.cl </p>
        </body>
        </html>
        """
        
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject

        message.attach(MIMEText(body, "html", "utf-8"))

        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        return print(colored("\n>> Correo Enviado, Revisa tu Inbox!\n", "green"))
    except Exception as e:
        print(colored(f"\n>> Error: {str(e)}", "red"))
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
  
            sismos = []
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    magnitud_str = celdas[4].text.strip()
                    profundidad_str = celdas[3].text.strip()
                    ubicacion_str = celdas[0].text.strip()  
                    fecha_str = celdas[1].text.strip()  
                    
                    try:
                        magnitud_str = magnitud_str.replace("Ml", "").replace("Mw", "").replace("Mww", "")
                        magnitud_str = magnitud_str.replace(" ", "")
                        magnitud = float(magnitud_str)
                        profundidad_str = profundidad_str.replace("km", "")
                        profundidad_str = profundidad_str.replace(" ", "")
                        profundidad = int(profundidad_str)
                        fecha_str, ubicacion = ubicacion_str.split("\n")
                    
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
        
        service = Service(executable_path="driver/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        
        try :
            driver.get(today_url)
            time.sleep(5)
            
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
            
            print(colored("\nProfundidades Obtenidas:", "yellow"))
            print(*profundidades, sep=", ")
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
            
            sismos = []
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    magnitud_str = celdas[4].text.strip()
                    profundidad_str = celdas[3].text.strip()
                    ubicacion_str = celdas[0].text.strip()  
                    fecha_str = celdas[1].text.strip()  
                    
                    try:
                        magnitud_str = magnitud_str.replace("Ml", "").replace("Mw", "").replace("Mww", "")
                        magnitud_str = magnitud_str.replace(" ", "")
                        magnitud = float(magnitud_str)
                        profundidad_str = profundidad_str.replace("km", "")
                        profundidad_str = profundidad_str.replace(" ", "")
                        profundidad = int(profundidad_str)
                        fecha_str, ubicacion = ubicacion_str.split("\n")
                    
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
            
            print(colored("\n> Sismo de Menor Magnitud: \n", "green"))
            for i, sismo in enumerate(sismos_ordenados[-1:]):
                print(colored(f"{i + 1}. Fecha y Hora: {sismo['fecha']} | Ubicación: {sismo['ubicacion']} | Magnitud: {sismo['magnitud']} Ml | Profundidad: {sismo['profundidad']} Km\n", "yellow"))
            
        finally:
            driver.quit()

    else:
        print(colored("> Error: No se pudo acceder a la URL", "red"))
            
    return

def tarea4():
    
    print("\n> Debes ingresar la fecha y el intervalo de horas para buscar los sismos.\n")
    while True:
        ano = input("> Ingresa el año (YYYY): ")
        mes = input("> Ingresa el mes (MM): ")
        dia = input("> Ingresa el día (DD): ")

        hora_inicio = input("> Ingresa la hora de inicio (HH:MM): ")
        hora_fin = input("> Ingresa la hora de finalización (HH:MM): ")

        fecha_inicio_str = f"{ano}-{mes}-{dia} {hora_inicio}"
        fecha_fin_str = f"{ano}-{mes}-{dia} {hora_fin}"

        fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d %H:%M')
        
        fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d %H:%M')

        hoy = datetime.datetime.now()
        
        if fecha_inicio >= fecha_fin:
            print(colored("> Error: La hora de inicio debe ser menor que la hora de fin.", "red"))
        elif fecha_inicio > hoy and fecha_fin > hoy:
            print("> No puedes ver sismos a futuro!")
        else:
            break

    CompleteDate = f"{ano}{mes}{dia}"
    today_url = f"https://www.sismologia.cl/sismicidad/catalogo/{ano}/{mes}/{CompleteDate}.html"

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

            sismos_en_rango = []

            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    magnitud_str = celdas[4].text.strip()
                    profundidad_str = celdas[3].text.strip().replace("km", "").replace(" ", "")
                    fecha_str, ubicacion_str = celdas[0].text.strip().split("\n")

                    try:
                        fecha_sismo = datetime.datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
                        magnitud_str = magnitud_str.replace("Ml", "").replace("Mw", "").replace("Mww", "")
                        profundidad = int(profundidad_str)
                        
                        if fecha_inicio <= fecha_sismo <= fecha_fin:
                            sismo = {
                                'fecha': fecha_sismo,
                                'magnitud': magnitud_str,
                                'ubicacion': ubicacion_str,
                                'profundidad': profundidad
                            }
                            sismos_en_rango.append(sismo)
                    except Exception as e:
                        print(colored(f"\n>> Error procesando los datos: {str(e)}", "red"))

            if sismos_en_rango:
                print(colored("\n> Sismos ocurridos en el intervalo de tiempo:", "green"))
                for i, sismo in enumerate(sismos_en_rango, 1):
                    print(colored(f"{i}. Fecha y Hora: {sismo['fecha']} | Ubicación: {sismo['ubicacion']} | Magnitud: {sismo['magnitud']} Ml | Profundidad: {sismo['profundidad']} Km", "yellow"))
            else:
                print(colored("> No se encontraron sismos en el intervalo de horas proporcionado.", "yellow"))

        except Exception as e:
            print(colored(f"\n> Ocurrió un error: {str(e)}\n", "red"))

        finally:
            print("\n")
            driver.quit()

    else:
        print(colored("> Error: No se pudo acceder a la URL", "red"))
        return
    
def tarea5():
    Year = datetime.datetime.today().strftime("%Y")
    Month = datetime.datetime.today().strftime("%m")
    CompleteDate = datetime.datetime.today().strftime("%Y%m%d")
    today_url = f"https://www.sismologia.cl/sismicidad/catalogo/{Year}/{Month}/{CompleteDate}.html"
    status = requests.get(today_url)
    print(colored("\n> Verificando URL...\n", "yellow"))

    if status.status_code == 200:
        print(colored("> URL Válida!", "green"))
        
        service = Service(executable_path="driver/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        
        try:
            driver.get(today_url)
            time.sleep(5)
            
            tabla_sismos = driver.find_element(By.CSS_SELECTOR, ".sismologia.detalle")
            filas = tabla_sismos.find_elements(By.TAG_NAME, 'tr')[1:]
            
            sismos = []
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    magnitud_str = celdas[4].text.strip()
                    profundidad_str = celdas[3].text.strip()
                    ubicacion_str = celdas[0].text.strip()  
                    fecha_str = celdas[1].text.strip()
                    
                    try:
                        magnitud_str = magnitud_str.replace("Ml", "").replace("Mw", "").replace("Mww", "").strip()
                        magnitud = float(magnitud_str)
                        profundidad_str = profundidad_str.replace("km", "").strip()
                        profundidad = int(profundidad_str)
                        fecha_str, ubicacion = ubicacion_str.split("\n")

                        sismo = {
                            'magnitud': magnitud,
                            'profundidad': profundidad,
                            'ubicacion': ubicacion,
                            'fecha': fecha_str
                        }
                        sismos.append(sismo)
                    except ValueError:
                        print(colored(f">> Error: No se pudo convertir la magnitud o profundidad: {magnitud_str} {profundidad_str}", "red"))
            
            if sismos:
                ultimo_sismo = sismos[0]
                print(colored("\n> Último sismo registrado:", "green"))
                print(f"- Fecha y Hora: {ultimo_sismo['fecha']}")
                print(f"- Ubicación: {ultimo_sismo['ubicacion']}")
                print(f"- Magnitud: {ultimo_sismo['magnitud']} Ml")
                print(f"- Profundidad: {ultimo_sismo['profundidad']} Km\n")
                
            else:
                print(colored("\n>> No se encontraron sismos para hoy.", "red"))
        
        finally:
            driver.quit()

    else:
        print(colored("> Error: No se pudo acceder a la URL", "red"))
        
    return

def tarea6():
    print("\n> Buscando el último sismo registrado...\n")
    
    Year = datetime.datetime.today().strftime("%Y")
    Month = datetime.datetime.today().strftime("%m")
    CompleteDate = datetime.datetime.today().strftime("%Y%m%d")
    today_url = f"https://www.sismologia.cl/sismicidad/catalogo/{Year}/{Month}/{CompleteDate}.html"
    fecha_actual = datetime.datetime.now()
    
    status = requests.get(today_url)
    print(colored(f"\n> Verificando URL para la fecha: {fecha_actual.strftime('%d/%m/%Y')}...\n", "yellow"))
    
    if status.status_code == 200:
        print(colored("> URL Valida!", "green"))
        service = Service(executable_path="driver/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        
        try:
            driver.get(today_url)
            time.sleep(3)
            
            tabla_sismos = driver.find_element(By.CSS_SELECTOR, ".sismologia.detalle")
            filas = tabla_sismos.find_elements(By.TAG_NAME, 'tr')[1:]
            
            sismos = []
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    fecha_str = celdas[0].text.strip()
                    fecha_str, _ = fecha_str.split("\n")
                    try:
                        fecha_datetime = datetime.datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                        sismos.append(fecha_datetime)
                    except ValueError:
                        print(colored(f">> Error: No se pudo convertir la fecha: {fecha_str}", "red"))
            
            if sismos:
                ultimo_sismo = max(sismos)
                tiempo_transcurrido = fecha_actual - ultimo_sismo
                
                print(colored("\n> Último sismo registrado:\n", "green"))
                print(f"- Fecha y Hora: {ultimo_sismo.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"- Tiempo transcurrido desde el último sismo: {tiempo_transcurrido}\n")
            else:
                print(colored("\n>> No se encontraron sismos en el día actual.", "red"))
        
        finally:
            driver.quit()
    else:
        print(colored("> Error: No se pudo acceder a la URL", "red"))
    return

def tarea7():
    while True:
        correo = input(colored("\n>> Ingresa tu correo para enviar la información del ultimo sismo: ", "cyan"))
        print(colored(f"\n>> Iniciando validación del correo: {correo}", "yellow"))
        if validate_gmail(correo):
            break
        else:
            print(colored(f"\n>> El correo: {correo} no es valido, intentalo nuevamente...", "red"))
             
    Year = datetime.datetime.today().strftime("%Y")
    Month = datetime.datetime.today().strftime("%m")
    CompleteDate = datetime.datetime.today().strftime("%Y%m%d")
    today_url = f"https://www.sismologia.cl/sismicidad/catalogo/{Year}/{Month}/{CompleteDate}.html"
    status = requests.get(today_url)
    print(colored("\n> Verificando URL...\n", "yellow"))

    if status.status_code == 200:
        print(colored("> URL Válida!", "green"))
        
        service = Service(executable_path="driver/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        
        try:
            driver.get(today_url)
            time.sleep(5)
            
            tabla_sismos = driver.find_element(By.CSS_SELECTOR, ".sismologia.detalle")
            filas = tabla_sismos.find_elements(By.TAG_NAME, 'tr')[1:]
            
            sismos = []
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    magnitud_str = celdas[4].text.strip()
                    profundidad_str = celdas[3].text.strip()
                    ubicacion_str = celdas[0].text.strip()  
                    fecha_str = celdas[1].text.strip()
                    
                    try:
                        magnitud_str = magnitud_str.replace("Ml", "").replace("Mw", "").replace("Mww", "").strip()
                        magnitud = float(magnitud_str)
                        profundidad_str = profundidad_str.replace("km", "").strip()
                        profundidad = int(profundidad_str)
                        fecha_str, ubicacion = ubicacion_str.split("\n")

                        sismo = {
                            'magnitud': magnitud,
                            'profundidad': profundidad,
                            'ubicacion': ubicacion,
                            'fecha': fecha_str
                        }
                        sismos.append(sismo)
                    except ValueError:
                        print(colored(f">> Error: No se pudo convertir la magnitud o profundidad: {magnitud_str} {profundidad_str}", "red"))
            
            if sismos:
                ultimo_sismo = sismos[0]
                print(colored("\n> Último sismo registrado:", "green"))
                print(f"- Fecha y Hora: {ultimo_sismo['fecha']}")
                print(f"- Ubicación: {ultimo_sismo['ubicacion']}")
                print(f"- Magnitud: {ultimo_sismo['magnitud']} Ml")
                print(f"- Profundidad: {ultimo_sismo['profundidad']} Km\n")
                
                print(colored("\n>> Enviando información del último sismo al correo.", "green"))
                send_gmail(correo, ultimo_sismo['magnitud'], ultimo_sismo['profundidad'], ultimo_sismo['ubicacion'], ultimo_sismo['fecha'])
            else:
                print(colored("\n>> No se encontraron sismos para hoy.", "red"))
        
        finally:
            driver.quit()

    else:
        print(colored("> Error: No se pudo acceder a la URL", "red"))
        
    return

def tarea8():
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
      
            sismos = []
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    magnitud_str = celdas[4].text.strip()
                    profundidad_str = celdas[3].text.strip()
                    ubicacion_str = celdas[0].text.strip()  
                    
                    try:
                        magnitud_str = magnitud_str.replace("Ml", "").replace("Mw", "").replace("Mww", "").replace(" ", "")
                        magnitud = float(magnitud_str)
                        profundidad_str = profundidad_str.replace("km", "").replace(" ", "")
                        profundidad = int(profundidad_str)
                        fecha_str, ubicacion = ubicacion_str.split("\n")
                    
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
            
            print(colored("\n> Top 3 sismos de mayor magnitud:\n", "green"))
            top_3_sismos = sismos_ordenados[:3]

            for i, sismo in enumerate(top_3_sismos):
                print(colored(f"{i + 1}. Fecha y Hora: {sismo['fecha']} | Ubicación: {sismo['ubicacion']} | Magnitud: {sismo['magnitud']} Ml | Profundidad: {sismo['profundidad']} Km\n", "yellow"))

            fechas = [sismo['fecha'] for sismo in top_3_sismos]
            magnitudes = [sismo['magnitud'] for sismo in top_3_sismos]

            x = np.arange(len(fechas))
            width = 0.35 

            fig, ax = plt.subplots()
            
            barras_magnitud = ax.bar(x + width/2, magnitudes, width, label='Magnitud (Ml)', color='tab:red')

            ax.set_xlabel('Sismos (Fecha)')
            ax.set_ylabel('Magnitud')
            ax.set_title('Top 3 Sismos: Magnitud')
            ax.set_xticks(x)
            ax.set_xticklabels(fechas)
            ax.legend()

            fig.tight_layout()
            plt.show()

        finally:
            driver.quit()

    else:
        print(colored("> Error: No se pudo acceder a la URL", "red"))
    return

def tarea9():
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
      
            sismos = []
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    profundidad_str = celdas[3].text.strip()
                    ubicacion_str = celdas[0].text.strip()  
                    fecha_str = celdas[1].text.strip()  
                    
                    try:
                        profundidad_str = profundidad_str.replace("km", "").replace(" ", "")
                        profundidad = int(profundidad_str)
                        fecha_str, ubicacion = ubicacion_str.split("\n")
                    
                        sismo = {
                            'profundidad': profundidad,
                            'fecha': fecha_str,
                            'ubicacion': ubicacion
                        }
                        sismos.append(sismo)
                    except ValueError:
                        print(colored(f">> Error: No se pudo convertir la profundidad: {profundidad_str}", "red"))
            
            print(colored(f"\n> Sismos del día: {len(sismos)}\n", "green"))

            fechas = [sismo['fecha'] for sismo in sismos]
            profundidades = [sismo['profundidad'] for sismo in sismos]

            fig, ax = plt.subplots()

            ax.bar(fechas, profundidades, color='tab:blue')

            ax.set_xlabel('Sismos (Fecha)')
            ax.set_ylabel('Profundidad (km)')
            ax.set_title('Comparación de la Profundidad de Todos los Sismos del Día')
            plt.xticks(rotation=90)

            fig.tight_layout()
            plt.show()

        finally:
            driver.quit()

    else:
        print(colored("> Error: No se pudo acceder a la URL", "red"))
    return

def tarea10():
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
      
            sismos = []
            
            for fila in filas:
                celdas = fila.find_elements(By.TAG_NAME, 'td')
                if celdas:
                    magnitud_str = celdas[4].text.strip()
                    profundidad_str = celdas[3].text.strip()
                    ubicacion_str = celdas[0].text.strip()  
                    fecha_str = celdas[1].text.strip()  
                    
                    try:
                        magnitud_str = magnitud_str.replace("Ml", "").replace("Mw", "").replace("Mww", "").replace(" ", "")
                        magnitud = float(magnitud_str)
                        profundidad_str = profundidad_str.replace("km", "").replace(" ", "")
                        profundidad = int(profundidad_str)
                        fecha_str, ubicacion = ubicacion_str.split("\n")
                    
                        sismo = {
                            'magnitud': magnitud,
                            'profundidad': profundidad,
                            'fecha': fecha_str,
                            'ubicacion': ubicacion
                        }
                        sismos.append(sismo)
                    except ValueError:
                        print(colored(f">> Error: No se pudo convertir la magnitud o profundidad: {magnitud_str} {profundidad_str}", "red"))
            
            print(colored(f"\n> Sismos del día: {len(sismos)}\n", "green"))

            fechas = [sismo['fecha'] for sismo in sismos]
            profundidades = [sismo['profundidad'] for sismo in sismos]
            magnitudes = [sismo['magnitud'] for sismo in sismos]

            x = np.arange(len(fechas))
            width = 0.35 

            fig, ax = plt.subplots()

            barras_profundidad = ax.bar(x - width/2, profundidades, width, label='Profundidad (km)', color='tab:blue')

            barras_magnitud = ax.bar(x + width/2, magnitudes, width, label='Magnitud (Ml)', color='tab:red')

            ax.set_xlabel('Sismos (Fecha)')
            ax.set_ylabel('Valores')
            ax.set_title('Comparación de la Profundidad y Magnitud de Todos los Sismos del Día')
            ax.set_xticks(x)
            ax.set_xticklabels(fechas, rotation=90)
            ax.legend()

            fig.tight_layout()
            plt.show()

        finally:
            driver.quit()

    else:
        print(colored("> Error: No se pudo acceder a la URL", "red"))
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
        print("1.- Mostrar Ranking de 3 Sismos con Mayor Magnitud")
        print(f"2.- Mostrar Profundidad Acumulada De Todos los Sismos del Día({fecha_actual})")
        print("3.- Mostrar Sismo De Menor Magnitud")
        print("4.- Mostrar Sismos Ocurridos En Un Intervalo De Tiempo.")
        print("5.- Mostrar Datos Del Ultimo Sismo.")
        print("6.- Mostrar Tiempo Transcurrido Desde El Ultimo Sismo")
        print("7.- Enviar Información Del Ultimo Sismo Al Correo")
        print("8.- Mostrar Grafico Intensidad De Los 3 Sismos De Mayor Magnitud")
        print("9.- Mostrar Grafico Profundidad De Los 3 Sismos De Mayor Magnitud")
        print(f"10.- Grafico Comparativo Sismos De Todos Los Sismos Del Día({fecha_actual})")
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