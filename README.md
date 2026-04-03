# PComb Parser - Multi-threaded Scanner & Analyzer

PComb Parser es una herramienta integral de reconocimiento de red diseñada para la velocidad y la claridad. Combina un escáner de puertos de alto rendimiento (multihilo) con un motor de análisis de reportes basado en expresiones regulares, permitiendo a los investigadores de seguridad identificar vectores de ataque en tiempo récord.

---

## Características Principales

* **Escaneo de Alta Velocidad**: Implementa `ThreadPoolExecutor` con 100 hilos concurrentes para escaneos locales y externos ultrarrápidos.
* **Banner Grabbing**: Intenta capturar la cabecera de respuesta de cada puerto abierto para identificar servicios y versiones.
* **Generación Automática de Reportes**: Guarda cada sesión de escaneo en archivos de texto organizados por IP y fecha dentro de la carpeta `/reportes`.
* **Analizador Inteligente (Parser)**: Procesa reportes existentes utilizando **Regex** para extraer una tabla limpia de puertos y servicios, facilitando la lectura de logs extensos.
* **Validación de Objetivos**: Incluye un módulo de validación de direcciones IP para prevenir errores de ejecución.

---

## Interfaz de Usuario

```
██████╗  ██████╗ ██████╗ ███╗   ███╗██████╗ 
██╔══██╗██╔════╝██╔═══██╗████╗ ████║██╔══██╗
██████╔╝██║     ██║   ██║██╔████╔██║██████╔╝
██╔═══╝ ██║     ██║   ██║██║╚██╔╝██║██╔══██╗
██║     ╚██████╗╚██████╔╝██║ ╚═╝ ██║██████╔╝
╚═╝      ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ 
        Scanner & Report Analyzer v3.0
```

---

## Instalación y Uso

Se recomienda el uso de un entorno virtual para gestionar las dependencias de forma aislada.

```bash
# Preparación del entorno
python -m venv venv
source venv/bin/activate

# Instalación de dependencias
pip install -r requirements.txt

# Ejecución
python pcomb_parser.py
```

---

## Flujo de Trabajo Recomendado

1. **Opción [1]**: Realiza un escaneo sobre el objetivo (ej. una VM de Windows o Linux).
2. **Resultados**: El script guardará el log detallado automáticamente.
3. **Opción [2]**: Carga el reporte generado para ver un resumen ejecutivo de los puertos y banners encontrados sin ruido innecesario.

---

## Autor
**ORAMI (2025)**
Estudiante de Ciberseguridad | Desarrollo Web
```
