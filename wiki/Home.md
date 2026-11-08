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

Esta entrega está **en preparación**. Las pruebas de Java y las validaciones estáticas
ya se ejecutaron. La ejecución de Docker y las evidencias de Prometheus, Grafana y Jaeger
están pendientes: el Docker local falla al iniciar su red, en un entorno cuyo kernel en
ejecución no tiene instalado su directorio de módulos correspondiente.

No se presentan las imágenes de ejemplo del profesor como resultados propios. Los
valores esperados que aparecen en las explicaciones tampoco son mediciones realizadas.

| Elemento | Estado |
|---|---|
| Fork e identificación del integrante | Preparados |
| Pruebas y cobertura | 47 pruebas correctas; umbral de cobertura superado |
| Panel adicional versionado | Implementado; visualización en vivo pendiente |
| Arquitectura y reflexión técnica | Redactadas a partir del código y la guía |
| Stack, consultas y capturas propias | Pendientes de ejecución |
| Trazas normales, lentas y con error | Pendientes de ejecución |
| Ciclo de alertas y correlación | Pendientes de ejecución |

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
La documentación oficial del taller se publicará en este Wiki; los archivos de `wiki/`
del repositorio mantienen una copia versionada de su contenido.
