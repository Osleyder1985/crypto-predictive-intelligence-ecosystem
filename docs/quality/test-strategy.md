# Estrategia de pruebas y calidad de software — CPIE

- Issue rector: #55
- Gobierno: ../governance/engineering-workflow.md
- Trazabilidad: ../governance/requirements-controls-evidence-matrix.md
- Roadmap: ../governance/remediation-roadmap.md
- Estado: estrategia inicial; todavía no existen módulos funcionales ni una suite CI que permita ejecutar los niveles descritos.
- Fecha: 2026-11-10

## 1. Propósito y límites

Definir cómo CPIE verificará software, datos, contratos, modelos y operaciones antes de considerar una capacidad apta para su uso previsto. La estrategia cubre pruebas manuales y automatizadas, desde componentes aislados hasta flujos integrados y escenarios operativos.

Este documento no afirma que las pruebas estén implementadas ni que CPIE tenga calidad validada. Describe el enfoque que debe materializarse conforme aparezcan requisitos, contratos y componentes. No fija porcentajes de cobertura, latencias objetivo, tolerancias numéricas ni umbrales financieros sin justificación técnica y de riesgo.

## 2. Principios obligatorios

1. Trazabilidad: requisito/control → caso de prueba → implementación → ejecución → evidencia.
2. Prueba proporcional al riesgo: mayor rigor para datos financieros, temporalidad, riesgo, autorización y órdenes.
3. Determinismo: tests unitarios y de contrato reproducibles, aislados de red y servicios externos.
4. Separación de datos: fixtures sintéticos, datasets de prueba y datos reales autorizados deben identificarse y no mezclarse silenciosamente.
5. Point-in-time correctness: cada prueba temporal respeta cuándo un dato/evento estuvo realmente disponible.
6. Sin leakage: ninguna variable, transformación, etiqueta ni decisión usa información posterior al instante de predicción.
7. Fallo seguro: si faltan datos, permisos, frescura o validaciones, la capacidad rechaza, degrada explícitamente o se abstiene.
8. Reproducibilidad: registrar versión de código, configuración, semillas cuando aplique, dataset/snapshot y entorno.
9. Evidencia honesta: distinguir PASS, FAIL, SKIPPED e INCONCLUSIVE; un test omitido no cuenta como aprobado.
10. No confundir cobertura con calidad: cobertura de líneas no sustituye calidad de casos, aserciones ni escenarios negativos.

## 3. Niveles y tipos de prueba

| Nivel/tipo | Qué verifica | Cuándo aplicarlo | Evidencia esperada |
|---|---|---|---|
| Static checks | Formato, lint, tipos, análisis estático y patrones peligrosos. | En cada cambio cuando existan herramientas y reglas. | Salida, versión y configuración. |
| Unit | Funciones/clases aisladas, invariantes y errores. | Lógica determinista de cada módulo. | Reporte por caso. |
| Property-based | Propiedades sobre múltiples entradas generadas. | Cálculos, normalización, parsers y estados. | Semilla, estrategia y contraejemplos. |
| Contract | Esquemas, compatibilidad y semántica entre productores/consumidores. | API, eventos, datos, modelos y adaptadores. | Contrato y reporte de compatibilidad. |
| Integration | Interacción entre componentes y persistencia. | Cuando existan límites de módulo, DB o almacenamiento. | Entorno, fixtures y reporte. |
| Data quality | Esquema, rangos, duplicados, huecos, orden temporal, linaje y frescura. | Ingesta, snapshots, features y datasets. | Perfil, anomalías y decisión. |
| Regression | Evitar reintroducir defectos o cambios semánticos no aprobados. | Para defectos corregidos y comportamientos críticos. | Test asociado al Issue. |
| Security | Autenticación, autorización, secretos, validación, dependencias y abuso. | En cada superficie de ataque/cambio sensible. | Hallazgos, severidad y remediación. |
| End-to-end | Flujo completo desde entrada hasta resultado visible/auditable. | Cuando exista una vertical integrada. | Escenario, entorno y trazas. |
| Performance/reliability | Rendimiento, recursos, concurrencia, recuperación y estabilidad. | Con cargas representativas y objetivos definidos. | Carga, hardware, configuración y mediciones. |
| Model validation | Leakage, generalización, calibración, robustez, drift y costes. | Antes de publicar predicciones o señales. | Protocolo, split temporal, benchmarks e informe OOS. |
| Operational/fault injection | Caídas, timeouts, duplicados, desconexión, reintentos y recuperación. | Adaptadores, jobs, persistencia y ciclo de órdenes. | Fallo inducido, estado final y reconciliación. |

