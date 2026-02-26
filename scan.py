#!/usr/bin/env python3

import os
import socket
import datetime
import pyfiglet
import ipaddress
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

# Inicializa colorama
init(autoreset=True)


# =========================
# BANNER
# =========================
def mostrar_banner():
    os.system("clear")
    ascii_banner = pyfiglet.figlet_format("PComb Parser")
    print(Fore.CYAN + Style.BRIGHT + ascii_banner)
    print(f"{Fore.MAGENTA}  Python Port Scanner v2.0  ")
    print(f"{Fore.WHITE}    By orami – InfoSec ⚔\n")


# =========================
# VALIDACIÓN DE IP
# =========================
def validar_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


# =========================
# CREAR ARCHIVO DE REPORTE
# =========================
def crear_archivo_reporte(ip):
    # Crear carpeta reportes si no existe
    os.makedirs("reportes", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"reporte_scan_{ip}_{timestamp}.txt"

    ruta_completa = os.path.join("reportes", nombre_archivo)

    archivo = open(ruta_completa, "w")
    archivo.write(f"Resultado del escaneo de {ip}\n")
    archivo.write("=" * 50 + "\n")
    archivo.write(f"Fecha: {datetime.datetime.now()}\n\n")

    return archivo, ruta_completa


# =========================
# ESCANEAR PUERTO INDIVIDUAL
# =========================
def escanear_puerto(ip, puerto):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        resultado = sock.connect_ex((ip, puerto))

        if resultado == 0:
            try:
                sock.send(b"\n")
                banner = sock.recv(1024).decode(errors="ignore").strip()
            except:
                banner = "No banner disponible"

            sock.close()
            return puerto, banner

        sock.close()
    except:
        pass

    return None


# =========================
# ESCANEO MULTIHILO
# =========================
def escanear_puertos(ip, puertos, archivo):
    print(f"\n{Fore.YELLOW}[~] Escaneando {ip}...\n")

    inicio = datetime.datetime.now()
    abiertos = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(escanear_puerto, ip, puerto) for puerto in puertos]

        for future in as_completed(futures):
            resultado = future.result()
            if resultado:
                puerto, banner = resultado
                print(f"{Fore.GREEN}[+] Puerto abierto: {puerto}")
                print(f"{Fore.CYAN}    Banner: {banner}\n")
                archivo.write(f"[+] Puerto abierto: {puerto}\n")
                archivo.write(f"    Banner: {banner}\n\n")
                abiertos.append(puerto)

    fin = datetime.datetime.now()
    duracion = fin - inicio

    archivo.write("=" * 50 + "\n")
    archivo.write(f"Puertos abiertos encontrados: {len(abiertos)}\n")
    archivo.write(f"Tiempo total: {duracion}\n")

    print(f"{Fore.CYAN}[✔] Escaneo completado en {duracion}")
    print(f"{Fore.WHITE}Puertos abiertos encontrados: {len(abiertos)}\n")


# =========================
# EJECUTAR ESCANEO
# =========================
def ejecutar_escaneo(ip, puertos):
    if not validar_ip(ip):
        print(f"{Fore.RED}[!] IP inválida. Usa formato 192.168.1.1\n")
        return

    archivo, ruta = crear_archivo_reporte(ip)
    escanear_puertos(ip, puertos, archivo)
    archivo.close()

    print(f"{Fore.CYAN}[✔] Reporte guardado en: {ruta}\n")


# =========================
# MENÚ PRINCIPAL
# =========================
def menu():
    while True:
        mostrar_banner()
        print(
            f"""{Fore.BLUE}
        1. Escaneo rápido (puertos comunes)
        2. Escaneo personalizado (puertos definidos)
        3. Escaneo completo (puertos 1-1024)
        4. Salir
{Style.RESET_ALL}"""
        )

        opcion = input(f"{Fore.YELLOW}Selecciona una opción: {Style.RESET_ALL}")

        if opcion == "1":
            ip = input(f"{Fore.YELLOW}IP objetivo: {Style.RESET_ALL}")
            puertos_comunes = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]
            ejecutar_escaneo(ip, puertos_comunes)

        elif opcion == "2":
            ip = input(f"{Fore.YELLOW}IP objetivo: {Style.RESET_ALL}")
            entrada = input("Puertos separados por coma (ej: 22,80,443): ")
            puertos = [
                int(p.strip()) for p in entrada.split(",") if p.strip().isdigit()
            ]
            ejecutar_escaneo(ip, puertos)

        elif opcion == "3":
            ip = input(f"{Fore.YELLOW}IP objetivo: {Style.RESET_ALL}")
            puertos = list(range(1, 1025))
            ejecutar_escaneo(ip, puertos)

        elif opcion == "4":
            print(f"\n{Fore.RED}Saliendo... ¡Hasta pronto, hacker!\n")
            break

        else:
            print(f"{Fore.RED}Opción inválida. Intenta nuevamente.\n")


# =========================
# PUNTO DE ENTRADA
# =========================
if __name__ == "__main__":
    menu()
