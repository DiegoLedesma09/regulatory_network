# Regulatory Network Analyzer

Este proyecto analiza redes de regulación genética, procesando interacciones entre factores de transcripción (TF) y genes para generar resúmenes de regulones. El programa lee datos de interacciones desde archivos TSV (basados en RegulonDB), clasifica los TFs según su efecto regulador (Activador, Represor o Dual), y genera un archivo de salida con estadísticas por TF.

## Requisitos

- Python 3.14 o superior
- No hay dependencias externas (solo bibliotecas estándar de Python)

## Instalación

1. Clona o descarga el repositorio.
2. Asegúrate de tener Python 3.14+ instalado.
3. Ejecuta el programa directamente con Python.

## Uso

```bash
python src/regulon_summary.py <archivo_entrada> <archivo_salida> [--min_genes N]
```

### Argumentos

- `archivo_entrada`: Ruta al archivo TSV de entrada con las interacciones (ej. `data/raw/NetworkRegulatorGene.tsv`)
- `archivo_salida`: Ruta al archivo de salida donde se guardará el resumen (ej. `results/regulon_summary.tsv`)
- `--min_genes N`: Opcional, entero positivo. Filtra TFs que regulan menos de N genes. Por defecto, incluye todos.

### Ejemplo

```bash
python src/regulon_summary.py data/raw/NetworkRegulatorGene.tsv results/regulon_summary.tsv --min_genes 2
```

Esto procesa el archivo de entrada, filtra TFs con al menos 2 genes regulados, y guarda el resultado en `results/regulon_summary.tsv`.

### Formato de entrada

El archivo TSV debe tener un encabezado con al menos las columnas:
- `3)RegulatorGeneName`: Nombre del TF
- `5)regulatedName`: Nombre del gen regulado
- `6)function`: Efecto (`+` para activador, `-` para represor, `+-` para dual)

Ejemplo de contenido:
```
1)regulatorId	2)regulatorName	3)RegulatorGeneName	4)regulatedId	5)regulatedName	6)function
RDBECOLICNC00001	AraC	AraC	RDBECOLIGNC00001	araA	+
RDBECOLICNC00001	AraC	AraC	RDBECOLIGNC00002	araB	-
```

### Formato de salida

Archivo TSV con columnas:
- `Gen`: Nombre del TF
- `No. de genes que regula`: Cantidad de genes únicos regulados
- `Genes regulados`: Lista de genes separados por coma
- `Efecto`: Clasificación (Activador, Represor, Dual)

Ejemplo:
```
Gen	No. de genes que regula	Genes regulados	Efecto
AraC	2	araA, araB	Dual
CRP	2	lacY, lacZ	Activador
```

## Estructura del proyecto

```
regulatory_network/
├── main.py                 # Punto de entrada alternativo
├── pyproject.toml          # Configuración del proyecto
├── README.md               # Este archivo
├── data/
│   ├── bloqueado.tsv       # Archivo de datos bloqueado
│   └── raw/
│       └── NetworkRegulatorGene.tsv  # Datos de entrada (ejemplo)
├── docs/
│   ├── ai.log.md           # Log de interacciones con IA
│   ├── casos_prueba.md     # Casos de prueba detallados
│   ├── context.md          # Contexto y requisitos del proyecto
│   └── design.md           # Diseño del algoritmo
├── results/                # Directorio de salida (creado automáticamente)
│   ├── new_tabla.txt
│   ├── parsetf.tsv
│   ├── regulon_summary.tsv
│   └── tf_output.txt
└── src/
    ├── read_args.py        # Módulo para parsing de argumentos
    └── regulon_summary.py  # Script principal
```

## Changelog

### v1.4 (Actual)
- **Manejo de errores robusto**: Captura errores de I/O (archivo no encontrado, permisos denegados, encoding incorrecto), validaciones de archivos vacíos o sin encabezado, argumentos inválidos (ej. min_genes negativo), y datos mal formados (columnas insuficientes, campos vacíos, efectos inválidos).
- **Mensajes de error claros**: Muestra mensajes específicos para facilitar la resolución de problemas.
- **Comentarios justificativos**: Agregados comentarios explicando por qué se manejan ciertos errores y cuáles no, para mantener el código limpio.
- **Validaciones adicionales**: Verifica integridad de datos antes del procesamiento.

### v1.3
- Agregado parámetro opcional `--min_genes` para filtrar TFs con pocos genes regulados.
- Actualizado flujo: usuario → CLI → main() → parse_arguments() → funciones.

### v1.2
- El programa ahora recibe argumentos desde línea de comandos: archivo de entrada y salida.
- Eliminadas rutas hardcoded.
- Flujo: usuario → CLI → main() → funciones.

### v1.1
- Lectura de datos desde archivo TSV (columnas 3, 5, 6).
- Salida a archivo en lugar de stdout.

## Casos de prueba

Para casos de prueba detallados, incluyendo escenarios normales y edge cases, consulta [docs/casos_prueba.md](docs/casos_prueba.md).

## Documentación adicional

- [docs/design.md](docs/design.md): Diseño del algoritmo y flujo de ejecución.
- [docs/context.md](docs/context.md): Contexto del proyecto y requisitos.
- [docs/ai.log.md](docs/ai.log.md): Log de prompts y actualizaciones con IA.

## Licencia

Este proyecto es de código abierto. Consulta el archivo LICENSE si existe.