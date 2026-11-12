# Web frontend framework POCs

**Status:** experimental; no framework selected and no validated baseline.
**Related:** Issue #5, PR #95, PR #96, PR #97.

## Implementations

- `poc/frontend/next-app`: Next.js App Router + React + TypeScript.
- `poc/frontend/react-spa`: Vite + React SPA + TypeScript.
- Both import the exact same JSON fixture and Draft 2020-12 schema from `poc/frontend/shared`; neither maintains a private fixture copy.
- Both validate the fixture at startup with Ajv before rendering.
- Both implement the same navigation and observable scenarios: overview, valid/invalid research range, PARTIAL data quality, NOT_AVAILABLE capabilities, recoverable ERROR/retry, evaluation comparison, and a clearly non-persistent local save affordance.

## Candidate versions captured for this POC

| Component | Exact candidate |
|---|---:|
| Node.js | 26.13.1 LTS (runtime to verify locally/CI) |
| React / React DOM | 19.3.1 |
| Next.js | 16.4.6 |
| Vite | 8.3.8 |
| @vitejs/plugin-react | 6.3.0 |
| TypeScript | 7.0.2 |
| Ajv | 8.17.1 |
| React type packages | 19.3.0 |

Versions are pinned in the two package manifests as candidates. A package manifest is not a lockfile; exact transitive resolution, integrity hashes, clean install, peer dependency resolution, and compatibility are not yet established.

## Local commands

Run each application from its own directory after Node.js 26.13.1 is available:

```powershell
npm install
npm run typecheck
npm run build
npm run dev
```

Do not run both builds concurrently on the 16 GB Windows target. Record the generated lockfile and retain it in the same PR after reviewing its contents. Do not use `npm install --package-lock-only` as a substitute for a successful clean installation/build.

## Known limitations

- No backend, API, authentication, server-side persistence, real market data, or trading capability.
- The save action only updates in-memory UI state and explicitly says it is not persisted.
- The error/retry scenario is deterministic and local; retry does not call a remote service.
- No automated browser E2E, accessibility audit, bundle analysis, performance/RAM profile, SBOM, license audit, or security scan has run.
- No package lockfiles have been generated or validated in this environment.
- `.github/workflows/web-frontend-poc.yml` defines a two-app Node.js 26.13.1 CI matrix, uses GitHub Actions pinned to full commit SHAs, generates a lockfile, performs `npm ci`, typechecks, builds, and uploads artifacts. Because the workflow itself is introduced by this PR and its base branch does not yet contain it, no run is currently triggered for this draft PR; activation requires the workflow to reach the default branch.
- The Next.js and Vite builds, TypeScript checks, and runtime interaction checks remain pending in CI and on the target Windows 11 machine.

## Comparison gates

Use identical browser version, viewport, fixture/schema commit, interaction sequence, and clean machine state. Record separately: clean install, dependency resolution, typecheck, production build, route/interaction behavior, accessibility, emitted artifact size, cold start, memory/CPU, and maintenance/security posture. Do not assign scores or thresholds until the applicable requirements define them.

## Current decision

**No selection.** These are implementation candidates only. Neither is a production application nor a validated baseline. PR remains draft until lockfiles, checks, and evidence are reviewed.
