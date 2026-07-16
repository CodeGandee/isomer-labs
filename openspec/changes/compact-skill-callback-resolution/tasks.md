## 1. Compact Resolution Contract

- [ ] 1.1 Add a dedicated compact callback execution serializer that emits only `id`, `source_type`, absolute `instruction_path`, and conditional `external: true` for each admitted callback.
- [ ] 1.2 Normalize `prompt` and `prompt_file` entrypoints to their resolved readable file and `skill_dir` entrypoints to `<resolved-directory>/SKILL.md` without changing stored callback records.
- [ ] 1.3 Preserve the standard CLI envelope, deterministic callback application order, empty-success behavior, stable callback ids, and resolution-relevant diagnostics in compact output.
- [ ] 1.4 Add `--explain` to `project skill-callbacks resolve` and route it to the existing full callback, registry, source, Toolbox status, and gated-id serialization.
- [ ] 1.5 Keep `list`, `show`, `register`, `install`, `disable`, and `validate` management payloads unchanged while removing their management-only fields from ordinary resolve output.

## 2. Purpose-Bounded Resolution State

- [ ] 2.1 Introduce a callback-resolution Project validation scope or dedicated loader that resolves Project and selected topic context without running unrelated environment, template, profile, research-record, or other capability validators.
- [ ] 2.2 Retain validation for visible callback registry integrity, requested insertion-point support, source readability and authorization, duplicate visible callback identity, deterministic ordering, and applicable Toolbox gating.
- [ ] 2.3 Ensure missing Toolbox registration remains a resolution-blocking diagnostic, disabled Toolbox callbacks remain omitted, and ordinary compact output does not expose active or disabled Toolbox management state.
- [ ] 2.4 Keep `project skill-callbacks validate` as the broad callback-health surface and `project validate` as the general Project-health surface.

## 3. Participating Skill Guidance

- [ ] 3.1 Update callback-participating DeepSci skills to process compact callback entries in returned order and read each `instruction_path` according to `source_type`.
- [ ] 3.2 Update callback-participating Kaoju skills with the same compact consumption, supplemental `skill_dir` handling, empty-success, and authority guidance.
- [ ] 3.3 Teach ordinary skill workflows not to request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields unless diagnosing callback resolution.
- [ ] 3.4 Update the research-paradigm skill validator and asset tests to require compact consumption wording for every manifest-declared callback insertion point.

## 4. CLI Documentation and Migration

- [ ] 4.1 Update CLI help, examples, and manual reference material to document compact default resolution and detailed `resolve --explain` output.
- [ ] 4.2 Document migration for callers that parsed full ordinary resolve records, directing execution consumers to compact locators and management consumers to `--explain`, `list`, or `show`.
- [ ] 4.3 Update the changelog with the breaking response change, bounded diagnostic behavior, and absence of registry or Toolbox storage migration.

## 5. Resolution and Regression Tests

- [ ] 5.1 Add unit tests for compact prompt, prompt-file, skill-directory, internal, and authorized external source projections with absolute instruction entrypoints.
- [ ] 5.2 Add tests proving exact compact field allowlists, deterministic array order, empty success, omitted management metadata, and stable serialized-size ceilings.
- [ ] 5.3 Add CLI tests for default compact output, `--explain` detail parity, resolve help, missing Project behavior, and unchanged management subcommand payloads.
- [ ] 5.4 Add Toolbox gating tests proving active admission, disabled omission, missing-registration failure diagnostics, context-specific disablement, and detailed explanation only when requested.
- [ ] 5.5 Add diagnostic-scope tests proving callback-relevant errors remain visible while unrelated Project validation errors neither appear nor change resolve exit status.
- [ ] 5.6 Update existing callback, Toolbox, CLI, DeepSci, Kaoju, and packaged-skill tests that consume the old ordinary resolve payload.

## 6. Validation

- [ ] 6.1 Run targeted User Skill Callback, Toolbox, CLI, Project-context, research-skill asset, and validator tests.
- [ ] 6.2 Run `pixi run validate-research-skills` and documentation validation.
- [ ] 6.3 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [ ] 6.4 Strictly validate `compact-skill-callback-resolution` and confirm every specified migration, safety rule, and payload-growth guard has implementation coverage.
