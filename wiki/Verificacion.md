# Verificación y evidencias

## Resultados ejecutados

El 8 de noviembre de 2026 a las **17:57:21 Bogotá (22:57:21 UTC)** terminó correctamente
la verificación en un directorio temporal nuevo con Java 21 y Maven 3.9.16:

```sh
mvn -o -B verify
```

Se seleccionó el JDK 21 para el proceso; no se cambió el Java predeterminado del sistema.
`-o` utiliza las dependencias ya presentes en la caché. En una máquina sin esa caché
se necesita acceso de red y se ejecuta `mvn -B verify`.

- 47 pruebas ejecutadas, cero fallas, cero errores y cero omisiones.
- Cobertura de líneas: 182 de 186, **97,85%**, superior al mínimo del 80%.
- Cobertura de ramas: 38 de 40, **95%**.
- JAR ejecutable generado correctamente.
- `docker compose config --quiet` correcto.
- YAML y JSON válidos; nueve gráficos, con IDs únicos y sin superposición.

El resumen comprobado contra los reportes XML está en
[`evidence/build-verification.json`](https://github.com/ItsN3M3515/DYAS-Monitoreo/blob/main/evidence/build-verification.json).
Se usó un directorio nuevo para evitar reutilizar las clases compiladas de `target/`:
la ejecución incremental había conservado clases con metadatos de líneas diferentes
y mostrado otra cobertura. El resultado anterior no se mezcló con la medición final.

El primer intento de pruebas falló en la inicialización de Mockito al intentar conectar
su agente a Java. El `pom.xml` ahora carga ese agente al iniciar el proceso de pruebas y
conserva el de JaCoCo, siguiendo la
[configuración documentada por Mockito](https://javadoc.io/static/org.mockito/mockito-core/5.23.0/org.mockito/org/mockito/Mockito.html#0.3).
La ejecución exitosa no usó el workaround temporal de `JAVA_TOOL_OPTIONS`.

## Bloqueo de Docker

El servicio Docker local está fallido por `start-limit-hit`. Su registro muestra que
la inicialización de red no pudo crear una regla NAT por falta de soporte `addrtype`.
Se observó un kernel en ejecución `7.3.0-4-cachyos`, mientras los directorios de módulos
instalados corresponden a `7.3.3-1-cachyos` y `6.18.60-2-cachyos-lts`. No existe el
directorio de módulos del kernel en ejecución, y `xt_addrtype` no está cargado.

La incompatibilidad explica de forma consistente el error, pero todavía falta comprobar
que arrancar con un kernel instalado resuelva todo el inicio del stack. No se modificaron
servicios, módulos ni reglas del host como parte de este diagnóstico de solo lectura.

## Resultados aún no ejecutados

Faltan el build de Docker, el arranque saludable de los servicios, los targets UP,
las mediciones PromQL, las capturas, las trazas, el ciclo de alertas, la correlación
y la verificación del panel aprovisionado en una instancia nueva. No se declara
completado ninguno de esos puntos.
