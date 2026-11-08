# Dashboard de Grafana

El dashboard **Tienda - Observabilidad** está definido en
[`grafana/dashboards/tienda.json`](https://github.com/ItsN3M3515/DYAS-Monitoreo/blob/main/grafana/dashboards/tienda.json).
Grafana lo carga mediante su proveedor de archivos. Las fuentes Prometheus y Jaeger
también se aprovisionan desde archivos del repositorio.

## Paneles

| Panel | Qué permite observar |
|---|---|
| Peticiones por segundo | Volumen de solicitudes por servicio |
| Tasa de errores 5xx | Proporción de fallas y umbral del 5% |
| Latencia p95 | Duración de solicitudes y umbral de 500 ms |
| Peticiones por endpoint y código de estado | Rutas y respuestas involucradas en un cambio de comportamiento |
| **Inventario: peticiones por endpoint** | Nuevo desglose del tráfico propio de inventario |
| Pedidos por resultado | Confirmaciones, falta de stock, productos inexistentes y fallas de inventario |
| Stock del inventario | Unidades disponibles por producto |
| Memoria heap usada | Memoria de objetos Java en uso por servicio |
| Uso de CPU del proceso | Fracción de CPU empleada por cada proceso |

## Panel adicional

El panel nuevo tiene identificador **12**, ocupa el ancho de la sección RED y utiliza:

```promql
sum by (uri) (rate(http_server_requests_seconds_count{application="inventario", uri!~"/actuator.*"}[1m]))
```

La leyenda identifica cada ruta. Comparar consultas de stock con reservas ayuda a
entender por qué el tráfico de inventario difiere del número de pedidos: k6 también
consulta stock directamente, y cada creación de pedido añade una reserva HTTP.

Se verificaron el JSON, los identificadores únicos y la ausencia de superposición
entre gráficos. El archivo conserva los ocho gráficos originales y añade el noveno.

## Evidencia pendiente

Falta verificar el aprovisionamiento en una instancia real, capturar el dashboard con
k6 activo y comprobar que el panel reaparece en una instancia nueva de Grafana usando
los archivos versionados. Una validación de JSON no demuestra esos resultados.
