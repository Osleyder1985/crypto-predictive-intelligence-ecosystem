# Primer vertical slice: investigación histórica de BTC

- **Estado:** propuesta de especificación; no implementada ni aprobada como baseline.
- **Issues rectores:** #2 (requisitos y casos de uso), #62 (piloto BTC), #66 (desarrollo incremental de aplicaciones).
- **Integración prevista:** #8–#10, #13, #20–#25, #29, #31, #39–#43, #51–#52, #55, #60 y #93.
- **Fecha:** 2026-11-12.

## 1. Propósito

Definir el primer flujo vertical visible de CPIE: un usuario selecciona Bitcoin, consulta un periodo histórico y obtiene una evaluación de investigación reproducible, con procedencia, calidad, limitaciones e incertidumbre explícitas. El usuario puede guardar esa evaluación y compararla con otra evaluación posterior.

Este slice es **research-only y read-only**. No genera órdenes, no habilita PAPER/SHADOW/LIVE y no presenta una hipótesis como causalidad demostrada.

## 2. Actor y caso de uso

**UC-BTC-RESEARCH-001 — Consultar y guardar una evaluación histórica de Bitcoin**

Actor principal: analista autenticado (el modelo de identidad y permisos sigue sujeto a #7 y #51).

Precondiciones:
- El usuario tiene permiso de lectura.
- El instrumento está identificado de forma inequívoca en el registro.
- El periodo solicitado y la granularidad son válidos.
- La fuente y el uso de sus datos están autorizados.
- Existe un snapshot reproducible o el sistema informa que no puede construirlo.

Flujo principal:
1. El analista abre la aplicación y selecciona Bitcoin y un instrumento/venue disponible.
2. Selecciona granularidad y periodo histórico.
3. CPIE valida elegibilidad del activo/instrumento, autorización de fuentes, cobertura, continuidad, calidad y disponibilidad temporal.
4. CPIE crea o recupera un snapshot con cutoff point-in-time y manifiesto de procedencia.
5. El sistema presenta el estado de los datos y sus limitaciones antes de interpretar resultados.
6. Cuando los datos y capacidades estén disponibles, presenta episodios alcistas/bajistas, eventos asociados como hipótesis no causales y zonas/escenarios técnicos con temporalidad point-in-time.
7. La respuesta incluye versión de metodología, referencias de evidencia, incertidumbre y campos no cuantificados.
8. El analista guarda una evaluación inmutable que referencia el snapshot, contratos y versiones utilizados.
9. El analista puede abrir una evaluación anterior y comparar cambios sin sobrescribir el registro original.

## 3. Alcance por incrementos

### Incremento A — Prototipo navegable temprano

- Identidad visual inicial, navegación y pantallas del flujo.
- Selector de activo/instrumento, granularidad y periodo.
- Vistas de estado de datos, resumen de investigación, detalle de evidencia e historial de evaluaciones.
- Fixtures **sintéticos** deterministas para demostrar estados y navegación.
- Etiqueta persistente y visible: DEMO — SYNTHETIC DATA; no usar precios ni noticias reales en fixtures simulados.
- Estados UI: PROTOTYPE, SIMULATED, NOT_AVAILABLE, PARTIAL, AVAILABLE y ERROR, con semántica documentada.
- Sin persistencia real, salvo que exista ya un servicio verificado; en caso contrario, guardar/comparar se representa como interacción de prototipo y se identifica como tal.

### Incremento B — Contrato y backend mínimo verificable

- Contrato versionado para consulta, estado de calidad, snapshot y evaluación guardada.
- Validación de permisos, parámetros, errores, idempotencia y paginación donde aplique.
- Persistencia de snapshot/manifiesto y evaluación inmutable.
- Contract tests y tests de integración con fixtures controlados.
- Ningún endpoint ni comportamiento se etiqueta como disponible hasta estar implementado y probado.

### Incremento C — Datos históricos reales autorizados

- Incorporar únicamente una fuente cuya licencia/permiso cubra el uso concreto.
- Selección definitiva de instrumento, venue, granularidad y periodo mediante #62 y los Issues de datos.
- Validar gaps, segmentos discontinuos, duplicados, revisiones, timestamps y cobertura.
- No rellenar huecos silenciosamente ni extrapolar periodos ausentes.
- Registrar fuente, método de captura, timestamp de disponibilidad, ingesta, checksum/manifiesto y limitaciones.

### Incremento D — Inteligencia integrada

- Episodios históricos conforme a #29.
- Eventos/noticias conforme a #21, #23 y #31, preservando publicación, disponibilidad, revisiones y evidencia contraria.
- Zonas y escenarios técnicos conforme a #93.
- Comparación longitudinal conforme a #39 y #60.
- Los resultados se integran solo cuando sus contratos y pruebas correspondientes sean verificables.

## 4. Contrato funcional mínimo a especificar en #51

La API deberá permitir, como mínimo conceptual:
- Consultar activos e instrumentos elegibles.
- Solicitar una evaluación indicando instrumento, periodo, granularidad y cutoff temporal.
- Consultar estado de ejecución y calidad/cobertura.
- Recuperar snapshot y procedencia.
- Recuperar resultado de investigación y sus limitaciones.
- Guardar/consultar evaluaciones y comparar dos versiones.

No se fijan aquí rutas HTTP, nombres definitivos de campos, tecnología, SLA ni esquema ejecutable. Esas decisiones requieren la especificación de #51 y los contratos de dominio pertinentes.

## 5. Estados y comportamiento ante fallos

| Situación | Comportamiento esperado |
|---|---|
| Fuente no autorizada | Rechazar la captura/consulta que dependa de ella y explicar el bloqueo. |
| Instrumento no identificado o no elegible | No inferir equivalencias; solicitar selección válida o informar no disponible. |
| Datos incompletos o discontinuos | Devolver estado parcial, intervalos cubiertos y limitaciones; no rellenar silenciosamente. |
| Snapshot no reproducible | No permitir guardar como evaluación reproducible; registrar causa. |
| Datos insuficientes para un análisis | Abstenerse de producir esa conclusión y mostrar NOT_AVAILABLE o estado equivalente. |
| Evento sin evidencia suficiente | Mostrarlo como no verificado/hipótesis o excluirlo; nunca afirmar causalidad. |
| Error de backend o timeout | Mostrar error recuperable y correlation ID cuando exista; no mostrar resultados antiguos como actuales sin indicarlo. |
| Datos sintéticos | Mostrar marca SIMULATED en toda vista, exportación y comparación. |

## 6. Modelo de evaluación guardada

Cada evaluación persistida deberá referenciar, como mínimo conceptual:
- Identificador inmutable de evaluación.
- Activo e instrumento.
- Periodo solicitado, granularidad y cutoff temporal.
- Snapshot/manifiesto de datos y estado de calidad.
- Versiones de contratos, transformaciones y metodologías.
- Resultados y evidencia asociada.
- Limitaciones, incertidumbre y estados no cuantificados.
- Fecha de creación y actor/servicio responsable.

Una evaluación nueva crea un registro nuevo. No actualiza ni reescribe el resultado histórico.

## 7. Criterios de aceptación del slice completo

- [ ] Existe un prototipo navegable que cubre el flujo de selección, consulta, resultados e historial.
- [ ] Toda información sintética está marcada inequívocamente y no puede confundirse con datos reales.
- [ ] El instrumento y la fuente usados en una evaluación real están autorizados y trazados.
- [ ] El snapshot permite reconstruir exactamente los datos y transformaciones utilizados, dentro de las limitaciones declaradas.
- [ ] La temporalidad point-in-time impide usar información posterior al cutoff.
- [ ] Datos parciales, errores y ausencia de evidencia se muestran explícitamente.
- [ ] Episodios, eventos y zonas solo aparecen cuando sus capacidades están implementadas y verificadas.
- [ ] Las evaluaciones guardadas son inmutables y comparables.
- [ ] Existen contract, integration y E2E tests aplicables, con resultados y artefactos auditables.
- [ ] La experiencia compartida entre web, Android e iOS consume contratos comunes; no duplica lógica de dominio.
- [ ] No existe dependencia de trading ni posibilidad de enviar órdenes desde este flujo.

## 8. Fuera de alcance

- Predicción validada, probabilidades calibradas o promesas de rentabilidad.
- Ranking multiactivo o recomendación de cartera.
- Señales ejecutables, órdenes, paper trading, shadow trading y trading LIVE.
- Atribución causal automática de movimientos a noticias.
- Selección definitiva de stack, fuente, venue, timeframe o periodo histórico.
- Certificación o declaración de conformidad ISO.

## 9. Dependencias y decisiones pendientes

- #62 debe definir el piloto BTC, instrumentos, fuentes, periodos y protocolo.
- #8–#10 deben permitir identificar activos e instrumentos.
- #13 debe resolver autorización de uso de fuentes.
- #20–#25 y #64 deben proporcionar contratos, temporalidad, calidad, continuidad y conservación.
- #29, #31 y #93 gobiernan las capacidades de investigación.
- #39 y #60 gobiernan predicciones y evaluación longitudinal cuando correspondan.
- #51 define API/contratos; #52 define estrategia y navegación de clientes.
- #55 define pruebas y evidencia; #66 establece evolución incremental y continua.

## 10. Regla de implementación

Implementar cada incremento mediante PR separado, vinculado a los Issues responsables. No crear una API ficticia, no declarar servicios funcionales por existir un prototipo y no activar required checks hasta que los workflows estén probados. Si una dependencia no está satisfecha, conservar el estado como pendiente y avanzar solo en las partes independientes.
