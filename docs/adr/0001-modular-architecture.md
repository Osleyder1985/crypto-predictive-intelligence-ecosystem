# ADR-0001: Arquitectura inicial modular de CPIE

- **Estado:** Aceptado como arquitectura objetivo inicial; sujeto a validación en pruebas de concepto de #5.
- **Fecha:** 2026-11-10
- **Responsable/rol:** Arquitectura de plataforma
- **Issues relacionados:** #4, #5, #7, #55, #56, #62, #64, #66
- **PR relacionado:** #78

## Contexto

CPIE debe soportar captura y conservación de datos de mercado, eventos y macroeconomía; preparación de datos; investigación y entrenamiento; inferencia; decisiones de cartera y riesgo; simulación y, solo tras autorización posterior, ejecución en exchanges. También debe ofrecer clientes web, Android e iOS sobre un backend y un modelo de datos común.

Hechos verificados en la reauditoría #71: el repositorio está en fase documental, no contiene implementación funcional, pruebas ejecutables ni CI. El entorno de desarrollo declarado para el proyecto es Windows 11 con recursos locales limitados (16 GB RAM). No existe evidencia que justifique operar desde el inicio una plataforma distribuida.

Restricciones de diseño:
- preservar trazabilidad, reproducibilidad y temporalidad point-in-time;
- separar predicción, decisión, gestión de riesgo y ejecución;
- mantener reglas críticas y credenciales fuera de los clientes y de los modelos;
- permitir desarrollo incremental de web, Android e iOS (#66);
- mantener PAPER como modo inicial y LIVE bloqueado;
- evitar infraestructura distribuida prematura y dependencias operativas no justificadas.

## Decisión

Adoptar un **monolito modular con límites de dominio explícitos**, contratos versionados y procesos de ejecución separados solo donde el aislamiento operacional o de seguridad lo justifique.

La unidad inicial de despliegue será una aplicación backend modular. Los trabajos largos (captura, backfills, cálculo de features, entrenamiento e inferencia por lotes) podrán ejecutarse como workers independientes construidos desde el mismo código y contratos. Esto permite aislar recursos y fallos sin convertir cada módulo de dominio en un microservicio.

### Módulos y responsabilidades

1. **Data Intelligence**
   - Adaptadores de fuentes y exchanges.
   - Captura de market, on-chain, derivatives, macro y news.
   - Registro de fuente, licencia, cobertura, timestamps y calidad.
   - No decide operaciones ni modifica límites de riesgo.

2. **Data Engineering**
   - Validación, normalización, deduplicación y reconciliación.
   - Conservación de originales y snapshots inmutables.
   - Contratos de observaciones, eventos y datasets.
   - Features reproducibles y temporalidad bitemporal/point-in-time.

3. **Predictive Intelligence**
   - Construcción de datasets de investigación y entrenamiento.
   - Modelos econométricos, estadísticos, ML y DL.
   - Regímenes, escenarios, ensembles y cuantificación/calibración de incertidumbre.
   - Versionado de modelos, features, parámetros y resultados.
   - No accede a credenciales de exchanges ni envía órdenes.

4. **Decision Intelligence**
   - Traducción de predicciones en hipótesis/señales evaluables.
   - Ranking de activos, portfolio construction y estado explícito NO_TRADE.
   - Horizonte, vigencia, condiciones, exposición y restricciones.
   - No elude ni modifica los controles de riesgo.

5. **Risk & Trading**
   - Política de riesgo independiente del modelo.
   - Order Intent, validación previa, idempotencia, órdenes, fills y reconciliación.
   - Adaptadores de exchange, límites, circuit breakers y kill switches.
   - PAPER por defecto; SHADOW según autorización; LIVE bloqueado.
   - Proceso/identidad y secretos aislados del backend de investigación.

6. **Platform & API**
   - API versionada, autenticación/autorización, sesiones y orquestación de casos de uso.
   - Contratos de lectura/escritura para clientes.
   - Auditoría, configuración, observabilidad y políticas transversales.
   - No contiene lógica cuantitativa duplicada en clientes.

7. **Client Applications**
   - Web, Android e iOS.
   - Consumen API y contratos compartidos.
   - No contienen credenciales de exchange, reglas de riesgo autoritativas ni lógica de ejecución.
   - Muestran claramente datos simulados, experimentales, no disponibles y verificados.

### Dependencias permitidas

- Los clientes dependen exclusivamente de contratos/API publicados.
- Platform/API orquesta casos de uso y depende de interfaces de los módulos; no debe apropiarse de su lógica de dominio.
- Los módulos de dominio no importan internamente implementaciones de otros módulos; colaboran mediante interfaces explícitas y contratos.
- Risk & Trading puede consumir decisiones aprobadas, pero Predictive Intelligence no depende de Risk & Trading.
- Ningún módulo de dominio escribe directamente en tablas propiedad de otro módulo. La integración usa interfaces/repositorios y eventos internos versionados.
- Se prohíben ciclos de dependencias entre módulos.
- Infraestructura (persistencia, colas, reloj, proveedores externos) se invierte detrás de puertos/adaptadores; no filtra SDKs externos al dominio.

### Procesos y aislamiento

- API: solicitudes interactivas y orquestación.
- Worker(s): captura, procesamiento, entrenamiento e inferencia batch; concurrencia limitada según recursos medidos.
- Trading adapter: proceso separado y deshabilitado por defecto; acceso mínimo a secretos; solo acepta órdenes validadas por Risk & Trading.
- Los workers comparten el código y los contratos de la aplicación inicialmente; no se presupone un broker externo.
- Para trabajos asíncronos, comenzar con persistencia transaccional y patrón outbox/inbox cuando sea necesario; incorporar broker solo si métricas de volumen, latencia, disponibilidad o aislamiento lo justifican.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas/riesgos | Evaluación |
|---|---|---|---|
| Monolito no modular | Menor coste inicial y despliegue sencillo | Acoplamiento, límites difusos, cambios de alto impacto y difícil aislamiento | Rechazada: no satisface gobierno de dominios y seguridad |
| Monolito modular | Despliegue simple; límites explícitos; pruebas por módulo; bajo coste operacional; extracción evolutiva | Requiere disciplina arquitectónica y control de dependencias | **Seleccionada** |
| Microservicios desde el inicio | Escalado y despliegue independientes; aislamiento de fallos | Complejidad de red, observabilidad, consistencia, seguridad, CI/CD y operación; coste elevado sin carga demostrada | Rechazada para la fase inicial |
| Híbrida distribuida desde el inicio | Aislamiento selectivo de cargas | Puede anticipar decisiones de infraestructura antes de medirlas | Pospuesta; aplicar solo a trading u otros procesos cuyo riesgo/carga lo exija |

No se han ejecutado benchmarks ni pruebas de carga; por tanto, la decisión no afirma superioridad de rendimiento. La selección se basa en el estado actual, las restricciones operativas y el coste/riesgo de complejidad distribuida.

## Flujos principales

### Datos e inteligencia

`Fuente → Adaptador → Raw inmutable → Validación/normalización → Observación/Event → Feature Set → Dataset point-in-time → Predicción → Resultado evaluado`

Cada transición conserva identificadores de procedencia y tiempos relevantes: event_time, available_at, ingested_at y recorded_at. La disponibilidad para una simulación se determina por lo que realmente se conocía en el instante evaluado, no por el timestamp retrospectivo del evento.

### Decisión y trading

`Predicción → Evaluación de vigencia/calidad → Decisión (incluye NO_TRADE) → Política de riesgo → Order Intent → Adaptador (PAPER/SHADOW) → Orden/Fill → Reconciliación → Resultado neto de costes`

LIVE permanece bloqueado fuera de esta decisión arquitectónica. Su habilitación requiere gates independientes de seguridad, cumplimiento, validación, operaciones y autorización explícita.

## Condiciones para extraer un módulo a servicio independiente

La extracción requiere un ADR específico y evidencia de al menos una necesidad concreta:
- perfil de carga incompatible con el resto y medido mediante pruebas reproducibles;
- necesidad de aislamiento de seguridad o credenciales que no pueda lograrse adecuadamente mediante proceso/identidad separados;
- requisitos distintos de disponibilidad, despliegue o escalado;
- límites de equipo/propiedad que justifiquen operación independiente;
- contención de fallos demostrablemente mejorada.

El caso debe incluir coste total operacional, contratos de red, autenticación servicio-a-servicio, observabilidad, consistencia, idempotencia, recuperación, CI/CD y plan de migración. No extraer por moda ni por tamaño del directorio.

## Justificación y evidencia

- Reauditoría #71: repositorio en fase documental; no existe implementación ni carga que justifique microservicios.
- Requisitos de #4: captura, investigación, entrenamiento, predicción, decisiones, trading y clientes.
- Roadmap: gates por fase, datos point-in-time, validación fuera de muestra y LIVE bloqueado.
- Estrategia de pruebas #55 y operaciones #56: requieren contratos verificables, pruebas por límites y recuperación.
- La arquitectura no selecciona todavía lenguaje, framework, base de datos, broker ni proveedor cloud. Esa decisión pertenece a #5 y debe apoyarse en comparación y POCs.

## Consecuencias

### Positivas
- Un despliegue y ciclo de desarrollo iniciales sencillos.
- Límites explícitos para proteger la separación de datos, modelos, decisiones y trading.
- Clientes independientes del backend y sin duplicación de reglas críticas.
- Workers aislables sin adoptar prematuramente una plataforma distribuida.
- Camino de extracción basado en evidencia.

### Costes y consecuencias negativas
- La disciplina de módulos, contratos y propiedad de datos debe imponerse desde el primer commit.
- Un único backend puede convertirse en cuello de botella si no se miden y aíslan las cargas.
- La ejecución de trading exige aislamiento adicional aunque comparta inicialmente repositorio y contratos.
- Los límites modulares deberán comprobarse mediante pruebas arquitectónicas y revisiones de dependencias.

## Riesgos residuales y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Monolito modular degenerando en monolito acoplado | Reglas de dependencias, pruebas arquitectónicas, ownership de módulos |
| Fuga temporal/leakage | Contratos point-in-time, datasets reproducibles y pruebas específicas |
| Modelos alterando ejecución o límites | Separación de interfaces, permisos y credenciales; Risk & Trading independiente |
| Sobrecarga de equipo/PC local | Workers limitados; medir memoria/CPU antes de paralelizar |
| Clientes divergentes | API/contratos versionados y reglas críticas en backend |
| Complejidad distribuida prematura | ADR y criterios medibles antes de extraer servicios |

## Revisión

Revisar esta decisión si las POCs de #5 demuestran incompatibilidad relevante con el entorno, o si pruebas de carga, seguridad o disponibilidad justifican separar un módulo. La revisión debe producir ADR sucesor; no editar silenciosamente la decisión aceptada.

## Historial

- 2026-11-10 — Decisión inicial basada en estado del repositorio, alcance y restricciones conocidas.
