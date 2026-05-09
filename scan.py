#!/usr/bin/env python3
import datetime
import ipaddress
import os
import re
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

import pyfiglet
from colorama import Fore, Style, init

# Esta linea activa los colores de colorama en la terminal.
init(autoreset=True)

# Esta constante indica la carpeta donde se guardaran los reportes.
REPORT_FOLDER = "reportes"


def clear_screen():
    # Esta funcion limpia la pantalla segun el sistema operativo.
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_banner():
    # Esta linea limpia la pantalla antes de mostrar el menu principal.
    clear_screen()

    # Esta linea genera el titulo grande del proyecto.
    ascii_banner = pyfiglet.figlet_format("PComb Parser")

    # Estas lineas imprimen el encabezado del programa.
    print(Fore.CYAN + Style.BRIGHT + ascii_banner)
    print(Fore.MAGENTA + "Scanner and Report Analyzer v3.0")
    print(Fore.WHITE + "Proyecto de practica para escaneo de puertos\n")


def pause():
    # Esta funcion detiene la ejecucion hasta que el usuario presione Enter.
    input("\nPresiona ENTER para continuar...")


def validar_ip(ip):
    # Esta linea intenta validar la IP recibida.
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        # Si la IP no es valida, devolvemos False.
        return False

    # Si la IP fue valida, devolvemos True.
    return True


def escanear_puerto(ip, port):
    # Este bloque intenta conectarse a un puerto concreto.
    try:
        # Esta linea crea un socket TCP.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            # Esta linea define un tiempo de espera corto.
            connection.settimeout(1.5)

            # Esta linea intenta abrir conexion con el puerto indicado.
            result = connection.connect_ex((ip, port))

            # Si el puerto no esta abierto, devolvemos None.
            if result != 0:
                return None

            try:
                # Esta linea intenta leer un banner del servicio abierto.
                banner = connection.recv(1024).decode(errors="ignore").strip()
            except OSError:
                # Si no se pudo leer nada, usamos un texto sencillo.
                banner = ""

            # Si el banner viene vacio, usamos un mensaje simple.
            if banner == "":
                banner = "No disponible"

            # Devolvemos una tupla con el puerto abierto y su banner.
            return port, banner
    except OSError:
        # Si hay un problema de red o socket, devolvemos None.
        return None


def obtener_lista_puertos():
    # Estas lineas muestran opciones basicas de escaneo.
    print("\n[1] Rapido (lista corta)")
    print("[2] Comun (1 al 100)")
    print("[3] Completo (1 al 1024)")

    # Esta linea pide la seleccion al usuario.
    option = input("Modo: ").strip()

    # Si elige rapido, devolvemos una lista simple de puertos comunes.
    if option == "1":
        return [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389, 8080]

    # Si elige comun, devolvemos los puertos del 1 al 100.
    if option == "2":
        return list(range(1, 101))

    # Si elige completo, devolvemos los puertos del 1 al 1024.
    if option == "3":
        return list(range(1, 1025))

    # Si la opcion no es valida, devolvemos None.
    return None


def guardar_resultado(ip, open_ports):
    # Esta linea crea la carpeta de reportes si no existe.
    os.makedirs(REPORT_FOLDER, exist_ok=True)

    # Esta linea genera una marca de tiempo para el nombre del archivo.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Esta linea forma el nombre final del archivo.
    filename = f"reporte_scan_{ip}_{timestamp}.txt"

    # Esta linea une la carpeta con el nombre del reporte.
    path = os.path.join(REPORT_FOLDER, filename)

    # Este bloque escribe el contenido del reporte.
    with open(path, "w", encoding="utf-8") as file:
        # Esta linea escribe un encabezado basico.
        file.write(f"Resultado del escaneo de {ip}\n")
        file.write("=" * 40 + "\n")

        # Este ciclo guarda cada puerto abierto y su banner.
        for port, banner in open_ports:
            file.write(f"[+] Puerto abierto: {port}\n")
            file.write(f"Banner: {banner}\n\n")

    # Devolvemos la ruta final para mostrarla en pantalla.
    return path


