# CPIE mobile framework POC protocol

- **Issue:** #99
- **Decision owner:** Issue #5 / ADR-0002
- **Status:** implementation candidate; no validated baseline
- **Cut-off:** 2026-11-12
- **Target development environment:** Windows 11 x64, 16 GB RAM
- **Platforms:** Android and iOS

## 1. Alternatives and exact stable candidates

| Dimension | React Native + Expo | Flutter |
|---|---|---|
| Framework candidate | React Native 0.88.1 | Flutter 3.50.0 |
| App framework/tooling | Expo SDK 58.0.23 | Flutter SDK 3.50.0 |
| UI language | TypeScript/JavaScript + React | Dart 3.14.0 |
| React/runtime | React 19.3.0 | Not applicable |
| Node runtime | Node 26.13.1 candidate; Expo SDK 58 minimum Node 22.13.x | Not required by Flutter SDK |
| Android development on Windows | Supported; Android Studio, SDK, JDK 17 | Supported; Android Studio, SDK, Java 17 minimum |
| iOS native build on Windows | Not local; macOS/Xcode required, or EAS cloud build | Not local; macOS/Xcode required, or a macOS CI/build host |
| Native integration | React Native native modules / Expo config plugins | Flutter plugins, FFI/JNI direct interop (Flutter 3.50 stable) |
| Web reuse | React concepts and TypeScript shared with Next.js web POC; UI components are not automatically shared | Same Dart/Flutter UI can target web, but it is a separate frontend technology from the Next.js POC |
| Fixture integration | Generated JSON assets imported by Metro; Ajv Draft 2020-12 validation | Generated JSON assets loaded with rootBundle; schema_engine Draft 2020-12 validation |

Expo SDK and React Native patch candidates were cross-checked against the npm stable tags at the cut-off: Expo 58.0.23, React Native 0.88.1 and Ajv 8.20.0. Expo's compatibility table provides the SDK-level React Native/React mapping; `npx expo install --check` and clean dependency resolution must still verify the exact combination. Flutter 3.50.0 / Dart 3.14.0 are from the official release announcement. A release number does not establish CPIE compatibility. The final package graph, patch updates, Android toolchain, Xcode version and iOS deployment target must be captured by clean POC runs.

## 2. Source-backed platform constraints

- React Native's Windows setup documents Node 22.11+, JDK 17, Android Studio and Android SDK. React Native's iOS native toolchain requires Xcode on macOS.
- Expo SDK 58 documents React Native 0.88, React 19.3, minimum Node 22.13.x, Android 7+ and iOS 16.4+; its SDK table records the corresponding Xcode version.
- Expo EAS Build produces installable Android/iOS binaries in cloud build environments. This introduces a provider dependency, credential handling, terms, quotas and potentially cost; none is approved by this POC.
- Flutter Android setup is supported on Windows and documents Android Studio, SDK platform/API 36 and command-line/build tools.
- Flutter iOS setup requires Xcode and macOS. Flutter 3.50 pairs with Dart 3.14 and its default Android toolchain uses AGP 9.3.1, Gradle 9.5.0, Kotlin 2.4.20 and Java 17 minimum.
- Flutter 3.50 marks FFIgen/JNIgen native interop stable; use only if an actual CPIE native integration requirement justifies it.

Official references:
- React Native 0.88 release: https://reactnative.dev/blog/2026/10/19/react-native-0.88
- React Native release/support overview: https://reactnative.dev/releases/overview
- React Native Windows/Android/iOS setup: https://reactnative.dev/docs/set-up-your-environment
- Expo SDK 58 compatibility: https://docs.expo.dev/versions/latest/
- Expo 58.0.23 package release: https://www.npmjs.com/package/expo
- React Native 0.88.1 package release: https://www.npmjs.com/package/react-native
- Ajv 8.20.0 package release: https://www.npmjs.com/package/ajv
- schema_engine 1.0.0 package, API, supported dialects and MIT license: https://pub.dev/packages/schema_engine
- Expo EAS Build: https://docs.expo.dev/build/introduction/
- Flutter 3.50 release: https://flutter.dev/blog/whats-new-in-flutter-3-50
- Flutter SDK archive: https://docs.flutter.dev/install/archive
- Flutter Android setup: https://docs.flutter.dev/platform-integration/android/setup
- Flutter iOS setup: https://docs.flutter.dev/platform-integration/ios/setup

