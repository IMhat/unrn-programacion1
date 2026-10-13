# TP Integrador 1 - Parte 1

Programa de linea de comandos que lee un archivo TXT de observaciones meteorologicas, valida cada
registro y genera un archivo JSON con los registros validos y los invalidos.

## Grupo
Mateo Martin Mansilla

## Forma de ejecucion

```bash
python adaptar_datos.py observaciones20260824.txt observaciones.json
```
- Primer argumento: archivo TXT de entrada.
- Segundo argumento: archivo JSON de salida.

Al terminar, el programa muestra por consola la cantidad de registros leidos, validos e invalidos.

## Estructura del JSON de salida

```json
{
    "resumen": {
        "cantidad_registros": 1820,
        "cantidad_validos": 1602,
        "cantidad_invalidos": 218
    },
    "registros_validos": [
        {
            "fecha": "24/08/2026",
            "hora": 0,
            "temperatura": 8.0,
            "humedad": 70.0,
            "presion": 1027.7,
            "direccion_viento": 80.0,
            "velocidad_viento": 13.0,
            "estacion": "AEROPARQUE AERO"
        }
    ],
    "registros_invalidos": [
        {
            "linea_original": "24082026     0   3.4   76           90    7     BARILOCHE AERO",
            "errores": [
                "presion invalida: ''"
            ]
        }
    ]
}
```

## Implementacion inicial

- **`adaptar_datos.py`**: recibe el TXT y el JSON de salida por argumento, recorre el archivo linea por linea, 
  separa los campos de cada registro (por posición fija, no con `split()`,
  porque en el archivo real hay columnas que a veces vienen vacias), y arma el JSON final.

- **`validaciones.py`**: tiene una función por cada dato a validar (fecha, hora, temperatura, humedad, presion, 
  direccion de viento, velocidad de viento y estación) y una funcion `validar_registro()` que las junta a todas.

## Implementacion 2 fase 1

 El modulo procesar_datos.py recibe tres argumentos:
 1_ Ruta al JSON
 2_ Estacion metereologica
 3_ Mediciones a analizar.

 ```bash
python procesar_datos.py datos/observaciones.json "AEROPARQUE AERO" temperatura
```

El modulo muestra por consola:

1_ cantidad de registros:
2_ valor minimo
3_ valor maximo
4_ promedio
5_ primeros registros filtrados

y genera un archivo CSV con los datos filtrados y una imagen PNG de la grafica.

## Implementacion 2 fase 2

# Estructura del proyecto

TP-Integrador-Parte-2/
├── conversor/
│   ├── adaptar_datos.py
│   └── validaciones.py
├── app_web/
│   ├── app.py
│   ├── procesar_datos.py
│   ├── datos.py
│   ├── estadistica.py
│   ├── graficos.py
│   ├── datos/
│   │   └── observaciones.json
│   └── salidas/
├── requirements.txt
└── README.md

Etapa 2 - Aplicación web con Streamlit
La aplicación web permite explorar los datos meteorológicos de manera interactiva mediante una interfaz gráfica.

Instalación de dependencias
Desde la carpeta app_web/:

 ```bash
python -m pip install -r requirements.txt
```
# El archivo requirements.txt contiene las dependencias necesarias:

1_ streamlit
2_ pandas
3_ matplotlib

# Ejecución de la aplicación
Desde la carpeta app_web/:

 ```bash
python -m streamlit run app.py -- datos/observaciones.json
```

# El argumento que aparece después de -- indica la ruta del archivo JSON que utilizará la aplicación.

La aplicación permite:

Seleccionar una estación meteorológica mediante un control desplegable.
Seleccionar una medición disponible.
Consultar las estadísticas de la selección: cantidad, mínimo, máximo y promedio.
Visualizar una tabla con los registros filtrados mediante Pandas.
Generar una gráfica de línea con Matplotlib.
Guardar la gráfica como imagen PNG.
Generar y descargar el archivo CSV con los registros filtrados.
Descargar la gráfica en formato PNG.
Mostrar mensajes de error cuando no se pueden cargar o procesar los datos.
La aplicación utiliza únicamente los registros válidos del JSON.

Organización de la lógica
La interfaz no reemplaza ni duplica las funciones de procesamiento desarrolladas en la Etapa 1. Cada módulo tiene una responsabilidad específica:

**`app.py`**: configura la interfaz, recibe la ruta del JSON, presenta los controles, llama a las funciones de procesamiento y muestra los resultados.
**`datos.py`**: carga el JSON, obtiene las estaciones disponibles y filtra las observaciones.
**`estadistica.py`**: calcula cantidad, mínimo, máximo y promedio mediante una función propia.
**`graficos.py`**: genera y guarda la gráfica de línea con Matplotlib.
**`procesar_datos.py`**: contiene la ejecución por línea de comandos y la función de generación del CSV.

Pandas se utiliza en la aplicación web para organizar y mostrar los registros en una tabla. Los cálculos estadísticos siguen realizándose mediante las funciones propias desarrolladas en la Etapa 1.

Archivos generados
Los resultados del procesamiento se guardan en la carpeta salidas/:

CSV: contiene fecha, hora, estación y la medición seleccionada.
PNG: contiene la gráfica de línea que representa la evolución de la medición a lo largo del tiempo.
Los nombres de los archivos identifican la fecha de generación, la estación y la medición analizada.

Flujo general del proyecto
Archivo TXT original
        |
        v
Conversión y validación
        |
        v
Archivo JSON
        |
        v
Carga y filtrado de registros válidos
        |
        v
Cálculo de estadísticas
        |
        +-----------> Archivo CSV
        |
        +-----------> Gráfica PNG
        |
        v
Aplicación web con Streamlit
        |
        +-----------> Estadísticas
        +-----------> Tabla de datos
        +-----------> Gráfica interactiva en la interfaz