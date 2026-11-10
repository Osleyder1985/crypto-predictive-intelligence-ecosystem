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
