# Context

Este proyecto analiza una red de regulación genética.

Los datos contienen interacciones entre factores de transcripción (TF) y genes.

Formato de los datos:

TF gene effect

## Ejemplo:

AraC araA + 
AraC araB - 
LexA recA - ```

## Objetivo del programa:

Generar una tabla que indique para cada TF:

Nombre del TF (esta solumna debe estar ordenada)
total de genes regulados
lista de genes regulados (ordenada)
Efecto regulador del gen
```

## Actualización v1.1

1. Leer los datos desde un archivo
    1.1 El archivo trae 7 columnas y las que vamos a usar son: 2, 5 y 6
2. Los resultados deberán mandarse a un archivo de salida 

## Actualización v1.2

Problema:
El programa depende de rutas fijas (hardcoded).

Nuevo requisito:
El programa debe recibir dos argumentos. El archivo de entrada y salida.

## Actualización v1.3

Problema:
El usuario necesita filtrar TFs con pocos genes regulados.

Nuevo requisito:
Agregar el parámetro opcional `--min_genes` para excluir TFs que regulan menos de ese número de genes.

## Actualización v1.4

Problema:
El programa podía fallar silenciosamente o con errores poco informativos ante archivos corruptos, permisos insuficientes o datos inválidos.

Nuevo requisito:
Implementar manejo de errores robusto y validaciones para casos edge:

- Manejo de errores de archivo (no encontrado, permisos, encoding).
- Validación de archivos vacíos o sin encabezado válido.
- Verificación de argumentos inválidos (ej. min_genes negativo).
- Detección de datos mal formados (columnas faltantes, campos vacíos, efectos inválidos).
- Mensajes de error claros y específicos para facilitar la resolución de problemas.