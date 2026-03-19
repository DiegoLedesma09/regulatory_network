regulon = {}
clas = {}

interacciones = [
    ("AraC", "araA", "+"),
    ("AraC", "araB", "-"),
    ("LexA", "recA", "-"),
    ("CRP", "lacZ", "+"),
    ("CRP", "lacY", "+"), 
]

if not interacciones:
    print("No hay interacciones registradas.")
    exit(1)
else: 
    for linea in sorted(interacciones):
        tf, target, efecto = linea
        
        # Creo un diccionario para cada tf
        if tf not in regulon:
            regulon[tf] = []
        
        # Agrego el target al diccionario de su tf
        if target not in regulon[tf]:
            regulon[tf].append(target)
        
        if efecto == "":
            continue
        if tf not in clas:
            clas[tf] = []
            if efecto == "+":
                clas[tf] = ["Activador"]
            elif efecto == "-":
                clas[tf] = ["Represor"]
            else:
                clas[tf] = ["Dual"]
            

# imprimir tabla final
print("Gen | No. de genes que regula | Genes regulados | Efecto")

for tf in regulon:
    numero = len(regulon[tf])
    genes = ", ".join(regulon[tf])
    efect = clas[tf]
    
    print(tf, "|", numero, "|", genes, "|", efect)