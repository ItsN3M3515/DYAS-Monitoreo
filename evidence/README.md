# Evidencias originales del taller

- Ejecución: https://github.com/ItsN3M3515/DYAS-Monitoreo/actions/runs/42535601486
- Entorno: VM aislada de GitHub, creada para esta ejecución.
- Código ejecutado: `51c225825fdd30194f073c8d889da390ace5a6d0`.
- Finalización de los ejercicios: `2026-11-08T23:38:36.498247Z`.
- Revisión visual: 21 capturas, incluidos los nueve gráficos y las tres trazas completas.
- Integridad: `runtime/manifest.json` conserva SHA-256 de 78 archivos generados por el colector.

Los archivos de `runtime/` se copiaron sin alterar del artefacto de Actions. Las capturas
mantienen sus píxeles originales; no se usaron las imágenes de ejemplo de `img/` como
pruebas de esta ejecución. El manifest se genera antes de la captura final de estado
Compose, por lo que `compose-status.json` es diagnóstico adicional y no figura en esa
lista de hashes. El manifest no contiene su propio hash.

## Contenido

| Archivos | Evidencia |
|---|---|
| `targets*`, `dashboard-provisioned.json` | Targets UP y panel 12 cargado desde el archivo |
| `query-*` | Consultas 3, 5, 6 y 7, sus respuestas y fases |
| `dashboard-*.png` | Dashboard normal, con errores, con latencia y tras la recuperación |
| `alert-*`, `alerts-*` | Pending, Firing e Inactive, con reglas e instancias |
| `trace-*`, `request-*` | Spans reales, relaciones de padres, solicitudes y capturas |
| `correlated-logs.json` | ERROR de los dos servicios con el mismo traceId |
| `*-browser.json` | URL, título, texto y errores de navegador de cada captura |
| `timeline.json`, `k6.log`, `compose-status.json` | Tiempos, tráfico y estado saludable del stack |

Las explicaciones de los valores medidos están en el
[Wiki](https://github.com/ItsN3M3515/DYAS-Monitoreo/wiki).
El log completo de todos los contenedores se conserva en el artefacto de Actions
(duración de siete días); los dos logs requeridos y el estado del stack se conservan
en Git para que la entrega no dependa de la caducidad de ese artefacto.

## Cómo interpretar k6

k6 es un generador de tráfico, sin umbrales de aprobación. Los 5xx introducidos
intencionalmente producen checks fallidos; los 404/409 de negocio también contribuyen
a `http_req_failed`. No se interpretan como un fallo oculto del workflow.

La duración configurada de doce minutos es un máximo para disponer de tráfico durante
los ejercicios. El colector lo detuvo deliberadamente al completar la recuperación,
tras aproximadamente 4 min 42 s. Esto explica el mensaje final de SIGTERM y una iteración
interrumpida. Se completaron 2.815 iteraciones y 7.807 solicitudes HTTP, aproximadamente
9,97 iteraciones/s. Se reportaron ocho iteraciones descartadas; el log no identifica su
causa exacta. Esta ejecución demuestra observabilidad y no certifica capacidad de carga
ni un objetivo estricto de diez iteraciones/s.
