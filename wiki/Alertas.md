# Alertas y recuperación

Las reglas originales de `prometheus/alertas.yml` se mantienen sin reducir sus umbrales
ni el tiempo requerido para dispararse. Se evalúan cada cinco segundos.

| Regla | Condición | Tiempo continuo |
|---|---|---|
| `TasaDeErroresAlta` | Proporción de respuestas 5xx mayor que 0,05 | 30 segundos |
| `LatenciaP95Alta` | p95 mayor que 0,5 segundos | 30 segundos |

Ambas consultas usan una ventana de un minuto y agrupan por `application`. Puede
haber una instancia por cada servicio. La tasa de errores configurada en el simulador
es una probabilidad por operación, no una garantía de que ambos servicios mostrarán
exactamente el mismo porcentaje HTTP.

## Secuencia de verificación

**Pendiente de ejecución:** todavía no se ha observado el ciclo de las alertas.

1. Mantener k6 activo, esperar una ventana de métricas y registrar ambas reglas Inactive.
2. Configurar `POST /api/fallas?tasaError=0.3` en inventario.
3. Registrar `TasaDeErroresAlta` en Pending y luego en Firing, junto al panel de errores
   del mismo intervalo. Guardar las etiquetas y valores reales de cada instancia.
4. Configurar `POST /api/fallas?latenciaMs=800`. Este cambio reemplaza la configuración
   completa: la tasa de errores vuelve a cero.
5. Registrar `LatenciaP95Alta` en Pending y en Firing y conservar una traza lenta.
6. Restablecer el simulador con `DELETE /api/fallas` y verificar por GET sus dos valores.
7. Mantener tráfico mientras la ventana deja atrás las muestras de falla y registrar
   ambas reglas nuevamente Inactive.

`Pending` significa que la condición ya se cumple, pero aún no durante todo el `for`.
`Firing` requiere que se mantenga; no basta un pico. El regreso a Inactive depende de
que la consulta deje de superar el umbral, no solo de recibir la respuesta del DELETE.

## Evidencias requeridas

Faltan las capturas y resultados de cada transición, sus timestamps y el panel de
errores durante Firing. Tampoco se ha medido todavía el tiempo real de recuperación.
El stack no incluye Alertmanager: estas alertas se visualizan en Prometheus y no envían
notificaciones externas.
