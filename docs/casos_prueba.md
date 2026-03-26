# Casos de Prueba – Regulón

## Caso 1: Lista de interacciones normal

**Descripción:** La lista `interacciones` tiene datos válidos y variados.

**Entrada:**
```python
interacciones = [
    ("AraC", "araA", "+"),
    ("AraC", "araB", "-"),
    ("LexA", "recA", "-"),
    ("CRP", "lacZ", "+"),
    ("CRP", "lacY", "+"),
]
```

**Salida esperada:**
```
Gen | No. de genes que regula | Genes regulados | Efecto
AraC | 2 | araA, araB | Dual
CRP | 2 | lacY, lacZ | Activador
LexA | 1 | recA | Represor
```

**Resultado:** Correcto

---

## Caso 2: Lista vacía

**Descripción:** La lista `interacciones` está vacía. El programa debería mostrar un mensaje de advertencia en lugar de imprimir una tabla vacía.

**Entrada:**
```python
interacciones = []
```

**Condición agregada:**
```python
if not interacciones:
    print("No hay interacciones registradas.")
```

**Salida esperada:**
```
No hay interacciones registradas.
```

**Resultado:** Correcto

---

## Caso 3: Un solo factor de transcripción

**Descripción:** Todas las interacciones pertenecen al mismo TF.

**Entrada:**
```python
interacciones = [
    ("AraC", "araA", "+"),
    ("AraC", "araB", "-"),
    ("AraC", "araC", "+"),
]
```

**Salida esperada:**
```
Gen | No. de genes que regula | Genes regulados | Efecto
AraC | 3 | araA, araB, araC | Dual
```

**Resultado:** Correcto

---

## Caso 4: Target duplicado en el mismo TF

**Descripción:** Un mismo gen aparece dos veces como target del mismo TF. El código evita duplicados gracias a la condición `if target not in regulon[tf]`.

**Entrada:**
```python
interacciones = [
    ("AraC", "araA", "+"),
    ("AraC", "araA", "-"),
]
```

**Salida esperada:**
```
Gen | No. de genes que regula | Genes regulados | Efecto
AraC | 1 | araA | Dual
```

**Resultado:** Correcto (no se duplica `araA`)

---

## Caso 5: Un solo factor de transcripción con un solo target

**Descripción:** Caso mínimo con una sola interacción.

**Entrada:**
```python
interacciones = [
    ("LexA", "recA", "-"),
]
```

**Salida esperada:**
```
Gen | No. de genes que regula | Genes regulados | Efecto
LexA | 1 | recA | Represor
```

**Resultado:** Correcto

---

## Caso 13: Archivo no encontrado

**Descripción:** El archivo TSV no existe en la ruta esperada.

**Entrada:** `data/raw/NetworkRegulatorGene.tsv` no existe.

**Comportamiento esperado:** El programa termina con un mensaje claro de error, sin traceback.

**Salida esperada:**
```
Error: archivo no encontrado
```

---

## Caso 14: Archivo sin permisos de lectura

**Descripción:** El archivo existe pero el usuario no tiene permisos de lectura.

**Entrada:** Archivo con permisos `000`.

**Comportamiento esperado:** El programa detecta el error de permisos y termina con un mensaje descriptivo.

**Salida esperada:**
```
Error: no se puede leer el archivo
```

---

## Caso 15: Archivo vacío

**Descripción:** El archivo existe pero no contiene ninguna línea (ni comentarios, ni encabezado, ni datos).

**Entrada:** Archivo vacío de 0 bytes.

**Comportamiento esperado:** El programa detecta que no hay encabezado ni interacciones y termina con un mensaje de error.

**Salida esperada:**
```
No hay interacciones registradas.
```

---

## Caso 16: Archivo solo con comentarios

**Descripción:** El archivo contiene únicamente líneas que empiezan con `#`.

**Entrada:**
```
# Este es un comentario
# Otro comentario
```

**Comportamiento esperado:** El programa ignora todas las líneas y termina indicando que no hay interacciones.

**Salida esperada:**
```
No hay interacciones registradas.
```

---

## Caso 17: Encabezado con columnas faltantes

**Descripción:** El archivo tiene encabezado pero le falta alguna columna requerida (por ejemplo, `6)function`).

