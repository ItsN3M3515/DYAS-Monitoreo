# Métricas y PromQL

**Ejecución pendiente:** todavía no se han obtenido resultados ni capturas propias.
Las consultas siguientes son las que se ejecutarán y conservarán junto a su instante
de medición. Las interpretaciones describen su significado, no un resultado observado.

## Targets

En `http://localhost:9090/targets`, los targets `pedidos:8081` e `inventario:8082`
del job `tienda` deben aparecer en **UP**. Esto prueba que Prometheus puede leer sus
métricas; no garantiza que todo su comportamiento de negocio sea correcto.

## Consulta 3: peticiones por segundo

```promql
sum by (application) (rate(http_server_requests_seconds_count{uri!~"/actuator.*"}[1m]))
```

Mide el incremento por segundo del contador HTTP durante el último minuto y agrupa
las rutas de cada servicio. Excluye salud y métricas. No es el número de usuarios ni
de pedidos: una iteración de k6 hace varias solicitudes.

## Consulta 5: proporción de errores 5xx

```promql
sum by (application) (rate(http_server_requests_seconds_count{uri!~"/actuator.*", status=~"5.."}[1m]))
/
sum by (application) (rate(http_server_requests_seconds_count{uri!~"/actuator.*"}[1m]))
```

Devuelve una fracción: `0.05` significa 5%, no 0,05%. Sin ninguna serie 5xx puede
devolver un resultado vacío, lo que no se debe sustituir por una medición inventada.
Se conservará también su resultado durante la fase de errores simulados.

## Consulta 6: latencia p95

```promql
histogram_quantile(0.95,
  sum by (application, le) (rate(http_server_requests_seconds_bucket{uri!~"/actuator.*"}[1m]))
)
```

Estima el p95 por servicio a partir de los buckets del histograma y devuelve segundos.
Por ejemplo, `0.8` equivaldría a 800 ms. Se necesitan tráfico y suficientes muestras
en la ventana para interpretar el valor.

## Consulta 7: pedidos por resultado

```promql
sum by (resultado) (increase(pedidos_total[5m]))
```

Estima cuántos pedidos de cada resultado hubo en los últimos cinco minutos. Es una
métrica de negocio y no incluye las consultas GET de los pedidos. `increase` puede
devolver decimales por la extrapolación entre scrapes, aunque el contador original
crezca en unidades enteras.

## Evidencia que falta

Se guardarán la captura de targets UP, los resultados JSON de las cuatro consultas,
el intervalo de tráfico y una interpretación de los valores realmente medidos.
