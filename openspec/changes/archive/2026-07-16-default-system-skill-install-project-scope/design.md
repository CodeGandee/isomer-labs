## Context

The shared `_target_options` decorator currently makes both `--target` and `--scope` required for `system-skills status`, `install`, `upgrade`, and `uninstall`. The installer resolver already accepts a concrete `SystemSkillScope`, maps `project` to target-specific roots under the exact process working directory, deduplicates shared roots for `--target all`, and records scope-aware bindings in the target-root receipt. The operator-owned `isomer-op-system-skill-mgr` already treats Project scope as the normal installation choice and requires explicit intent for user-wide installation.

The requested change is a CLI default, not a new resolution mode. It must preserve the existing meaning of Project scope, avoid inferring an Isomer or Git root from an ancestor, and avoid silently changing the scope rules for inspection, upgrade, or removal.

## Goals / Non-Goals

**Goals:**

- Accept `isomer-cli system-skills install --target <target>` and resolve it exactly as an explicit `--scope project` install.
- Keep `--scope user` an explicit opt-in and preserve all explicit scope behavior.
- Keep the effective scope concrete before target resolution so installer services, result payloads, diagnostics, and receipt schemas remain unchanged.
- Make help, discovery templates, packaged system-skill guidance, examples, validation, and migration notes distinguish the install default from the other scope-required commands.
- Prove that omitted scope writes only beneath target-specific Project roots under the exact current working directory and does not touch user roots.

**Non-Goals:**

- Defaulting scope for `status`, `upgrade`, or `uninstall`.
- Defaulting or removing the required `--target` option.
- Searching upward for an initialized Isomer Project, Git root, or other anchor.
- Changing target paths, the `all` target deduplication rules, selection defaults, projection modes, force semantics, receipt formats, arbitrary-root policy, or extension registration behavior.
- Adding a new output-schema field solely to distinguish an omitted scope from an explicit Project scope.

## Decisions

### Give `install` a Dedicated Scope Option Contract

The install command will use a dedicated option decorator whose `--scope` choice defaults to `project` and whose help displays that default. The existing shared target option contract remains scope-required for `status`, `upgrade`, and `uninstall`.

This keeps the safety boundary visible in code and Click help. Parameterizing one shared decorator was considered, but separate decorators make it harder for a future edit to accidentally default destructive or ambiguous commands. Making scope optional in the callback and filling it later was also rejected because downstream code should continue receiving a concrete `SystemSkillScope`.

### Resolve Omitted and Explicit Project Scope Through the Same Path

Click will supply `project` before `resolve_targets` runs. No fallback logic will be added to `resolve_targets`, the installer service, or receipt writing. Omitted scope and explicit `--scope project` therefore produce the same normalized root, target-scope bindings, human output, JSON payload, diagnostics, and manifest content.

Adding an `implicit_scope` or `scope_source` field was considered but rejected. The public contract needs the effective scope and resolved path, which already exist; exposing parser provenance would create an output-schema distinction without changing authorization or filesystem behavior.

### Preserve Exact-CWD Project Resolution

The default retains the existing Project-scope rule: `<cwd>` is the exact process working directory. The CLI will not discover a parent Isomer Project or Git root, and it will not require the current directory to be initialized. Tests will invoke omitted-scope installs from nested and ordinary directories and assert that only the expected local target root changes.

This preserves deterministic behavior and avoids making the default depend on ambient repository discovery.

### Keep User Scope and Other Operations Explicit

Only an explicit `--scope user` can select a user root. `status`, `upgrade`, and `uninstall` continue to fail with a missing-option diagnostic when scope is omitted. The packaged system-skill manager may continue passing its selected scope explicitly because its workflow records user intent and installation posture; it will also explain that the low-level install command defaults to Project scope when called without the option.

Defaulting every target-resolving command was rejected because an implicit root is undesirable for removal and refresh, and ambiguous for status checks used in repair workflows.

### Teach the Short Install Form Without Hiding Explicit User Intent

Project-install examples and extension discovery install templates will omit `--scope project` where they demonstrate the default. User-wide examples will retain `--scope user`. Status, upgrade, and uninstall examples will retain explicit scope. Documentation will state that the short install form is equivalent to explicit Project scope and is anchored to the exact current working directory.

Keeping every Project example explicit was considered, but it would leave the new behavior undiscoverable. Removing scope from user-wide examples was rejected because it would change their destination.

## Risks / Trade-offs

- [Automation may have relied on omitted scope failing before mutation] → Treat this as an intentional command-contract change, add a changelog entry, document the new local mutation, and test exact target paths.
- [A user may run the short form from an unintended directory] → Keep `--target` required, display `[default: project]` in help, document exact-cwd anchoring prominently, and report the effective scope and resolved root in output.
- [A shared decorator change could accidentally default other commands] → Use a dedicated install option decorator and regression-test missing-scope failure for `status`, `upgrade`, and `uninstall`.
- [Docs or packaged skills may continue saying every command requires scope] → Extend existing documentation and packaged-skill validation fixtures, scan active guidance, and update structured extension command templates.

## Migration Plan

1. Introduce the install-only Click option contract and preserve a concrete scope value at the resolver boundary.
2. Add CLI tests for omitted-scope Project installation, explicit scope equivalence, exact-cwd anchoring, user-root non-mutation, help output, and unchanged failures on the other commands.
3. Update extension discovery payloads, packaged system-skill manager guidance, README, tutorials, CLI reference, developer documentation, validators, and changelog.
4. Run focused installer and documentation tests, then the full repository validation and distribution smoke checks.

Rollback is a code and documentation revert. Existing explicit-scope invocations and receipts remain valid in either direction, and no data migration is required.

## Open Questions

None.
