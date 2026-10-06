import os
import matplotlib.pyplot as plt

def generar_grafica(registros, estacion, medicion, ruta_grafica):
    fechas_horas = []
    valores = []

    for registro in registros:
        fecha_hora = (
            registro["fecha"]
            + " "
            + str(registro["hora"])
            + ":00"
        )

        fechas_horas.append(fecha_hora)
        valores.append(registro[medicion])

    plt.figure(figsize=(10, 5))

    plt.plot(
        fechas_horas,
        valores,
        marker="o"
    )

    plt.title(
        medicion + " - " + estacion
    )

    plt.xlabel("Fecha y hora")
    plt.ylabel(medicion)

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(ruta_grafica)
    plt.close()

    return ruta_grafica

