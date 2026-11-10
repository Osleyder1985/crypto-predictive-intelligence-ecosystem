# ADR-0002: Criterios y shortlist inicial del stack tecnológico

- **Estado:** Propuesto; no autoriza todavía fijar versiones ni iniciar despliegues de producción.
- **Fecha:** 2026-11-10
- **Responsable/rol:** Arquitectura y plataforma
- **Issues relacionados:** #4, #5, #7, #55, #56, #62, #66
- **PR relacionado:** pendiente

## Contexto

La arquitectura inicial (ADR-0001) establece un monolito modular con API, workers y aislamiento del proceso de trading. El repositorio aún no contiene código ni POCs ejecutadas. El entorno conocido de desarrollo es Windows 11 con 16 GB RAM; por tanto, la selección debe minimizar instalaciones pesadas y permitir pruebas locales reproducibles.

La documentación oficial consultada indica una restricción relevante: PyTorch en Windows documenta soporte de Python 3.9–3.12. En cambio, Next.js requiere Node.js 20.9 o posterior, React Native requiere Node 22.11 o posterior, y PostgreSQL 18 está en soporte activo. Por ello, las versiones no deben elegirse solo por ser las más nuevas: hay que respetar la intersección de compatibilidad del stack.

## Shortlist propuesta (pendiente de POC)

| Dominio | Candidato principal | Alternativa | Estado y razón |
|---|---|---|---|
| Lenguaje de backend/quant | Python 3.12.x | Python 3.13.x | 3.12 es la base inicial de POC por compatibilidad documentada con PyTorch Windows; no fijar patch hasta probar wheels y dependencias. |
| Procesamiento tabular | Polars | pandas | Polars se prueba como motor principal por ejecución columnar/lazy; pandas se conserva como interoperabilidad y alternativa para librerías que lo requieran. |
| API | FastAPI + Pydantic | Django REST Framework | FastAPI es candidato por API tipada y separación clara de contratos; medir validación, documentación, auth y testing. |
| Persistencia transaccional | PostgreSQL 18.x | PostgreSQL 17.x | PostgreSQL 18 es versión mayor soportada; validar drivers, migraciones, backup/restore y Docker/Windows. |
| Datos históricos/analíticos | Parquet + PyArrow | CSV solo para intercambio simple | Parquet como formato columnar versionado; CSV no será formato canónico para datasets grandes. |
| Archivos originales | Filesystem local tras interfaz de Object Storage | S3-compatible remoto | Empezar local para desarrollo; elegir proveedor y retención en decisión separada. No limitar la conservación por un umbral arbitrario. |
| Econometría/series | statsmodels + arch | Implementaciones especializadas | Incorporar por necesidad de modelo; probar wheels Windows y compatibilidad NumPy/SciPy. |
| ML clásico | scikit-learn + XGBoost | LightGBM | Baselines y modelos tabulares; comparar rendimiento, explicabilidad y facilidad de reproducir. |
| Deep Learning | PyTorch CPU primero | GPU/CUDA si hardware y POC lo justifican | No asumir GPU NVIDIA. Mantener entrenamiento pesado opcional/remoto si 16 GB RAM limitan. |
| Tracking de experimentos | MLflow local | Registro propio mínimo temporal | POC local primero; tracking server y backend PostgreSQL solo cuando exista necesidad de compartir/concurrencia. |
| Web | Next.js + TypeScript | React SPA | Candidato para experiencia web completa; verificar bundle, SSR y despliegue frente al alcance real. |
| Android/iOS | React Native + Expo | Flutter | Candidato para compartir UI/lógica entre plataformas; Windows permite flujo Android, pero la compilación nativa local de iOS requiere macOS. Expo EAS ofrece builds cloud Android/iOS; evaluar dependencia y coste antes de producción. |
| Contenedores local | Docker Compose + WSL2 | Servicios nativos Windows | Compose para reproducibilidad de dependencias; limitar servicios concurrentes por 16 GB RAM. |
| Observabilidad | OpenTelemetry como estándar de instrumentación; backend por decidir | Instrumentación nativa | No elegir stack de métricas/logs antes de definir despliegue, retención y coste. |

## Restricciones de versión y compatibilidad

- Python 3.12.x es la versión candidata inicial para POC de ML en Windows porque la guía oficial de PyTorch consultada documenta Windows + Python 3.9–3.12. Si PyTorch amplía soporte, reevaluar sin cambiar la base hasta ejecutar pruebas.
- Node.js debe cumplir al menos 22.11 para el entorno React Native consultado; Next.js documenta mínimo 20.9. Usar una línea LTS común, verificar compatibilidad de Expo/React Native y fijar patch en lockfile cuando el POC pase.
- PostgreSQL 18.x es candidato por soporte activo; seleccionar patch soportado al crear la imagen/instalador y revisar política de upgrades.
- No fijar versiones de Polars, FastAPI, scikit-learn, XGBoost, PyTorch, MLflow, Next.js o Expo en este ADR: el lockfile y la matriz CI de POC deben demostrar la combinación real.

