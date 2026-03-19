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