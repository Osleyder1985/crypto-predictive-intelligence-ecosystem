# Protocolo de POC para selección de clientes web y móviles

- **Estado:** protocolo propuesto; ninguna tecnología cliente queda aprobada por este documento.
- **Fecha de corte:** 2026-11-12.
- **Issue propietario:** #5.
- **Relacionado:** #52, #55, #66; PR #94 y PR #95.
- **Entorno de desarrollo:** Windows 11 x64, 16 GB RAM, equipo CPIE registrado en Issue #5.

## 1. Decisión que debe producir la POC

Seleccionar por separado:
1. La arquitectura del cliente web: Next.js o React SPA.
2. La tecnología móvil: React Native + Expo o Flutter.
3. La estrategia de contratos y componentes compartidos sin duplicar reglas de dominio.

No se presupone que un único framework tenga que cubrir las tres plataformas. Se evaluará coste total de ciclo de vida, mantenibilidad, accesibilidad, rendimiento, integración con API, builds, distribución y dependencia de proveedor.

## 2. Actualización de evidencia upstream

Al 2026-11-12, el calendario oficial de Node.js muestra:
- Node.js 26: Active LTS desde 2026-10-28, EOL previsto 2029-04-30.
- Node.js 24: Maintenance LTS desde 2026-10-20, EOL previsto 2028-04-30.
- Node.js 27: Alpha, no apto para baseline de producción.

Por política latest-stable-first, Node.js 26 LTS es el primer candidato a evaluar. Node.js 24 LTS queda como alternativa de compatibilidad. La versión exacta instalada y el soporte efectivo de cada versión de Next.js, React Native, Expo y dependencias deben quedar registrados en la ejecución; la etiqueta LTS por sí sola no demuestra compatibilidad.

Next.js documenta Windows (incluido WSL) y mínimo Node.js 20.9. React Native documenta Windows para Android, exige Node 22.11 o posterior y requiere macOS/Xcode para builds iOS nativos locales. Expo EAS permite builds cloud para iOS y Android; su plan Free publica una cuota mensual limitada (actualmente 15 builds Android y 15 iOS), con colas de baja prioridad. Los límites y precios son variables y deben reconsultarse antes de decidir dependencia de producción.

Flutter documenta SDK multiplataforma para Android, iOS y web. La compilación/distribución iOS debe probarse con el flujo oficial disponible y los requisitos Apple vigentes; no inferir que Windows elimina la dependencia de macOS para compilar código iOS nativo.

Fuentes oficiales consultadas:
- https://nodejs.org/en/about/previous-releases
- https://nextjs.org/docs/app/getting-started/installation
- https://reactnative.dev/docs/set-up-your-environment
- https://docs.expo.dev/build/
- https://expo.dev/pricing
- https://docs.flutter.dev/install

## 3. Matriz de alternativas

| Dimensión | Next.js + TypeScript | React SPA + TypeScript | React Native + Expo | Flutter |
|---|---|---|---|---|
| Plataforma primaria | Web | Web | Android/iOS; web posible según alcance | Android/iOS/web |
| Modelo UI | React + App Router/SSR/Server Components según uso | React client-side; SSR requiere solución adicional | React Native; componentes nativos | Widgets y Dart |
| Reutilización con web | Alta con React, pero no implica reutilizar componentes DOM en móvil | Alta con React web, no reutiliza directamente UI nativa | Comparte lógica/contratos con React web; UI nativa separada | Un solo toolkit UI entre targets, con adaptaciones por plataforma |
| SEO/renderizado servidor | Capacidad integrada | Requiere arquitectura adicional si es necesario | No aplica a app nativa | Flutter web no sustituye automáticamente una web SEO-first |
| Integración API | HTTP/typed clients | HTTP/typed clients | HTTP/typed clients | HTTP/typed clients |
| Windows 11 | Soportado | Soportado | Android soportado con toolchain | Desarrollo Windows soportado |
| Build iOS | No aplica | No aplica | EAS cloud o macOS/Xcode | Debe validar flujo macOS/Xcode para build iOS |
| Riesgo principal | Complejidad innecesaria si CPIE no necesita SSR; modelo server/client | Añadir SSR/SEO más adelante puede requerir re-arquitectura | Diferencias web/native y dependencia opcional de EAS | Dart y ecosistema separado de TypeScript; integración de componentes web |
| POC obligatoria | Rutas, layouts, accesibilidad, consumo API, build producción | Mismas rutas y escenarios, bundle/build y routing | Android físico/emulador, navegación, deep links, build iOS cloud | Android, web, navegación, accesibilidad y ruta de build iOS |

No asignar puntuaciones subjetivas de “mejor” sin ejecutar el mismo alcance y recoger evidencia comparable.

## 4. Prototipo común obligatorio

Implementar el mismo flujo funcional mínimo definido en PR #95:
1. Overview con banner DEMO.
2. Navegar a nueva investigación.
3. Seleccionar BTC, instrumento sintético y rango de fechas.
4. Validar campos y mostrar estados de carga/error.
5. Mostrar estado de datos SIMULATED y limitaciones.
6. Mostrar resultado sintético, evidencia y sección NOT_AVAILABLE.
7. Abrir historial y comparar dos evaluaciones sintéticas.
8. Navegación atrás, recarga y deep link donde aplique.

Todos los fixtures deben ser deterministas y estar marcados DEMO — DATOS SINTÉTICOS. No conectar exchanges, no usar datos de mercado actuales y no crear API ficticia. Se puede usar un adaptador local de fixtures con interfaz reemplazable por el contrato API futuro.

## 5. Criterios y evidencias que recoger

