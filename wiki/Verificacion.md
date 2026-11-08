# Verificación y evidencias

## Resultado de la entrega

El [run completo 42535601486](https://github.com/ItsN3M3515/DYAS-Monitoreo/actions/runs/42535601486)
terminó correctamente el 8 de noviembre de 2026. Los ejercicios finalizaron a las
**18:38:36 Bogotá (23:38:36 UTC)**, con el simulador restablecido y ambas alertas Inactive.

Se verificaron el arranque del stack desde cero, cuatro servicios saludables y Jaeger
running, los dos targets de aplicación UP, las consultas 3/5/6/7, nueve gráficos con
datos, trazas normal/lenta/fallida con tres spans conectados, el ciclo de ambas reglas
y los logs ERROR coincidentes. Los archivos originales y sus hashes están en
[`evidence/`](https://github.com/ItsN3M3515/DYAS-Monitoreo/tree/main/evidence).

## Build y pruebas

El 8 de noviembre de 2026 a las **17:57:21 Bogotá (22:57:21 UTC)** terminó correctamente
una verificación en un directorio temporal nuevo con Java 21 y Maven 3.9.16:

```sh
mvn -o -B verify
```

Se seleccionó JDK 21 solo para ese proceso; no se cambió el Java predeterminado.
`-o` usa las dependencias ya presentes en caché. Sin esa caché se necesita red y se
usa `mvn -B verify`.

- 47 pruebas, cero fallas, cero errores y cero omisiones.
- Cobertura de líneas: 182/186, **97,85%**, superior al mínimo de 80%.
- Cobertura de ramas: 38/40, **95%**.
- JAR ejecutable generado y verificación de JaCoCo correcta.
- Compose, YAML y JSON válidos; nueve gráficos con IDs únicos sin superposición.

[Resumen original del build](https://github.com/ItsN3M3515/DYAS-Monitoreo/blob/main/evidence/build-verification.json).
También pasó el [CI estándar](https://github.com/ItsN3M3515/DYAS-Monitoreo/actions/runs/42532932496),
que compila, prueba, verifica cobertura, construye la imagen y valida Prometheus.

## Problemas encontrados y resolución

1. El primer intento local de pruebas falló al conectar el agente de Mockito a la JVM.
   El POM ahora lo carga al iniciar las pruebas, conservando JaCoCo, siguiendo la
   [configuración de Mockito](https://javadoc.io/static/org.mockito/mockito-core/5.23.0/org.mockito/org/mockito/Mockito.html#0.3).
   El build exitoso no necesitó el workaround de `JAVA_TOOL_OPTIONS`.
2. La ejecución incremental había conservado clases con metadatos de líneas diferentes
   y produjo otra cobertura. Se verificó en un directorio nuevo para usar una medición
   reproducible, sin mezclar reportes anteriores.
3. La primera ejecución aislada inició el stack pero falló en una aserción del colector:
   Grafana deja `meta.provisioned=false` si `allowUiUpdates=true`. Su
   [implementación](https://github.com/grafana/grafana/blob/v13.2.3/pkg/api/dashboard.go#L214)
   confirma que la bandera controla edición. Se verificaron el nombre de archivo
   `provisionedExternalId` y la consulta del panel. También se corrigió una carrera:
   k6 debe terminar de arrancar antes de poder detenerlo y debe usar `--no-deps` para
   no recrear los servicios ya iniciados.
4. Las capturas iniciales fueron blancas. Se actualizó el navegador y se añadieron
   comprobaciones de contenido y diagnóstico; no se aisló cuál de esos dos cambios
   resolvió esas páginas iniciales. Después, una ejecución pasó los checks de backend,
   pero la revisión visual detectó canvas omitidos y trazas con un padre ausente.
5. Un [diagnóstico específico](https://github.com/ItsN3M3515/DYAS-Monitoreo/actions/runs/42535152562)
   comprobó que los canvas tenían datos y que los screenshots de viewport mostraban
   los gráficos, con y sin GPU. Las capturas full-page omitían esos mismos gráficos.
   Se usó un viewport que incluye los nueve paneles y se verificaron sus píxeles.
6. Las trazas seleccionadas antes recibían un padre artificial del colector, sin un
   span exportado para ese padre. Se dejó que pedidos creara la raíz y se recuperó
   el traceId del log real. Se exigieron una raíz y todos los enlaces de padres.
   La ejecución final y la revisión visual verificaron ambas correcciones.

No se reutilizan las capturas rechazadas ni se presentan los intentos previos como
si fueran la ejecución final. Las reglas Prometheus originales no se alteraron.

## Docker de Powerstation: diagnóstico separado

En el diagnóstico local de solo lectura, el kernel en ejecución era `7.3.0-4-cachyos`,
pero los módulos instalados eran de `7.3.3-1-cachyos` y `6.18.60-2-cachyos-lts`.
Faltaba el directorio de módulos de la versión ejecutada y `xt_addrtype` no estaba
cargado. El registro de Docker mostraba un fallo al crear una regla NAT por falta
presunta de soporte `addrtype`; systemd llegó a `start-limit-hit`.

La incompatibilidad explica de forma consistente el error. No se modificaron módulos,
servicios ni firewall y no se reinició el host. El taller se ejecutó en una VM nueva
de GitHub; no se afirma que Powerstation se haya reparado. Su recuperación queda
como una tarea de host separada, con las autorizaciones y el gate de su vault.

## Límites de la medición

k6 se configuró a diez iteraciones/s y se detuvo al completar las evidencias, antes de
su máximo de doce minutos. Por eso su log termina con SIGTERM y una iteración
interrumpida. Registró 2.815 iteraciones completas, 7.807 solicitudes HTTP, 220 checks
fallidos por los errores previstos y ocho iteraciones descartadas. Los registros no
identifican la causa exacta de esos ocho descartes. No es un benchmark de capacidad.

La medición de p95 usa un histograma y una ventana; difiere de la duración de un span
individual. Los datos describen el runner de esta ejecución, no producción. El runner
se apagó después del workflow: las evidencias son duraderas, sus servicios localhost no.
