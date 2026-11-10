# CPIE — Matriz de compatibilidad de versiones

- **Fecha de corte inicial:** 2026-11-10
- **Estado:** Baseline no validada; matriz de candidatos documentales.
- **Autoridad:** ADR-0002 y Issue #5.
- **Entorno objetivo conocido:** Windows 11 x64, 16 GB RAM.
- **Regla:** ningún candidato se considera probado o aprobado por aparecer en esta tabla.

## 1. Estados controlados

| Estado | Significado |
|---|---|
| CANDIDATE | Release estable identificado en fuente oficial; pendiente de POC |
| COMPATIBILITY-LANE | Versión secundaria para aislar una restricción concreta |
| TESTING | POC iniciada; evidencia incompleta |
| PASS | Pruebas definidas ejecutadas y evidencia reproducible disponible |
| FAIL | Prueba ejecutada y fallo reproducible |
| BLOCKED | No se pudo probar por dependencia, hardware, acceso o entorno |
| VALIDATED-BASELINE | Combinación exacta aprobada tras revisar todos los controles aplicables |
| DEFERRED | No necesaria para la fase actual o falta caso de uso |

## 2. Candidatos y compatibilidad conocida

| Tecnología / dominio | Latest Stable Candidate (corte) | Compatibility lane / mínimo conocido | Plataforma objetivo | Estado | Evidencia |
|---|---|---|---|---|---|
| Python runtime general | 3.15.2 | 3.12.x aislado para PyTorch Windows | Windows 11 x64 | CANDIDATE | https://www.python.org/getit/windows/ |
| Python + PyTorch Windows | No asumir 3.15 compatible | 3.9–3.12 según guía oficial consultada | Windows 11 x64, CPU primero | COMPATIBILITY-LANE | https://docs.pytorch.org/get-started/locally/ |
| Node.js | 26.13.0 LTS | 24.22.2 LTS | Windows 11 x64 / CI | CANDIDATE | https://github.com/nodejs/node/releases |
| PostgreSQL | 18.6 | Otras majors soportadas solo por necesidad probada | Contenedor/Windows | CANDIDATE | https://www.postgresql.org/docs/release/18.6/ |
| PyTorch | Canal Stable; registrar versión exacta del selector al ejecutar POC | CPU; GPU/CUDA no asumida | Windows 11 x64 | CANDIDATE | https://docs.pytorch.org/get-started/locally/ |
| Polars | Consultar release estable al inicio de POC | Rango Python y wheels Windows por verificar | Windows 11 x64 | CANDIDATE | https://pypi.org/project/polars/ |
| PyArrow | Consultar release estable al inicio de POC | Rango Python y wheels Windows por verificar | Windows 11 x64 | CANDIDATE | https://pypi.org/project/pyarrow/ |
| NumPy / SciPy | Consultar releases estables al inicio de POC | Compatibilidad conjunta con Python, PyArrow, statsmodels y PyTorch | Windows 11 x64 | CANDIDATE | https://pypi.org/project/numpy/ ; https://pypi.org/project/scipy/ |
| statsmodels / arch | Consultar releases estables al inicio de POC | Wheels y compatibilidad NumPy/SciPy por verificar | Windows 11 x64 | CANDIDATE | https://www.statsmodels.org/stable/ ; https://arch.readthedocs.io/ |
| scikit-learn | Consultar release estable al inicio de POC | Rango Python/NumPy/SciPy por verificar | Windows 11 x64 | CANDIDATE | https://scikit-learn.org/stable/install |
| XGBoost / LightGBM | Consultar releases estables al inicio de POC | Wheels, runtime y backend CPU/GPU por verificar | Windows 11 x64 | CANDIDATE | https://xgboost.readthedocs.io/en/stable/install.html ; https://lightgbm.readthedocs.io/ |
| FastAPI / Pydantic | Consultar releases estables al inicio de POC | Rango Python y compatibilidad transitiva por verificar | Windows 11 x64 / CI | CANDIDATE | https://fastapi.tiangolo.com/ ; https://docs.pydantic.dev/latest/ |
| MLflow | Consultar release estable al inicio de POC | Backend local primero; PostgreSQL solo si POC lo justifica | Windows 11 x64 / Docker | CANDIDATE | https://mlflow.org/docs/latest/ |
| Next.js / React | Consultar releases estables al inicio de POC | Node.js compatible con framework y toolchain | Windows 11 x64 / CI | CANDIDATE | https://nextjs.org/docs |
| React Native / Expo | Consultar releases estables compatibles al inicio de POC | Node.js y Android SDK; build iOS cloud/macOS | Windows 11 x64 + EAS opcional | CANDIDATE | https://reactnative.dev/docs/ ; https://docs.expo.dev/ |
| Docker Desktop / Compose | Consultar release estable al inicio de POC | WSL2; medir consumo concurrente | Windows 11 x64 | CANDIDATE | https://docs.docker.com/desktop/ ; https://docs.docker.com/compose/ |

