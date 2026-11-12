# Especificación de navegación y prototipo multiplataforma CPIE

- **Estado:** propuesta de diseño funcional; no es implementación ni decisión de stack.
- **Fecha:** 2026-11-12.
- **Issues:** #2 (casos de uso), #5 (selección tecnológica), #52 (clientes), #66 (desarrollo incremental).
- **Relacionado:** PR #94 (vertical slice de investigación BTC).

## 1. Objetivo y límites

Definir una primera experiencia navegable coherente para web, Android e iOS, comenzando por el caso de uso UC-BTC-RESEARCH-001. La especificación debe poder implementarse con el stack que resulte de las POCs de #5, sin acoplar navegación ni reglas de dominio a un framework.

El prototipo es research-only y read-only. No contiene conexión a exchanges, órdenes, trading, gestión de cartera ni credenciales. No implica que API, autenticación, persistencia o servicios estén implementados.

## 2. Principios de experiencia

1. **Research-first:** el usuario llega a investigación y evidencia, no a una pantalla de trading.
2. **Estado antes que conclusión:** mostrar disponibilidad y calidad de datos antes de interpretar el resultado.
3. **Trazabilidad visible:** cada resultado debe permitir identificar instrumento, periodo, cutoff, snapshot, metodología y procedencia cuando estén disponibles.
4. **Honestidad de producto:** distinguir PROTOTYPE, SIMULATED, EXPERIMENTAL, AVAILABLE, PARTIAL, NOT_AVAILABLE y ERROR.
5. **No look-ahead:** una vista histórica debe mostrar el cutoff temporal y no presentar información posterior como si hubiera sido conocida entonces.
6. **Un solo dominio:** clientes consumen contratos comunes; no replican cálculos, permisos ni reglas críticas.
7. **Accesibilidad y adaptación:** navegación por teclado/lector de pantalla, foco visible, contraste suficiente, escalado de texto y estados no comunicados solo por color.
8. **Degradación explícita:** si un servicio no existe, el prototipo muestra una vista demostrativa etiquetada; no simula éxito de red ni persistencia real.

## 3. Mapa de navegación

### Navegación principal

| Área | Ruta conceptual | Propósito | Estado inicial |
|---|---|---|---|
| Overview | /overview | Resumen del espacio de investigación y accesos recientes | PROTOTYPE |
| Research | /research | Selección de activo, instrumento y periodo; inicio de consulta | PROTOTYPE |
| Evaluations | /evaluations | Historial de evaluaciones guardadas y comparación | PROTOTYPE; sin persistencia real |
| Evidence | /evidence/:id | Fuentes, eventos, procedencia y limitaciones de una evaluación | PROTOTYPE |
| Settings | /settings | Preferencias visuales y configuración no sensible | PROTOTYPE |

No añadir ahora secciones de trading, cartera, órdenes, API keys ni automatización de inversión. La navegación no debe sugerir que esas capacidades están disponibles.

### Adaptación por plataforma

- **Web:** navegación lateral persistente en pantallas amplias; en anchos reducidos, navegación compacta y contenido en una columna.
- **Android/iOS:** navegación inferior para las áreas principales; pantallas de detalle con navegación atrás nativa; filtros y selectores en hojas o pantallas dedicadas cuando el espacio sea limitado.
- **Compartido:** nombres, jerarquía, iconografía semántica, estados, contratos y reglas de presentación comunes.
- **Específico de plataforma:** gestos, navegación atrás, teclado, permisos del sistema y notificaciones solo cuando un caso de uso aprobado los requiera.

La implementación no debe forzar idéntica disposición pixel a pixel; debe conservar equivalencia funcional, semántica y visual.

## 4. Pantallas del primer prototipo

### 4.1 Overview

- Estado global del entorno: DEMO / SIMULATED.
- Acceso principal a “Nueva investigación”.
- Lista demostrativa de evaluaciones recientes, claramente sintética.
- Tarjetas de capacidades con su estado real (prototipo/no disponible).
- No mostrar P&L, balances, predicciones ni precios reales en fixtures.

### 4.2 Nueva investigación

- Activo: BTC como piloto, etiquetado como selección de demostración.
- Instrumento/venue: selector sin valor predeterminado definitivo hasta resolver #62.
- Granularidad y periodo: opciones de fixture, sin sugerir que existe cobertura real.
- Cutoff temporal explícito cuando la consulta sea histórica.
- Validación de parámetros y mensajes de ausencia de instrumento/fuente.
- Acción “Ver demostración” separada de cualquier futura acción “Ejecutar análisis”.

### 4.3 Estado y calidad de datos

- Estado de fuente y autorización.
- Cobertura solicitada frente a cobertura disponible, solo si existen datos verificables.
- Gaps, segmentos discontinuos, frescura y limitaciones.
- Identificación clara de SIMULATED frente a AVAILABLE/PARTIAL.
- No fabricar porcentajes, conteos, latencia ni puntuaciones.

### 4.4 Resultado de investigación

- Resumen descriptivo del periodo.
- Secciones separadas para episodios, eventos/hipótesis y estructura técnica.
- Cada sección puede mostrar NOT_AVAILABLE si la capacidad no está implementada.
- Evidencia favorable y contraria; hipótesis no equivale a causalidad.
- Mostrar versión de metodología, snapshot, cutoff e incertidumbre cuando existan.
- En prototipo, todos los ejemplos son sintéticos y no deben parecer una recomendación financiera.

