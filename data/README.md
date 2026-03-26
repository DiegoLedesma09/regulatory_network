# Dataset: Regulatory interactions (RegulonDB)

## Fuente
RegulonDB

## Archivo
NetworkRegulatorGene.tsv

## Versión
v14.5

## Formato
TSV (tab-separated values)

## Columnas relevantes
- regulatorName
- regulatedName
- function

## Observaciones
- el archivo tiene encabezado
- puede tiene columnas adicionales
- solo se usarán tres columnas en este proyecto
- La columna de efecto puede tener los siguiente valores: +, -,

## Estructura del proyecto

La estructura sigue una separación clara de responsabilidades orientada a proyectos de análisis bioinformático:

- **`docs`** — Concentra toda la documentación del proyecto: casos de prueba, contexto del problema y decisiones de diseño. Mantenerla separada del código facilita la navegación y la colaboración.

- **`data`** - Almacena los datos crudos del archivo de Regulon y el README para la documentación.

- **`results`** — Almacena los archivos de salida generados por los scripts.

- **`src`** — Contiene los módulos Python con la lógica principal del análisis. Aislar el código fuente en su propia carpeta permite escalar el proyecto agregando más scripts sin contaminar la raíz.