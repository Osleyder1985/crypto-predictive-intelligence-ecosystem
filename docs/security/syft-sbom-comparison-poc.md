# Syft SBOM comparison POC

- Issue: #86
- Branch: poc/issue-86-syft-sbom-comparison
- Candidate: Anchore Syft 1.57.1, Windows x86_64
- Target: the existing clean CPython 3.12.10 workload environment at %TEMP%\cpie-uv-312-clean2.
- Purpose: independently inventory the installed environment and compare package coverage with the CycloneDX Python SBOM from the same target environment.
- Status: design and reproducible local procedure only; Syft has not yet been downloaded, signature-verified, executed or compared.

## Why Syft is complementary

CycloneDX Python inspects Python distribution metadata in an installed interpreter. Syft scans a filesystem and supports Python and other package ecosystems, plus file/binary catalogers. This gives an independent discovery path and may expose additional components or evidence. It does not guarantee that every native library or operating-system component is detected.

The comparison must use the **same unchanged target environment** as the CycloneDX Python run. Do not compare the Syft result to a different or subsequently modified virtual environment.

## Pinned Windows release and artifact verification

Use the exact release archive:

- syft_1.57.1_windows_amd64.zip
- syft_1.57.1_checksums.txt
- syft_1.57.1_checksums.txt.sigstore.json

