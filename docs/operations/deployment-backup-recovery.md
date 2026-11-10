# Estrategia de despliegue, configuración, copias de seguridad y recuperación — CPIE

- Issue rector: #56
- Gobierno de cambios: ../governance/engineering-workflow.md
- Estrategia de pruebas: ./test-strategy.md
- Matriz de trazabilidad: ../governance/requirements-controls-evidence-matrix.md
- Roadmap: ../governance/remediation-roadmap.md
- Estado: diseño inicial; no existen todavía servicios CPIE desplegables ni procedimientos de recuperación probados.
- Fecha: 2026-11-10

## 1. Propósito y límites

Definir los controles de ciclo de vida operacional para construir, configurar, desplegar, respaldar, restaurar y recuperar CPIE. La estrategia prioriza reproducibilidad, protección de datos, mínimo privilegio y recuperación consistente de estados financieros y de órdenes.

Este documento no acredita que haya infraestructura, backups, despliegues ni recuperación implementados. Tampoco selecciona proveedor cloud, orquestador, base de datos, política de retención ni objetivos RPO/RTO. Esas decisiones requieren arquitectura, análisis de riesgo, costes, obligaciones legales y pruebas.

## 2. Principios operativos

1. Separación estricta de entornos y credenciales.
2. Configuración declarativa y versionada; secretos fuera del repositorio.
3. Artefactos de despliegue identificables, reproducibles y vinculados a commit.
4. Cambios de esquema compatibles, auditables y con plan de reversión.
5. Backups cifrados, protegidos contra borrado/alteración y restaurables.
6. Una copia de seguridad no se considera válida hasta que se restaura y verifica.
7. Recuperación idempotente: reiniciar procesos no debe duplicar órdenes, fills ni eventos.
8. Fallo seguro: si el estado de una orden o la integridad de los datos no puede reconciliarse, bloquear nuevas operaciones y requerir resolución.
9. Observabilidad y auditoría sin registrar secretos ni información sensible innecesaria.
10. LIVE permanece bloqueado hasta superar los controles específicos de trading, seguridad, cumplimiento y autorización.

## 3. Entornos

| Entorno | Propósito | Datos y credenciales | Restricciones |
|---|---|---|---|
| Local development | Desarrollo aislado y depuración. | Datos sintéticos o datasets de prueba autorizados; credenciales ficticias. | No conectar cuentas con fondos reales por defecto. |
| Test/CI | Validación automatizada reproducible. | Fixtures sintéticos y servicios efímeros; secretos de prueba mínimos. | Prohibidas órdenes reales y datos sensibles de producción. |
| Staging | Ensayo integrado previo a release. | Datos anonimizados/sintéticos o autorizados; sandbox de proveedores. | Sin capital real; configuración separada de producción. |
| Production | Servicio real aprobado. | Datos y credenciales de producción protegidos. | Activación por gate, permisos mínimos, monitoreo, backup y rollback probados. |

Cada entorno debe tener identificador, configuración, fuentes de datos, endpoints, roles, secretos, límites y políticas explícitas. Está prohibido reutilizar accidentalmente credenciales de producción en local, test o staging.

## 4. Configuración y secretos

- Separar configuración no sensible de secretos.
- Validar configuración al iniciar; fallar explícitamente ante campos requeridos ausentes o inválidos.
- No usar valores por defecto inseguros para autenticación, cifrado, permisos o trading.
- Inyectar secretos desde un mecanismo dedicado de gestión de secretos; nunca desde código, archivos versionados, imágenes o logs.
- Limitar el acceso por servicio, entorno y función; registrar lectura/cambio cuando la plataforma lo permita.
- Rotar credenciales según riesgo, política del proveedor y ante exposición o sospecha.
- API keys de exchange sin permisos de retiro; separar permisos de lectura y trading cuando el proveedor lo permita.
- Los modelos y procesos de investigación no deben leer secretos de ejecución ni modificar permisos.
- En caso de exposición: revocar/rotar inmediatamente, preservar evidencia sin copiar el secreto y gestionar incidente mediante Issue restringido si contiene detalles sensibles.

La selección de tecnología de secretos y cifrado se resolverá en ADR cuando se conozcan el entorno y las restricciones reales.

## 5. Construcción y despliegue

Todo release debe identificar:
- Commit SHA, branch y PR de origen.
- Versión del código y artefactos construidos.
- Dependencias y versiones, idealmente con lockfiles/manifiestos.
- Configuración del entorno y migraciones requeridas, excluyendo secretos.
- Checks y pruebas ejecutados, resultados y excepciones.
- Compatibilidad conocida, riesgos y procedimiento de rollback.
- Responsable/rol que autoriza la promoción.

