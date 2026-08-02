import os
import sys
import subprocess
from datetime import datetime

# 1. Menú de opciones para el usuario
print("-" * 50)
print("     ESCÁNER CON BASE DE DATOS NMAP VULNERS")
print("-" * 50)
print("1. Escanear por Nombre de Dominio (ej: pizza.com)")
print("2. Escanear por Dirección IP (ej: 32.193.235.103)")
opcion = input("\nSelecciona una opción (1 o 2): ").strip()

if opcion == "1":
    target_input = input("Introduce el dominio: ").strip()
    target_input = target_input.replace("https://", "").replace("http://", "").split("/")[0]
elif opcion == "2":
    target_input = input("Introduce la IP: ").strip()
else:
    print("\n Opción no válida. Saliendo.")
    sys.exit()

print("-" * 50)
print(f"Objetivo: {target_input}")
print(f"Inicio del escaneo: {str(datetime.now())}")
print(" Ejecutando motor de Nmap + Base de datos Vulners...")
print(" (Esto puede tardar un momento mientras analiza los servicios)...")
print("-" * 50)

# 2. Ejecución del comando Nmap local (Puertos web 80,443 y detección de vulnerabilidades)
# -sV: Detecta las versiones exactas del software (Apache, Nginx, etc.)
# --script=vulners: Usa la base de datos local para buscar fallos conocidos de esa versión
comando = ["nmap", "-sV", "-p", "80,443", "--script=vulners", target_input]

try:
    # Ejecutamos el comando y capturamos la salida en vivo
    resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
    
    # 3. Procesamiento inteligente de los resultados en pantalla
    lineas = resultado.stdout.split("\n")
    filtrando_vulnerabilidades = False
    
    print("\n[+] RESULTADOS ENCONTRADOS LOCALMENTE:\n")
    for linea in lineas:
        # Resaltar datos importantes para que sea fácil de leer en Termux
        if "PORT" in linea or "open" in linea:
            print(f" \033[1;32m{linea}\033[0m") # Texto en verde para puertos abiertos
        elif "CVE-" in linea:
            print(f"   \033[1;31m[!] {linea.strip()}\033[0m") # Texto en rojo para vulnerabilidades (CVE)
        elif "vulners:" in linea:
            print(f"\n Analizando fallos de seguridad detectados:")
            filtrando_vulnerabilidades = True
        else:
            if linea.strip():
                print(f" {linea}")

except FileNotFoundError:
    print("\n[X] Error: Nmap no está instalado en tu Termux.")
    print("Por favor ejecuta en tu terminal: pkg install nmap -y")
except subprocess.CalledProcessError as e:
    print(f"\n[X] Error al ejecutar Nmap: {e}")

print("\n" + "-" * 50)
print(" Análisis de vulnerabilidades local finalizado.")
print("-" * 50)