Official release assets are published by [Anchore Syft](https://github.com/anchore/syft/releases/tag/v1.57.1). Anchore documents that the checksum file is signed using Sigstore; Syft releases from v1.54.0 use a Sigstore bundle. Verification of this bundle requires Cosign 2.5.0 or newer. See [Anchore download verification](https://oss.anchore.com/docs/installation/verification/).

Do not run the binary unless:
1. Cosign verifies the checksum file's Sigstore bundle against the Anchore Syft GitHub Actions identity and GitHub OIDC issuer.
2. The downloaded Windows archive SHA-256 matches the entry in the signed checksum file.
3. The extracted executable reports version 1.57.1.

## PowerShell procedure

Run from the repository root. The commands keep the downloaded executable, SBOM outputs and logs under %TEMP%; they do not install Syft system-wide or modify the workload environment.

~~~powershell
$ErrorActionPreference = "Stop"

$version = "1.57.1"
$work = Join-Path $env:TEMP "cpie-syft-1.57.1"
$targetEnv = Join-Path $env:TEMP "cpie-uv-312-clean2"
$archiveName = "syft_$($version)_windows_amd64.zip"
$checksumsName = "syft_$($version)_checksums.txt"
$bundleName = "syft_$($version)_checksums.txt.sigstore.json"

New-Item -ItemType Directory -Force $work | Out-Null

$archive = Join-Path $work $archiveName
$checksums = Join-Path $work $checksumsName
$bundle = Join-Path $work $bundleName
$baseUrl = "https://github.com/anchore/syft/releases/download/v$version"

Invoke-WebRequest "$baseUrl/$archiveName" -OutFile $archive
Invoke-WebRequest "$baseUrl/$checksumsName" -OutFile $checksums
Invoke-WebRequest "$baseUrl/$bundleName" -OutFile $bundle

$cosign = Get-Command cosign -ErrorAction SilentlyContinue
if (-not $cosign) {
    throw "Cosign is required for Sigstore verification. Install/verify Cosign >= 2.5.0, then rerun this procedure."
}

$cosignVersion = (& cosign version 2>&1 | Out-String)
$cosignVersion

$versionMatch = [regex]::Match($cosignVersion, "(?m)\b(?:v)?(\d+)\.(\d+)\.(\d+)\b")
if (-not $versionMatch) {
    throw "Could not determine Cosign version"
}
$cosignDetected = [version]::Parse("$($versionMatch.Groups[1].Value).$($versionMatch.Groups[2].Value).$($versionMatch.Groups[3].Value)")
if ($cosignDetected -lt [version]"2.5.0") {
    throw "Cosign >= 2.5.0 is required for Sigstore bundle verification"
}

& cosign verify-blob $checksums --bundle $bundle --certificate-identity-regexp 'https://github\.com/anchore/syft/\.github/workflows/.+' --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
if ($LASTEXITCODE -ne 0) {
    throw "Syft checksums signature verification failed"
}

$checksumLine = Get-Content $checksums | Where-Object { $_ -match "\s+$([regex]::Escape($archiveName))$" } | Select-Object -First 1
if (-not $checksumLine) {
    throw "The signed checksum file does not contain $archiveName"
}

$expectedHash = ($checksumLine.Trim() -split "\s+")[0].ToLowerInvariant()
$actualHash = (Get-FileHash $archive -Algorithm SHA256).Hash.ToLowerInvariant()
"EXPECTED SHA256: $expectedHash"
"ACTUAL SHA256:   $actualHash"

if ($actualHash -ne $expectedHash) {
    throw "Syft archive checksum mismatch"
}

$extract = Join-Path $work "extracted"
Expand-Archive -LiteralPath $archive -DestinationPath $extract -Force
$syft = Join-Path $extract "syft.exe"
if (-not (Test-Path $syft)) {
    throw "syft.exe not found in the expected archive root"
}

$versionOutput = (& $syft version 2>&1 | Out-String)
$versionOutput
if ($versionOutput -notmatch "1\.57\.1") {
    throw "Unexpected Syft version"
}

if (-not (Test-Path (Join-Path $targetEnv "Scripts\python.exe"))) {
    throw "The clean CPython 3.12 target environment is missing"
}

$outputDir = Join-Path $work "results"
New-Item -ItemType Directory -Force $outputDir | Out-Null
$native = Join-Path $outputDir "python-312-syft-native.json"
$cyclonedx = Join-Path $outputDir "python-312-syft.cdx.json"

& $syft scan $targetEnv -o "json=$native" -o "cyclonedx-json@1.6=$cyclonedx"
if ($LASTEXITCODE -ne 0) {
    throw "Syft scan failed"
}

Get-FileHash $native, $cyclonedx -Algorithm SHA256
~~~

If the release archive's internal layout differs and syft.exe is not at the archive root, inspect the extracted file list and select the actual executable path; do not download a different version to work around it.

## Evidence to return

Record:
- Windows version/build and target interpreter version.
- Cosign version and successful signature-verification result.
- Expected and actual archive SHA-256.
- Syft version output.
- Syft native JSON and CycloneDX JSON SHA-256.
- Package counts by Syft package type and total cataloged packages.
- The exact scan target path and whether the target environment changed after the CycloneDX Python generation.

Keep generated JSON under the work directory initially. Do not commit raw SBOMs until the repository artifact-retention policy is decided.

## Comparison method — no count-only acceptance

Compare CycloneDX Python and Syft results using normalized package coordinates:
1. Prefer Package URL (PURL) when both tools provide it.
2. Otherwise use normalized ecosystem/type + package name + version.
3. Preserve architecture, qualifiers and namespace where present; do not collapse distinct packages with the same name/version.
4. Classify each result as shared, CycloneDX-Python-only, or Syft-only.
5. Investigate every material discrepancy, especially PyTorch, SciPy, Polars runtime, PyArrow and native DLLs.
6. Treat missing license metadata, ambiguous license expressions and file-level notices as separate findings; do not infer legal clearance from package counts.

The comparison script is deliberately deferred until the actual Syft JSON schema and output from the pinned binary have been inspected. Do not invent a parser from expected output.

## Acceptance criteria

- [ ] Downloaded exact Syft 1.57.1 Windows x64 release.
- [ ] Verified signed checksums with Cosign >= 2.5.0.
- [ ] Verified archive SHA-256 against the signed checksum file.
- [ ] Confirmed executable version 1.57.1.
- [ ] Scanned the unchanged CPython 3.12.10 target environment.
- [ ] Preserved native Syft JSON and CycloneDX 1.6 output hashes.
- [ ] Compared normalized package coordinates and investigated discrepancies.
- [ ] Assessed native/bundled library coverage and license-notice limitations.

## Limitations

- This POC is not a vulnerability scan; Grype/OSV/pip-audit are separate work.
- Syft output is not proof of complete discovery.
- Package-level license metadata is not a complete third-party notice inventory.
- A matching component count does not prove matching coverage.
- No production approval, baseline approval or legal clearance is implied.
