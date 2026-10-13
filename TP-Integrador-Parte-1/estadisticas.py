


def calcular_estadisticas(registros,medicion):

    valores = []

    for registro in registros:
        valores.append(registro[medicion])

    cantidad = len(valores)

    minimo = valores [0]
    maximo = valores [0]
    suma = 0

    for valor in valores:
        if valor < minimo:
            minimo = valor

        if valor > maximo:
            maximo = valor

        suma += valor

    promedio = suma / cantidad

    estadisticas = {
        "cantidad": cantidad,
        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio
    }

    return estadisticas