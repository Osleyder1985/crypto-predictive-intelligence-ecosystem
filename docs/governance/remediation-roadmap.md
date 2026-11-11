# Programa maestro de remediación y excelencia de CPIE

- **Proyecto:** Crypto Predictive Intelligence Ecosystem (CPIE)
- **Issue rector:** [#70 — Programa maestro de remediación y excelencia](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/70)
- **Auditoría inicial:** [#67](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/67)
- **Última reauditoría:** [#71](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/71)
- **Estado del programa:** Planificado; ninguna fase se considera completada por la existencia de este documento.

## 1. Propósito y alcance

Este documento establece el orden de remediación, los entregables, las dependencias y los criterios de salida para llevar CPIE desde su estado inicial de planificación hasta una plataforma de inteligencia predictiva y trading algorítmico verificable, segura y operable.

El roadmap coordina los Issues existentes. No los sustituye, no autoriza cierres sin evidencia y no implica que los trabajos descritos estén implementados.

## 2. Principios de ejecución

1. Mantener trazabilidad: requisito → Issue → ADR/decisión → PR → pruebas → evidencia → release.
2. Registrar cada problema o decisión material en un Issue; entregar cambios mediante Pull Request vinculado.
3. No integrar directamente en `main` cuando el flujo de PR esté habilitado.
4. No declarar una capacidad implementada, validada, segura, conforme o terminada sin evidencia reproducible.
5. No inventar métricas, umbrales, probabilidades, resultados ni certificaciones.
6. Distinguir alineación normativa, controles implementados, controles verificados y certificación independiente.
7. Mantener trading LIVE bloqueado hasta superar los controles de seguridad, validación, cumplimiento y autorización.
8. Desarrollar web, Android e iOS incrementalmente desde las primeras fases, según [#66](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/66).
9. Preferir una arquitectura modular simple; introducir infraestructura distribuida solo cuando exista necesidad demostrada.
10. Permitir avance por entregables independientes cuando sus dependencias estén satisfechas, sin forzar el cierre masivo de una fase.

## 3. Fases del programa

### Fase 0 — Auditoría, gobierno y control del cambio

- **Objetivo:** establecer una base de control verificable.
- **Issues:** #6, #67, #68, #71.
- **Entregables:** registro de hallazgos; protección efectiva de ramas; reglas de PR, bypass y permisos; convenciones de Issues/PR; ADR y trazabilidad.
- **Salida:** configuración efectiva de `main` verificada; PR obligatorio y protecciones críticas activas o excepciones justificadas; flujo PR probado; hallazgos trazados y priorizados.

### Fase 1 — Alcance, requisitos y gobierno de calidad

- **Objetivo:** especificar producto, usuarios, límites y criterios verificables de calidad.
- **Issues:** #1, #2, #3, #65, #69.
- **Entregables:** alcance; requisitos funcionales/no funcionales; casos de uso; matriz de trazabilidad; registro de obligaciones legales y regulatorias por jurisdicción y modelo operativo.
- **Salida:** requisitos verificables; supuestos y riesgos explícitos; referencias normativas con edición, fuente, aplicabilidad y controles asociados.

### Fase 2 — Arquitectura, tecnología y seguridad por diseño

- **Objetivo:** definir una arquitectura coherente, segura y evolutiva.
- **Issues:** #4, #5, #7, #51, #52, #66.
- **Entregables:** diagramas de contexto, componentes y flujos; ADR de arquitectura/tecnología; límites de confianza; inventario de activos; threat model; contratos iniciales backend/API/clientes; esqueletos navegables de aplicaciones.
- **Salida:** decisiones críticas justificadas; amenazas y riesgos residuales documentados; responsabilidades y dependencias definidas; clientes evolucionan con contratos versionados y sin duplicar reglas críticas.

### Fase 3 — Fundaciones de ingeniería, pruebas, CI/CD y operaciones

- **Objetivo:** hacer que cada cambio sea construible, verificable, seguro y recuperable.
- **Issues:** #55, #56, #53, #54, coordinado con #68.
- **Entregables:** estructura de repositorio; convenciones; configuración y secretos; CI con lint, análisis estático, pruebas y controles de dependencias; estrategia de pruebas; logging, métricas, trazas, auditoría, backups y runbooks.
- **Salida:** pipeline reproducible en PR; pruebas positivas y negativas automatizadas; secretos fuera del repositorio/logs; restauración y rollback probados; gates de GitHub corresponden a checks existentes y funcionales.

### Fase 4 — Plataforma de datos y contratos temporales

- **Objetivo:** construir datos confiables, trazables y disponibles según el momento real de conocimiento.
- **Issues:** #8–#28, #64.
- **Entregables:** Asset Registry e Instrument Registry; contratos de observaciones, eventos, features y procedencia; temporalidad point-in-time/bitemporal; captura raw inmutable; snapshots, versionado, retención; calidad, huecos, discontinuidades, licencias y cobertura.
- **Salida:** contratos versionados; linaje desde dato original hasta feature/predicción; controles de duplicados, temporalidad, unidades, precisión, disponibilidad y datos ausentes; prevención de leakage temporal.

### Fase 5 — Inteligencia histórica, features y modelos predictivos

- **Objetivo:** desarrollar predicciones reproducibles y conscientes de su incertidumbre.
- **Issues:** #29–#43, #60, #62.
- **Entregables:** episodios, regímenes, análisis de eventos y features versionadas; objetivos y horizontes predefinidos; baselines y modelos econométricos/estadísticos/ML/DL; ensembles cuando aporten valor demostrado; evaluación walk-forward/out-of-sample y backtesting sin leakage.
- **Salida:** protocolo congelado antes de comparar candidatos finales; benchmarks y costes explícitos; resultados reproducibles fuera de muestra; probabilidades etiquetadas como calibradas solo con evidencia; correlación y precedencia temporal no se presentan como causalidad demostrada.

### Fase 6 — Decisión, cartera y gestión de riesgo

- **Objetivo:** transformar análisis en decisiones disciplinadas, incluida la abstención.
- **Issues:** #44–#46.
- **Entregables:** señales separadas de predicciones; estado `NO_TRADE`; ranking y construcción de cartera; límites de exposición, liquidez y pérdidas.
- **Salida:** cada señal incluye horizonte, vigencia, condiciones, riesgo y evidencia; abstención probada; límites no modificables por modelos sin autorización; evaluación neta de costes y riesgo.

### Fase 7 — Trading seguro y simulación

- **Objetivo:** validar el ciclo de órdenes antes de operar con capital real.
- **Issues:** #47–#50, #57–#59.
- **Entregables:** adaptadores de exchange; contratos normalizados; order intent, ciclo de vida, idempotencia, fills y reconciliación; PAPER y SHADOW; circuit breakers, kill switches, autorización, gestión de secretos y auditoría.
- **Salida:** pruebas de fallos, duplicados, latencia, desconexión, fills parciales y reconciliación superadas; PAPER/SHADOW verificados; LIVE bloqueado hasta satisfacer #59 y recibir autorización explícita independiente.

### Fase 8 — API, aplicaciones y experiencia de producto

- **Objetivo:** ofrecer experiencia coherente sobre capacidades verificadas del backend.
- **Issues:** #51, #52, #66; integración continua con fases 2–7.
- **Entregables:** API versionada; web, Android e iOS; integración progresiva de módulos; estados de interfaz: prototipo, en desarrollo, implementado/verificado y no disponible.
- **Salida:** datos simulados identificados como tales; predicciones experimentales no presentadas como validadas; reglas críticas en backend; pruebas de integración y accesibilidad por plataforma.

### Fase 9 — Observabilidad, mantenimiento y mejora continua

- **Objetivo:** detectar degradación, incidentes y cambios de contexto.
- **Issues:** #53, #54, #63, #56.
- **Entregables:** monitorización de datos, servicios, modelos y ejecución; drift y degradación; alertas, rollback y retirada de modelos; experimentos y artefactos reproducibles; auditorías periódicas.
- **Salida:** alertas accionables y procedimientos probados; retirada de modelos sin perder trazabilidad; evidencias operativas, de recuperación y revisión periódica.

## 4. Gates globales

| Gate | Condición |
|---|---|
| A — Gobierno | Cambios trazables, repositorio controlado y decisiones registradas. |
| B — Diseño | Requisitos, arquitectura, riesgos y contratos definidos para el módulo. |
| C — Calidad | Pruebas, seguridad y CI proporcionales al riesgo. |
| D — Datos | Calidad, temporalidad, procedencia y licencias aceptables para el uso previsto. |
| E — Inteligencia | Evaluación fuera de muestra, robustez, incertidumbre y limitaciones documentadas. |
| F — Operación | Controles, observabilidad, recuperación y autorización verificadas. |

Un módulo avanza únicamente cuando satisface los gates que le resulten aplicables. Los criterios deben ser verificables y proporcionales a la criticidad.

## 5. Referencias normativas y técnicas

La aplicabilidad y las ediciones vigentes deben verificarse y registrarse en [#69](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/69), consultando fuentes oficiales. Evaluar, entre otras:

- ISO/IEC/IEEE 12207 — procesos del ciclo de vida del software.
- ISO/IEC 25010 — modelo de calidad del producto.
- ISO/IEC 27001 — gestión de seguridad de la información.
- ISO/IEC 42001 e ISO/IEC 23894 — gestión y riesgos de IA.
- ISO 9001 — gestión de calidad organizacional, si corresponde al alcance.
- OWASP ASVS/MASVS y prácticas de cadena de suministro de software, según las superficies aplicables.

Adoptar controles inspirados en una norma no equivale a conformidad ni certificación.

## 6. Métricas del programa

No establecer objetivos numéricos arbitrarios. Definir previamente denominador, fuente y método. Medir al menos:

- Issues/controles con evidencia aceptada frente a los aplicables.
- PR que superan los gates requeridos.
- Defectos críticos abiertos y reincidencias.
- Cobertura de trazabilidad requisito–prueba.
- Reproducibilidad de datasets, experimentos y releases.
- Resultados OOS, calibración y rendimiento neto de costes por régimen/horizonte.
- Incidentes de seguridad, disponibilidad y recuperación.

Toda métrica debe incluir periodo, población, método, limitaciones y rol responsable.

## 7. Cadencia y mantenimiento

- Revisar el roadmap al inicio de cada fase y ante cambios relevantes de alcance, riesgo o arquitectura.
- Actualizar dependencias y estado después de cada PR relevante.
- Reutilizar Issues existentes; crear subtareas solo para brechas concretas.
- Publicar avances con enlaces a PR, pruebas y evidencias, distinguiendo completado, bloqueado y pendiente.
- Mantener este documento sincronizado con el Issue #70.

## 8. Relaciones principales

- Auditoría inicial: [#67](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/67).
- Reauditoría: [#71](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/71).
- Protección del repositorio: [#68](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/68).
- Matriz de trazabilidad: [#69](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/69).
- Gobernanza: [#6](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/6).
- Pruebas: [#55](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/55).
- Seguridad: [#7](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/7).
- Aplicaciones incrementales: [#66](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/66).

## 9. Criterios de cierre del Issue rector

El Issue #70 solo podrá cerrarse cuando:
- El roadmap esté versionado y enlazado desde el Issue.
- Fases, objetivos, Issues, entregables, dependencias y criterios de salida estén documentados.
- Se reutilicen los Issues existentes y se hayan identificado duplicidades.
- Gates globales y restricciones LIVE estén explícitos.
- La matriz #69 mantenga trazabilidad con requisitos, controles y evidencias.
- Exista un mecanismo verificable de actualización.
- Ninguna fase se declare completada sin PR integrado y evidencia.

El cierre de #70 no equivale a completar todas las fases de remediación.


---

## 10. Reauditoría de estado — 2026-11-11

### Alcance y criterio de evidencia

Esta actualización complementa, no reemplaza, las auditorías históricas de los Issues #67 y #71. Se consultaron nuevamente los Issues abiertos, los Pull Requests abiertos, los documentos de gobierno y arquitectura, los cambios de los PR #87–#91 y los checks disponibles para los commits examinados.

Los estados siguientes describen únicamente la evidencia accesible en esta revisión. La presencia de un documento o una POC no equivale a implementación del producto, aprobación de arquitectura, conformidad normativa ni preparación para producción.

### Fotografía del repositorio

- Repositorio: `Osleyder1985/crypto-predictive-intelligence-ecosystem`.
- Rama predeterminada: `main`.
- Issues abiertos observados: 73.
- Pull Requests abiertos observados en la actualización del 2026-11-11: #87, #88, #90, #91 y #92 (5 en total).
- #87, #88, #90 y #91 permanecen en Draft; #92 no está en Draft. Se añadieron revisiones técnicas de tipo COMMENT a #87, #90 y #91; no equivalen a aprobación.
- PR #87: evaluación documental de herramientas de cadena de suministro.
- PR #88: reconstrucción de entornos Python mediante uv y lockfiles.
- PR #90: generación de SBOM CycloneDX.
- PR #91: procedimiento de comparación Syft/CycloneDX.

### Evidencia técnica observada

- La arquitectura modular, ADR-0001, ADR-0002, threat model, matriz de compatibilidad, estrategia de pruebas, documentación de operaciones y roadmap están versionados.
- Existe workflow específico de compatibilidad Python/Windows y se observaron POC cuantitativas ejecutadas.
- Para PR #88, el run #42998870533 terminó con cuatro jobs satisfactorios en HEAD `121c91cd705997345afce4ba12b54e2100445c50` y publicó cuatro artifacts de evidencia. La documentación se actualizó después en HEAD `7b379dce7c320bac0d3cd2ef7cd8546ef0950222`; el run #18 (`42999290951`) para ese HEAD estaba en ejecución en la última consulta.
- La POC cuantitativa integrada mediante PR #85 valida únicamente el alcance sintético/CPU-only descrito en su evidencia; no valida predicción con mercado real ni selección tecnológica global.
- El Issue #5 registra que la selección tecnológica permanece parcial/no aprobada como baseline por falta de cierre de licencias transitivas, SBOM, notices, lockfiles integrales e integración representativa.
- PR #90 contiene resultados locales documentados para CycloneDX, pero el JSON SBOM continúa sin artifact CI verificable ni retención duradera.
- PR #91 describe un procedimiento, pero no se encontró evidencia de ejecución real de Syft y comparación de inventarios en el estado revisado.

### Hallazgos vigentes

| ID | Hallazgo | Severidad | Tratamiento |
|---|---|---|---|
| RA-01 | README de raíz insuficiente para orientar instalación, arquitectura, estado y contribución. | Media | Reutilizar #1/#6; corregir mediante PR. |
| RA-02 | No se ha demostrado una aplicación CPIE funcional integrada para web, Android e iOS. | Crítica | Reutilizar #66 y los Issues de producto/backend. |
| RA-03 | La CI existente es específica de POC; no demuestra aún una estrategia general de calidad para todos los componentes. | Alta | Reutilizar #55/#56 y definir gates solo sobre checks existentes. |
| RA-04 | ADR-0002 y selección tecnológica siguen sin baseline global aprobada. | Alta | Continuar #5 con evidencia de licencias, dependencias e integración. |
| RA-05 | Cobertura completa de SBOM, licencias, notices y vulnerabilidades aún no demostrada. | Alta | Continuar #86 y PR #87–#91 sin duplicar trabajo. |
| RA-06 | Algunas descripciones de Issues/auditorías conservan estados históricos que ya no describen la situación posterior a PR #85 y #87–#91. | Alta | Añadir reauditorías fechadas; no sobrescribir ni borrar evidencia histórica. |
| RA-07 | La trazabilidad requisito–control–prueba–evidencia aún no está demostrada de extremo a extremo. | Alta | Reutilizar #69 y #55. |
| RA-08 | No se ha demostrado despliegue, restauración, rollback ni operación de una plataforma funcional. | Alta | Reutilizar #53/#54/#56 y gates de Fase 3/9. |

### Evaluación específica de PR abiertos

- **#87:** documento actualizado en su rama para incorporar los resultados y límites de #88–#91. Se registró una revisión técnica COMMENT; no se observó CI.
- **#88:** cuatro jobs satisfactorios y cuatro artifacts para HEAD `121c91cd705997345afce4ba12b54e2100445c50`; documentación posterior actualizada. El run del HEAD documental más reciente seguía pendiente en la última consulta. Artifacts temporales expiran el 2027-02-09; retención durable pendiente.
- **#90:** resultados locales documentados; falta artifact verificable de CI, cobertura de Syft y análisis automatizado de vulnerabilidades/licencias. Revisión técnica COMMENT publicada.
- **#91:** procedimiento documentado; ejecución y comparación real pendientes. Revisión técnica COMMENT publicada.
- **#92:** esta reauditoría fechada está abierta como PR, sin CI reportado para el commit examinado.
- **Dependencias de ramas:** #90 conserva como base `6ffc5b9e95f742204429e900cb97abdaad154ee0`, tres commits por detrás del HEAD actualizado de #88. #91 conserva como base `6674d3f78801b455c16654084edd91d2691a2dab`, anterior al HEAD actual de #90. Restackear en orden y revisar cada diff antes de integrar; no asumir que squash preserva SHA dependientes.

### Gobierno, seguridad y normas

- El Issue #68 contiene evidencia histórica de ruleset `protect-main` activo y de PR obligatorio. Esta reauditoría no repitió una verificación administrativa completa de todos los controles de GitHub; por tanto, no certifica el estado actual de cada ajuste de protección.
- Los estados de Dependency Graph, Dependabot, Secret Scanning, Push Protection y Code Scanning deben mantenerse como no verificados cuando no exista evidencia administrativa directa.
- La matriz #69 debe registrar edición vigente, fuente oficial, aplicabilidad, control, responsable y evidencia. No declarar conformidad ISO ni certificación por adopción documental.
- El programa mantiene bloqueado el trading LIVE hasta superar los gates aplicables y obtener autorización explícita e independiente.

### Orden de remediación actualizado

1. Sincronizar esta reauditoría con #71 y el roadmap #70, conservando el historial.
2. Actualizar descripciones de #86 y #88 con evidencia posterior, sin cerrar Issues por inferencia.
3. [x] Completar los riesgos/limitaciones específicos de los Issues #11–#21; los 11 placeholders `undefined` fueron sustituidos por riesgos concretos. Mantener los Issues abiertos hasta cumplir sus criterios de aceptación.
4. Resolver el criterio administrativo de evidencia de #83: el JSON local `poc-results/python-cpi-workload-3.12-local.json` no está adjunto ni versionado. No cerrar mientras siga pendiente la decisión y preservación de evidencia.
5. Completar #87–#91 y su cadena de dependencias con CI para HEAD actual, artifacts de SBOM, ejecución Syft, escáneres y revisiones verificables.
6. Completar #5/#69/#55/#56 con selección tecnológica, trazabilidad y controles automatizados adecuados.
7. Iniciar la primera vertical funcional de producto según #66 solo cuando sus contratos, dependencias y gates aplicables estén satisfechos.

### Veredicto

**Estado global: FUNDACIÓN DOCUMENTAL AVANZADA / POC PARCIALES DEMOSTRADAS / PRODUCTO FUNCIONAL NO DEMOSTRADO / NO APTO PARA PRODUCCIÓN.**

No se asigna una puntuación global numérica: todavía no existe evidencia de producto integrado suficiente para calcular una calificación defendible. La auditoría no autoriza cierres, merges, habilitación de trading LIVE ni declaraciones de conformidad.

### Límites de esta reauditoría

Esta revisión es una auditoría documental y de evidencia accesible desde GitHub. No ejecutó el repositorio completo en un entorno limpio, no realizó pentest, no escaneó todos los artefactos binarios, no verificó todos los ajustes administrativos de GitHub y no probó aplicaciones o despliegues. Esos trabajos siguen pendientes y deben registrarse como tales.
