## 1. Validator Scaffolding

- [x] 1.1 Add `scripts/validate_research_paradigm_skillset.py` with a small CLI, repository-root discovery, deterministic diagnostic objects, and nonzero exit behavior for validation errors.
- [x] 1.2 Add built-in rule defaults for core stale terms, resolved TBD ids, and disallowed coupling patterns, plus `skillset/research-paradigm/validation.toml` for narrow allow-zone file globs, section headings, and pattern-specific allowances.
- [x] 1.3 Add a Pixi task such as `validate-research-skills` that runs the validator against `skillset/research-paradigm`.

## 2. Validation Rules

- [x] 2.1 Implement skill discovery and `SKILL.md` structural checks for `isomer-rsch-*` folder naming, frontmatter `name` and `description`, near-top `## Workflow`, numbered workflow steps, `## Reference Routing`, and fallback guidance.
- [x] 2.2 Implement `agents/openai.yaml` checks for `interface.display_name` matching the skill name and `interface.default_prompt` invoking the same `$isomer-rsch-*` skill.
- [x] 2.3 Implement local reference extraction from `SKILL.md` for backticked and Markdown-linked `references/`, `assets/`, and `scripts/` paths, and report missing same-skill targets.
- [x] 2.4 Implement whole-subtree Markdown/YAML scanning with role classification for active docs, explanatory files, resolved-surface sections, canonical registry files, and directly loaded local contract registry mirrors.
- [x] 2.5 Implement `[[tbd-surface:<id>]]` extraction, lookup against the canonical shared TBD registry, and stale resolved-placeholder rejection for workspace, recording, lifecycle, CLI topic-context, and execution-extension surfaces.
- [x] 2.6 Implement hard-coded local/source path and runtime-coupling checks for local absolute paths, source-analysis paths, archived OpenSpec change paths, `extern/orphan` paths, DeepScientist runtime paths, command wrappers, runner homes, and source runtime APIs.
- [x] 2.7 Implement stale lifecycle/workspace term checks for Research Goal, Research Thread, Research Branch, and Isomer Workspace with narrow allow zones for source-term mapping, provenance, license, deferred-resource, and resolved-surface sections.
- [x] 2.8 Implement local registry mirror consistency checks so directly loaded contract registry sections match the shared registry by resolved-ID coverage and normalized resolution text.

## 3. Tests

- [x] 3.1 Add unit-test fixtures for a minimal valid research-paradigm skillset.
- [x] 3.2 Add failing fixture tests for stale active terms, resolved path TBD placeholders, unregistered TBD ids, broken local references, hard-coded source paths, and manifest mismatches.
- [x] 3.3 Add allow-zone fixture tests proving source-term mapping tables, provenance files, license notices, deferred-resource notes, rejected-runtime sections, and resolved-surface mapping tables are allowed only for their matching rules.
- [x] 3.4 Add registry fixture tests for shared registry lookup, local mirror match, missing mirror IDs, extra mirror IDs, and changed normalized resolution text.
- [x] 3.5 Add whole-subtree scan tests showing unlinked Markdown/YAML files are still classified and validated.
- [x] 3.6 Add tests for diagnostic format, file and line reporting, and nonzero exit behavior.

## 4. Repository Application

- [x] 4.1 Run the new validator against the current `skillset/research-paradigm` tree and repair any legitimate failures without weakening accepted domain language.
- [x] 4.2 Run `pixi run validate-research-skills`, `pixi run test`, and `openspec validate add-research-paradigm-skillset-validation`.
- [x] 4.3 Update `context/plans/research-paradigm-skill-gaps.md` to mark Stage 6 items complete and mark the Stage 9 skillset validation item complete after the validator passes.
- [x] 4.4 Run `openspec validate --all` after implementation is complete.
