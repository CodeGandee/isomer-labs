## 1. Reconcile the Versioned-Receipt Foundation

- [ ] 1.1 Land or synchronize the `detect-versioned-system-extensions` predecessor so its OpenAI metadata versioning, receipt schema, compatibility rules, extension catalog, and idempotent `remember` primitive form the implementation baseline for this change.
- [ ] 1.2 Identify and replace predecessor behavior that scans default provider skill roots during Project initialization or treats detected state as stronger than an explicit Project declaration.

## 2. Add Internal Skill-Inspection Primitives

- [ ] 2.1 Add the `isomer-cli internals` command group and a read-only `inspect-system-skill-root` command that requires an explicit `--skill-root` and supports category, extension, and group filters.
- [ ] 2.2 Implement reusable explicit-root inspection that owns receipt discovery and schema parsing, accepts supported legacy receipts, resolves one-level directory and symlink projections, and reports broken links, invalid shapes, unmanaged matches, version state, and complete or partial families.
- [ ] 2.3 Add a read-only `classify-system-skill-inventory` command that accepts repeated skill names and versioned structured JSON input, maps only packaged catalog entries, and reports complete and partial extension families without filesystem discovery.
- [ ] 2.4 Define deterministic versioned JSON payloads for both internal commands using the standard CLI wrapper, `mutated: false`, explicit evidence bases, member sets, receipt or projection state where applicable, and stable diagnostics.
- [ ] 2.5 Add unit tests for explicit-root filtering, absent and legacy receipts, directory and symlink projections, broken or invalid projections, version diagnostics, inventory classification, partial families, malformed input, deterministic ordering, and the guarantee that neither command searches implicit roots.

## 3. Package the System-Skill Manager

- [ ] 3.1 Create the core `isomer-op-system-skill-mgr` source bundle with `detect-extensions`, `reconcile-extensions`, `install-extension`, `status`, and `repair` subcommands, plus release-aligned version metadata in `agents/openai.yaml`.
- [ ] 3.2 Document and implement the manager's declaration-first trust ladder: trust Project declarations, inspect receipts in host-supplied project roots, then classify the host-visible live inventory, while preserving the evidence basis in user-facing results.
- [ ] 3.3 Make manager reconciliation additive and idempotent by calling Project `remember` only for complete families during authorized mutation workflows, never calling `forget` for absence, and leaving detection-only and status workflows read-only.
- [ ] 3.4 Make the installation workflow use the operator host's own selected skill root, register a successfully installed complete extension, retry registration without reinstalling after partial failure, and report when a host refresh is required.
- [ ] 3.5 Add the manager to the core packaged-system-skill catalog, generated asset projection, indexes, documentation, and skillset validation coverage.

## 4. Integrate Operator Workflows

- [ ] 4.1 Update `isomer-op-entrypoint` routing so extension detection, reconciliation, installation, status, and repair delegate to `isomer-op-system-skill-mgr` without embedding provider path conventions.
- [ ] 4.2 Update `isomer-op-project-mgr init-project` to invoke manager reconciliation after successful direct Project initialization and to register complete receipt-backed or live-inventory families unless the user explicitly opts out.
- [ ] 4.3 Define operator guidance for declared-but-unavailable extensions, partial discovery, registration failure after installation, and newly installed skills that require a refreshed agent session.
- [ ] 4.4 Add skill-validation and workflow tests that cover declaration-first routing, project-root receipt fallback, live-inventory fallback, opt-out behavior, idempotent reruns, and non-destructive handling when different operators expose different inventories.

## 5. Restore Conservative Direct CLI Boundaries

- [ ] 5.1 Remove inferred extension declarations and hard-coded provider-root observations from direct `project init`, preserving Project creation and explicit user-supplied declarations.
- [ ] 5.2 Retain `project system-extensions detect` as a read-only explicit-root wrapper around the internal inspector, require at least one supplied root, and remove all default project, home, and provider root discovery from that command.
- [ ] 5.3 Keep low-level `system-skills` installation and Project `remember` or `forget` commands explicit and independent, with no implicit cross-command registration.
- [ ] 5.4 Update CLI unit tests to prove direct initialization, direct installation, and root inspection neither infer the active agent host nor mutate extension declarations without an explicit registration command.

## 6. Document and Validate the Change

- [ ] 6.1 Update user and developer documentation to distinguish operator-managed automation from direct CLI best-effort behavior, describe the evidence order and opt-out, and explain stale declarations, explicit-root receipts, ambient inventory, compatibility warnings, and refresh requirements.
- [ ] 6.2 Run packaged-skill generation or synchronization and all skillset validators, then confirm source and packaged copies are consistent.
- [ ] 6.3 Run focused unit tests followed by `pixi run lint`, `pixi run typecheck`, and `pixi run test`, and resolve regressions within the change scope.
- [ ] 6.4 Run `openspec validate agent-guided-system-extension-reconciliation --strict` and verify every requirement scenario has corresponding implementation or test evidence.
