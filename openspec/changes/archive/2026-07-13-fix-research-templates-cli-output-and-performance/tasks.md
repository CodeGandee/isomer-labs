## 1. Bound Research Template Context Resolution

- [x] 1.1 Add an explicit opt-in context-validation scope for research-template operations while keeping full Project validation as the default for every existing caller.
- [x] 1.2 Limit the template scope to Project discovery, topic selection, selected Research Topic Config identity, Topic Workspace mapping and path bounds, local active context, and Workspace Runtime inputs required by template operations.
- [x] 1.3 Add focused tests proving research-template context resolution skips unrelated User Skill Callback, Toolbox, Domain Agent Team Template, and Topic Agent Team Profile validation while full validation commands retain it.

## 2. Normalize Research Template Failures

- [x] 2.1 Add a template-specific command runner that reuses common option merging and the bounded context scope without changing the shared research-record or research-idea runners.
- [x] 2.2 Render context-resolution and template-operation failures as human-readable text by default, preserving diagnostics, domain error code, non-zero exit status, and known mutation state.
- [x] 2.3 Render the same failures through the `isomer-cli-output.v1` wrapper when root-level `--print-json` is requested, with the exact template subcommand path and stable structured fields.
- [x] 2.4 Migrate `create`, `list`, `show`, `refresh`, `compile`, and `remove` to the template runner without removing or renaming their successful payload fields.
- [x] 2.5 Add CLI regression tests for default text failures, requested JSON failures, context guidance, representative template domain errors, and non-mutating failure claims.

## 3. Use Indexed Template Reads

- [x] 3.1 Add one indexed-row mapping helper that preserves template record identity, status, transition metadata, venue, paper type, preview status, updated timestamp, and the `main` default marker.
- [x] 3.2 Change `templates list` to query exact semantic id `kaoju:writing-template` through `query_index_list`, apply venue and paper-type filters, and remove its dependency on `list_records`.
- [x] 3.3 Keep `show`, `refresh`, `compile`, and `remove` on the shared indexed named-template lookup, then reopen canonical record detail or mutation APIs only after identity selection.
- [x] 3.4 Preserve query diagnostics and rebuild guidance without adding read-time index repair or a lifecycle-record fallback.
- [x] 3.5 Add tests with unrelated lifecycle records and indexed rows proving template list and named lookup issue bounded indexed queries and return compatible summaries.

## 4. Verification

- [x] 4.1 Run the focused research-template, CLI error-reporting, context-resolution, and query-index unit tests and resolve regressions.
- [x] 4.2 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` and report any unrelated pre-existing failures separately.
- [x] 4.3 Run `openspec validate fix-research-templates-cli-output-and-performance --strict`.
