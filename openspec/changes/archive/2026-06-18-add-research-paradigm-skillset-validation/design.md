## Context

`skillset/research-paradigm` is now mostly contract-driven Markdown: each `isomer-rsch-*` skill has a `SKILL.md`, one-level local references, and an `agents/openai.yaml` manifest. Prior OpenSpec changes settled workspace paths, durable recording, lifecycle vocabulary, CLI topic context, and execution/provider extension refs. The remaining Stage 6 problem is that conformance is still checked by manual `rg` searches and reviewer judgment.

The current `research-paradigm-skills` spec already requires validation for structure, naming consistency, workflow formatting, self-containment, placeholder registration, and runtime-coupling removal. This change turns those requirements into a deterministic repository command with tests.

## Goals / Non-Goals

**Goals:**

- Provide a local validation harness that reports deterministic diagnostics for `skillset/research-paradigm`.
- Validate the Stage 6 checks from `context/plans/research-paradigm-skill-gaps.md`.
- Preserve intentional source-term mapping, provenance, and deferred-resource notes through explicit allow zones.
- Keep the implementation lightweight and runnable through Pixi without adding new third-party dependencies.
- Add fixture-based unit tests so stale-term and allow-zone behavior is stable.

**Non-Goals:**

- Do not validate live Research Topic, Research Inquiry, Research Task, Run, Artifact, Evidence Item, Gate, or workspace records.
- Do not implement provider-backed execution, scheduler behavior, or artifact-format validation.
- Do not lint all prose quality or enforce every agent-style writing rule.
- Do not add hosted CI unless the repository's supported Pixi platforms or runner availability make that reliable; a repository command is sufficient for this stage.

## Decisions

### Decision 1: Implement a stdlib Python validator under `scripts/`

The harness will be a repository script, likely `scripts/validate_research_paradigm_skillset.py`, invoked by a Pixi task such as `pixi run validate-research-skills`. It should use Python stdlib modules for path walking, regex checks, frontmatter parsing, constrained `agents/openai.yaml` field extraction, and optional TOML config loading through `tomllib`.

Alternative considered: extend the OpenSpec CLI. Rejected because this validator checks repository skill bundle hygiene, not OpenSpec artifact validity, and it should run after ordinary skill edits without requiring a new OpenSpec command.

Alternative considered: use a full Markdown/YAML parser dependency. Rejected for Stage 6 because the current Markdown path references and manifests are simple, and a constrained parser keeps the tool easy to run in the existing Pixi environment.

### Decision 2: Use explicit rule codes and line-based diagnostics

The validator should emit diagnostics as `path:line: CODE message` and exit nonzero when any error exists. Suggested codes are `RPS001 stale-term`, `RPS002 resolved-path-tbd`, `RPS003 unregistered-tbd`, `RPS004 hardcoded-source-path`, `RPS005 broken-skill-reference`, `RPS006 manifest-name`, and `RPS007 skill-layout`.

This makes failures easy for agents and humans to repair. It also gives unit tests stable expectations without coupling tests to full prose output.

### Decision 3: Distinguish active guidance from allowed explanatory zones

The validator must not treat every occurrence of stale source vocabulary as an error. Source-term mapping tables, provenance references, license notices, and deferred-resource notes intentionally mention legacy terms such as DeepScientist, Research Goal, Research Thread, Research Branch, and Isomer Workspace.

Accepted direction from exploration: use strict active-text validation with narrow, rule-specific allow zones. The validator should validate every Markdown and YAML file under `skillset/research-paradigm`, then classify files and sections by role rather than scanning only `SKILL.md` files or directly linked references.

The design should use a small allow-zone model:

- Path-based zones for files such as `references/provenance.md`, `references/source-term-mapping.md`, `PROVENANCE.md`, license notices, and deferred-resource notes.
- Section-based zones for headings such as `## Source-Term Mappings`, `## Rejected Runtime Concepts`, and resolved TBD-surface mapping sections in local contract copies.
- Pattern-specific allowances, for example former `path-*` IDs inside "Resolved Workspace Path Surfaces" tables but not as emitted `[[tbd-surface:path-*]]` placeholders.

The key boundary is that active `SKILL.md` workflow, routing, guardrail, and durable-output guidance should use current Isomer domain language.

### Decision 4: Put mutable rule data in config, not hard-coded prose

Core forbidden terms, resolved placeholder IDs, and disallowed coupling patterns should live in the Python validator defaults. Add `skillset/research-paradigm/validation.toml` for narrow allow-zone file globs, section headings, and pattern-specific allowances.

This keeps future Stage 7 and Stage 8 edits from requiring code changes for every allowed deferred-resource note while still making allow-zone changes reviewable. The config should not own severity or redefine core domain rules.

### Decision 5: Validate TBD registries through a shared canonical registry and local mirrors

The shared registry at `isomer-rsch-shared/references/tbd-surface-registry.md` should be canonical for the subtree. Directly loaded local contract files such as `references/isomer-research-contract.md`, `references/writing-contract.md`, `references/outline-contract.md`, and `references/audit-gate.md` can contain local `## TBD Surface Registry` mirror sections for self-contained skill behavior.

The validator should compare directly loaded local registry mirrors against the shared registry and require exact resolved-ID coverage plus normalized resolution text. Normalization may ignore whitespace and Markdown formatting differences, but it must not hide missing IDs, extra IDs, or changed resolution meaning.

Alternative considered: validate placeholders only against the shared registry and ignore local mirrors. Rejected because copied local contract files could drift while still appearing self-contained to a loaded skill.

Alternative considered: require only matching IDs and allow local wording to differ. Rejected because local text can drift semantically even when IDs remain present.

### Decision 6: Treat repository command as the Stage 6 integration point

Add a Pixi task rather than relying only on direct script invocation. Hosted CI is optional and should be deferred unless the repo adds a compatible runner path. The current Pixi workspace declares `linux-aarch64`, while common GitHub-hosted Linux runners are x64, so adding a fragile workflow would create operational noise.

## Risks / Trade-offs

- False positives on legitimate mapping/provenance text → Mitigate with explicit allow zones and fixture tests for allowed examples.
- False negatives from too-broad allow zones → Keep allow zones narrow by file path, section heading, and pattern type; do not allow stale terms globally.
- Regex Markdown parsing misses exotic links → Scope Stage 6 to the observed skill bundle patterns and add tests for backticked `references/...`, Markdown links, and local asset/script refs.
- Constrained YAML parsing misses future manifest complexity → Validate only the required `interface.display_name` and `interface.default_prompt` fields for now; switch to a YAML parser only if manifests become structurally complex.
- Local registry mirror comparison becomes brittle if docs reorder sections → Parse registry tables by heading and ID, and compare normalized cells instead of raw lines.
- CI is deferred → The Pixi task still gives agents and developers one command to run locally, and CI can be added later when runner/platform support is settled.

## Migration Plan

1. Add the validator script and optional validation config.
2. Add fixture-based unit tests for pass and fail cases.
3. Add the Pixi task.
4. Run the validator against the current `skillset/research-paradigm` tree and repair any legitimate failures.
5. Update `context/plans/research-paradigm-skill-gaps.md` after the harness passes.

Rollback is simple: remove the script, tests, optional config, and Pixi task. No durable research data or runtime contracts are migrated by this change.

## Open Questions

No blocking design questions remain. The apply phase can choose exact rule-code names, function names, and config key names as long as the resulting behavior preserves the accepted strictness, scan surface, allow-zone, and registry-mirror decisions.
