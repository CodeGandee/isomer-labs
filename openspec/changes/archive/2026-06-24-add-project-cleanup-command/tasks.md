## 1. Cleanup Planning Model

- [x] 1.1 Add cleanup part definitions for `bootstrap`, `project-config`, `houmao-overlay`, `content-policy`, `topic-workspace`, `runtime`, and `content-root`.
- [x] 1.2 Add cleanup plan/result data structures with JSON serialization for selected parts, dry-run status, planned removals, removed targets, skipped targets, warnings, diagnostics, and Project root.
- [x] 1.3 Implement Project authority resolution for cleanup using a valid Project Manifest when available, malformed-manifest fallback when needed, and explicit or current-directory Project root fallback when no manifest exists.
- [x] 1.4 Implement content-root selection for cleanup from Project Manifest path defaults, `--content-dir <content-dir>`, or the built-in `isomer-content/` default.
- [x] 1.5 Implement Topic Workspace resolution for selected topics, all-topics cleanup, manifest-registered workspaces, and derived workspace defaults without treating unregistered directories as Research Topic authority.
- [x] 1.6 Validate every planned cleanup target as project-local, not equal to the Project root, and safe with respect to `.isomer-labs/`, `.houmao/`, and selected content-root boundaries.
- [x] 1.7 Add symlink handling that removes only exact planned symlink entries or refuses unsafe symlink targets without recursively following destinations.

## 2. Cleanup Execution

- [x] 2.1 Implement dry-run behavior so cleanup builds and reports the plan without creating, modifying, or deleting files.
- [x] 2.2 Implement default non-mutating behavior when neither `--dry-run` nor `--yes` is supplied, including guidance that `--yes` is required for deletion.
- [x] 2.3 Implement confirmed deletion for planned file, symlink, and directory targets after the full plan is validated.
- [x] 2.4 Implement absent-target skipping and deterministic per-target diagnostics for failed removals.
- [x] 2.5 Implement `runtime` cleanup for `state.sqlite`, runtime-owned directories, and adapter runtime material under the selected Topic Workspace while preserving topic definition and team-profile source material.
- [x] 2.6 Implement `bootstrap` cleanup as a composition of Project config, Houmao overlay, generated content policy files, and known init-created workspace cleanup while preserving unknown files by default.
- [x] 2.7 Implement content-root purge refusal unless `--purge-content-root` is supplied, and confirmed full-root removal only after stronger safety validation.

## 3. CLI Integration

- [x] 3.1 Register Project-scoped `isomer-cli project cleanup` with `--part`, `--topic`, `--all-topics`, `--content-dir`, `--purge-content-root`, `--dry-run`, and `--yes` options.
- [x] 3.2 Wire cleanup command options through `CliOptions` or command-local dispatch into the cleanup planner/executor.
- [x] 3.3 Emit deterministic human-readable cleanup summaries and versioned JSON output through the existing CLI output wrapper.
- [x] 3.4 Update `isomer-cli --help` and `isomer-cli project cleanup --help` expectations to include cleanup command and destructive controls.
- [x] 3.5 Update existing Project Manifest overwrite diagnostics from `isomer-cli project init` to name cleanup dry-run as the supported reinitialization preview path without running cleanup automatically.

## 4. Documentation and Operator Skill

- [x] 4.1 Update `docs/isomer-cli.md` with cleanup command syntax, parts, dry-run behavior, confirmation behavior, purge behavior, and side-effect boundaries.
- [x] 4.2 Update workflow and troubleshooting docs that mention failed reinitialization or manual deletion to route through cleanup dry-run and confirmed cleanup.
- [x] 4.3 Add `cleanup-project` guidance to `skillset/operator/isomer-admin-project-mgr`, including help text, subcommand table entry, CLI-boundary examples, output contract updates, and guardrails.
- [x] 4.4 Update project-manager skill validation rules and unit fixtures to require cleanup guidance, the `cleanup-project` subcommand, and cleanup CLI-boundary terms.
- [x] 4.5 Ensure operator guidance preserves unknown content by default and distinguishes local `.houmao/` overlay cleanup from live Houmao agent cleanup.

## 5. Tests

- [x] 5.1 Add CLI tests for `project cleanup --part project-config --dry-run` and default non-mutating cleanup, asserting `.isomer-labs/` remains intact and JSON reports `mutated = false`.
- [x] 5.2 Add CLI tests for confirmed `project-config`, `houmao-overlay`, and `content-policy` cleanup.
- [x] 5.3 Add CLI tests for `bootstrap` cleanup before reinitialization, including a successful later `isomer-cli project init`.
- [x] 5.4 Add CLI tests for `topic-workspace` and `runtime` cleanup with selected topics, preserving topic definition and team-profile source material for runtime cleanup.
- [x] 5.5 Add CLI tests for malformed manifest and missing manifest cleanup fallback behavior.
- [x] 5.6 Add safety tests for out-of-project targets, Project-root refusal, content-root purge refusal, confirmed purge with opt-in, unknown content preservation, and symlink handling.
- [x] 5.7 Add output-contract tests for deterministic text and JSON cleanup plan/result fields.
- [x] 5.8 Add or update operator-skill validation tests for project-manager cleanup guidance.

## 6. Validation

- [x] 6.1 Run `openspec validate add-project-cleanup-command --strict`.
- [x] 6.2 Run `pixi run python -m unittest tests.unit.test_isomer_cli`.
- [x] 6.3 Run `pixi run python -m unittest tests.unit.test_validate_skillsets`.
- [x] 6.4 Run `pixi run validate-operator-skills`.
- [x] 6.5 Run `pixi run lint` and `pixi run test`.