No todos los módulos necesitan todos los tipos desde el primer commit. Cada Issue de módulo seleccionará los tipos aplicables y justificará exclusiones.

## 4. Pirámide y ejecución

### Base: pruebas rápidas y deterministas
- Unit tests, property-based tests y static checks.
- Sin llamadas a exchanges, proveedores externos ni APIs reales.
- Fixtures pequeños, explícitos y versionados.
- Aserciones diagnósticas; independencia del reloj real, red y orden de ejecución.

### Capa intermedia: contratos, datos e integración
- Validar esquemas y compatibilidad antes de integrar cambios.
- Usar servicios efímeros o entornos aislados cuando sea necesario.
- Controlar reloj, zona horaria, semillas y dependencias externas.
- Incluir datos inválidos, incompletos, duplicados, retrasados y fuera de orden.
- Verificar transacciones, idempotencia y consistencia entre persistencia y eventos.

### Capa superior: E2E, seguridad y operación
- Pocos escenarios, representativos y de alto riesgo.
- Sandbox o simuladores; nunca enviar órdenes reales desde CI.
- Credenciales sintéticas y permisos mínimos.
- Casos negativos: autorización denegada, datos obsoletos, dependencia caída y respuesta malformada.
- Recuperación, rollback y reconciliación comprobados.

## 5. Requisitos de prueba por dominio

### 5.1 Ingesta y calidad de datos
Verificar:
- Esquema, tipos, unidades, precisión y campos obligatorios.
- Identidad de fuente, instrumento, mercado y granularidad.
- Duplicados, gaps, timestamps desordenados y discontinuidades.
- Coherencia OHLCV sin asumir que todos los mercados tienen idénticas reglas.
- Timestamps event_time, available_at, ingested_at y recorded_at cuando el contrato los requiera.
- Timezones, límites de sesión, calendarios y conversiones UTC.
- Reintentos idempotentes y respuestas parciales.
- Linaje, checksum/manifiesto y reproducibilidad de snapshots.
- Licencia, términos de uso y autorización de cada fuente.

Los datos defectuosos deben rechazarse, ponerse en cuarentena o etiquetarse según una política explícita. No interpolar ni rellenar gaps silenciosamente.

### 5.2 Features y temporalidad
- Recalcular features a partir de snapshots congelados.
- Demostrar que cada feature solo usa información disponible en el instante de corte.
- Probar ventanas móviles, warm-up, nulos y cambios de granularidad.
- Verificar que joins temporales no incorporen datos futuros.
- Comprobar consistencia batch/incremental.
- Versionar contratos de features para reproducir resultados anteriores.

### 5.3 Inteligencia predictiva
- Splits cronológicos y walk-forward; evitar particiones aleatorias que rompan la causalidad temporal.
- Separar selección de features/hiperparámetros del conjunto final OOS.
- Mantener baselines ingenuos y benchmarks relevantes.
- Incluir fees, spread, slippage, funding y demás costes pertinentes.
- Medir por horizonte, régimen y subperiodo, informando tamaños muestrales.
- Pruebas de leakage, sensibilidad, estabilidad y robustez.
- Evaluar calibración solo cuando el modelo emita probabilidades y existan datos suficientes.
- Registrar incertidumbre no cuantificada cuando no haya calibración defendible.
- Evitar selección retrospectiva de activos, periodos o modelos.
- Distinguir asociación, precedencia temporal e hipótesis causal.

No se acepta un modelo por una métrica aislada ni por el mejor resultado histórico. El protocolo y los criterios de selección se fijan antes de comparar candidatos finales.

### 5.4 Decisión, cartera y riesgo
- Invariantes de exposición, concentración, liquidez, límites y compatibilidad de instrumentos.
- Comportamiento NO_TRADE ante evidencia insuficiente, riesgo excesivo o datos inválidos.
- Rechazo de señales vencidas, duplicadas o fuera de contexto.
- Pruebas de límites en frontera, valores extremos y combinaciones adversas.
- Separación entre recomendación del modelo y autorización del motor de riesgo.
- El modelo no puede elevar límites ni autorizar operaciones.

