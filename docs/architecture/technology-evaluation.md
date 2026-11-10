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
