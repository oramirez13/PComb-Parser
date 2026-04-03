#!/usr/bin/env python3
import os  # Gestión de rutas y comandos del sistema
import socket  # Conexiones de red a bajo nivel
import datetime  # Registro de marcas de tiempo para reportes
import pyfiglet  # Generación de banners ASCII art
import ipaddress  # Validación de formato de direcciones IP
import re  # Búsqueda de patrones en los reportes (regex)
from colorama import init, Fore, Style  # Estética visual en terminal
from concurrent.futures import ThreadPoolExecutor, as_completed  # Multihilo

# Inicializa colorama para Arch Linux y Windows
init(autoreset=True)


# =========================================================
# CONFIGURACIÓN Y ESTÉTICA
# =========================================================
def mostrar_banner():
    """Limpia pantalla y muestra el logo de la herramienta"""
    os.system("cls" if os.name == "nt" else "clear")
    ascii_banner = pyfiglet.figlet_format("PComb Parser")
    print(Fore.CYAN + Style.BRIGHT + ascii_banner)
    print(f"{Fore.MAGENTA}  Scanner & Report Analyzer v3.0")
    print(f"{Fore.WHITE}    By orami – InfoSec ⚔\n")


# =========================================================
# LÓGICA DE ESCANEO (Basada en scan.py)
# =========================================================
def escanear_puerto(ip, puerto):
    """Intenta conectar a un puerto y obtener su banner"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.5)  # Tiempo de espera para la conexión
        resultado = sock.connect_ex((ip, puerto))

        if resultado == 0:
            try:
                # Intento de Banner Grabbing
                banner = sock.recv(1024).decode(errors="ignore").strip()
            except:
                banner = "No banner disponible"
            sock.close()
            return puerto, banner
        sock.close()
    except:
        pass
    return None


def ejecutar_escaneo_completo(ip, puertos):
    """Gestiona el escaneo multihilo y guarda el reporte"""
    if not validar_ip(ip):
        print(Fore.RED + "[!] IP inválida.")
        return

    os.makedirs("reportes", exist_ok=True)  # Crea carpeta si no existe
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"reporte_scan_{ip}_{timestamp}.txt"
    ruta_completa = os.path.join("reportes", nombre_archivo)

    print(Fore.YELLOW + f"\n[~] Escaneando {ip} con 100 hilos...")

    abiertos = []
    with open(ruta_completa, "w") as archivo:
        archivo.write(f"Resultado del escaneo de {ip}\n" + "=" * 40 + "\n")

        # Uso de ThreadPoolExecutor para máxima velocidad
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(escanear_puerto, ip, p) for p in puertos]
            for future in as_completed(futures):
                res = future.result()
                if res:
                    p, b = res
                    print(f"{Fore.GREEN}[+] Puerto {p} ABIERTO | Banner: {b}")
                    archivo.write(f"[+] Puerto abierto: {p}\n    Banner: {b}\n\n")
                    abiertos.append(p)

    print(Fore.CYAN + f"\n[✔] Escaneo finalizado. Reporte: {ruta_completa}")
    input("\nPresiona ENTER para volver...")


def validar_ip(ip):
    """Verifica que la IP sea válida antes de escanear"""
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False


# =========================================================
# LÓGICA DE ANÁLISIS (Basada en el nuevo Parser)
# =========================================================
def analizar_reportes_existentes():
    """Lee y extrae datos de reportes previos en la carpeta 'reportes'"""
    if not os.path.exists("reportes"):
        print(Fore.RED + "[-] No se encontró la carpeta de reportes.")
        return

    archivos = [f for f in os.listdir("reportes") if f.endswith(".txt")]
    if not archivos:
        print(Fore.YELLOW + "[-] No hay archivos de reporte disponibles.")
        return

    print(Fore.BLUE + "\n[+] Reportes encontrados:")
    for i, arc in enumerate(archivos, 1):
        print(f"    [{i}] {arc}")

    try:
        sel = int(input(Fore.YELLOW + "\n[?] Número de reporte a analizar: "))
        archivo_sel = archivos[sel - 1]

        with open(os.path.join("reportes", archivo_sel), "r") as f:
            contenido = f.read()

        # Extracción inteligente con expresiones regulares (Regex)
        puertos = re.findall(r"\[\+\] Puerto abierto: (\d+)", contenido)
        banners = re.findall(r"Banner: (.*)", contenido)

        print(Fore.CYAN + f"\n--- Resumen de {archivo_sel} ---")
        for p, b in zip(puertos, banners):
            print(f"{Fore.GREEN}Port: {p.ljust(5)} | {Fore.WHITE}Service: {b}")

    except:
        print(Fore.RED + "[!] Selección inválida.")
    input("\nPresiona ENTER para volver...")


# =========================================================
# MENÚ PRINCIPAL
# =========================================================
def menu():
    while True:
        mostrar_banner()
        print(f"{Fore.GREEN}[1]{Fore.WHITE} Iniciar Escaneo de Puertos")
        print(f"{Fore.GREEN}[2]{Fore.WHITE} Analizar Reportes Guardados")
        print(f"{Fore.RED}[3]{Fore.WHITE} Salir\n")

        op = input(Fore.YELLOW + "Selección > ")

        if op == "1":
            ip = input(Fore.CYAN + "IP Objetivo: ")
            print(
                "\n[1] Rápido (Top 20) | [2] Comunes (Top 100) | [3] Completo (1-1024)"
            )
            modo = input("Modo: ")
            if modo == "1":
                p_list = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3389, 8080]
            elif modo == "2":
                p_list = list(range(1, 101))
            else:
                p_list = list(range(1, 1025))
            ejecutar_escaneo_completo(ip, p_list)
        elif op == "2":
            analizar_reportes_existentes()
        elif op == "3":
            print(Fore.MAGENTA + "Until we meet again Hacker...")
            break


if __name__ == "__main__":
    menu()
