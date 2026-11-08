# Taller de monitoreo y observabilidad

**Integrante:** Pablo Tamayo — pablotago@unisabana.edu.co.

**Repositorio:** https://github.com/ItsN3M3515/DYAS-Monitoreo

## Propósito

El taller utiliza una tienda pequeña para aprender a reconocer una falla y encontrar su
causa mediante métricas, logs y trazas. El caso importante es crear un pedido: la
solicitud entra al servicio `pedidos`, que necesita reservar unidades en `inventario`.
Una demora o un error de inventario puede afectar al cliente de pedidos, aunque sean
procesos diferentes.

El objetivo es demostrar ese efecto con datos de una ejecución propia y explicar cómo
se conectan las señales. La lógica de tienda sirve como escenario para el diagnóstico.

## Estado verificable de la entrega

Esta entrega está **ejecutada y documentada**. El [run completo 42535601486](https://github.com/ItsN3M3515/DYAS-Monitoreo/actions/runs/42535601486)
levantó el stack desde cero en una VM aislada de GitHub, generó tráfico, verificó las
consultas y trazas, provocó fallas, observó las alertas y comprobó la recuperación.
Los ejercicios se realizaron el 8 de noviembre de 2026, aproximadamente entre las
**18:33:53 y 18:38:36 Bogotá (23:33:53 a 23:38:36 UTC)**.

El Docker de Powerstation tenía un problema de kernel/módulos y no fue reparado:
la ejecución aislada permite verificar el repositorio sin modificar ese host. Las
mediciones corresponden al runner, no al rendimiento de Powerstation ni a producción.

No se presentan las imágenes de ejemplo del profesor como resultados propios.
Las tablas de resultados distinguen mediciones propias de los ejemplos explicativos.

| Elemento | Estado |
|---|---|
| Fork e identificación del integrante | Confirmados |
| Pruebas y cobertura | 47 pruebas correctas; umbral de cobertura superado |
| Panel adicional versionado | Cargado desde `tienda.json` en una instancia nueva; nueve gráficos con datos |
| Arquitectura y reflexión técnica | Documentadas y conectadas con los resultados |
| Stack, consultas y capturas propias | Stack saludable, dos targets UP, consultas 3/5/6/7 y capturas originales |
| Trazas normales, lentas y con error | Tres spans de dos servicios, una raíz real y cadena de padres completa |
| Ciclo de alertas y correlación | Ambas reglas Pending/Firing/Inactive; logs de los dos servicios con el mismo traceId |

## Lectura de la entrega

- [Arquitectura del sistema](Arquitectura)
- [Métricas y consultas PromQL](Metricas)
- [Dashboard y panel adicional](Dashboard)
- [Trazas distribuidas](Trazas)
- [Alertas y recuperación](Alertas)
- [Correlación de logs y trazas](Correlacion)
- [Reflexión técnica](Reflexion-final)
- [Verificación y evidencias](Verificacion)

El enunciado completo y la rúbrica se conservan en el
[README del repositorio](https://github.com/ItsN3M3515/DYAS-Monitoreo/blob/main/README.md).
La documentación oficial del taller se publica en este Wiki; los archivos de `wiki/`
del repositorio mantienen una copia versionada de su contenido.