**Nota temporal:** PostgreSQL publica su calendario de releases menores y anunciaba el siguiente ciclo para el 12-Nov-2026. Revisar esta fila después de esa fecha; no anticipar versiones futuras. Fuente: https://www.postgresql.org/developer/roadmap/

## 3. Matriz de POC obligatoria

Por cada ejecución, registrar una fila por combinación exacta. No sobrescribir resultados previos.

| Campo | Obligatorio |
|---|---|
| poc_id | Identificador único |
| technology / component | Componente evaluado |
| version_exact | Versión completa, sin comodines |
| release_channel | Stable / LTS / pre-release (esta última solo experimental) |
| release_date | Fecha upstream |
| source_url | Página oficial de release o instalación |
| os_build / architecture | Versión exacta del sistema y x64/ARM64 |
| runtime_versions | Python, Node, Java, .NET u otros aplicables |
| package_manager / lockfile | Herramienta y archivo/hash |
| dependency_resolution | Resultado completo de resolver dependencias |
| binary_support | Wheel/installer/container disponible y origen |
| test_command / test_result | Comando y resultado verificable |
| integration_result | Resultado al combinar con componentes CPIE |
| performance_profile | Dataset, repeticiones, tiempo, RAM, CPU, disco |
| security_review | Advisories, SBOM y resultado de escaneo |
| license_review | Licencia directa/transitiva y uso comercial |
| evidence_artifact | Logs, reportes, hashes y ubicación |
| status | Estado controlado de la sección 1 |
| tested_at / reviewer | Fecha UTC y responsable |
| decision / rationale | Adoptar, mantener lane, rechazar o bloquear; con razón |

## 4. Orden de evaluación

1. Python 3.15.x general y Python 3.12.x + PyTorch Windows, en entornos separados.
2. Polars/PyArrow y stack numérico en cada lane; imports, lectura/escritura, tipos, fechas, reproducibilidad y memoria.
3. PostgreSQL 18.x: drivers, migraciones, constraints, índices, backup y restore.
4. FastAPI/Pydantic: contratos, auth, validación, OpenAPI, integración y pruebas.
5. Modelos: statsmodels/arch, scikit-learn, XGBoost/LightGBM y PyTorch; CPU como baseline inicial.
6. MLflow local y artefactos; después integración con PostgreSQL si se justifica.
7. Node.js LTS, Next.js y React Native/Expo; builds, tests y consumo de API.
8. Docker Compose/WSL2: servicios mínimos y perfil de RAM con carga definida.

## 5. Reglas de promoción

- Un PASS aislado no convierte toda la combinación en baseline.
- La promoción requiere pruebas de componentes, integración, seguridad, licencias, reproducibilidad y rollback según el alcance.
- Si dos componentes solo funcionan con runtimes diferentes, conservar lanes separadas hasta demostrar que el coste de integración es aceptable.
- Registrar incompatibilidades reales; no deducirlas solo por ausencia de documentación.
- Toda actualización de versión debe abrir evaluación en rama separada y comparar contra la baseline actual.
- No cambiar la baseline durante un ciclo de evaluación o análisis de mercado sin una release técnica controlada.
- No usar dependencias pre-release en la baseline normal.
- Los lockfiles deben fijar versiones y hashes de artefactos para builds reproducibles.
- Revisión periódica de releases y revisión extraordinaria ante advisories de seguridad.

## 6. Línea base actual

**Validated Baseline: ninguna.** CPIE no ha ejecutado todavía estas POCs ni benchmarks en el equipo objetivo. La documentación de upstream demuestra existencia y restricciones publicadas, no compatibilidad funcional de CPIE. Los campos de prueba y medición permanecen pendientes.
