import sys
import os
import csv

from datos import cargar_json, filtrar_datos
from estadisticas import calcular_estadisticas
from graficos import generar_grafica


def generar_csv(registros, medicion, ruta_csv):
    try:
        archivo = open(
            ruta_csv,
            "w",
            newline="",
            encoding="utf-8"
        )

        escritor = csv.writer(archivo)
        escritor.writerow([
            "fecha",
            "hora",
            "estacion",
            medicion
        ])

        for registro in registros:
            escritor.writerow([
                registro["fecha"],
                registro["hora"],
                registro["estacion"],
                registro[medicion]
            ])

        archivo.close()

    except OSError:
        raise Exception(
            "no se pudo escribir el archivo " + ruta_csv
        )


def main():
    if len(sys.argv) != 4:
        print("cantidad de argumentos invalida")
        sys.exit(1)

    ruta_json = sys.argv[1]
    estacion = sys.argv[2]
    medicion = sys.argv[3]

    if os.path.exists(ruta_json) == False:
        print("no existe el archivo "+ ruta_json)
        sys.exit(1)

    try:
        datos = cargar_json(ruta_json)
        filtrados = filtrar_datos(
            datos,
            estacion,
            medicion
        )

        if len(filtrados) == 0:
            print("no se encontraron registros")
            sys.exit(1)

        estadisticas = calcular_estadisticas(
            filtrados,
            medicion
        )

        carpeta = os.path.dirname(ruta_json)

        nombre_estacion = estacion.lower().replace(
            " ",
            "_"
        )

        nombre_archivo = (
            "2026-10-07_"
            + nombre_estacion
            + "_"
            + medicion
        )

        ruta_csv = os.path.join(
            carpeta,
            nombre_archivo + ".csv"
        )

        ruta_grafica = os.path.join(
            carpeta,
            nombre_archivo + ".png"
        )

        generar_csv(
            filtrados,
            medicion,
            ruta_csv
        )

        generar_grafica(
            filtrados,
            estacion,
            medicion,
            ruta_grafica
        )

        print("estadisticas:")
        print(estadisticas)

        print("\nprimeros registros filtrados:")

        cantidad = min(5, len(filtrados))

        for i in range(cantidad):
            print(filtrados[i])

        print("\nCSV guardado en: " + ruta_csv)
        print("grafica guardada en: " + ruta_grafica)

    except Exception as error:
        print("error: " + str(error))
        sys.exit(1)

main()

