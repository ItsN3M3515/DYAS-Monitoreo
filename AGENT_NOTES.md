# Contexto compartido del taller

## Estado y alcance

El taller está ejecutado, con evidencia real revisada y contenido final del Wiki.
La publicación del cierre debe comprobarse contra los hashes remotos antes de informar
al usuario. No confundir la terminación técnica con la entrega en la plataforma del curso.

- Usuario: único integrante Pablo Tamayo, pablotago@unisabana.edu.co.
- Destino confirmado: `ItsN3M3515/DYAS-Monitoreo`, código y Wiki.
- `origin` es el fork del usuario; `upstream` conserva el repositorio del profesor.
- El usuario pidió commits por cambios lógicos, pequeños pero no por cada línea.
- El usuario ya creó la primera página del Wiki. No volver a pedirlo.
- El código de negocio no necesitó cambios. Se modificaron build de pruebas, dashboard,
  automatización de evidencia y documentación.

## Autorización de host: conservar este límite

El usuario permitió **solo diagnóstico local de Docker en modo lectura** sin el gate
HomeLab. No autorizó reparar servicios, modificar firewall o módulos, ni reiniciar.
El gate no llegó a READY: su intento restringido falló por red/permisos y la revisión
automática rechazó el retry de host porque el script puede despertar Ark. No eludir
ese rechazo. El usuario aprobó expresamente usar la cuenta GitHub indicada arriba.

Docker local se diagnosticó el 8 de noviembre de 2026, aproximadamente a las 22:49 UTC:
kernel `7.3.0-4-cachyos`, sin directorio de módulos para esa versión, `xt_addrtype` no
cargado, y módulos instalados para `7.3.3-1-cachyos` y `6.18.60-2-cachyos-lts`. Docker
falló creando NAT y llegó a `start-limit-hit`. No se modificó el host. Es evidencia
fechada; comprobar de nuevo si se trabaja en una reparación autorizada.

## Verificación completa

- Run final: https://github.com/ItsN3M3515/DYAS-Monitoreo/actions/runs/42535601486
- Código ejecutado: `51c225825fdd30194f073c8d889da390ace5a6d0`.
- Ejercicios completos: 2026-11-08 23:33:53 a 23:38:36 UTC, runner aislado de GitHub.
- Compose desde cero: pedidos, inventario, Prometheus y Grafana saludables; Jaeger running.
- Ambos targets UP, consultas 3/5/6/7 y nueve gráficos con datos.
- Proporción 5xx de la fase de errores: inventario 26,27%, pedidos 15,84%.
- Traza lenta: inventario 800,646 ms; petición de pedidos 802,905 ms.
- Trazas normal/lenta/fallida: tres spans, dos servicios, una raíz y padres completos.
- Error correlacionado: `c5a8c8ae32a66fd74a32c9f4b1006845`; inventario 500 y pedidos 503.
- Ambas reglas Pending/Firing/Inactive. La primera captura de errores tiene inventario
  Firing y pedidos Pending; otra captura posterior confirma ambos Firing.
- Simulador restablecido y ambas reglas Inactive a las 23:38:30 UTC.
- 21 PNG originales revisados visualmente; hashes comprobados. El runner se apagó.

El build desde un directorio nuevo con Java 21 terminó a las 22:57:21 UTC: 47 pruebas
correctas, 97,85% de líneas y 95% de ramas. Su resumen está en
`evidence/build-verification.json`. CI estándar también pasó, incluida imagen y promtool.

## Intentos anteriores y límites

1. `42533260244`: stack correcto; colector falló por interpretar `meta.provisioned`.
   Grafana 13.2.3 deja false con `allowUiUpdates=true`; se verificó `provisionedExternalId`
   y contenido exacto del panel. Se corrigió además la carrera de arranque/limpieza de k6.
2. `42533717336`: targets y APIs correctos, pero capturas blancas. Se actualizó el
   navegador, se esperó contenido y se añadieron diagnósticos. No se aisló cuál de
   esos cambios resolvió las primeras páginas blancas.
3. `42534246884`: backend completo, pero la revisión visual rechazó canvas omitidos y
   trazas con un padre externo inventado por el colector.
4. `42535152562`: diagnóstico comparativo. Canvas con píxeles y viewport correctos,
   con y sin GPU; full-page omitía los mismos gráficos. Se cambió a viewport 1800×1900
   con comprobación de píxeles. Se seleccionan ahora traceId de logs reales sin padre
   artificial. El run final verificó estas correcciones.

Las reglas Prometheus no se cambiaron. k6 se detuvo deliberadamente al terminar los
pasos; su SIGTERM y una iteración interrumpida son esperados. Reportó 2.815 iteraciones,
7.807 solicitudes HTTP y ocho iteraciones descartadas, sin diagnóstico de su causa
exacta. No presentar el ejercicio como benchmark de diez iteraciones/s garantizadas.

## Archivos y publicación

- Wiki oficial: https://github.com/ItsN3M3515/DYAS-Monitoreo/wiki
- `wiki/`: fuente versionada de las nueve páginas y sidebar; mantener igual al Wiki.
- `evidence/runtime/`: originales del run final, incluido manifest, timeline, capturas,
  consultas, trazas, logs correlacionados, k6 y estado Compose.
- `evidence/README.md`: procedencia y límites; `wiki/Verificacion.md`: relato completo.
- El artefacto de Actions dura siete días; todos los archivos del manifest están en Git.
  El log completo adicional de Compose solo está en ese artefacto; los logs requeridos
  y el estado del stack sí están en Git.
- Checkout temporal del Wiki: `/tmp/dyas-monitoreo-wiki`.
- Pendiente de acción del usuario: revisar el Wiki y entregar los enlaces donde indique
  el curso. No se conoce una fecha límite y no se ha enviado nada a la plataforma académica.
- Reparar Docker de Powerstation es una tarea separada con autorización y gate propios;
  no hace falta hacerlo para revisar las evidencias de este taller.

## Historial de cambios hasta este cierre

- `f4698a5`: build: load Mockito agent explicitly during tests
- `8b29451`: dashboard: add inventory traffic breakdown by endpoint
- `8b42049`: docs: identify participant and explain workshop architecture
- `86a9988`: docs: prepare runtime evidence and record fresh build verification
- `c200b63`: ci: collect workshop evidence in an isolated Docker runner
- `464ec67`: ci: verify dashboard file provenance and wait for traffic startup
- `e474126`: docs: explain isolated execution and preserve workshop handoff
- `b894164`: ci: validate page rendering and retain browser diagnostics
- `1f55392`: ci: select real root traces from application logs
- `b5b7e7e`: ci: diagnose chart canvas pixels and compare browser rendering
- `51c2258`: fix: capture painted dashboard charts within the viewport
- `bdc7e11`: evidence: preserve live targets metrics and normal distributed trace
- `3d223cf`: evidence: preserve error latency and recovery exercises
- `65d7530`: docs: interpret measured metrics and the provisioned dashboard
- `7f44ad1`: docs: explain connected traces alert timing and correlated errors
- `1f45f66`: evidence: record run provenance integrity and traffic limits