Flujo objetivo:
1. Crear artefacto desde un commit identificado.
2. Ejecutar validaciones estáticas, pruebas y análisis de seguridad aplicables.
3. Publicar artefacto inmutable con hash o identificador verificable.
4. Desplegar en test/staging y ejecutar smoke/integration tests.
5. Revisar métricas, logs y comportamiento inicial.
6. Promover el mismo artefacto probado; no reconstruir silenciosamente otro artefacto para producción.
7. Registrar release, aprobaciones, cambios y resultado.
8. Si se detecta regresión, detener promoción y ejecutar rollback o mitigación documentada.

La estrategia de despliegue progresivo (canary, blue/green u otra) se seleccionará solo si la arquitectura y el coste operacional lo justifican.

## 6. Migraciones y cambios de esquema

- Toda migración debe estar versionada y asociada a Issue/PR.
- Revisar compatibilidad entre versión anterior y nueva de aplicación.
- Preferir cambios aditivos y fases expand/contract cuando sea viable.
- Definir precondiciones, impacto, duración estimada basada en medición, locks y consumo de recursos.
- Hacer backup/snapshot antes de cambios destructivos cuando aplique.
- Probar migración y rollback en un entorno representativo con datos sintéticos o autorizados.
- No asumir que revertir el código revierte automáticamente una migración de datos.
- Registrar versión de esquema y estado de migración.
- Ante migración parcial o inconsistente, detener el despliegue y aplicar runbook; no repetir ciegamente.

## 7. Copias de seguridad y retención

Antes de seleccionar frecuencia y retención, identificar clases de datos, criticidad, coste, obligaciones legales, volumen y tasa de cambio. No fijar números arbitrarios.

El plan debe determinar para cada clase:
- Qué se respalda: base de datos, archivos, objetos, configuraciones no secretas, manifiestos, metadatos, modelos y artefactos necesarios para reproducir.
- Método: snapshot consistente, backup lógico/físico, versionado de objetos u otra técnica validada.
- Frecuencia y retención, justificadas por RPO y riesgo de pérdida.
- Cifrado en tránsito y reposo; custodia y rotación de claves.
- Separación de permisos entre operador y administrador de backups.
- Protección frente a borrado accidental, ransomware y corrupción.
- Ubicación, redundancia y dependencias regionales/proveedor.
- Verificación de integridad, catálogo e inventario de copias.
- Caducidad y borrado conforme a política y obligaciones aplicables.

No incluir credenciales ni secretos de producción en backups ordinarios de configuración. Si un secreto debe respaldarse por necesidad operacional, utilizar mecanismo separado, cifrado y acceso altamente restringido.

## 8. Restauración y recuperación

Un procedimiento de recuperación debe documentar:
1. Condición de activación y autoridad que declara incidente.
2. Alcance afectado y clasificación de datos/servicios.
3. Aislamiento de componentes dañados o comprometidos.
4. Selección de backup/snapshot íntegro y compatible.
5. Restauración en entorno controlado.
6. Validación de integridad, conteos, hashes, relaciones y consistencia temporal.
7. Reaplicación controlada de cambios/eventos posteriores al snapshot cuando proceda.
8. Reconciliación de estados con sistemas externos.
9. Validación funcional y de seguridad antes de reabrir tráfico.
10. Autorización de retorno, monitoreo reforzado y revisión post-incidente.

La restauración no debe sobrescribir la única copia válida ni destruir evidencia del incidente. Los ejercicios deben medir tiempos observados; RTO/RPO solo se declaran cumplidos tras prueba y dentro del alcance probado.

## 9. Recuperación específica de trading

La recuperación del sistema de trading tiene controles adicionales y no se reduce a restaurar la base de datos.

- Tras reinicio o desconexión, mantener bloqueada la creación de nuevas órdenes hasta reconciliar el estado local con el exchange.
- Consultar órdenes abiertas, órdenes históricas, fills, balances y posiciones mediante APIs autorizadas.
- Usar identificadores de cliente idempotentes cuando el exchange los soporte; persistirlos antes de enviar la orden.
- Distinguir orden enviada, aceptada, rechazada, parcialmente ejecutada, completada, cancelada y estado desconocido.
- Si se perdió la respuesta al envío, consultar primero el estado remoto; no reenviar a ciegas.
- Registrar discrepancias y resolverlas mediante flujo auditable.
- Reprocesar eventos de forma idempotente y conservar orden/offset/identificador de origen.
- Probar escenarios de fills parciales, cancelación concurrente, retrasos, rate limits, eventos repetidos y respuestas fuera de orden.
- Si no puede garantizarse consistencia, pasar a estado seguro (no nuevas órdenes) y solicitar intervención autorizada.
- No reactivar LIVE automáticamente después de un reinicio, restauración o despliegue.