### 5.5 Trading y adaptadores
Hasta nueva autorización, CI y pruebas automatizadas usan simuladores o sandbox, nunca capital real.
- Idempotencia ante reintentos y timeouts.
- Estados de orden y transiciones válidas/ inválidas.
- Fills parciales, cancelaciones, rechazos y ejecuciones tardías.
- Desconexión antes/después del envío y respuesta perdida.
- Rate limits, backoff y concurrencia.
- Reconciliación con exchange tras reinicio.
- Balance, permisos y reglas del instrumento.
- Circuit breaker, kill switch y bloqueo de LIVE.
- Verificar que las credenciales no permiten retiros ni aparecen en logs.

### 5.6 API y aplicaciones
- Contratos y compatibilidad de versiones.
- Autenticación, autorización por recurso/acción y acceso denegado.
- Validación de entrada y serialización.
- Manejo de errores, paginación, límites y cancelación.
- Consistencia entre web, Android e iOS.
- No presentar datos simulados como reales ni predicciones experimentales como validadas.
- Accesibilidad y pruebas de usabilidad por plataforma.
- Pruebas de seguridad web/API y móviles con baseline OWASP seleccionada y versionada.

## 6. Datos de prueba y fixtures

Mantener categorías separadas:
1. Synthetic fixtures: generados para invariantes, límites y fallos; deben identificarse como sintéticos.
2. Curated test datasets: subconjuntos versionados y autorizados, con fuente, periodo, licencia, checksum y limitaciones.
3. External sandbox responses: respuestas simuladas o sandbox; registrar proveedor, fecha y versión.
4. Production-derived data: solo con base legal, autorización, minimización y política de acceso/retención. Nunca incluir secretos ni datos personales innecesarios en el repositorio público.

Cada fixture registra propósito, esquema, origen, generador/método, versión, hash cuando corresponda y condiciones de uso. No almacenar datasets grandes en Git si corresponde un almacenamiento de artefactos con control de acceso y retención.

## 7. Calidad de pruebas y flaky tests

- Un test flaky no se convierte en PASS por reintentar hasta obtener resultado favorable.
- Registrar frecuencia, causa, entorno y responsable de investigación.
- Aislar temporalmente un test inestable solo con Issue, justificación, alcance y fecha de revisión; no ocultar fallos críticos.
- No reducir cobertura ni eliminar aserciones para hacer pasar el pipeline sin explicar el cambio.
- Los tests deben fallar ante el defecto que pretenden detectar; revisar mutaciones o pruebas negativas en controles críticos cuando sea viable.
- Evitar dependencia del reloj real, red pública, orden de ejecución o estado compartido.
- Mantener logs útiles y sanitizados.

## 8. CI y gates de merge

No hay CI configurada actualmente. Los siguientes gates son objetivo de implementación, no controles activos.

Secuencia propuesta:
1. Validación de formato y estructura.
2. Lint y análisis estático apropiados al stack seleccionado.
3. Unit y property-based tests.
4. Contratos y pruebas de integración aplicables.
5. Escaneo de secretos y dependencias.
6. Pruebas de seguridad según superficie y criticidad.
7. Construcción reproducible de artefactos.
8. E2E/sandbox para módulos con flujo integrado.

Reglas:
- Añadir workflows mediante PR independiente y vinculado a los Issues de CI/CD.
- Probarlos en ramas/PR antes de marcarlos como required checks.
- Exigir solo checks existentes, estables y con contexto identificado.
- No añadir gates ficticios ni bloquear el repositorio con checks sin workflow.
- Documentar excepciones; no permitir que silencien un fallo crítico.
- La protección técnica de la rama se gestiona en #68; este documento no la activa.

## 9. Reporte y evidencia de ejecución

Cada ejecución relevante debe permitir reconstruir:
- test_run_id único.
- Issue/requisito/control cubierto.
- Commit SHA y versión del test.
- Entorno, dependencias y configuración.
- Dataset/fixture/snapshot y hash.
- Semillas y reloj simulado cuando apliquen.
- Herramientas y versiones.
- Casos ejecutados, omitidos y fallidos.
- Resultado global y por caso: PASS, FAIL, SKIPPED o INCONCLUSIVE.
- Logs/reportes sanitizados y ubicación del artefacto.
- Limitaciones, flaky tests y excepciones.
- Fecha UTC y rol revisor.