### 4.5 Evaluaciones

- Lista de evaluaciones con ID, activo/instrumento, periodo, fecha y estado.
- La acción de guardar en demo solo cambia estado local de la demostración y debe informar “no persistido”.
- Comparación visual de dos registros sintéticos sin afirmar cambios reales de mercado.
- En backend futuro, cada evaluación será inmutable y tendrá referencias de snapshot/versiones según PR #94.

### 4.6 Evidencia y detalle

- Fuente, tipo de evidencia, publicación/disponibilidad/ingesta si aplica.
- Enlaces y documentos de soporte cuando estén autorizados.
- Estado de verificación, evidencia contraria y limitaciones.
- Diferenciar hecho observado, inferencia, hipótesis y conclusión no cuantificada.

## 5. Componentes UI compartidos

- AppShell y navegación principal.
- AssetInstrumentSelector.
- PeriodRangeSelector y CutoffSelector.
- CapabilityStatusBadge (con texto accesible, no solo color).
- DataQualitySummary.
- EvidenceList y EvidenceDetail.
- ResearchSection.
- EvaluationList y EvaluationComparison.
- EmptyState, ErrorState, LoadingState y PartialDataState.
- DemoBanner persistente para fixtures sintéticos.

Los nombres son conceptos funcionales, no nombres de clases obligatorios ni selección de librería.

## 6. Modelo de estados de interfaz

| Estado | Significado | Presentación obligatoria |
|---|---|---|
| PROTOTYPE | Vista/flujo sin servicio funcional | Etiqueta “Prototipo” |
| SIMULATED | Datos/acciones sintéticos | Banner “DEMO — DATOS SINTÉTICOS” |
| EXPERIMENTAL | Capacidad real aún no validada para uso operativo | Etiqueta experimental y limitaciones |
| AVAILABLE | Capacidad implementada y verificada para ese contexto | Mostrar procedencia y fecha de verificación |
| PARTIAL | Resultado real incompleto | Explicar cobertura y omisiones |
| NOT_AVAILABLE | No existe dato/capacidad suficiente | Explicar causa si se conoce |
| ERROR | Fallo de operación | Mensaje recuperable y correlation ID cuando exista |

La UI no debe convertir automáticamente un error en “sin datos”, ni usar datos cacheados como actuales sin informar su antigüedad.

## 7. Criterios de aceptación del prototipo

- [ ] El usuario puede navegar Overview → Research → Data Status → Result → Evidence → Evaluations.
- [ ] El flujo puede recorrerse en web y en prototipo móvil con equivalencia funcional.
- [ ] Todos los fixtures y acciones simuladas llevan marca DEMO — DATOS SINTÉTICOS.
- [ ] No aparecen precios, noticias, métricas ni rendimientos reales inventados.
- [ ] Los estados PROTOTYPE/SIMULATED/NOT_AVAILABLE/PARTIAL/ERROR son distinguibles y accesibles.
- [ ] Formularios validan entradas y exponen errores de forma accesible.
- [ ] Navegación por teclado, foco visible, lector de pantalla y escalado de texto se verifican en las plataformas incluidas.
- [ ] La interfaz no contiene lógica de dominio, credenciales de exchange ni ejecución de órdenes.
- [ ] Los elementos que dependen de backend se identifican como no disponibles hasta existir contrato y pruebas.
- [ ] Se registra evidencia reproducible de navegación y pruebas de accesibilidad/usabilidad aplicables.

## 8. Estrategia de validación y decisiones pendientes

1. #5 debe cerrar la comparación y POCs de Next.js/TypeScript frente a React SPA y React Native/Expo frente a Flutter; esta especificación no elige ganador.
2. El prototipo debe demostrar build y navegación en web y Android; iOS debe validarse mediante un flujo reproducible compatible con las restricciones de Windows y los servicios cloud que se acepten.
3. Documentar coste, dependencia de proveedor, requisitos de cuentas/certificados, distribución, actualización y plan de salida para cualquier servicio de build cloud.
4. #51 debe definir los contratos que sustituirán fixtures; no crear endpoints ficticios.
5. #55 debe definir pruebas automatizadas y manuales de navegación, accesibilidad, estados y consistencia entre plataformas.
6. #66 gobierna la evolución continua: integrar cada capacidad backend verificada en los clientes mediante incrementos verticales.

## 9. Fuera de alcance

- Decisión final de framework, lenguaje, librerías o proveedor de build.
- Diseño visual final, branding definitivo o sistema de diseño completo.
- Backend, API, autenticación real, persistencia y sincronización.
- Datos reales, análisis real, predicción, ranking o señales.
- Trading, órdenes, cartera, exchange credentials y notificaciones de ejecución.
- Afirmar conformidad o certificación ISO.

## 10. Regla de evolución

El prototipo se acepta como prototipo, no como producto funcional. Cada incremento posterior sustituirá únicamente las fixtures de la capacidad integrada, manteniendo los mismos estados, contratos y pruebas de regresión. Ninguna pantalla cambiará de SIMULATED a AVAILABLE sin evidencia de implementación, autorización, pruebas y procedencia.
