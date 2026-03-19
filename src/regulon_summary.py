regulon = {}
clas = {}
interacciones = []
import os

# Ruta relativa al script, sin importar desde dónde se ejecute
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_entrada = os.path.join(BASE_DIR, "..", "data", "raw", "NetworkRegulatorGene.tsv")
os.makedirs("results", exist_ok=True)
ruta_salida = os.path.join(BASE_DIR, "..", "results", "regulon_summary.tsv")

# Valido la existencia de mi archivo
if not os.path.exists(ruta_entrada):
    print("Error: archivo no encontrado")
    exit(1)

with open(ruta_entrada, "r") as infile:
    for linea in infile:
        linea = linea.strip()
        # Validación de lineas vacías y comentarios
        if not linea or linea.startswith("#"):
            continue
        
        # Validacion de columnas
        columnas = linea.split("\t")
        if len(columnas) <= 5:
            print("El archivo no cubre el número de columnas asignado")
            
        # Salto el encabezado para evitar depender del índice de las líneas de comentarios
        if columnas[0].startswith("1)"):
            continue
        
        # Usaré las columnas que tienen los nombres de los genes y el efecto
        tf = columnas[1]
        target = columnas[4]
        efecto = columnas[5]
        
        # Valido que ninguna de mis columnas esté vacía
        if tf == "" or target == "" or efecto == "":
            continue
        
        # Validacion de los efectos en la regulacion
        regulaciones = ["+", "-", "+-"]
        if efecto not in regulaciones:
            continue

        interacciones.append((tf, target, efecto))


if not interacciones:
    print("No hay interacciones registradas.")
    exit(1)
else:
    for tf, target, efecto in sorted(interacciones):

        if tf not in regulon:
            regulon[tf] = []
        if target not in regulon[tf]:
            regulon[tf].append(target)

        if efecto == "":
            continue

        if tf not in clas:
            if efecto == "+":
                clas[tf] = "Activador"
            elif efecto == "-":
                clas[tf] = "Represor"
        else:
            if clas[tf] == "Activador" and efecto == "-":
                clas[tf] = "Dual"
            elif clas[tf] == "Represor" and efecto == "+":
                clas[tf] = "Dual"
            elif clas[tf] == "+-":
                clas[tf] = "Dual"

with open(ruta_salida, "w") as outfile:
    outfile.write("Gen\tNo. de genes que regula\tGenes regulados\tEfecto\n")
    for tf in regulon:
        numero = len(regulon[tf])
        genes = ", ".join(regulon[tf])
        efecto = clas.get(tf, "Desconocido")
        outfile.write(f"{tf}\t{numero}\t{genes}\t{efecto}\n")