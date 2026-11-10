# Flujo de ingeniería y gobierno de cambios

- **Proyecto:** Crypto Predictive Intelligence Ecosystem (CPIE)
- **Issue rector:** [#6 — Gobernanza técnica](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/6)
- **Protección de ramas:** [#68](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/68)
- **Roadmap:** [Programa maestro de remediación](./remediation-roadmap.md)

## 1. Regla de trazabilidad

Todo cambio material debe poder recorrerse en ambas direcciones:

`necesidad/requisito → Issue → decisión/ADR → branch → PR → verificaciones → evidencia → merge/release`

No se debe cerrar un Issue porque se haya creado un PR. Se cierra cuando los criterios de aceptación aplicables están demostrados y los cambios están integrados.

## 2. Tipos de Issues

- **Defecto:** comportamiento incorrecto, pasos de reproducción, impacto y evidencia.
- **Capacidad/mejora:** problema del usuario, caso de uso, resultado y criterios de aceptación.
- **Investigación/decisión:** pregunta, alcance, método, fuentes, alternativas, incertidumbre y conclusión.
- **Arquitectura/seguridad:** contexto, límites, riesgos, decisión requerida, mitigaciones y validación.
- **Tarea de ingeniería:** entregables concretos, dependencias y pruebas.

Las plantillas en `.github/ISSUE_TEMPLATE/` proporcionan una estructura inicial. Se pueden usar Issues en blanco cuando la categoría no encaje; no se debe forzar una clasificación incorrecta.

## 3. Contenido mínimo de un Issue

1. Contexto y problema.
2. Objetivo y alcance/no alcance.
3. Causa conocida o hipótesis, distinguiendo ambas.
4. Solución propuesta y alternativas.
5. Dependencias y riesgos.
6. Criterios de aceptación verificables.
7. Evidencias esperadas.
8. Relaciones con requisitos, Issues y ADRs.

No inventar métricas, umbrales, causas, resultados ni niveles de confianza. Indicar explícitamente lo que no se conoce.

## 4. Ramas

Convención recomendada: `<tipo>/<issue>-<descripcion-corta>`.

Ejemplos:
- `docs/6-engineering-governance`
- `feat/120-asset-registry`
- `fix/135-candle-validation`
- `security/140-secret-handling`

Las ramas de trabajo parten de la rama base vigente. No usar force-push salvo recuperación excepcional, justificada y trazada. No incluir secretos en nombres, commits, artefactos ni logs.

## 5. Pull Requests

Todo PR debe:
- Enlazar el Issue correcto; usar `Closes #N` solo cuando el PR realmente satisfaga todos los criterios de cierre del Issue.
- Explicar problema, causa/justificación, solución y alternativas.
- Declarar riesgos, compatibilidad y efecto sobre datos.
- Enumerar pruebas ejecutadas y resultados reales.
- Identificar verificaciones no ejecutadas y limitaciones.
- Actualizar documentación, contratos y ADRs afectados.
- Mantener el alcance acotado y revisable.

La plantilla `.github/pull_request_template.md` recoge estos puntos.

## 6. Revisión y merge

- Revisar el diff completo, no solo el título o la descripción.
- Verificar coherencia con el Issue, arquitectura, seguridad y criterios de aceptación.
- Ejecutar pruebas apropiadas al tipo y riesgo del cambio. Para documentación, validar estructura, enlaces y consistencia; no declarar pruebas de código que no aplican.
- No exigir aprobación independiente imposible en un repositorio cuyo único colaborador humano es el propietario. En ese caso, registrar revisión/autoverificación del propietario y exigir los checks automatizados que realmente existan y sean estables.
- No habilitar status checks obligatorios antes de que existan y pasen de forma consistente.
- No hacer merge si el diff no ha sido analizado o las verificaciones aplicables fallan.
- Preferir squash merge para mantener historial legible, salvo que el tipo de cambio requiera otra estrategia.

Estas reglas de proceso no sustituyen la protección técnica de la rama. La configuración efectiva de `main` se gestiona por separado en #68.

## 7. Decisiones de arquitectura (ADR)

Las decisiones que afecten arquitectura, stack, contratos, seguridad, datos, modelos, despliegue o trading deben registrarse en `docs/adr/` usando [la plantilla ADR](../adr/0000-template.md).

Un ADR debe registrar estado (propuesto, aceptado, rechazado, sustituido), contexto, decisión, alternativas, consecuencias, riesgos, evidencia y enlaces a Issues/PRs. No sobrescribir una decisión aceptada para ocultar su historia: crear un ADR sucesor y marcar el anterior como sustituido.

## 8. Etiquetas y milestones

Taxonomía inicial recomendada para crear en GitHub (no se considera aplicada hasta verificarla en la configuración del repositorio):

- **Tipo:** `type:bug`, `type:feature`, `type:research`, `type:architecture`, `type:security`, `type:documentation`, `type:operations`.
- **Prioridad:** `priority:p0`, `priority:p1`, `priority:p2`, `priority:p3`.
- **Estado:** `status:blocked`, `status:needs-evidence`, `status:ready`.
- **Área:** `area:data`, `area:predictive`, `area:trading`, `area:apps`, `area:platform`.

Usar solo las etiquetas necesarias; evitar etiquetas redundantes o mantener simultáneamente dos taxonomías equivalentes. Los milestones deben representar fases/objetivos con entregables y fechas únicamente cuando estas sean reales y acordadas. No asignar fechas ficticias.

## 9. Versionado y releases

- Usar versionado semántico cuando CPIE tenga releases consumibles y una política de compatibilidad definida.
- Cada release debe enlazar commits/PRs, cambios, migraciones, artefactos, verificaciones y riesgos conocidos.
- No etiquetar prototipos o modelos experimentales como releases de producción.

## 10. Seguridad y datos sensibles

Nunca incluir claves API, tokens, contraseñas, secretos, datos personales o archivos de configuración local con credenciales en Issues, PRs, commits o logs. Si se detecta una exposición, tratarla como incidente: revocar/rotar el secreto y registrar el incidente sin copiar el valor expuesto.

## 11. Estado de implementación

Este documento y las plantillas definen el proceso documental. No demuestran que:
- `main` esté protegida;
- labels o milestones estén configurados;
- CI/CD o status checks existan;
- el repositorio tenga certificación ISO;
- las aplicaciones o servicios estén implementados.

Esas condiciones requieren configuración y evidencia independiente en los Issues correspondientes.
