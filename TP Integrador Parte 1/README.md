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