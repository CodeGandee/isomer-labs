# Package Check Playbook

Use this reference to verify package, solver, executable, module, container, backend, license, or environment availability before computed work. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Separate package knowledge from availability**. Use package cards and domain index only to choose likely tools and checks.
2. **Check import or executable existence**. Verify Python import, CLI executable, module, container, solver, service, or library path as appropriate.
3. **Capture version and backend details**. Record package version, executable version, accelerator backend, MPI/OpenMP state, module state, license state, and environment facts that affect validity.
4. **Run a minimal smoke test when available**. Use a tiny package-specific example, dry run, input parse, or versioned self-check that does not pretend to be final science.
5. **Save a durable diagnostic**. Store <SCIENCE_PACKAGE_CHECK> evidence with status passed, failed, or blocked and diagnostic paths.
6. **Interpret status conservatively**. Passed means the current environment can run at least the smoke path; failed means attempted and did not work; blocked means required credentials, data, module, license, network, allocation, or confirmation are missing.

## Preferences

- Prefer the smallest smoke path that proves route viability (if the solver has no smoke path, otherwise record version and executable/import evidence).
- Prefer recording failed and blocked checks when they determine the route.
- Prefer environment facts that affect scientific validity over incidental setup noise.

## Constraints

- <SCIENCE_PACKAGE_CHECK> must precede computed work when availability matters.
- Package cards must not be treated as install, import, executable, license, or backend proof.
- A passed import alone should not imply solver correctness when a smoke test is available and relevant.
- Failed or blocked checks must include diagnostic evidence when they affect the route.

## Quality Gates

### Metrics

- Package-check step coverage: fraction of import or executable check, version/backend capture, smoke test, durable result file, and science.package_check node steps completed or explicitly blocked; higher is better.
- Blocked-check count: number of package checks blocked by missing credentials, data, modules, licenses, hardware, or unsupported runtime paths; lower is better.

### Checks

- Availability gate: import, executable, module, container, service, or solver path is checked.
- Version gate: version and backend details are recorded when relevant.
- Smoke gate: minimal test is run or explicitly unavailable.
- Diagnostic gate: evidence path exists for passed, failed, or blocked status.
- Route gate: package status supports proceed, repair, install/setup request, blocker, or alternate package route.
