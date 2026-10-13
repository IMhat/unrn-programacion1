from pathlib import Path

base = Path("datos")
archivo = base / "reportes" / "reporte_2026.csv"

desde_actual = Path.cwd() / archivo
desde_home = Path.home() / "proyecto" / archivo

print(base)
print(type(base))
print(archivo)
print(desde_actual)
print(desde_home)

from pathlib import Path

archivo = Path(
    "datos/reportes/reporte_2026.csv"
)

print(archivo.name) # nombre completo del archivo
print(archivo.stem) # nombre del archivo sin extension
print(archivo.suffix) # extensión del archivo
print(archivo.parent) # rutas padre

from pathlib import Path

ruta = Path("datos")

print(ruta.exists())
print(ruta.is_file())
print(ruta.is_dir())

print(ruta)

from pathlib import Path

carpeta = Path("datos")

for elemento in carpeta.iterdir():
    print(elemento.name)
    print("  Archivo:", elemento.is_file())
    print("  Directorio:", elemento.is_dir())