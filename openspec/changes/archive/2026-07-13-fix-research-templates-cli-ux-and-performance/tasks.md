## 1. Context-Sensitive CLI Examples

- [x] 1.1 Add `COMMAND_EXAMPLES` entries for `ext research templates`, `ext research records`, and `ext research ideas` in `src/isomer_labs/cli/examples.py`.
- [x] 1.2 Add unit tests that invoke unknown subcommands under each group and assert the emitted examples match the group.

## 2. Indexed Template Lookup

- [x] 2.1 Replace `list_records` with `query_index_list` in `_find_template_record` in `src/isomer_labs/cli/commands/research_templates_ext.py`, filtering by `semantic_id="kaoju:writing-template"` and `status="ready"` and matching `template_name` in returned metadata.
- [x] 2.2 Ensure `_find_template_record` still returns a dict with `id`, `status`, and `transition_metadata` and still skips archived records.
- [x] 2.3 Add a focused unit test verifying that `_find_template_record` resolves the correct record without calling `list_records`.

## 3. Verification

- [x] 3.1 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` and resolve any diagnostics.
- [x] 3.2 Run `openspec validate fix-research-templates-cli-ux-and-performance --strict`.
