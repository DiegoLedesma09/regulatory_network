
regulon = {}

interacciones = [
    ("AraC", "araA", "+"),
    ("AraC", "araB", "-"),
    ("LexA", "recA", "-"),
    ("CRP", "lacZ", "+"),
    ("CRP", "lacY", "+"), 
]
    
for linea in sorted(interacciones):
        tf, target, reg = linea
        
        if tf not in regulon:
            regulon[tf] = []
        
        if target not in regulon[tf]:
            regulon[tf].append(target)

# imprimir tabla final
print("Gen | No. de genes que regula | Genes regulados")

for tf in regulon:
    numero = len(regulon[tf])
    genes = ", ".join(regulon[tf]) # Puse el join para deshacerme de la estructura de lista en el print
    
    print(tf, "|", numero, "|", genes)