| Área | Evidencia requerida |
|---|---|
| Instalación | Versiones exactas de runtimes, SDK, IDE, dependencias y comandos |
| Reproducibilidad | Lockfile, hashes cuando el gestor lo soporte, build limpio desde checkout |
| Funcionalidad | Mismos casos de navegación, validación, errores, empty/partial/simulated |
| Accesibilidad | Teclado, foco, lector de pantalla, escalado, contraste y semántica |
| Rendimiento | Build/dev startup, navegación, tamaño artefacto y mediciones repetidas con método declarado |
| Recursos | RAM/CPU/disco en reposo y durante build/emulador; no fijar umbrales sin requisito |
| Compatibilidad | Windows 11; navegador; Android físico/emulador; iOS simulator/build cloud cuando sea posible |
| Integración | Cliente API tipado, errores HTTP, cancelación, timeout y no duplicar reglas de dominio |
| Mantenimiento | Complejidad de toolchain, frecuencia de upgrades, disponibilidad de librerías y soporte |
| Seguridad | Dependencias, advisories, permisos, almacenamiento local, secrets y SBOM |
| Licencias | Dependencias directas y transitivas, obligaciones y uso previsto |
| Coste | Coste actual y escenarios de builds, distribución, CI, cuentas Apple/Google y salida del proveedor |

No usar un único tiempo de build como benchmark. Registrar entorno, caché fría/caliente, número de repeticiones, mediana y dispersión cuando la muestra lo permita. Separar tiempos de descarga de tiempos de compilación.

## 6. Diseño de las POCs

### POC-WEB-01

Construir el mismo prototipo en:
- Next.js + TypeScript.
- React SPA + TypeScript (Vite u opción estable equivalente, versión exacta registrada).

Probar rutas, layout responsive, carga/error/empty states, formularios, accesibilidad, build de producción y cliente API de fixture.

### POC-MOBILE-01

Construir el mismo prototipo en:
- React Native + Expo.
- Flutter.

Probar navegación, listas, formularios, estados, accesibilidad, orientación/tamaños, persistencia local solo de demo, deep links y build Android. Para iOS, documentar y ejecutar el camino viable desde Windows (EAS u otro servicio aprobado), registrar cuenta/certificados requeridos, coste, cola, artefacto y posibilidad de reproducir el build.

### POC-INTEGRATION-01

Una vez comparados los clientes:
- Consumir un contrato OpenAPI de prueba versionado, no endpoint de producción inventado.
- Generar/verificar cliente tipado si procede.
- Probar compatibilidad de errores, nullability, fechas UTC, paginación y estados PARTIAL/NOT_AVAILABLE.
- Confirmar que los clientes no contienen cálculos de dominio ni autorización autoritativa.

## 7. Condiciones de ejecución en Windows 11 con 16 GB

- No ejecutar simultáneamente dos emuladores ni todos los servicios Docker.
- Registrar RAM disponible antes, durante y después; pico muestreado y método de muestreo.
- Medir por separado build web, build Android y ejecución del emulador.
- Preferir Android físico cuando esté disponible para reducir consumo de emulador; documentar dispositivo y versión.
- Mantener cada POC aislada en su propia rama/directorio y lockfile.
- No instalar toolchains completos de todas las alternativas en paralelo sin medir el espacio y RAM.
- iOS no se considerará validado solo por compilar la web o por mostrar una vista en Expo Go.

## 8. Regla de evaluación y selección

Primero aplicar gates eliminatorios:
- No puede completar el flujo funcional común.
- No tiene un camino viable y reproducible para una plataforma objetivo.
- Accesibilidad esencial no alcanzable sin rediseño desproporcionado.
- Dependencias o licencias incompatibles con el uso previsto.
- Reproducibilidad/actualización no controlables.
- Dependencia de proveedor sin coste, límites y plan de salida aceptables.

Después comparar las opciones que superen gates mediante criterios ponderados, pero los pesos deben acordarse y justificarse con requisitos antes de puntuar. No inventar pesos ni umbrales en este protocolo.

La decisión final debe incluir:
- Combinación seleccionada y versiones exactas.
- Alternativas rechazadas y evidencia de rechazo.
- Limitaciones conocidas y deuda aceptada.
- Coste inicial y recurrente estimado con fuentes/fecha.
- Plan de actualización, rollback y salida de servicios.
- ADR aprobado mediante PR y matriz de compatibilidad actualizada.

## 9. Estado actual y trabajo no realizado

- POCs Python cuantitativas previas no validan Next.js, React SPA, React Native, Expo ni Flutter.
- No hay evidencia aportada aquí de build CPIE web/Android/iOS para ninguna de estas cuatro alternativas.
- No se ejecutaron comandos en el PC del usuario durante este trabajo.
- No se declara una tecnología seleccionada ni una Validated Baseline.
- Issue #5 permanece abierto hasta cumplir los criterios globales, incluidos licencias, lockfiles, seguridad e integración.

## 10. Criterios de aceptación de este protocolo

- [ ] El mismo alcance y fixtures se ejecutan en las cuatro alternativas relevantes.
- [ ] Versiones exactas y fuentes oficiales quedan registradas.
- [ ] Web y Android se prueban en Windows 11 objetivo.
- [ ] El camino de build iOS se demuestra y sus dependencias/costes se documentan.
- [ ] Evidencia de accesibilidad y rendimiento comparable.
- [ ] Licencias directas/transitivas y seguridad revisadas.
- [ ] Lockfiles y builds reproducibles.
- [ ] Criterios/pesos de selección aprobados antes de puntuar.
- [ ] ADR de decisión presentado en PR separado o claramente versionado.
