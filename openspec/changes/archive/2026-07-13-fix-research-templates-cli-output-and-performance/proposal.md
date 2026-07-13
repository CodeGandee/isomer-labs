## Why

`isomer-cli ext research templates` currently emits raw JSON for domain failures even when the caller did not request JSON, and every template command pays for Project-wide validation that is unrelated to selecting or operating on one Topic Workspace's writing templates. The `list` command also scans all lifecycle records instead of using the existing query index, so the surface is inconsistent and becomes slower as Project configuration and Workspace Runtime grow.

## What Changes

- Make research-template domain failures use the standard CLI output mode: concise Isomer diagnostics in text mode and the versioned `isomer-cli-output.v1` wrapper when root-level `--print-json` is requested.
- Preserve non-zero exit codes, known mutation state, and actionable topic-selection guidance for context-resolution and template-operation failures.
- Resolve only the Project, Research Topic Config, Topic Workspace, and Workspace Runtime information required by research-template commands; do not validate unrelated User Skill Callback registries or other Project features that these commands do not consume.
- Make `templates list` query `kaoju:writing-template` rows through the read-only research record query index and preserve its existing template summary, default-marker, venue filter, and paper-type filter behavior.
- Keep indexed single-template lookup for `show`, `refresh`, `compile`, and `remove`, with no fallback to a full lifecycle-record scan during normal reads.
- Add focused regression tests for output-mode selection, bounded context work, indexed queries, stable results, and non-mutating failures.
- **BREAKING**: callers that parse failure JSON without passing root-level `--print-json` must add that flag; JSON failures will use the versioned CLI wrapper instead of an unwrapped research-record payload.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `isomer-cli-error-reporting`: Research-template domain failures honor the root output mode and use normalized Isomer diagnostics.
- `cli-topic-context-resolution`: Research-template commands resolve and validate the selected Topic Workspace without validating unrelated Project capabilities.
- `research-record-query-index`: Research-template list and lookup operations use the read-only query index instead of materializing all lifecycle records.

## Impact

- Affects `src/isomer_labs/cli/commands/research_templates_ext.py`, its command runner or output adapter, and the smallest context-resolution API needed to request template-specific validation.
- Affects focused research-template CLI tests and any shared context-resolution tests needed to prove skipped validation is bounded to commands that opt into the template scope.
- Does not change template generation, LaTeX compilation, record mutation semantics, `paper-pass`, generic research-record commands, User Skill Callback validation commands, or Project-wide validation behavior.