## Alternativas deliberadamente no adoptadas de inicio

| Tecnología | Decisión inicial | Condición para reconsiderar |
|---|---|---|
| Kubernetes | No adoptar | Necesidad probada de orquestación multi-host/alta disponibilidad que Compose y plataforma objetivo no cubran |
| Kafka | No adoptar | Volumen, throughput, retención/replay y consumidores independientes medidos |
| Redis | No adoptar | Caso medido de cache, coordinación o colas que no pueda cubrirse con PostgreSQL u otro componente ya elegido |
| TimescaleDB | No adoptar por defecto | Benchmarks de consultas/retención/compresión que demuestren beneficio suficiente frente a PostgreSQL + particionamiento/Parquet |
| Microservicios | No adoptar de inicio | Criterios ADR-0001 y caso económico/operacional demostrado |
| GPU/CUDA | No asumir | Hardware compatible y benchmark reproducible que justifique coste y mantenimiento |

## POCs obligatorias antes de aceptación final

1. **Entorno Python Windows:** instalar Python 3.12 x64 en venv; resolver wheels para Polars, PyArrow, NumPy, SciPy, statsmodels, scikit-learn, XGBoost y PyTorch CPU; ejecutar import smoke tests y un entrenamiento pequeño.
2. **Datos tabulares:** comparar Polars y pandas con el mismo dataset sintético/histórico controlado; medir tiempo, RAM, exactitud y resultados; no usar datos con licencias no autorizadas.
3. **Persistencia:** PostgreSQL 18 con migración, escritura/lectura temporal, índices, backup y restore; comparar volumen pequeño y representativo.
4. **API:** FastAPI con contratos Pydantic, validación, auth de prueba, OpenAPI, pruebas de contrato y latencia bajo carga definida.
5. **Tracking:** MLflow local; registrar parámetros, métricas, artefactos y reproducir una ejecución; medir uso de disco y RAM.
6. **Web:** build Next.js, pruebas, rutas autenticadas y consumo de API.
7. **Móvil:** prototipo Expo en Android físico/emulador; generar build iOS con EAS cloud y documentar límites, credenciales, costes y dependencia del servicio.
8. **Contenedores:** ejecutar solo los servicios mínimos en Docker Compose/WSL2; medir memoria en reposo y bajo carga.

Cada POC registrará hardware/software exactos, lockfiles, comandos, dataset/fixture, repeticiones, resultados brutos, limitaciones y decisión. No establecer umbrales de rendimiento arbitrarios: derivarlos de requisitos y perfil de carga antes de medir.

## Coste, licencias y riesgos

- Priorizar licencias open source compatibles con uso comercial; revisar licencia y obligaciones de cada dependencia y servicio antes de incorporar.
- Separar coste de licencia, cloud, almacenamiento, ancho de banda, CI, build móvil y operación.
- Expo EAS y otros servicios gestionados son dependencias opcionales; documentar límites, costes y plan de salida.
- Evitar dependencia de proveedor en formatos de datos, contratos y artefactos.
- Mantener SBOM, lockfiles, hashes y política de actualización una vez exista implementación.
- No subir secretos, tokens ni credenciales a archivos de configuración o pipelines.

## Criterio de aceptación del ADR

Este ADR solo pasará a Aceptado cuando las POCs críticas se ejecuten en el entorno Windows objetivo o se documente explícitamente qué parte requiere CI/servicio remoto. La shortlist es una hipótesis priorizada, no un resultado de benchmark ni una aprobación final del stack.

## Fuentes oficiales consultadas

- Python on Windows: https://docs.python.org/3/using/windows.html
- PyTorch local installation / Windows support: https://docs.pytorch.org/get-started/locally/
- Polars installation: https://docs.pola.rs/user-guide/installation/
- scikit-learn installation: https://scikit-learn.org/stable/install
- XGBoost installation: https://xgboost.readthedocs.io/en/stable/install.html
- PostgreSQL versioning: https://www.postgresql.org/support/versioning/
- PostgreSQL 18 documentation: https://www.postgresql.org/docs/18/
- statsmodels installation: https://www.statsmodels.org/dev/install.html
- MLflow tracking server: https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/
- Next.js installation: https://nextjs.org/docs/app/getting-started/installation
- React Native environment setup: https://reactnative.dev/docs/set-up-your-environment
- Expo EAS Build: https://docs.expo.dev/build/
- Docker Desktop WSL2: https://docs.docker.com/desktop/features/wsl/


---

## Addendum 1 — Política de selección `latest-stable-first` (2026-11-10)

**Esta adenda prevalece sobre cualquier recomendación anterior de usar Python 3.12.x como runtime general inicial.** La recomendación 3.12 queda acotada a una línea de compatibilidad para componentes que todavía la exijan.

