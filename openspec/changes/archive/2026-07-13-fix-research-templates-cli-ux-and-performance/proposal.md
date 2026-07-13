## Why

The new `isomer-cli ext research templates` command group has two rough edges that hurt usability now that it is in daily use. Unknown-command errors show generic project-level examples instead of templates-specific examples, and every template operation scans all lifecycle records because it routes through `list_records`. These issues are small but noticeable, so we should polish them before the surface stabilizes.

## What Changes

- Add context-sensitive CLI examples for `ext research templates` (and sibling `ext research records` / `ext research ideas` groups) so unknown-command and usage errors show relevant commands instead of generic project examples.
- Replace the `list_records`-based template lookup in `research_templates_ext.py` with a query-index-backed lookup that filters by semantic id and then by `template_name` metadata, avoiding a full lifecycle-record scan.
- Add focused unit tests for the new error examples and for the faster lookup path.

## Capabilities

### New Capabilities

- `research-templates-cli-errors`: Context-sensitive usage examples for the `isomer-cli ext research templates` command group and sibling research extension groups.
- `research-templates-query-performance`: Fast indexed lookup of writing-template records by semantic id and template name.

### Modified Capabilities

- (none)

## Impact

- `src/isomer_labs/cli/examples.py` gains new example entries.
- `src/isomer_labs/cli/commands/research_templates_ext.py` uses `query_index_list` instead of `list_records` for `_find_template_record`.
- `tests/unit/test_research_templates_ext.py` gains regression tests for examples and lookup performance behavior.
- No public CLI contract changes; existing commands and outputs remain the same.
