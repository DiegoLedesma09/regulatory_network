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