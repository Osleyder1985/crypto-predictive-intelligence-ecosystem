# Matriz de trazabilidad de requisitos, normas, controles y evidencias (CPIE)

- Issue rector: [#69](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/69)
- Auditoría base: [#67](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/67)
- Roadmap: [remediation-roadmap.md](remediation-roadmap.md)
- Verificación de fuentes: 2026-11-10
- Estado: baseline inicial; los controles técnicos permanecen mayoritariamente planificados o abiertos.

## 1. Propósito y reglas

Esta matriz conecta objetivos y requisitos CPIE con Issues, controles, artefactos, pruebas y evidencias. Es un instrumento de gobernanza y auditoría interna; no sustituye los textos normativos, una evaluación jurídica ni una auditoría/certificación independiente.

**No se declara conformidad ni certificación.** La adopción de prácticas inspiradas en normas no demuestra cumplimiento completo. Las cláusulas exactas deberán contrastarse con copias legítimamente disponibles de las ediciones aplicables antes de afirmar correspondencia cláusula-a-cláusula. Esta versión utiliza dominios/temas y no reproduce texto protegido.

### Estados controlados

| Estado | Significado |
|---|---|
| NO_EVALUADO | No existe evaluación suficiente de aplicabilidad o estado. |
| NO_APLICABLE_JUSTIFICADO | Exclusión documentada con alcance, motivo, riesgo residual, rol que acepta y fecha de revisión. |
| PLANIFICADO | Existe requisito/Issue, pero el control no está implementado. |
| IMPLEMENTADO | El artefacto/control existe, pero falta verificación suficiente. |
| VERIFICADO | Prueba/evidencia ejecutada, aprobada y reproducible para el alcance indicado. |
| EVIDENCIA_CADUCADA | La evidencia ya no representa la versión, configuración, periodo o entorno actual. |
| BLOQUEADO | Dependencia, permiso o decisión impide avanzar. |

El estado se asigna por control, no por norma completa. Un Issue o documento no prueba que un control técnico esté implementado. La evidencia debe identificar versión/commit, fecha, entorno, resultado y rol responsable.

## 2. Registro normativo y fuentes oficiales

Fuentes consultadas en los catálogos oficiales ISO/OWASP el 2026-11-10:

| Referencia | Edición/estado confirmado | Aplicabilidad preliminar | Tratamiento |
|---|---|---|---|
| ISO/IEC/IEEE 12207 | 2026, edición 2, publicada abril 2026; reemplaza 2017. | Alta como referencia del ciclo de vida de software. | Requisitos, arquitectura, construcción, verificación, operación, mantenimiento y retirada. |
| ISO/IEC 25010 | 2023, edición 2. | Alta para calidad del producto software. | Derivar atributos, métricas y métodos de prueba sin inventar umbrales. |
| ISO/IEC 27001 | 2022, edición 3, con Amd 1:2024. | Alta como referencia de seguridad; SGSI formal sujeto al alcance organizativo. | Riesgos, activos, controles, responsabilidades, incidentes y continuidad. |
| ISO/IEC 42001 | 2023, edición 1. | Alta si CPIE desarrolla, proporciona o utiliza IA dentro del alcance organizativo. | Gobierno de IA, responsabilidades, impactos, evaluación y mejora. |
| ISO/IEC 23894 | 2023, edición 1. | Alta para riesgos específicos de IA/ML. | Identificación, análisis, evaluación, tratamiento y seguimiento de riesgos IA. |
| ISO 9001 | 2026, edición 6, publicada el 16-09-2026; reemplaza 2015. | Condicional: depende de establecer un sistema organizativo de gestión de calidad. | No tratar como requisito de un repositorio aislado ni como certificación automática. |
| OWASP ASVS | 5.0.0, estable, publicada 30-05-2025. | Alta para controles técnicos web/API. | Seleccionar requisitos según arquitectura y riesgo. |
| OWASP MASVS | Versión vigente no fijada en esta revisión. | Aplicable al diseñar las apps móviles. | Verificar versión oficial y fijar baseline en el diseño móvil. |

### Fuentes

- ISO/IEC/IEEE 12207:2026 — https://www.iso.org/standard/90219.html
- ISO/IEC 25010:2023 — https://www.iso.org/standard/78176.html
- ISO/IEC 27001:2022 — https://www.iso.org/standard/27001
- ISO/IEC 27001:2022/Amd 1:2024 — https://www.iso.org/standard/88435.html
- ISO/IEC 42001:2023 — https://www.iso.org/standard/42001
- ISO/IEC 23894:2023 — https://www.iso.org/standard/77304.html
- ISO 9001:2026 — https://www.iso.org/standard/88464.html
- OWASP ASVS 5.0.0 — https://asvs.owasp.org/
- OWASP MASVS — https://mas.owasp.org/

El responsable de calidad debe volver a consultar los catálogos oficiales ante cada revisión planificada y ante cualquier aviso de nueva edición, enmienda o retirada. La fecha de consulta no garantiza vigencia futura.

## 3. Matriz maestra de trazabilidad

Los identificadores RQ son estables. Los Issues especifican o implementan el área; su existencia no satisface por sí sola el control.

| ID / requisito | Norma / dominio | Issue(s) | Control y resultado exigido | Rol responsable | Artefacto y verificación | Estado inicial |
|---|---|---|---|---|---|---|
| RQ-001 Alcance y límites | 12207 ciclo de vida; ISO 9001 condicional | #1, #65 | Usuarios, usos, exclusiones, jurisdicciones; separar análisis, predicción, señal y ejecución; no prometer rentabilidad ni causalidad no demostrada. | Product owner + calidad | Alcance y registro de supuestos; revisión y trazabilidad a casos de uso. | PLANIFICADO |
| RQ-002 Requisitos funcionales | 12207 requisitos; 25010 adecuación funcional | #2 | Requisitos atómicos con ID, prioridad, criterios de aceptación y comportamiento ante errores/datos insuficientes. | Product owner + ingeniería | Catálogo/casos de uso; pruebas enlazadas por requisito. | PLANIFICADO |
| RQ-003 Calidad del producto | 25010; 12207 verificación/validación | #3, #55 | Métrica, método, población, entorno y umbral justificado para rendimiento, fiabilidad, seguridad, mantenibilidad, portabilidad y usabilidad. | Arquitectura + QA | Matriz de calidad; pruebas/mediciones reproducibles. | PLANIFICADO |
| RQ-004 Arquitectura y contratos | 12207 arquitectura/diseño; 25010 mantenibilidad | #4, #51, #52, #66 | Límites de dominio, dependencias permitidas, contratos versionados y backend común; extraer servicios solo con evidencia. | Architecture owner | ADRs, diagramas, contratos; revisión y pruebas de contrato/integración. | PLANIFICADO |
| RQ-005 Selección tecnológica | 12207 diseño/adquisición; 25010 compatibilidad | #5 | Seleccionar por carga, coste, soporte, licencia, interoperabilidad y entorno; evitar infraestructura prematura. | Arquitectura + ingeniería | ADRs/matriz comparativa; PoCs y benchmarks reproducibles. | PLANIFICADO |
| RQ-006 Gobierno del cambio | 12207 configuración; ISO 9001 información documentada, condicional | #6, #68, #69 | Issue → ADR cuando aplique → branch → PR → checks → evidencia → merge/release. | Maintainer + calidad | engineering-workflow.md, plantillas y reglas GitHub; prueba integral de PR. | IMPLEMENTADO parcialmente; GitHub BLOQUEADO |
| RQ-007 Seguridad por diseño | 27001 riesgos; ASVS; 12207 | #7, #51, #52, #55 | Inventariar activos, actores, amenazas, superficies, límites de confianza, mitigaciones y riesgos residuales. | Security owner | Threat model/diagramas; revisión de amenazas y pruebas negativas. | PLANIFICADO |
| RQ-008 Gobierno de datos | 12207 calidad; 27001 protección; 23894 riesgo IA | #8–#28, #64 | Raw inmutable, linaje, timestamps point-in-time, disponibilidad, licencias, duplicados, huecos, discontinuidades y anti-leakage. | Data engineering + data governance | Contratos, catálogo, snapshots; validadores y tests temporales. | PLANIFICADO |
| RQ-009 Gobierno de modelos | 42001; 23894; 12207 | #29–#43, #60, #62, #63 | Inventario/versionado, propósito, datos, evaluación, limitaciones, supervisión, drift y retirada. | AI/ML owner | Model cards/registro; reproducción, walk-forward/OOS y monitorización. | PLANIFICADO |
| RQ-010 Predicciones e incertidumbre | 23894; 42001; 25010 fiabilidad | #29–#43, #60, #62 | Separar predicción, escenario, señal y causalidad; marcar incertidumbre no cuantificada; abstenerse si falta evidencia. | Quant research + AI/ML | Contrato de predicción/protocolo; OOS, benchmarks, calibración y sensibilidad. | PLANIFICADO |
| RQ-011 Decisión y riesgo | 27001 acceso; 23894; 12207 | #44–#46, #7 | Señales con horizonte/vigencia/riesgo; NO_TRADE; límites de exposición/pérdidas en backend, no modificables por modelos. | Risk owner + backend | Política de riesgo y decision contract; tests de límites y escenarios extremos. | PLANIFICADO |
| RQ-012 Trading seguro | 27001; 12207 operación; ASVS API | #47–#50, #57–#59 | PAPER/SHADOW antes de LIVE; idempotencia, reconciliación, mínimo privilegio, secretos aislados, kill switch y autorización independiente. | Trading operations + security | Especificación/runbooks; sandbox y fault injection; prueba de bloqueo LIVE. | PLANIFICADO; LIVE BLOQUEADO |
| RQ-013 Seguridad web/API | 27001; ASVS 5.0.0; 25010 | #7, #51, #55 | Autenticación/autorización, validación, sesiones, datos, logging seguro y dependencias según threat model. | AppSec + backend | Perfil ASVS; SAST, dependency scan y pruebas de autorización/DAST. | PLANIFICADO |
| RQ-014 Seguridad móvil | 27001; MASVS por fijar; 25010 | #52, #66, #55 | Apps comparten contratos; no contienen reglas críticas; proteger secretos, sesiones y datos locales. | Mobile lead + AppSec | Arquitectura móvil y matriz de plataformas; MASVS y pruebas por plataforma. | PLANIFICADO |
| RQ-015 Pruebas y gates | 12207 V&V; 25010; ASVS | #55, #56, #68 | Unit, integration, contract, property, regression, data, security y E2E; gates solo para checks existentes y estables. | QA + DevOps | Estrategia/CI/reportes; ejecución reproducible en PR. | PLANIFICADO |
| RQ-016 Operación y recuperación | 12207 operación; 27001 continuidad; 25010 fiabilidad | #53, #54, #56, #63 | Logs, métricas, alertas, auditoría, backup/restore, rollback, incidentes y degradación de modelos/datos. | SRE/operations + owners | Runbooks/telemetría; simulacros y alertas probadas. | PLANIFICADO |
| RQ-017 Cumplimiento legal | 12207 adquisición; 27001 obligaciones | #65 | Evaluar jurisdicción, actividad, instrumento, usuario y proveedor; bloquear funciones no evaluadas legalmente. | Compliance + asesoría jurídica | Matriz jurisdicción/escenario; fuentes oficiales fechadas y revisión competente. | PLANIFICADO |
| RQ-018 Mejora continua | ISO 9001 condicional; 12207; 27001/42001 según SG | #6, #53, #54, #63, #67, #70, #71 | Revisiones, no conformidades, acciones correctivas, cambios y lecciones. | Quality owner + maintainer | Plan de auditoría/registro correctivo; auditorías repetibles. | PLANIFICADO |
| RQ-019 Aplicaciones incrementales | 12207; 25010; MASVS | #66, #51, #52 | Prototipos tempranos; evolución vertical; estados reales; simulación etiquetada; integración con contratos verificados. | Product + frontend/mobile + backend | Matriz de capacidades/prototipos; pruebas integradas por plataforma. | PLANIFICADO |
| RQ-020 Repositorio y cadena de suministro | 27001; 12207 configuración; ASVS | #6, #55, #56, #68 | PR obligatorio, no force-push/delete, bypass justificado, scans de dependencias/secretos y permisos mínimos. | Repository admin + DevSecOps | Export de ruleset/CI/política; lectura efectiva, PR de prueba y resultados de scans. | BLOQUEADO (#68); resto PLANIFICADO |

## 4. Trazabilidad bidireccional y registro de evidencias

1. Todo requisito tiene ID estable RQ-nnn y uno o más Issues propietarios.
2. Cada control técnico independiente recibe ID CTL-nnn al especificarse.
3. Cada implementación enlaza Issue y requisito satisfecho.
4. Cada prueba declara requisito/control, versión probada, entorno y resultado.
5. Cada evidencia enlaza commit/PR, workflow o informe, fecha, entorno, alcance y resultado.
6. Requisito sin prueba/evidencia permanece como brecha, aunque exista código.
7. Control sin requisito debe justificar origen: riesgo, obligación, ADR o mantenimiento.
8. NO_APLICABLE_JUSTIFICADO exige alcance, motivo, riesgo residual, rol que acepta y fecha de revisión.

Registro mínimo por evidencia: ID único; requisito/control; Issue, ADR, PR y commit; tipo de artefacto; versión/hash; fecha UTC; entorno/alcance; método y resultado PASS/FAIL/INCONCLUSIVE; responsable/revisor; limitaciones, excepciones y fecha de revisión. No publicar secretos, tokens ni datos personales innecesarios.

## 5. Brechas iniciales comprobadas

| ID | Brecha/evidencia | Issue | Acción | Estado |
|---|---|---|---|---|
| GAP-001 | main tiene protected=false y protection.enabled=false; rulesets devuelve []. Verificado 2026-11-10. | #68 | Activar reglas con permisos administrativos; verificar configuración y PR controlado. | BLOQUEADO por falta de acceso administrativo desde la integración. |
| GAP-002 | Plantillas/workflow/ADR integrados por PR #73; YAML validado sintácticamente; renderizado visual no probado. | #6 | Probar renderizado en GitHub y completar flujo. | IMPLEMENTADO parcialmente. |
| GAP-003 | No existe CI/CD ni status checks; no procede exigir checks inexistentes. | #55, #56, #68 | Crear pipeline, probarlo y luego exigir checks estables. | PLANIFICADO. |
| GAP-004 | No hay código funcional, tests, threat model, contratos, arquitectura detallada ni apps. | #2–#66 | Entregar artefactos por fases del roadmap. | PLANIFICADO. |
| GAP-005 | Auditoría inicial carecía de matriz versionada/evidencias de conformidad. | #67, #69 | Mantener esta matriz y asociar evidencias por PR. | Documento IMPLEMENTADO; cobertura técnica incompleta. |
| GAP-006 | Aplicabilidad de ISO 9001:2026 al alcance organizativo no evaluada. | #1, #69 | Determinar si existe un SGC organizativo dentro del alcance. | NO_EVALUADO. |
| GAP-007 | Baseline vigente de OWASP MASVS no fijada. | #52, #55, #69 | Consultar fuente oficial y seleccionar alcance/version. | NO_EVALUADO. |
| GAP-008 | No hay certificación externa ni auditoría independiente acreditada. | #67, #69 | No declarar certificación; evaluar necesidad solo si se decide perseguirla. | No se reclama certificación. |

La auditoría #67 concluyó que el repositorio era un contenedor de planificación, no un producto implementado. Los documentos de gobierno posteriores no alteran por sí solos esa conclusión técnica.

## 6. Roles y responsabilidades

Una persona puede asumir varios roles en un equipo pequeño, pero deben distinguirse las responsabilidades y registrarse los conflictos de independencia. No se inventan nombres.

| Rol | Responsabilidad |
|---|---|
| Product owner | Alcance, prioridades y aceptación. |
| Architecture owner | Arquitectura, contratos, ADRs y deuda técnica. |
| Security owner | Threat model, vulnerabilidades y excepciones. |
| Data owner | Calidad, linaje, licencias, retención y temporalidad. |
| AI/ML owner | Inventario, validación, riesgo, incertidumbre, drift y retirada. |
| Risk/trading owner | Límites, autorizaciones y controles operativos. |
| QA/quality owner | Pruebas, evidencias, auditorías y acciones correctivas. |
| Repository administrator | Rulesets, permisos, bypass y configuración GitHub. |
| Compliance/legal reviewer | Análisis jurídico por jurisdicción/modelo operativo. |

Si no existe revisor independiente, declarar esa limitación y compensarla con pruebas automatizadas, revisión técnica diferida o control independiente cuando la criticidad lo requiera. No fingir aprobación independiente.

## 7. Revisión y mantenimiento

- Revisar ante cambios materiales de alcance, arquitectura, riesgo, proveedor, modelo IA o superficie de ataque.
- Consultar fuentes oficiales ante nuevas ediciones, enmiendas o retiradas.
- Cambiar estados solo después de incorporar artefactos/evidencias, no por intención o comentarios.
- Registrar cambios en PR y conservar resultados fallidos, excepciones y evidencias caducadas.
- Reabrir controles afectados por cambios incompatibles o evidencia caducada.
- Hacer revisión bidireccional desde requisitos a pruebas/evidencias y desde pruebas/controles a requisitos/riesgos.
- No fijar porcentajes globales de cumplimiento sin universo aplicable, denominador, método y evidencia.

## 8. Limitaciones

- Baseline de gobernanza, no análisis cláusula por cláusula de los textos ISO completos.
- Resúmenes públicos confirman identificadores, ediciones, estado y alcance general, pero no sustituyen los textos íntegros.
- No se inspeccionaron sistemas desplegados, cuentas externas, secretos, infraestructura ni entornos de ejecución.
- No hay software funcional para verificar controles técnicos.
- Aplicabilidad legal depende de jurisdicción, instrumentos, usuarios y modelo operativo.
- OWASP aporta guías técnicas; no equivale a certificación ISO.

## 9. Criterios para marcar VERIFICADO

Un control solo pasa a VERIFICADO cuando: alcance y criterio están definidos; el control está integrado en versión identificable; prueba/revisión fue ejecutada sobre esa versión y entorno; resultado reproducible sin fallos críticos abiertos; excepciones y limitaciones registradas; evidencia fechada y enlazada; revisión realizada por rol competente. Si no hay independencia posible, debe declararse.

## 10. Historial

| Fecha | Cambio |
|---|---|
| 2026-11-10 | Primera baseline: fuentes oficiales, RQ-001–RQ-020, estados iniciales, brechas, roles y reglas de evidencia/mantenimiento. |