No incluir claves, tokens, datos sensibles ni dumps de producción sin sanitizar.

## 10. Defectos y no conformidades

Todo fallo relevante debe producir un Issue o vincularse a uno existente. Debe contener resultado esperado/observado, pasos de reproducción, entorno, impacto justificado, evidencia sanitizada, causa confirmada o hipótesis, corrección, test de regresión, riesgo residual y condiciones de cierre.

Cuando sea posible, demostrar que el test falla antes de la corrección y pasa después. No cerrar un defecto solo porque el pipeline vuelva a verde si falta la prueba de regresión.

## 11. Responsabilidades

| Rol | Responsabilidad |
|---|---|
| QA/quality owner | Estrategia, trazabilidad, calidad de evidencia y excepciones. |
| Responsable del módulo | Casos de prueba, fixtures y aceptación técnica. |
| Data owner | Calidad, procedencia, licencias y pruebas temporales. |
| AI/ML owner | Protocolo, leakage, calibración y robustez. |
| Security owner | Threat model, pruebas de seguridad y hallazgos. |
| Risk/trading owner | Invariantes de riesgo, simulación y bloqueo LIVE. |
| DevOps/SRE | CI, artefactos, entornos, observabilidad y recuperación. |

Si una persona asume varios roles, registrar el conflicto de independencia. No inventar revisiones independientes.

## 12. Secuencia de implantación

| Etapa | Entregable | Dependencias | Criterio de salida |
|---|---|---|---|
| T0 Fundaciones | Herramientas, convención de tests, fixtures y reporte. | Stack/arquitectura (#4, #5). | Decisiones registradas y entorno reproducible. |
| T1 CI mínimo | Workflow de static checks y unit tests sobre código existente. | Stack definido. | Workflow probado en PR, logs y artefactos visibles. |
| T2 Contratos/datos | Validadores, fixtures y tests temporales. | Contratos/modelo de datos (#8–#28, #64). | Casos positivos/negativos reproducibles. |
| T3 Seguridad/integración | Scans, integration tests y autorización. | Threat model (#7), API/arquitectura (#51). | Hallazgos críticos tratados y resultados auditables. |
| T4 Modelos | Validación OOS, benchmarks y leakage tests. | Datos y contratos predictivos. | Protocolo congelado y evaluación reproducible. |
| T5 Operación/trading | Sandbox, fault injection, recovery y E2E. | Motor de decisión/trading. | Escenarios críticos superados; LIVE sigue bloqueado hasta sus gates. |

Las etapas pueden avanzar en paralelo si sus dependencias concretas están satisfechas. No simular componentes aún no construidos.

## 13. Criterios de implantación

- [ ] Herramientas y convenciones seleccionadas mediante decisiones trazadas.
- [ ] Estrategia específica por módulo enlazada a requisitos y riesgos.
- [ ] CI ejecuta checks reales en PR.
- [ ] Checks obligatorios activos solo después de probar estabilidad.
- [ ] Fixtures sintéticos y datasets autorizados identificados y gestionados.
- [ ] Escenarios negativos críticos cubiertos.
- [ ] Reportes y artefactos accesibles y reproducibles.
- [ ] Fallos generan defectos trazables y tests de regresión.
- [ ] Módulos predictivos tienen validación temporal/OOS y controles anti-leakage.
- [ ] Operaciones probadas en simulación/sandbox; sin órdenes reales en CI.

## 14. Estado actual y limitaciones

A fecha de esta versión:
- El repositorio contiene documentos de gobierno, plantillas y matriz de trazabilidad.
- No se ha verificado código funcional, contratos ejecutables ni módulos CPIE.
- No existe CI/CD ni status checks configurados.
- No hay suite ejecutable ni reportes de tests.
- No se han creado fixtures ni datasets CPIE en este repositorio.
- No hay evidencia de pruebas de integración, seguridad, rendimiento, modelos o E2E.
- La protección de main permanece pendiente en #68.

Todos los niveles descritos son una estrategia objetivo y no deben presentarse como capacidades implantadas.

## 15. Historial

| Fecha | Cambio |
|---|---|
| 2026-11-10 | Primera versión de la estrategia de pruebas por riesgo, dominio, evidencia y etapas de implantación. |
