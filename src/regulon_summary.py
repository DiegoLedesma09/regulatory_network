import os
import argparse
# ===================================================================================================
# Responsabilidad: Leer un archivo, obtener sus interacciones y generar una tupla con las interacciones
# Entrada: Una ruta relativa para poder manejar el archivo desde la posición del programa
# Salida: Una tupla con las interacciones del archivo "NetworkRegulatorGene.tsv"
# ===================================================================================================

def lecture_validation(ruta_entrada):
    """
    ===============================================================================================
    Lee un archivo, identifica las columnas requiridas para obtener las interacciones de TFs con sus respectivos
    targets, así como el efecto que tiene sobre el target.
     
    Args:
        ruta_entrada (str): Ruta del archivo con las interacciones de la red
    
    Returns:
        interacciones (tup(str, str, str): Interacciones completas usando solamente TF, target y efecto.
        
    ==============================================================================================
    """
    interacciones = []
    lineas_descartadas = 0 
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
    
    return(interacciones)

# ===================================================================================================
# Responsabilidad: Construir una estructura de datos que me permita organizar las interacciones del regulon
# Entrada: Una tupla que contenga las interacciones de los TF en el regulon
# Salida: Un diccionario que organice targets según su TF
# ====================================================================================================
def construir_regulon(interacciones):
    """
    ==============================================================================================
    Construye un diccionario que organiza los targets por su TF regulador.

    Args:
        interacciones (tpl(str, str, str)): Una tupla con las interacciones de TF, target y efecto.

    Returns:
        regulon (dict): Diccionario con TFs como claves y listas de targets como valores.
    ==============================================================================================
    """
    regulon = {}

    for tf, target in sorted(interacciones):
        if tf not in regulon:
            regulon[tf] = []
        if target not in regulon[tf]:
            regulon[tf].append(target)

    return(regulon)

# ===================================================================================================
# Responsabilidad: Obtener la clasificación del efecto de cada TF sobre sus targets
# Entrada: Una tupla que contenga las interacciones de los TF en el regulon
# Salida: Un diccionario que clasifique TFs según su efecto sobre los targets
# ====================================================================================================
def obtener_efecto_TF(interacciones, regulon):
    """
    =============================================================================================
    Obtiene el efecto esperado del regulador (Activador(+), Represor (-) o Dual (+-)) por cada TF
    en una lista de reguladores

    Args:
        interacciones (tpl(str, str, str)): Tupla con las interacciones de TF, target y efecto.
        regulon (dict): Diccionario con TFs como claves.
    
    Returns:
        clas (dict): Diccionario con los TFs clasificados según la actividad que tienen sobre el target
    =============================================================================================
    """
    clas = {}

    for tf, target, efecto in sorted(interacciones):
        if tf not in clas:
            clas[tf] = "Activador" if efecto == "+" else "Represor" if efecto == "-" else "Dual"
        else:
            if clas[tf] != "Dual" and clas[tf] != efecto:
                clas[tf] = "Dual"

    return(clas)

# ===================================================================================================
# Responsabilidad: Clasificar los TFs del regulon
# Entrada: Una tupla que contenga las interacciones de los TF en el regulon
# Salida: Dos diccionarios que organicen targets según su TF y TF´s según el efecto sobre los targets
# ====================================================================================================
def clasificacion_TF(interacciones):
    """
    ==============================================================================================
    De una lista de interacciones, clasifico targets por TF, además, clasifico los TFs segun el efecto
    regulatorio que tiene sobre los targets.

    Args:
        interacciones (tpl(str, str, str)) = Una clasificacion de targets según su TF, y una construccion de los efectos que
        tiene sobre el target.

    Returns:
        regulon, clas (dict) = Regresa diccionarios de TFs con targets asociados, así como diccionarios con el efecto asociado.
    ==============================================================================================
    """
    regulon = construir_regulon(interacciones)
    clas = obtener_efecto_TF(interacciones, regulon)
    return(regulon, clas)

# ==================================================================================================
# Responsabilidad = Imprimir las interacciones en un archivo de salida
# Entrada = Dos diccionarios que clasifiquen los TFs según targets y efecto, una ruta de salida
# relativa, y un filtro opcional de número mínimo de genes regulados
# ==================================================================================================
def generar_salida(regulon, clas, ruta_salida, minimal_genes=0):
    """
    ===================================================================================================
    Imprime la salida de los diccionarios de interacciones entre TFs, filtrando TFs con pocos genes.

    Args:
        regulon (dict): Diccionario con los TFs y targets asociados
        clas (dict): Diccionario con los TFs y sus efectos
        ruta_salida (str): Ruta relativa del archivo donde se desea imprimir el archivo
        minimal_genes (int): Filtra TFs con menos de este número de genes regulados
    ===================================================================================================
    """
    with open(ruta_salida, "w") as outfile:
        outfile.write("Gen\tNo. de genes que regula\tGenes regulados\tEfecto\n")
        for tf in regulon:
            numero = len(regulon[tf])
            if numero < minimal_genes:
                continue
            genes  = ", ".join(regulon[tf])
            efecto = clas.get(tf, "Desconocido")
            outfile.write(f"{tf}\t{numero}\t{genes}\t{efecto}\n")

    print(f"Archivo generado: {ruta_salida}")

def parse_arguments():
    """
    Define y parsea los argumentos de línea de comandos.

    Esta función crea el parser de argparse, configura los argumentos posicionales
    `input_file` y `output_file`, y el argumento opcional `--min_genes`.

    Returns:
        argparse.Namespace: Contiene `input_file`, `output_file` y `min_genes`.
    """
    parser = argparse.ArgumentParser(description="Resumen de regulones")
    parser.add_argument("input_file", help="Archivo de entrada")
    parser.add_argument("output_file", help="Archivo de salida")
    parser.add_argument("--min_genes", type=int, default=0, help="Filtrar TFs con menos de este número de genes regulados")
    return parser.parse_args()


def main():
    args = parse_arguments()

    ruta_entrada = args.input_file
    ruta_salida = args.output_file
    minimal_genes = args.min_genes 
    
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    if not os.path.exists(ruta_entrada):
        print("Error: archivo no encontrado")
        exit(1)

    interacciones = lecture_validation(ruta_entrada)
    regulon, clas = clasificacion_TF(interacciones)
    generar_salida(regulon, clas, ruta_salida, minimal_genes)

main()