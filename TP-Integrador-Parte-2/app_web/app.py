import sys
from pathlib import Path
from datetime import date

import streamlit as st
import pandas as pd

from datos import (
    cargar_json,
    filtrar_datos,
    obtener_estaciones,
    obtener_mediciones
)
from estadisticas import calcular_estadisticas
from graficos import generar_grafica
from procesar_datos import generar_csv


def main():
    st.set_page_config(
        page_title="Datos meteorológicos",
        page_icon="🌦️",
        layout="wide"
    )

    st.title("🌦️ Explorador de datos meteorológicos")
    st.write(
        "Elegí una estación y una medición "
        "para consultar sus datos."
    )

    # Recibir la ruta del JSON.
    if len(sys.argv) < 2:
        st.error("No se indicó la ruta del archivo JSON.")
        st.code(
            "python -m streamlit run app.py -- datos/observaciones.json"
        )
        return

    ruta_json = Path(sys.argv[1])

    # Cargar el JSON completo.
    try:
        datos = cargar_json(str(ruta_json))
    except (OSError, ValueError, TypeError) as error:
        st.error(f"Error al cargar el JSON: {error}")
        return

    # Obtener las opciones mediante funciones del módulo datos.
    try:
        estaciones = obtener_estaciones(datos)
        mediciones = obtener_mediciones()
    except (KeyError, TypeError, ValueError) as error:
        st.error(f"Error al obtener las opciones: {error}")
        return

    if not estaciones or not mediciones:
        st.warning("No hay estaciones o mediciones disponibles.")
        return

    # Controles de la interfaz.
    st.sidebar.header("Seleccionar datos")

    estacion = st.sidebar.selectbox(
        "Estación meteorológica",
        estaciones
    )

    medicion = st.sidebar.selectbox(
        "Medición",
        mediciones
    )

    # Filtrar con la función existente.
    try:
        filtrados = filtrar_datos(
            datos,
            estacion,
            medicion
        )
    except Exception as error:
        st.error(f"Error al filtrar los datos: {error}")
        return

    if not filtrados:
        st.warning("No hay registros para esta selección.")
        return

    # Calcular estadísticas con la función existente.
    try:
        estadisticas = calcular_estadisticas(
            filtrados,
            medicion
        )
    except Exception as error:
        st.error(f"Error al calcular estadísticas: {error}")
        return

    # Mostrar estadísticas.
    st.subheader("Estadísticas")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Cantidad", estadisticas["cantidad"])
    col2.metric("Mínimo", estadisticas["minimo"])
    col3.metric("Máximo", estadisticas["maximo"])
    col4.metric("Promedio", round(estadisticas["promedio"], 2))

    # Pandas se utiliza únicamente para mostrar la tabla.
    st.subheader("Datos filtrados")
    tabla = pd.DataFrame(filtrados)
    st.dataframe(tabla, use_container_width=True)

    # Preparar rutas de salida.
    carpeta_salida = Path(__file__).parent / "salidas"

    try:
        carpeta_salida.mkdir(parents=True, exist_ok=True)

        nombre_estacion = (
            estacion.lower()
            .replace(" ", "_")
            .replace("/", "_")
        )

        nombre_archivo = (
            date.today().isoformat()
            + "_"
            + nombre_estacion
            + "_"
            + medicion
        )

        ruta_csv = carpeta_salida / (nombre_archivo + ".csv")
        ruta_png = carpeta_salida / (nombre_archivo + ".png")

        # Reutilizar las funciones de generación de archivos.
        generar_csv(
            filtrados,
            medicion,
            str(ruta_csv)
        )

        generar_grafica(
            filtrados,
            estacion,
            medicion,
            str(ruta_png)
        )

        st.subheader("Gráfico de evolución")
        st.image(
            str(ruta_png),
            caption=f"{medicion.capitalize()} - {estacion}",
            use_container_width=True
        )

        st.download_button(
            "Descargar CSV",
            data=ruta_csv.read_bytes(),
            file_name=ruta_csv.name,
            mime="text/csv"
        )

        st.download_button(
            "Descargar gráfico PNG",
            data=ruta_png.read_bytes(),
            file_name=ruta_png.name,
            mime="image/png"
        )

        st.success("CSV y gráfico generados correctamente.")

    except Exception as error:
        st.error(f"Error al generar los archivos: {error}")


if __name__ == "__main__":
    main()