Los simuladores y sandbox deben cubrir estos escenarios antes de considerar cualquier promoción operativa. El acceso LIVE requiere gates y autorización independientes.

## 10. Observabilidad e incidentes

Registrar de forma estructurada:
- Identificador de servicio, entorno, versión y commit.
- Correlation/request ID y trace ID cuando aplique.
- Estado de health/readiness y dependencias.
- Errores, reintentos, latencia y resultados de jobs.
- Eventos de configuración, despliegue, migración y recuperación.
- Operaciones sensibles con actor/rol, autorización, resultado y referencia de auditoría.

No registrar tokens, claves API, contraseñas, secretos, datos personales innecesarios ni payloads financieros sensibles sin controles específicos. Definir niveles de severidad, escalamiento, comunicación, preservación de evidencia y revisión post-incidente.

## 11. Pruebas operativas obligatorias antes de producción

- Configuración inválida o incompleta impide iniciar de forma insegura.
- Secretos ausentes, expirados o con permisos insuficientes generan fallo controlado.
- Backup consistente y restauración íntegra.
- Restauración de archivos/objetos y metadatos asociados.
- Migración, compatibilidad y rollback en entorno representativo.
- Pérdida de conectividad con base de datos/proveedor y recuperación.
- Reinicio durante un job y reanudación sin duplicar efectos.
- Reconciliación de órdenes/fills/posiciones en simulación.
- Revocación/rotación de credenciales y respuesta a exposición simulada.
- Health checks y alertas accionables.
- Verificación de que LIVE permanece bloqueado en entornos no autorizados y después de recuperación.

Cada prueba debe seguir la estrategia de docs/quality/test-strategy.md y conservar evidencia reproducible.

## 12. Decisiones pendientes de ADR

No fijar hasta contar con requisitos, arquitectura y evidencia:
- Proveedor/entorno de despliegue y regiones.
- Contenedores/orquestación, si se justifican.
- Base de datos, almacenamiento de objetos y mecanismo de backup.
- Gestión de secretos, cifrado y custodia de claves.
- Frecuencia/retención de backups.
- RPO/RTO por clase de servicio/dato.
- Estrategia de migración y rollback.
- Alta disponibilidad y recuperación regional.
- Herramientas de observabilidad y gestión de incidentes.

Cada ADR debe comparar alternativas, costes, riesgos, portabilidad, dependencia del proveedor y requisitos legales.

## 13. Criterios de implantación

- [ ] Entornos y límites de seguridad definidos.
- [ ] Configuración validada y secretos fuera del repositorio/logs.
- [ ] Artefactos reproducibles e identificados por commit/hash.
- [ ] Despliegue y rollback probados en entorno representativo.
- [ ] Migraciones versionadas y estrategia de compatibilidad verificada.
- [ ] Backups definidos con frecuencia/retención justificadas.
- [ ] Restauración probada y evidencia conservada.
- [ ] RPO/RTO definidos por análisis de impacto y demostrados mediante pruebas.
- [ ] Recuperación de jobs y estados idempotente.
- [ ] Reconciliación de órdenes y fills probada en simulación.
- [ ] Runbooks, alertas y gestión de incidentes probados.
- [ ] Autorización LIVE independiente; reactivación automática prohibida.

## 14. Estado actual y limitaciones

A fecha de esta versión:
- No hay aplicación ni servicio CPIE desplegable verificado.
- No hay infraestructura, pipeline de despliegue ni entornos test/staging/production configurados en el repositorio.
- No se ha seleccionado proveedor ni stack de despliegue.
- No hay política aprobada de backup/retención ni pruebas de restauración.
- No existen RPO/RTO definidos y medidos.
- No hay runbooks operativos probados ni evidencia de recuperación de órdenes.
- La estrategia es documental; no demuestra controles técnicos implementados.
- LIVE permanece bloqueado.

## 15. Historial

| Fecha | Cambio |
|---|---|
| 2026-11-10 | Primera versión de la estrategia de despliegue, configuración, backups y recuperación. |