## 3. Comparable product slice

Both apps consume the same canonical synthetic JSON fixture from `poc/frontend/shared`; the JSON Schema is synchronized alongside it and SHA-256 checked. A deterministic sync script materializes platform-specific asset copies. React Native validates the fixture against Draft 2020-12 at runtime with Ajv 8.20.0. Flutter validates the same schema at load and test time with `schema_engine` 1.0.0 (Dart >=3.13, MIT, no runtime dependencies). The package is new and has limited adoption signals; its inclusion is experimental and must pass POC compatibility, security and license checks before any baseline decision. No app may maintain a manually edited fixture variant.

Required screens/states:
1. Overview with persistent synthetic/demo disclosure and BTC demo instrument.
2. Valid research period and explicit validation of invalid date range.
3. PARTIAL quality with missing interval and limitations.
4. NOT_AVAILABLE technical structure with reason.
5. Recoverable error and local retry; no network call.
6. Comparison of two synthetic evaluations with IDs/snapshots and no inferred market performance.
7. Local "mark evaluation" action explicitly identified as non-persistent.

No real market data, backend, API, authentication, durable storage, push notifications, background execution or trading.

## 4. Required measurements

For each framework, record the exact:
- SDK, runtime, package manager, direct/transitive dependency versions, lockfile and integrity hashes.
- Windows build, CPU/RAM, Android Studio, JDK, SDK/NDK, Gradle/AGP, emulator/device model and OS/API.
- macOS build, Xcode, CocoaPods/Swift Package Manager, iOS SDK/deployment target, simulator/device and signing setup.
- Install, static analysis, test, Android build, iOS build and runtime outcomes, including full logs and artifact hashes.
- APK/AAB/IPA size; cold-start method; memory/CPU sampling method; frame behavior; offline scenario behavior.
- Accessibility results for TalkBack/VoiceOver, dynamic text scaling, contrast, focus order, semantic labels and touch targets.
- SBOM, license/NOTICE inventory, vulnerability scan and exceptions.

Run frameworks sequentially on the 16 GB Windows machine. Do not compare debug build performance against release build performance. Use the same device, OS version, screen dimensions, fixture hash, scenario order and test procedure. Do not invent thresholds; derive them from product requirements or report observations without pass/fail thresholds.

## 5. Current implementation state

- React Native + Expo prototype source: `poc/mobile/react-native`.
- Flutter prototype source: `poc/mobile/flutter`.
- Fixture materialization/hash verification: `scripts/sync_mobile_fixtures.mjs`.
- Run instructions: `poc/mobile/README.md`.

This PR creates source scaffolding and CI definitions only. The workflow defines Linux Android checks/builds for pull requests and manual-only macOS iOS Simulator builds for both frameworks to avoid unexpected macOS runner charges. The workflow is not yet in the default branch, so neither path has run. No npm install, Flutter pub get, analyzer, unit/widget test, Android build, iOS build, device run, accessibility audit, performance profile, SBOM or license audit has been executed in this environment. The Flutter Draft 2020-12 validator dependency has not yet been resolved or tested against the CPIE fixture.

## 6. Decision gates

Do not select a framework until both implementations complete equivalent Android tests and an iOS build/test path. Compare:
- Functional parity and ability to implement the actual CPIE product slice.
- Developer workflow and fit with existing web/TypeScript expertise.
- Native capability and plugin dependency risks.
- Android/iOS build reproducibility and signing/release operations.
- App size, startup, memory/CPU, responsiveness and offline resilience.
- Accessibility, security, privacy, dependency maintenance and total cost.
- Web/backend contract reuse without forcing inappropriate UI code sharing.

**No framework selected.** React Native + Expo and Flutter remain POC candidates only.
