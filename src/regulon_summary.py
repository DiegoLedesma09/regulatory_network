
regulon = {}

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

# imprimir tabla final
print("Gen | No. de genes que regula | Genes regulados")

for tf in regulon:
    numero = len(regulon[tf])
    genes = ", ".join(regulon[tf]) 
    
    print(tf, "|", numero, "|", genes)