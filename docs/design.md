# Diseño del algoritmo 

- Lista de genes de regulador (sin repeticiones)
- Recorrer todas las interacciones (línea)
- Para cada interacción
    - Obtener el TF
    - Obtener el target
    - Sí el TF no esta en la lista de reguladores
        - Guardar el TF en reguladores
    - Si el gene no esta en la lista de genes por regulador
        - Guarda el gene asociado

- Recorrer toda la lista de los reguladores
    - Contar los genes de la lista de genes regulados por el TF
    - Imprime regulador, conteo y lista de genes.