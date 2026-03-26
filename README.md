# README
## Estructura del proyecto
```
regulatory_network/
├── docs/
│   ├── casos_prueba.md
│   ├── context.md
│   └── design.md
├── results/
│   └── regulon_summary.tsv
├── src/
│   └── regulon_summary.py
├── .gitignore
├── main.py
├── pyproject.toml
└── README.md
```

### Justificación

La estructura sigue una separación clara de responsabilidades orientada a proyectos de análisis bioinformático:

- **`docs/`** — Concentra toda la documentación del proyecto: casos de prueba, contexto del problema y decisiones de diseño. Mantenerla separada del código facilita la navegación y la colaboración.
- **`results/`** — Almacena los archivos de salida generados por los scripts (como `regulon_summary.tsv`). Separarlos del código fuente evita mezclar artefactos generados con lógica del programa y simplifica el `.gitignore`.
- **`src/`** — Contiene los módulos Python con la lógica principal del análisis. Aislar el código fuente en su propia carpeta permite escalar el proyecto agregando más scripts sin contaminar la raíz.
- **`main.py`** — Punto de entrada del proyecto, ubicado en la raíz para que sea fácilmente identificable y ejecutable desde cualquier entorno.
- **`pyproject.toml`** — Archivo de configuración del proyecto y sus dependencias, siguiendo el estándar moderno de Python (PEP 517/518).
- **`.gitignore`** — Excluye archivos generados, entornos virtuales y artefactos locales del control de versiones.