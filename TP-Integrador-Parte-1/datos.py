import json

def cargar_json(ruta_json):
    try:
        archivo = open(ruta_json, "r", encoding="utf-8")
        datos = json.load(archivo)
        archivo.close()

        return datos

    except FileNotFoundError:
        raise Exception("no existe el archivo " + ruta_json)

    except json.JSONDecodeError:
        raise Exception("no es un JSON valido")

    except OSError:
        raise Exception("no se pudo leer el archivo " + ruta_json)


def filtrar_datos(datos, estacion, medicion):
    mediciones_disponibles = [
        "temperatura",
        "humedad",
        "presion",
        "direccion_viento",
        "velocidad_viento"
    ]

    if medicion not in mediciones_disponibles:
        raise Exception("medicion invalida: " + medicion)

    registros = datos["registros_validos"]

    filtrados = []

    for registro in registros:
        if registro["estacion"] == estacion:
            filtrados.append(registro)

    return filtrados
