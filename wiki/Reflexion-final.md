# Reflexión técnica

Esta reflexión se basa en el código y en la ejecución propia del taller. Las páginas
de resultados conservan las capturas, los JSON y los timestamps de las observaciones.

## Monitoreo y observabilidad

El monitoreo comprueba condiciones conocidas: por ejemplo, si la proporción de errores
5xx supera el 5%. La observabilidad permite investigar qué ocurre dentro del sistema
usando las señales disponibles. En este taller, una alerta podría mostrar que pedidos
está fallando; los logs con `traceId` y la traza permitirían averiguar si el error se
originó en inventario y cómo llegó hasta la respuesta al cliente.

La alerta es el comienzo de la investigación. En la ejecución propia, la proporción
5xx llegó a 26,27% en inventario y 15,84% en pedidos. El mismo traceId apareció en
ambos logs y en una traza con 500 en inventario y 503 en pedidos. Así se pudo atribuir
la causa a la dependencia usando evidencias del mismo intervalo y de la misma petición.

## Percentiles frente al promedio

El promedio resume todas las duraciones en una sola cifra y puede ocultar solicitudes
muy lentas. Por ejemplo, 95 solicitudes de 10 ms y cinco de 2.000 ms tienen un promedio
de 109,5 ms, aunque cinco usuarios esperaron dos segundos. Un percentil permite describir
la experiencia de una fracción concreta de solicitudes y definir un objetivo de servicio.

El p95 estima un límite que cubre el 95% de las observaciones. No garantiza la experiencia
del 5% restante. En Prometheus se calcula a partir de los buckets del histograma, por
lo que es una estimación: hacen falta una ventana con tráfico y suficiente resolución
en los buckets para interpretarlo correctamente.

## Por qué 404 y 409 no activan la alerta de errores

En este escenario, `tablet` no existe y `portatil` no tiene stock. Responder 404 o 409
es el comportamiento previsto de la aplicación, mientras que 500 o 503 representan
una falla del servicio o de su dependencia. La regla selecciona solo `status=~"5.."`
para medir este segundo caso y evitar alertas causadas por solicitudes de negocio que
el taller genera deliberadamente.

Eso no convierte todos los 4xx de cualquier sistema en irrelevantes. Un aumento anormal
de rechazos puede necesitar su propia investigación; la decisión depende del significado
del código en cada producto y del objetivo que se desea medir.

## Qué cambia con RestClient.create()

La implementación usa el builder autoconfigurado de Spring Boot. Ese builder incorpora
la observación de la llamada y la propagación del contexto mediante `traceparent`.
Sustituirlo por un cliente creado directamente con `RestClient.create()`, sin añadir
instrumentación equivalente, elimina esa configuración en este proyecto.

La reserva podría seguir funcionando como operación HTTP, pero inventario ya no recibiría
automáticamente el contexto de la petición de pedidos. El resultado esperado serían
trazas separadas, y se perdería la relación padre-hijo necesaria para recorrer ambos
servicios como una sola petición. Ese cambio no se ha aplicado a la entrega.

## Aplicación a la bonificación del Proyecto 3

En el proyecto del curso habría que instrumentar sus servicios reales, configurar sus
targets en Prometheus y adaptar las métricas de negocio a ese dominio. El tablero debe
mostrar throughput, errores y p95 con umbrales derivados del SLO acordado para el proyecto;
copiar el valor de 500 ms del taller sin justificarlo no define ese objetivo.

También se necesitan reglas de alerta accionables, contexto de traza entre al menos dos
componentes y logs con `traceId`. Si se elige la vía de logs centralizados, hacen falta
un colector y un sistema con búsqueda, como Alloy y Loki. El stack actual solo conserva
logs en los contenedores y muestra alertas en Prometheus: no incluye Alertmanager ni
notificaciones externas.

La evidencia del proyecto debe demostrar que esa configuración funciona en sus propios
flujos, con métricas y trazas reales. La preparación de este taller no demuestra por sí
sola que la bonificación del otro proyecto ya se haya cumplido.

## Lo que aportó la ejecución

Con 800 ms de latencia artificial, el span de inventario midió 800,646 ms y la
solicitud completa en pedidos 802,905 ms. La traza mostró dónde estaba la espera;
las métricas agregadas y sus alertas mostraron su impacto en ambos servicios.
Restablecer el simulador no hizo desaparecer inmediatamente las alertas, porque
sus consultas aún incluían muestras anteriores en la ventana de un minuto.

La verificación necesitó varias capas: una API podía devolver datos correctos y, aun
así, una captura omitir los gráficos; tres spans con el mismo traceId podían conservar
un padre externo ausente. Se comprobó el contenido de los canvas, se revisaron las
imágenes y se exigió una raíz real con todos sus enlaces. Pasar una comprobación
automática ayudó, pero no sustituyó revisar el resultado que debía ver el evaluador.
