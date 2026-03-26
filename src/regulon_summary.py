import os

regulon = {}
clas = {}
interacciones = []
lineas_descartadas = 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_entrada = os.path.join(BASE_DIR, "..", "data", "raw", "NetworkRegulatorGene.tsv")
ruta_salida = os.path.join(BASE_DIR, "..", "results", "regulon_summary.tsv")
os.makedirs(os.path.join(BASE_DIR, "..", "results"), exist_ok=True)

if not os.path.exists(ruta_entrada):
    print("Error: archivo no encontrado")
    exit(1)

# Columnas requeridas
COLUMNAS_REQUERIDAS = {"3)RegulatorGeneName", "5)regulatedName", "6)function"}

with open(ruta_entrada, "r") as infile:
    encabezado = None
    indice = {}

    for linea in infile:
        linea = linea.strip()

        if not linea or linea.startswith("#"):
            continue

        columnas = linea.split("\t")

        # La primera línea no-comentario es el encabezado
        if encabezado is None:
            encabezado = [col.strip() for col in columnas]

            # Validar columnas requeridas
            if not COLUMNAS_REQUERIDAS.issubset(set(encabezado)):
                faltantes = COLUMNAS_REQUERIDAS - set(encabezado)
                print(f"Error: columnas faltantes en el archivo: {faltantes}")
                exit(1)

            # Mapear nombre → índice (robusto ante reordenamientos)
            indice["tf"]     = encabezado.index("3)RegulatorGeneName")
            indice["target"] = encabezado.index("5)regulatedName")
            indice["efecto"] = encabezado.index("6)function")
            continue

        # Validar número mínimo de columnas
        if len(columnas) <= max(indice.values()):
            lineas_descartadas += 1
            continue

        tf     = columnas[indice["tf"]].strip()
        target = columnas[indice["target"]].strip()
        efecto = columnas[indice["efecto"]].strip()

        if not tf or not target or not efecto:
            lineas_descartadas += 1
            continue

        if efecto not in {"+", "-", "+-"}:
            lineas_descartadas += 1
            continue

        interacciones.append((tf, target, efecto))

if lineas_descartadas:
    print(f"Advertencia: {lineas_descartadas} línea(s) descartadas por datos inválidos.")

if not interacciones:
    print("No hay interacciones registradas.")
    exit(1)

for tf, target, efecto in sorted(interacciones):
    if tf not in regulon:
        regulon[tf] = []
    if target not in regulon[tf]:
        regulon[tf].append(target)

    if tf not in clas:
        clas[tf] = "Activador" if efecto == "+" else "Represor" if efecto == "-" else "Dual"
    else:
        if clas[tf] != "Dual" and clas[tf] != efecto:
            clas[tf] = "Dual"

with open(ruta_salida, "w") as outfile:
    outfile.write("Gen\tNo. de genes que regula\tGenes regulados\tEfecto\n")
    for tf in regulon:
        numero = len(regulon[tf])
        genes  = ", ".join(regulon[tf])
        efecto = clas.get(tf, "Desconocido")
        outfile.write(f"{tf}\t{numero}\t{genes}\t{efecto}\n")

print(f"Archivo generado: {ruta_salida}")