# CPIE mobile framework POCs

Two independent prototypes compare React Native + Expo with Flutter. Neither is a selected production stack.

## Canonical fixture

The canonical fixture and JSON Schema remain in `poc/frontend/shared` (introduced by PR #97). Do not edit generated copies. From the repository root, run:

```powershell
node .\scripts\sync_mobile_fixtures.mjs
node .\scripts\sync_mobile_fixtures.mjs --check
```

The sync script copies the canonical fixture and schema into both app asset directories and verifies SHA-256 equality. Generated copies are gitignored. The build must fail if the sync or hash check fails.

## React Native + Expo

Candidate versions at the 2026-11-12 cut: Expo SDK 58.0.23, React Native 0.88.1, React 19.3.0, Ajv 8.20.0, TypeScript 7.0.2, Node.js 26.13.1. Expo's SDK reference maps SDK 58 to RN 0.88 / React 19.3 and requires Node.js 22.13.x or newer.

```powershell
cd .\poc\mobile\react-native
npm install
npm run typecheck
npm test
npx expo-doctor
npm run android
```

For iOS, a local native build requires macOS/Xcode. EAS Build can produce Android/iOS artifacts in cloud infrastructure; account, credentials, project configuration, service terms, cost and build quota must be evaluated before relying on it.

## Flutter

Candidate version at the 2026-11-12 cut: Flutter 3.50.0 with Dart 3.14.0. Flutter 3.50 requires Java 17 minimum for its default Android toolchain; the exact installed Android Studio, SDK, AGP, Gradle and NDK versions must be captured by the POC.

```powershell
cd .\poc\mobile\flutter
flutter pub get
flutter analyze
flutter test
flutter build apk
```

Flutter Android development is supported on Windows. Flutter iOS builds require macOS/Xcode; plan a macOS CI runner or other authorized macOS build host. Do not claim that Flutter can compile iOS locally on Windows.

## Common scenarios

Both prototypes expose the same seven fixture scenarios: overview, valid research range, invalid range, partial data, not available, recoverable error/retry, and evaluation comparison. They use only synthetic fixture data. The "mark evaluation" action is in-memory only and explicitly not persisted.

## Evidence gates

Record separately for each framework and exact toolchain:
- Clean dependency resolution, lockfile, integrity hashes and package/license inventory.
- Static analysis, unit/widget tests and production Android build.
- iOS build on macOS/Xcode, install/run tests on iOS simulator and (where available) physical device.
- Equivalent scenario checks, screen reader semantics, text scaling, contrast and touch target review.
- APK/AAB/IPA size, cold start, memory/CPU, frame behavior and offline behavior on the same device/OS/browser/build mode.
- CI logs, artifacts, SHA-256, commit, OS image and tool versions.

No thresholds or weighted score are preselected. No build, runtime, device test, performance result, license approval or framework selection is claimed by this scaffolding.
