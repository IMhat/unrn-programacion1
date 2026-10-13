import sys
import os
import json
import validaciones


# El archivo de datos tiene columnas de ancho fijo (no separadas siempre por un solo espacio), asi que para leer cada dato usamos 
# "cortes" deposiciones dentro del renglon en vez de line.split()

# regla:

# FECHA     HORA  TEMP   HUM   PNM    DD    FF     NOMBRE
# 24082026     0   8.0   70  1027.7   80   13     AEROPARQUE AERO

CORTE_FECHA_INICIO = 0
CORTE_FECHA_FIN = 8
CORTE_HORA_FIN = 14
CORTE_TEMP_FIN = 20
CORTE_HUM_FIN = 25
CORTE_PNM_FIN = 33
CORTE_DD_FIN = 38
CORTE_FF_FIN = 43


def es_linea_de_datos(linea):
    # Una linea es de datos si sus primeros 8 caracteres son la fecha
    primer_campo = linea[CORTE_FECHA_INICIO:CORTE_FECHA_FIN]
    return primer_campo.isdigit()


def separar_campos(linea):
    # Corta el renglon en los 8 campos que nos interesan

    fecha_texto = linea[CORTE_FECHA_INICIO:CORTE_FECHA_FIN].strip()
    hora_texto = linea[CORTE_FECHA_FIN:CORTE_HORA_FIN].strip()
    temp_texto = linea[CORTE_HORA_FIN:CORTE_TEMP_FIN].strip()
    hum_texto = linea[CORTE_TEMP_FIN:CORTE_HUM_FIN].strip()
    pnm_texto = linea[CORTE_HUM_FIN:CORTE_PNM_FIN].strip()
    dd_texto = linea[CORTE_PNM_FIN:CORTE_DD_FIN].strip()
    ff_texto = linea[CORTE_DD_FIN:CORTE_FF_FIN].strip()
    nombre_texto = linea[CORTE_FF_FIN:].strip()

    return fecha_texto, hora_texto, temp_texto, hum_texto, pnm_texto, dd_texto, ff_texto, nombre_texto


def formatear_fecha(fecha_texto):
    # Pasa "24082026" (DDMMAAAA) a "24/08/2026" para que sea mas legible.
    dia = fecha_texto[0:2]
    mes = fecha_texto[2:4]
    anio = fecha_texto[4:8]
    return dia + "/" + mes + "/" + anio


def armar_registro(fecha_texto, hora_texto, temp_texto, hum_texto, pnm_texto, dd_texto, ff_texto, nombre_texto):
    registro = {
        "fecha": formatear_fecha(fecha_texto),
        "hora": int(hora_texto),
        "temperatura": float(temp_texto),
        "humedad": float(hum_texto),
        "presion": float(pnm_texto),
        "direccion_viento": float(dd_texto),
        "velocidad_viento": float(ff_texto),
        "estacion": nombre_texto
    }
    return registro


def procesar_archivo(lineas):
    # Recorre todas las lineas del TXT y devuelve dos listas

    registros_validos = []
    registros_invalidos = []

    for linea in lineas:
        linea_sin_salto = linea.rstrip("\n")

        if es_linea_de_datos(linea_sin_salto) == False:
            continue

        fecha_texto, hora_texto, temp_texto, hum_texto, pnm_texto, dd_texto, ff_texto, nombre_texto = separar_campos(linea_sin_salto)

        errores = validaciones.validar_registro(
            fecha_texto, hora_texto, temp_texto, hum_texto,
            pnm_texto, dd_texto, ff_texto, nombre_texto
        )

        if len(errores) == 0:
            registro = armar_registro(fecha_texto, hora_texto, temp_texto, hum_texto, pnm_texto, dd_texto, ff_texto, nombre_texto)
            registros_validos.append(registro)
        else:
            registro_invalido = {
                "linea_original": linea_sin_salto,
                "errores": errores
            }
            registros_invalidos.append(registro_invalido)

    return registros_validos, registros_invalidos


def main():
    if len(sys.argv) != 3:
        print("Error: cantidad de argumentos invalida")
        sys.exit(1)

    archivo_entrada = sys.argv[1]
    archivo_salida = sys.argv[2]

    if os.path.exists(archivo_entrada) == False:
        print("Error: no existe el archivo " + archivo_entrada)
        sys.exit(1)

    try:
        archivo = open(archivo_entrada, "r")
        lineas = archivo.readlines()
        archivo.close()
    except OSError:
        print("Error: no se pudo leer el archivo " + archivo_entrada)
        sys.exit(1)

    registros_validos, registros_invalidos = procesar_archivo(lineas)

    cantidad_registros = len(registros_validos) + len(registros_invalidos)

    datos_json = {
        "resumen": {
            "cantidad_registros": cantidad_registros,
            "cantidad_validos": len(registros_validos),
            "cantidad_invalidos": len(registros_invalidos)
        },
        "registros_validos": registros_validos,
        "registros_invalidos": registros_invalidos
    }

    try:
        archivo = open(archivo_salida, "w")
        json.dump(datos_json, archivo, indent=4, ensure_ascii=False)
        archivo.close()
    except OSError:
        print("Error: no se pudo escribir el archivo " + archivo_salida)
        sys.exit(1)

    print("Procesamiento terminado")
    print("Registros leidos: " + str(cantidad_registros))
    print("Registros validos: " + str(len(registros_validos)))
    print("Registros invalidos: " + str(len(registros_invalidos)))


main()