def ejecutar_escaneo_completo(ip, ports):
    # Si la IP no es valida, se detiene el flujo.
    if not validar_ip(ip):
        print(Fore.RED + "[!] IP invalida.")
        return

    # Esta linea informa que el escaneo ha iniciado.
    print(Fore.YELLOW + f"\n[~] Escaneando {ip}...\n")

    # Esta lista almacenara solo los puertos encontrados abiertos.
    open_ports = []

    # Este bloque ejecuta el escaneo usando varios hilos de forma simple.
    with ThreadPoolExecutor(max_workers=50) as executor:
        # Esta lista crea una tarea por cada puerto.
        futures = [executor.submit(escanear_puerto, ip, port) for port in ports]

        # Este ciclo recoge los resultados a medida que terminan.
        for future in as_completed(futures):
            result = future.result()

            # Si el resultado es None, el puerto estaba cerrado o fallo.
            if result is None:
                continue

            # Estas lineas guardan y muestran el puerto abierto.
            port, banner = result
            open_ports.append((port, banner))
            print(Fore.GREEN + f"[+] Puerto {port} abierto | Banner: {banner}")

    # Esta linea ordena la lista final para que el reporte quede claro.
    open_ports.sort(key=lambda item: item[0])

    # Si no se encontro nada, se informa y se sale.
    if len(open_ports) == 0:
        print(Fore.RED + "\n[-] No se encontraron puertos abiertos en el rango elegido.")
        return

    # Esta linea guarda el reporte final en disco.
    report_path = guardar_resultado(ip, open_ports)

    # Esta linea confirma la ubicacion del archivo generado.
    print(Fore.CYAN + f"\n[+] Escaneo finalizado. Reporte guardado en: {report_path}")


def analizar_reportes_existentes():
    # Si la carpeta de reportes no existe, se informa al usuario.
    if not os.path.exists(REPORT_FOLDER):
        print(Fore.RED + "[-] No existe la carpeta de reportes.")
        return

    # Esta lista toma solo los archivos de texto disponibles.
    files = [file for file in os.listdir(REPORT_FOLDER) if file.endswith(".txt")]

    # Si no hay archivos, se informa con un mensaje sencillo.
    if len(files) == 0:
        print(Fore.YELLOW + "[-] No hay reportes guardados.")
        return

    # Esta linea ordena los nombres para mostrarlos mejor.
    files.sort()

    # Estas lineas imprimen la lista numerada de reportes.
    print(Fore.BLUE + "\n[+] Reportes encontrados:")
    for index, filename in enumerate(files, start=1):
        print(f"    [{index}] {filename}")

    # Esta linea pide el numero del reporte que se quiere abrir.
    option = input(Fore.YELLOW + "\n[?] Numero de reporte a analizar: ").strip()

    # Si el usuario no escribe un numero, se detiene.
    if not option.isdigit():
        print(Fore.RED + "[!] Debes escribir un numero valido.")
        return

    # Esta linea convierte la seleccion en entero.
    position = int(option) - 1

    # Si el numero queda fuera de rango, se informa.
    if position < 0 or position >= len(files):
        print(Fore.RED + "[!] El numero elegido no existe.")
        return

    # Esta linea forma la ruta del archivo seleccionado.
    selected_file = os.path.join(REPORT_FOLDER, files[position])

    # Este bloque abre y lee todo el contenido del reporte.
    with open(selected_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Estas expresiones extraen puertos y banners del texto guardado.
    ports = re.findall(r"\[\+\] Puerto abierto: (\d+)", content)
    banners = re.findall(r"Banner: (.*)", content)

    # Esta linea imprime el encabezado del resumen.
    print(Fore.CYAN + f"\n--- Resumen de {files[position]} ---")

    # Si no se extrajo nada, lo indicamos.
    if len(ports) == 0:
        print(Fore.YELLOW + "No se encontraron puertos dentro del reporte.")
        return

    # Este ciclo muestra cada puerto con su banner asociado.
    for port, banner in zip(ports, banners):
        print(f"{Fore.GREEN}Puerto: {port.ljust(5)} {Fore.WHITE}| Banner: {banner}")


def menu():
    # Este bucle mantiene activo el programa hasta que se elija salir.
    while True:
        # Esta linea muestra el encabezado principal.
        mostrar_banner()

        # Estas lineas imprimen las opciones disponibles.
        print(f"{Fore.GREEN}[1]{Fore.WHITE} Iniciar escaneo de puertos")
        print(f"{Fore.GREEN}[2]{Fore.WHITE} Analizar reportes guardados")
        print(f"{Fore.RED}[3]{Fore.WHITE} Salir\n")

        # Esta linea pide la opcion al usuario.
        option = input(Fore.YELLOW + "Seleccion > ").strip()

        # Si la opcion es 1, se inicia el escaneo.
        if option == "1":
            ip = input(Fore.CYAN + "IP objetivo: ").strip()
            ports = obtener_lista_puertos()

            # Si la lista de puertos no se pudo definir, se informa.
            if ports is None:
                print(Fore.RED + "[!] Modo invalido.")
                pause()
                continue

            # Esta linea ejecuta el escaneo final.
            ejecutar_escaneo_completo(ip, ports)
            pause()

        # Si la opcion es 2, se revisan reportes ya guardados.
        elif option == "2":
            analizar_reportes_existentes()
            pause()

        # Si la opcion es 3, el programa termina.
        elif option == "3":
            print(Fore.MAGENTA + "Cerrando PComb Parser...")
            break

        # Cualquier otro valor se considera invalido.
        else:
            print(Fore.RED + "[!] Opcion invalida.")
            pause()


if __name__ == "__main__":
    # Esta condicion ejecuta el menu solo cuando el archivo se corre directamente.
    menu()
