#!/usr/bin/env python3
import os
import socket
import datetime
import pyfiglet
from colorama import init, Fore, Style

# Inicializa colorama
init(autoreset=True)

# Función para mostrar el banner artístico
def mostrar_banner():
    os.system("clear")  # Limpia la pantalla para que se vea mejor
    ascii_banner = pyfiglet.figlet_format("PComb Parser")
    print(Fore.CYAN + Style.BRIGHT + ascii_banner)
    print(f"{Fore.MAGENTA}🛡  Python Port Scanner v1.0  🛡")
    print(f"{Fore.WHITE}    By orami – CyberSec ⚔\n")

# Función para crear el archivo de reporte
def crear_archivo_reporte(ip):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre = f"reporte_scan_{ip}_{timestamp}.txt"
    archivo = open(nombre, "w")
    return archivo

# Función para escanear puertos
def escanear_puertos(ip, puertos, archivo):
    print(f"\n{Fore.YELLOW}[~] Escaneando {ip}...\n")
    archivo.write(f"Resultado del escaneo de {ip}\n")
    archivo.write("=" * 40 + "\n")
    for puerto in puertos:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        resultado = sock.connect_ex((ip, puerto))
        if resultado == 0:
            print(f"{Fore.GREEN}[+] Puerto abierto: {puerto}")
            archivo.write(f"[+] Puerto abierto: {puerto}\n")
        sock.close()

# Función que ejecuta el escaneo completo
def ejecutar_escaneo(ip, puertos):
    archivo = crear_archivo_reporte(ip)
    escanear_puertos(ip, puertos, archivo)
    archivo.close()
    print(f"\n{Fore.CYAN}[✔] Escaneo completado. Reporte guardado.\n")

# Menú principal
def menu():
    while True:
        mostrar_banner()
        print(f"""{Fore.BLUE}
        1. Escaneo rápido (puertos comunes)
        2. Escaneo personalizado (puertos definidos)
        3. Escaneo completo (puertos 1-1024)
        4. Salir
{Style.RESET_ALL}""")
        opcion = input(f"{Fore.YELLOW}Selecciona una opción: {Style.RESET_ALL}")

        if opcion == "1":
            ip = input(f"{Fore.YELLOW}IP objetivo: {Style.RESET_ALL}")
            puertos_comunes = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]
            ejecutar_escaneo(ip, puertos_comunes)

        elif opcion == "2":
            ip = input(f"{Fore.YELLOW}IP objetivo: {Style.RESET_ALL}")
            entrada = input("Puertos separados por coma (ej: 22,80,443): ")
            puertos = [int(p.strip()) for p in entrada.split(",") if p.strip().isdigit()]
            ejecutar_escaneo(ip, puertos)

        elif opcion == "3":
            ip = input(f"{Fore.YELLOW}IP objetivo: {Style.RESET_ALL}")
            puertos = list(range(1, 1025))
            ejecutar_escaneo(ip, puertos)

        elif opcion == "4":
            print(f"\n{Fore.RED} Saliendo... ¡Hasta pronto, hacker!\n")
            break
        else:
            print(f"{Fore.RED} Opción inválida. Intenta nuevamente.\n")

# Punto de entrada
if __name__ == "__main__":
    menu()