**Entrada:**
```
1)regulatorId	2)regulatorName	3)RegulatorGeneName	4)regulatedId	5)regulatedName
```

**Comportamiento esperado:** El programa detecta la columna faltante antes de procesar datos y termina con un mensaje que indica cuál falta.

**Salida esperada:**
```
Error: columnas faltantes en el archivo: {'6)function'}
```

---

## Caso 18: Fila con efecto inválido

**Descripción:** Una fila tiene un valor en la columna `6)function` que no es `+`, `-` ni `+-`.

**Entrada:**
```
... AraC ... araA ... ?
```

**Comportamiento esperado:** La fila se descarta silenciosamente y se contabiliza en el aviso final. El resto de las interacciones válidas se procesan con normalidad.

**Salida esperada:**
```
Advertencia: 1 línea(s) descartadas por datos inválidos.
```

---

## Caso 19: Fila con campos vacíos

**Descripción:** Una fila tiene el nombre del TF o del gen regulado vacío.

**Entrada:**
```
RDBECOLICNC00001		(campo target vacío)	araA	+
```

**Comportamiento esperado:** La fila se descarta y se contabiliza en el aviso. Las demás filas válidas se procesan.

**Salida esperada:**
```
Advertencia: 1 línea(s) descartadas por datos inválidos.
```

---

## Caso 20: Columnas en diferente orden

**Descripción:** El archivo conserva los mismos nombres de columna del encabezado pero en un orden distinto al original.

**Entrada:**
```
6)function	5)regulatedName	3)RegulatorGeneName	...
+	araA	AraC	...
```

**Comportamiento esperado:** El programa detecta los índices correctos a partir del encabezado y procesa los datos sin error.

**Salida esperada:** Archivo de salida generado correctamente con los mismos resultados que si las columnas estuvieran en orden original.

---

## Caso 21: Interacciones duplicadas

**Descripción:** El archivo contiene dos filas con exactamente el mismo TF, gen regulado y efecto.

**Entrada:**
```
AraC	araA	+
AraC	araA	+
```

**Comportamiento esperado:** El gen `araA` aparece una sola vez en la lista de genes regulados por `AraC`. El programa elimina duplicados silenciosamente.

**Salida esperada:**
```
AraC	1	araA	Activador
```

---

## Caso 22: Archivo de salida generado correctamente

**Descripción:** El programa completa una ejecución normal con datos válidos.

**Entrada:** Archivo TSV con al menos una interacción válida.

**Comportamiento esperado:** Se crea el archivo `results/regulon_summary.tsv`, con encabezado y una fila por cada TF. El archivo puede abrirse y revisarse.

**Salida esperada:**
```
Gen	No. de genes que regula	Genes regulados	Efecto
AraC	2	araA, araB	Dual
```

---

## Caso 23: TF con efectos mixtos (clasificación Dual)

**Descripción:** Un mismo TF aparece con efecto `+` en una fila y `-` en otra.

**Entrada:**
```
AraC	araA	+
AraC	araB	-
```

**Comportamiento esperado:** El TF se clasifica como `Dual` al detectar efectos contradictorios.

**Salida esperada:**
```
AraC	2	araA, araB	Dual
```

---

## Caso 24: Directorio de salida no existe

**Descripción:** La carpeta `results/` no existe al momento de ejecutar el programa.

**Entrada:** Sistema de archivos sin la carpeta `results/`.

**Comportamiento esperado:** El programa crea la carpeta automáticamente antes de escribir el archivo de salida, sin error.

**Salida esperada:** Carpeta `results/` creada y archivo `regulon_summary.tsv` generado correctamente.

---

## Caso 25: Archivo con solo una interacción válida

**Descripción:** El archivo tiene muchas filas pero solo una pasa todas las validaciones.

**Entrada:** 10 filas, 9 con datos inválidos, 1 válida.

**Comportamiento esperado:** El programa procesa correctamente la única fila válida y genera el archivo de salida con una entrada.

**Salida esperada:**
```
Advertencia: 9 línea(s) descartadas por datos inválidos.
Gen	No. de genes que regula	Genes regulados	Efecto
AraC	1	araA	Activador
```