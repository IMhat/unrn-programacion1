from datetime import datetime

# Este modulo tiene una funcion para validar cada dato del .txt

def es_numero(texto):
    # Intenta convertir el texto a numero. Si funciona, es numero.
    try:
        float(texto)
        return True
    except ValueError:
        return False


def es_fecha_valida(fecha_texto):
    # La fecha tiene que tener 8 numeros y formato DDMMAAAA
    if len(fecha_texto) != 8:
        return False

    if fecha_texto.isdigit() == False:
        return False

    dia = int(fecha_texto[0:2])
    mes = int(fecha_texto[2:4])
    anio = int(fecha_texto[4:8])

    # Con datetime nos fijamos si esa fecha existe de verdad
    try:
        datetime(anio, mes, dia)
    except ValueError:
        return False

    return True


def es_hora_valida(hora_texto):
    if hora_texto.isdigit() == False:
        return False

    hora = int(hora_texto)

    if hora < 0 or hora > 23:
        return False

    return True


def es_humedad_valida(hum_texto):
    if es_numero(hum_texto) == False:
        return False

    humedad = float(hum_texto)

    if humedad < 0 or humedad > 100:
        return False

    return True


def es_direccion_viento_valida(dd_texto):
    if es_numero(dd_texto) == False:
        return False

    direccion = float(dd_texto)

    if direccion < 0 or direccion > 360:
        return False

    return True


def es_velocidad_viento_valida(ff_texto):
    if es_numero(ff_texto) == False:
        return False

    velocidad = float(ff_texto)

    if velocidad < 0:
        return False

    return True


def es_estacion_valida(nombre_texto):
    if nombre_texto.strip() == "":
        return False

    return True


def validar_registro(fecha_texto, hora_texto, temp_texto, hum_texto, pnm_texto, dd_texto, ff_texto, nombre_texto):
    # Junta todos los errores que encuentra en el registro.
    errores = []

    if es_fecha_valida(fecha_texto) == False:
        errores.append("fecha invalida: '" + fecha_texto + "'")

    if es_hora_valida(hora_texto) == False:
        errores.append("hora invalida: '" + hora_texto + "'")

    if es_numero(temp_texto) == False:
        errores.append("temperatura invalida: '" + temp_texto + "'")

    if es_humedad_valida(hum_texto) == False:
        errores.append("humedad invalida: '" + hum_texto + "'")

    if es_numero(pnm_texto) == False:
        errores.append("presion invalida: '" + pnm_texto + "'")

    if es_direccion_viento_valida(dd_texto) == False:
        errores.append("direccion de viento invalida: '" + dd_texto + "'")

    if es_velocidad_viento_valida(ff_texto) == False:
        errores.append("velocidad de viento invalida: '" + ff_texto + "'")

    if es_estacion_valida(nombre_texto) == False:
        errores.append("nombre de estacion vacio")

    return errores