# Trazas distribuidas

**Evidencia pendiente de ejecución.** No se han capturado aún trazas propias normales,
lentas ni fallidas. Las imágenes del README original son material de referencia.

## Estructura que se verificará

Para `POST /api/pedidos`, la instrumentación está preparada para producir:

1. Un span servidor en `pedidos`, que representa la solicitud del cliente.
2. Un span cliente en `pedidos`, que representa la llamada HTTP de reserva.
3. Un span servidor en `inventario`, que representa la recepción de esa reserva.

El encabezado W3C `traceparent` relaciona esos spans dentro de una traza. Se comprobarán
el mismo traceId, los servicios de cada span y la relación padre-hijo, además del conteo.
La presencia de tres spans aislados no demuestra por sí sola una traza distribuida.

## Traza normal

Con el simulador en cero se creará un pedido de un producto con stock y se abrirá su
traza en Jaeger. Se conservarán su identificador, la captura y las duraciones de los
spans. No se presupone una duración concreta: depende del entorno de la ejecución.

## Traza lenta

Se configurará `latenciaMs=800`, manteniendo tráfico. La captura debe mostrar que la
espera ocurre dentro del span servidor de inventario y que la llamada de pedidos
también espera por esa dependencia. Los spans están anidados: sumar todas sus duraciones
contaría varias veces el mismo tiempo.

La latencia del span cliente incluye el servicio remoto y costes adicionales de HTTP,
red y ejecución; su diferencia con el span servidor no mide exclusivamente la red.

## Recuperación

Después de la prueba se restablecerá el simulador mediante `DELETE /api/fallas` y se
verificará su estado. Jaeger se consulta en `http://localhost:16686`; desde Grafana,
la fuente Jaeger del taller permite consultar una traza por su identificador.
