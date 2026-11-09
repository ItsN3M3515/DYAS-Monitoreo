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

| Criterio de la rúbrica | Resultado y evidencia |
|---|---|
| Repositorio y stack | Fork e integrante identificados; 47 pruebas correctas, cobertura de líneas 97,85% y arranque desde cero: [verificación](Verificacion) |
| Métricas y PromQL | Dos targets UP; consultas 3/5/6/7 con resultados originales e interpretación: [métricas](Metricas) |
| Dashboard en Grafana | Nueve gráficos con datos; panel adicional versionado y cargado desde `tienda.json` en una instancia nueva: [dashboard](Dashboard) |
| Trazas distribuidas | Trazas normal y lenta de ambos servicios; inventario explica la demora de 800 ms: [trazas](Trazas) |
| Alertas | Ambas reglas Pending/Firing/Inactive, dashboard durante la falla y recuperación después del reset: [alertas](Alertas) |
| Correlación de logs y trazas | Logs ERROR de ambos servicios y traza con el mismo traceId, relacionados con las métricas: [correlación](Correlacion) |
| Documentación en Wiki | Secciones completas, diagrama propio y capturas originales: [arquitectura](Arquitectura) y páginas de este índice |
| Reflexión técnica | Las cinco preguntas del enunciado, con resultados propios y aplicación al Proyecto 3: [reflexión](Reflexion-final) |

## Enlaces para entregar

La entrega oficial es este Wiki; el README no exige PDF. Estos enlaces identifican el
trabajo y pueden copiarse en la actividad del curso:

```text
Taller de Monitoreo y Observabilidad
Integrante: Pablo Tamayo — pablotago@unisabana.edu.co
Repositorio: https://github.com/ItsN3M3515/DYAS-Monitoreo
Wiki (documentación y evidencias): https://github.com/ItsN3M3515/DYAS-Monitoreo/wiki
Ejecución completa: https://github.com/ItsN3M3515/DYAS-Monitoreo/actions/runs/42535601486
```

La publicación en GitHub conserva el trabajo; el envío a la actividad académica se
realiza por separado en la plataforma indicada por el curso.

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
