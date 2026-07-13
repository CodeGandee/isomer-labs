## Context

The `isomer-cli ext research templates` command group was introduced in `add-kaoju-paper-writing`. It currently reuses the generic CLI error formatting and record-listing primitives. Two issues surfaced during first use:

1. When a user types an unknown subcommand such as `isomer-cli ext research templates fd`, the emitted `ISOCLI001` diagnostic shows the correct `Usage:` line but lists generic project examples (`project validate`, `project topics list`, etc.) because `examples_for_command` has no entry for `ext research templates` and falls back to the `project` default.
2. Every template operation (`show`, `refresh`, `compile`, `remove`) calls `list_records` to locate the writing-template record by `template_name`. `list_records` opens the workspace runtime and materializes every lifecycle record for the topic, which becomes slow as the topic accumulates records.

## Goals / Non-Goals

**Goals:**
- Provide context-sensitive examples for unknown commands and usage errors under `ext research templates`, `ext research records`, and `ext research ideas`.
- Make template record lookup O(indexed query) instead of O(all records).
- Keep the public CLI output contract unchanged for successful commands.

**Non-Goals:**
- Redesigning the overall CLI error format.
- Adding new template commands or changing template file generation.
- Optimizing other record-listing flows.

## Decisions

- **Add examples to `src/isomer_labs/cli/examples.py` rather than customizing the group.** The existing `COMMAND_EXAMPLES` registry is the canonical place for usage examples, and `diagnostic_for_click_exception` already consumes it via `examples_for_command`. Adding entries for `ext research templates`, `ext research records`, and `ext research ideas` fixes the inconsistency for all usage errors in those groups with no CLI plumbing changes.
- **Use `query_index_list` for template lookup.** The workspace runtime maintains a SQLite query index (`research_record_index`) with `semantic_id`, `status`, and `metadata_json`. `query_index_list` issues a targeted SQL query against that index. We will filter by `semantic_id="kaoju:writing-template"` and `status="ready"`, then scan the small result set for the matching `template_name` in `metadata`. This avoids the full lifecycle-record scan performed by `list_records`.
- **Keep the same return shape from `_find_template_record`.** The function still returns a dict with the same keys (`id`, `status`, `transition_metadata`) so callers need no changes beyond the lookup implementation.

## Risks / Trade-offs

- **Query index staleness** → `query_index_list` depends on the query index being up to date. The index is refreshed on every record mutation in the same codebase, so this is consistent with other CLI commands.
- **Status filtering** → Using `status="ready"` skips `archived` or `blocked` templates. This matches the current intent: users operate on the active template. If a template is blocked, `create` will report the existing directory error before lookup matters; `show`/`refresh`/`compile`/`remove` should not silently match a blocked/archived record.

## Open Questions

- None.
