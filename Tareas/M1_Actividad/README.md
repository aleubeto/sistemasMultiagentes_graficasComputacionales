# M1. Actividad

### Conoce y aplica una herramienta para la implementación de sistemas multiagentes.

Dadas las siguientes variables:

- Habitación de `M`x`N` espacios.
- Número de agentes.
- Porcentaje de celdas inicialmente sucias.
- Tiempo máximo de ejecución.

Realiza la siguiente simulación:

- Inicializa las celdas sucias (ubicaciones aleatorias).
- Todos los agentes empiezan en la celda `[1,1]`.

En cada paso de tiempo:
- Si la celda está sucia, entonces aspira.
- Si la celda está limpia:
    - el agente elije una dirección aleatoria para moverse (unas de las 8 celdas vecinas)
    - elije la acción de movimiento (si no puede moverse allí, permanecerá en la misma celda).
- Se ejecuta el tiempo máximo establecido.

Deberás recopilar la siguiente información durante la ejecución:

- Tiempo necesario hasta que todas las celdas estén limpias (o se haya llegado al tiempo máximo).
- Porcentaje de celdas limpias después del termino de la simulación.
- Número de movimientos realizados por todos los agentes.
- Analiza cómo la cantidad de agentes impacta el tiempo dedicado, así como la cantidad de movimientos realizados.

Desarrolla un informe con lo observado.
