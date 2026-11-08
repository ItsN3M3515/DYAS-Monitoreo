# Contexto compartido del taller

## Alcance y autorizaciones

- El usuario pidió completar el taller, diagnosticar Docker y hacer commits pequeños
  por cambio lógico. No se debe declarar terminada la entrega sin evidencia real.
- Único integrante confirmado: Pablo Tamayo, pablotago@unisabana.edu.co.
- Cuenta GitHub confirmada para fork, publicación de código y Wiki: `ItsN3M3515`.
- `origin` apunta al fork; `upstream` conserva el repositorio del profesor.
- El usuario autorizó una excepción al gate HomeLab **solo para diagnóstico local de
  Docker en modo lectura**. No autorizó cambios de servicios, firewall, módulos ni reinicio.
- El gate HomeLab no llegó a READY. El intento restringido falló por red/permisos;
  la revisión automática rechazó ejecutarlo con acceso al host porque puede despertar Ark.
  No intentar eludir ese rechazo. El trabajo de ejecución se trasladó a un runner aislado.

## Cambios y comprobaciones

- `f4698a5`: Mockito se carga como agente de pruebas desde Maven; se preserva JaCoCo.
- `8b29451`: noveno gráfico, panel 12, tráfico de inventario por endpoint.
- `8b42049`: integrante, arquitectura, portada y reflexión del Wiki.
- `86a9988`: guías de medición y resultado del build desde un directorio temporal nuevo.
- `c200b63`: workflow manual y colector de evidencia sobre el stack real.
- `464ec67`: corrección del significado de metadata de Grafana y del arranque de k6.

La verificación desde cero con JDK 21 terminó el 8 de noviembre de 2026 a las 22:57:21
UTC: 47 pruebas correctas; cobertura de líneas 182/186 (97,85%) y de ramas 38/40 (95%).
El resumen está en `evidence/build-verification.json`. Una ejecución incremental había
reutilizado clases compiladas con metadatos de líneas diferentes; no usar ese resultado
para sustituir la medición del build nuevo.

CI estándar verificado en verde:
https://github.com/ItsN3M3515/DYAS-Monitoreo/actions/runs/42532932496

## Docker local: último diagnóstico, sin reparación

En la comprobación de lectura del 8 de noviembre de 2026, aproximadamente a las 22:49
UTC, el kernel era `7.3.0-4-cachyos`, sin directorio de módulos instalado para esa
versión. Había directorios para `7.3.3-1-cachyos` y `6.18.60-2-cachyos-lts`.
`xt_addrtype` no estaba cargado. Docker había fallado al crear una regla NAT y systemd
había llegado a `start-limit-hit`. Ver el detalle en `wiki/Verificacion.md`.

No inferir de este diagnóstico que un reinicio ya se haya hecho ni que resolvería
cualquier otro problema. No se modificó el host. Una reparación del host sigue
requiriendo autorización y las instrucciones de su vault.

## Evidencia de ejecución: tarea activa

Primer intento aislado:
https://github.com/ItsN3M3515/DYAS-Monitoreo/actions/runs/42533260244

El stack inició correctamente. El colector falló por una aserción incorrecta:
Grafana 13.2.3 deja `meta.provisioned=false` cuando `allowUiUpdates=true`. Su implementación
en `pkg/api/dashboard.go`, líneas 214-222, confirma que la bandera controla la edición.
Se verifica ahora `provisionedExternalId` y el contenido del panel. Se corrigió además
la carrera de limpieza con k6: su arranque se espera y usa `--no-deps`.

Segundo intento, en progreso al escribir esta nota:
https://github.com/ItsN3M3515/DYAS-Monitoreo/actions/runs/42533717336

El workflow inicia una VM nueva, levanta Compose con `--wait`, genera tráfico y recoge
datos y capturas mediante `tools/workshop_evidence.py`. Restablece las fallas y apaga
únicamente el stack del runner al terminar. No requiere reparar Powerstation.

## Publicación y continuación

- Wiki: https://github.com/ItsN3M3515/DYAS-Monitoreo/wiki
- Copia fuente de las páginas: `wiki/`. Su contenido debe mantenerse igual al Wiki.
- El usuario ya inicializó el Wiki; no volver a pedirlo.
- Checkout temporal del Wiki: `/tmp/dyas-monitoreo-wiki`.
- Las páginas de ejecución todavía dicen pendiente; actualizar solo con datos observados.
- Descargar el artefacto `workshop-evidence` del intento exitoso; comprobar resultados y
  revisar visualmente las capturas antes de incorporarlas a `evidence/` y al Wiki.
- Conservar en Git capturas, resultados de consultas, trazas y logs correlacionados:
  el artefacto de Actions caduca a los siete días. No usar imágenes del profesor como propias.
- Hacer commits separados para evidencia normal/métricas, evidencia de fallas y resultados
  documentados; publicar el código y el Wiki y verificar los hashes remotos.
