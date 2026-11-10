# Evaluación tecnológica inicial de CPIE

- **Issue:** [#5 — Investigar y seleccionar el stack tecnológico](https://github.com/Osleyder1985/crypto-predictive-intelligence-ecosystem/issues/5)
- **ADR:** [ADR-0002 — Criterios y shortlist inicial](../adr/0002-technology-shortlist.md)
- **Estado:** Investigación documental preliminar; POCs y selección final pendientes.
- **Fecha de corte:** 2026-11-10

## 1. Método

La selección se basa en:
1. Compatibilidad con Windows 11 x64 y recursos locales conocidos (16 GB RAM).
2. Compatibilidad entre versiones del ecosistema científico.
3. Madurez, documentación, interoperabilidad y disponibilidad de paquetes binarios.
4. Licencias y posibilidad de uso comercial.
5. Coste operativo y complejidad de despliegue.
6. Reproducibilidad, portabilidad y facilidad de probar.
7. Evitar infraestructura que no tenga un caso de uso demostrado.

No se han ejecutado POCs en el equipo Windows objetivo ni benchmarks de CPIE. Por tanto, no se presentan resultados de rendimiento, consumo de RAM ni costes numéricos.

## 2. Matriz de evaluación preliminar

| Componente | Candidato | Evidencia documental | Riesgo/pendiente | Estado |
|---|---|---|---|---|
| Runtime cuantitativo | Python 3.12.x | PyTorch documenta soporte Windows para Python 3.9–3.12 | Debe probarse resolución de dependencias y wheels | POC pendiente |
| DataFrame | Polars | Instalación oficial mediante pip; extras opcionales para PyArrow/NumPy/SQLAlchemy | Comparar memoria/tiempo y compatibilidad de operaciones | POC pendiente |
| Compatibilidad tabular | pandas | Amplia interoperabilidad; usado por dependencias científicas | Evitar duplicar pipelines y copias de memoria | Evaluar necesidad |
| API | FastAPI | Framework Python candidato; requiere pruebas de auth, contratos y despliegue | No hay prueba del patrón modular en CPIE | POC pendiente |
| Base transaccional | PostgreSQL 18.x | Versión 18 soportada; documentación 18.6 vigente al corte | Validar instalador/imagen, migraciones y restore | POC pendiente |
| Analítica | Parquet + PyArrow | Formato/stack candidato interoperable | Validar particionamiento, schema evolution y lectura point-in-time | POC pendiente |
| Econometría | statsmodels + arch | statsmodels 0.15 documenta soporte Python 3.10–3.15 | Verificar wheels Windows y compatibilidad conjunta | POC pendiente |
| ML clásico | scikit-learn + XGBoost | Instalación oficial scikit-learn en Windows; XGBoost publica wheels Windows | Comparar LightGBM y probar artefactos reproducibles | POC pendiente |
| Deep Learning | PyTorch CPU | Instalación oficial Windows; Python 3.9–3.12 según guía consultada | No se conoce GPU; consumo RAM/tiempo por medir | POC pendiente |
| Experiment tracking | MLflow | Tracking local con SQLite y artefactos locales; PostgreSQL para backend compartido | Evaluar consumo, seguridad y migración | POC pendiente |
| Web | Next.js + TypeScript | Next.js admite Windows y Node.js >=20.9 | Verificar integración con API y rendimiento | POC pendiente |
| Mobile | React Native + Expo | React Native documenta Windows/Android; Mac requerido para build iOS local; EAS ofrece build cloud | Dependencia de Expo/EAS, coste y flujo iOS | POC pendiente |
| Contenedores | Docker Compose + WSL2 | Docker documenta WSL2 y requisitos de Windows 11; mínimo 8 GB RAM para WSL2 | Con 16 GB no ejecutar todos los servicios pesados juntos | POC pendiente |
| Observabilidad | OpenTelemetry + backend por seleccionar | Estándar candidato de instrumentación | Elegir backend según despliegue y retención | Diferido |

## 3. Recomendación provisional

La combinación con mejor justificación inicial para someter a POC es:

- Backend y ciencia de datos: Python 3.12.x.
- Procesamiento: Polars, con pandas solo donde la interoperabilidad lo exija.
- API: FastAPI.
- Persistencia transaccional: PostgreSQL 18.x.
- Datos analíticos: Parquet/PyArrow y almacenamiento de objetos detrás de interfaz.
- Modelos: statsmodels/arch, scikit-learn, XGBoost y PyTorch CPU.
- Tracking: MLflow local.
- Web: Next.js + TypeScript.
- Android/iOS: React Native + Expo, con EAS para build iOS desde Windows.
- Desarrollo local: Docker Compose/WSL2 con servicios mínimos.

Esto es una **shortlist**, no stack aprobado. No hay pruebas en el equipo objetivo ni mediciones. El orden de POCs debe comenzar por el entorno Python (riesgo de compatibilidad), después persistencia/procesamiento y finalmente API/clientes.

## 4. Versiones y mantenimiento

No se fijan versiones exactas de dependencias en este documento. Al superar las POCs:
- fijar versiones compatibles en lockfiles;
- declarar versiones runtime de Python y Node;
- mantener hashes/artefactos reproducibles;
- usar actualizaciones de seguridad y ventanas de mantenimiento;
- probar upgrades en branch/CI antes de promoverlos;
- mantener una matriz de compatibilidad runtime × sistema operativo × librerías críticas;
- revisar licencias y avisos de seguridad en cada release.

Python 3.12.x es el primer candidato, no una imposición permanente: reevaluar cuando PyTorch y el resto del stack tengan una intersección de soporte Windows demostrada.

## 5. Decisiones explícitamente aplazadas

- Kubernetes, Kafka, Redis y TimescaleDB.
- Proveedor cloud y object storage remoto.
- GPU/CUDA y entrenamiento distribuido.
- Backend de observabilidad.
- Proveedor de autenticación.
- Proveedor de CI y despliegue.
- Versiones exactas de librerías y runtimes.

Cada aplazamiento debe resolverse por requisito y evidencia, no por preferencia de moda.

## 6. Fuentes oficiales

- Python: https://docs.python.org/3/using/windows.html
- PyTorch: https://docs.pytorch.org/get-started/locally/
- Polars: https://docs.pola.rs/user-guide/installation/
- scikit-learn: https://scikit-learn.org/stable/install
- XGBoost: https://xgboost.readthedocs.io/en/stable/install.html
- PostgreSQL releases: https://www.postgresql.org/support/versioning/
- statsmodels: https://www.statsmodels.org/dev/install.html
- MLflow: https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/
- Next.js: https://nextjs.org/docs/app/getting-started/installation
- React Native: https://reactnative.dev/docs/set-up-your-environment
- Expo EAS: https://docs.expo.dev/build/
- Docker Desktop: https://docs.docker.com/desktop/features/wsl/

## 7. Estado de aceptación

- [x] Shortlist por dominio documentada.
- [x] Restricciones críticas de compatibilidad identificadas documentalmente.
- [x] Tecnologías diferidas y motivos documentados.
- [ ] POCs reproducibles ejecutadas en Windows 11 objetivo.
- [ ] Resultados de compatibilidad, rendimiento y RAM registrados.
- [ ] Licencias revisadas para dependencias seleccionadas.
- [ ] Versiones y políticas de actualización fijadas.
- [ ] ADR convertido a Aceptado con evidencia.


---

## 8. Política `latest-stable-first` y matriz de compatibilidad (2026-11-10)

Se adopta la política descrita en ADR-0002: evaluar primero la versión estable upstream más reciente, pero no aprobarla automáticamente. La **Validated Baseline** será una combinación exacta que haya superado POCs y controles; no equivale a la lista de releases más recientes.

### Corrección de la recomendación de Python

La recomendación anterior de Python 3.12.x como runtime inicial general queda sustituida. Python 3.15.2 es la última versión estable identificada en el corte y será la primera línea de evaluación general. Sin embargo, PyTorch documenta actualmente soporte de Python 3.9–3.12 en Windows. Por tanto, Python 3.12.x se mantiene únicamente como compatibility lane para la POC de PyTorch Windows. La viabilidad de separar entornos/procesos y compartir contratos/datasets se debe probar; no se asume resuelta.

### Candidatos al corte

| Tecnología | Candidato estable | Alternativa | Evidencia/limitación | Estado CPIE |
|---|---|---|---|---|
| Python | 3.15.2 | 3.12.x para PyTorch Windows | Python.org identifica 3.15.2 como último Python 3 estable; PyTorch Windows documenta 3.9–3.12 | No probado |
| Node.js | 26.13.0 LTS | 24.22.2 LTS | Releases oficiales identifican ambas como LTS | No probado |
| PostgreSQL | 18.6 | Otra major soportada si hay bloqueo de compatibilidad | Release notes oficiales de 18.6; revisar nuevo ciclo menor anunciado para 12-Nov-2026 | No probado |
| PyTorch | Stable del selector oficial | CPU primero; GPU solo con hardware/POC que lo justifique | Capturar la versión exacta generada por el selector al ejecutar la POC; Windows documenta Python 3.9–3.12 | No probado |
| Resto de librerías y frameworks | Última versión estable upstream al inicio de cada POC | Última línea soportada compatible | Registrar versión exacta, rango Python/Node, wheels, OS, licencia y fuente | No verificado |

La matriz detallada, con campos de evidencia y estado, se mantiene en [Version Compatibility Matrix](version-compatibility-matrix.md). No se declaran versiones instaladas, pruebas superadas ni compatibilidad efectiva a partir de la documentación solamente.

### Procedimiento obligatorio de actualización

1. Consultar el canal oficial de releases y descartar pre-releases.
2. Registrar versión, fecha, URL, soporte vigente, licencia y advisories relevantes.
3. Resolver compatibilidad transitiva y disponibilidad de wheels/binarios para Windows 11 x64.
4. Ejecutar pruebas aisladas y luego integración con fixtures reproducibles.
5. Medir RAM, tiempo, almacenamiento y coste en condiciones documentadas; no inventar umbrales.
6. Fijar versiones y hashes solo para la combinación probada; mantener lockfiles separados si existen lanes incompatibles.
7. Promover a Validated Baseline únicamente con evidencia y revisión; documentar rollback y excepciones.

### Estado

La política queda documentada, pero la shortlist continúa provisional. No se han ejecutado POCs en el equipo Windows objetivo, no se han medido recursos y no se han aprobado versiones finales. Los checks de aceptación de la sección 7 que dependan de pruebas siguen pendientes.
