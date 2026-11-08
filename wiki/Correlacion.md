# Correlación entre métricas, logs y trazas

**Evidencia pendiente.** No se ha seleccionado una petición real con errores ni un
traceId propio. Se conservarán las dos líneas de log y la traza de esa misma petición.

## Recorrido de diagnóstico

La métrica agregada indica que las fallas han aumentado y acota el intervalo a investigar.
Los logs explican el error concreto. La traza une la solicitud recibida por pedidos
con la reserva que llegó a inventario.

Durante la fase de errores se buscará una línea `ERROR` de
`edu.unisabana.dyas.tienda.comun.ManejadorErrores` en pedidos. Su mensaje debería
describir la falla de la dependencia, y la respuesta de pedidos será 503 cuando el
cliente traduzca una respuesta 500 de inventario.

Con el traceId de esa línea se buscará la línea correspondiente en inventario y se
abrirá la traza en `http://localhost:16686/trace/<traceId>`. El traceId debe coincidir
en ambos logs; los spanId serán diferentes porque identifican operaciones distintas.

## Qué se verificará

- La coincidencia exacta del traceId en pedidos, inventario y Jaeger.
- El mensaje original de `FallaSimuladaException` en inventario y su traducción a
  `InventarioNoDisponibleException` en pedidos.
- Las marcas de error y excepciones de los spans, además del código HTTP de respuesta.
- Que los logs, la traza y el panel de errores correspondan al mismo intervalo.

El manejador registra explícitamente el error en la observación HTTP y en el span
actual porque intercepta la excepción. Sin esa instrumentación, devolver un 5xx no
bastaría para conservar todos los detalles de la excepción en esas señales.
