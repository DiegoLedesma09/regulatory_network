# README

Este proyecto analiza redes de regulación genética, procesando interacciones entre factores de transcripción (TF) y genes para generar resúmenes de regulones.

## Uso

```bash
python src/regulon_summary.py <archivo_entrada> <archivo_salida> [--min_genes N]
```

- `archivo_entrada`: Archivo TSV con las interacciones (ej. data/raw/NetworkRegulatorGene.tsv)
- `archivo_salida`: Archivo donde se guardará el resumen
- `--min_genes`: Opcional, filtra TFs con menos de N genes regulados

## Actualización v1.4

Se mejoró la robustez del programa con:

- **Manejo de errores**: Captura errores de I/O, archivos inválidos y datos mal formados, mostrando mensajes claros.
- **Validaciones**: Verifica integridad de archivos y argumentos.
- **Comentarios**: Justificación explícita de estrategias de manejo de errores para mantener el código limpio y mantenible.