### Política normativa del proyecto

1. Para cada tecnología se identifica primero la versión estable más reciente publicada por el proyecto upstream en la fecha de evaluación.
2. Se excluyen Alpha, Beta, Release Candidate, Nightly, Preview y builds experimentales de la baseline normal. Pueden probarse en una pista experimental aislada, sin promoverlas automáticamente.
3. «Más reciente» no significa «aprobada». Ninguna versión pasa a la **Validated Baseline** sin superar pruebas unitarias, integración, seguridad, compatibilidad, reproducibilidad y rendimiento/coste aplicables.
4. Se mantienen dos referencias diferenciadas:
   - **Latest Stable Candidate:** versión estable upstream que conviene evaluar ahora.
   - **Validated Baseline:** combinación exacta de versiones, plataformas, dependencias y artefactos que CPIE haya probado y aprobado.
5. La matriz de compatibilidad es el registro de autoridad para candidatos, rangos soportados, restricciones, evidencia, estado de prueba y fecha de revisión.
6. No se fijan versiones finales ni se actualizan lockfiles de producción antes de las POCs. Los experimentos sí deben registrar versiones exactas y hashes.
7. Cada actualización se evalúa primero en una rama/CI aislada; no se promueve a la baseline por el mero hecho de ser un release estable nuevo.
8. Si una dependencia crítica aún no soporta el runtime más reciente, se debe probar aislamiento por entorno/proceso o una línea secundaria compatible. No se degrada todo el stack sin demostrar que es necesario.
9. Se registran OS, arquitectura, runtime, versión de paquete, backend de cómputo (CPU/GPU), gestor de paquetes, wheels/binarios disponibles y restricciones de compilación.
10. Las versiones de seguridad deben revisarse también entre ciclos de mantenimiento; cualquier excepción o bloqueo debe quedar documentado.

### Candidatos verificados al corte

| Componente | Latest Stable Candidate al 2026-11-10 | Línea secundaria / restricción | Estado CPIE |
|---|---|---|---|
| Python | 3.15.2 | Python 3.12.x como compatibility lane para PyTorch en Windows, mientras la guía oficial mantenga ese límite | Candidato; no probado en CPIE |
| Node.js | 26.13.0 LTS | 24.22.2 LTS como alternativa LTS | Candidato; no probado en CPIE |
| PostgreSQL | 18.6 | Mantener otra major soportada solo si una dependencia o migración lo exige | Candidato; no probado en CPIE |
| PyTorch | Build Stable ofrecida por el selector oficial en la fecha de la POC; registrar versión exacta y comando generado | En Windows, la guía consultada declara Python 3.9–3.12 | Versión exacta pendiente de captura y prueba |

La página oficial de PostgreSQL anunciaba el siguiente ciclo de releases menores para el 12-Nov-2026; por tanto, 18.6 es el candidato documentado en este corte y la matriz debe revisarse después de esa publicación, sin anticipar su número o contenido.

### Efecto sobre la shortlist

- Python 3.15.x se convierte en la línea general prioritaria de evaluación, no en runtime aprobado.
- Python 3.12.x se conserva como línea secundaria aislada para probar PyTorch en Windows. No se debe forzar la instalación de todo el stack científico en una sola versión de Python si la matriz demuestra incompatibilidad.
- Node.js 26 LTS es la primera línea a evaluar para el ecosistema web/móvil; Node.js 24 LTS queda como alternativa de compatibilidad.
- PostgreSQL 18.6 es el candidato de base de datos al corte, sujeto a actualización de patch y pruebas de backup/restore, migraciones, drivers y contenedores.
- PyTorch debe instalarse desde el canal Stable oficial, no Preview/Nightly, y su versión exacta debe quedar registrada en la evidencia de POC.

### POCs y promoción

La primera fase compara entornos separados: (A) Python latest stable con librerías científicas compatibles; (B) Python 3.12 en Windows para PyTorch y dependencias requeridas. Se evaluará si ambas líneas pueden coexistir en entornos virtuales independientes o procesos aislados sin duplicación de datos ni contratos. La integración conjunta se probará solo después de verificar cada entorno por separado.

La matriz viva está en [Version Compatibility Matrix](../architecture/version-compatibility-matrix.md). Hasta que se completen las POCs y la revisión de licencias, el estado del ADR continúa **Propuesto**.

### Fuentes oficiales para los candidatos del corte

- Python 3.15.2 (estable): https://www.python.org/getit/windows/
- Node.js 26.13.0 LTS y 24.22.2 LTS: https://github.com/nodejs/node/releases
- PostgreSQL 18.6: https://www.postgresql.org/docs/release/18.6/
- Calendario de releases PostgreSQL: https://www.postgresql.org/developer/roadmap/
- Selector Stable y restricciones Windows/Python de PyTorch: https://docs.pytorch.org/get-started/locally/
