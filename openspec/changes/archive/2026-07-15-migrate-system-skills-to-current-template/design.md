## Context

The current skill-writing authority is `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-agent-skill-handling`. Its history shows the relevant transition in two July 15 commits: `dbd425f` replaced the old required `## Common Mistakes` section with strict `## Guardrails` and `## Troubleshooting Guide`, then `e3673cf` made troubleshooting optional and applied the format to skill subpages. The current guide also requires discovery-oriented frontmatter, `## Overview`, `## When to Use`, a concise numbered workflow, and a freeform fallback.

Isomer packages system skills from `src/isomer_labs/assets/system_skills/manifest.toml`. The manifest declares 55 active skill roots: 19 core skills, 22 DeepSci skills, and 14 Kaoju skills. Those roots contain 614 active Markdown files after excluding source provenance, migration notes, and passive templates. The audit found:

- 44 entrypoints and 13 active subpages with `## Common Mistakes`.
- Three entrypoints with both `## Guardrails` and `## Common Mistakes`.
- One entrypoint with neither section.
- 34 pages with 179 top-level Guardrails bullets that do not start with `DO NOT` or `MUST`.
- Seven entrypoints without `## Overview`, 11 without `## When to Use`, and 10 descriptions that do not start with `Use when`.
- 21 executable pages with a numbered `## Workflow` but no current-template freeform fallback.
- No active `## Troubleshooting Guide` sections.

The repository exposes packaged assets through compatibility symlinks under `skillset/`, and `scripts/validate_skillsets.py` already validates those assets by group and domain-specific rules. The working tree also contains unrelated edits, including edits to `isomer-op-system-skill-mgr`, so implementation must preserve the current working-tree content and avoid reconstructing files from `HEAD`.

## Goals / Non-Goals

**Goals:**

- Make every manifest-declared active system-skill entrypoint conform to the current authoring template without changing its purpose or trigger boundary.
- Inspect every active subpage and apply workflow, Guardrails, and troubleshooting rules when the page is executable or contains behavioral guidance.
- Preserve all domain-specific rules, evidence contracts, safety boundaries, output contracts, public command names, and local links.
- Add one manifest-aware validation pass that prevents old-template sections and structural regressions across core and extension groups.
- Keep diagnostics precise enough to identify the affected file, line, and rule.

**Non-Goals:**

- Reorganizing Isomer subpages from `references/` to `commands/`; `commands/` is an Imsight repository convention, while Isomer has stable references and specs for both layouts.
- Rewriting skill behavior, adding subcommands, changing callback stages, or changing the packaged manifest.
- Editing immutable source snapshots under `org/`, migration records under `migrate/`, passive output material under `templates/`, licenses, or provenance documents.
- Adding placeholder troubleshooting sections where no concrete recoverable problem exists.
- Reformatting every reference document into an entrypoint; non-executable explanatory pages remain reference documents.

## Decisions

### Use the Current Guide and Its History as the Migration Authority

The implementation will use the checked-out guide as the current rule set and the `dbd425f` to `e3673cf` transition as evidence for identifying old-template content. The strongest old-template marker is `## Common Mistakes`, but the pass will also close current-template gaps in entrypoint sections, discovery descriptions, executable workflows, existing Guardrails, and optional troubleshooting structure.

An alternative was to replace only the `## Common Mistakes` heading. That would leave mixed behavioral contracts, duplicate sections, loose Guardrails, and executable pages that still fail the current guide.

### Derive the Active Scope from the Packaged Manifest

The validator and migration inventory will start from every `skills` path in each manifest group. Within each declared skill root, the pass will inspect `SKILL.md` and active Markdown pages, including root-level binding pages and pages under `commands/`, `references/`, and `scenarios/`.

Directories classified as source provenance (`org/`), migration work (`migrate/`), or passive output templates (`templates/`) remain outside the runtime-template scope. Existing research-paradigm role rules and allow zones provide the same distinction. This prevents historical source copies from being silently rewritten and avoids reporting intentional old terminology inside audit material.

An alternative was to scan every `SKILL.md` and Markdown file below the package asset root. That would incorrectly classify embedded source snapshots as live Isomer skills and violate their provenance contract.

### Separate Mechanical Detection from Semantic Conversion

Mechanical checks will inventory headings, frontmatter, workflows, and Guardrails bullets. Each `Common Mistakes` item will then be classified before editing:

1. A prohibited behavior becomes one concise `DO NOT ...` guardrail.
2. A required behavior becomes one concise `MUST ...` guardrail.
3. A recoverable execution problem becomes a first-level troubleshooting problem with one second-level `If <problem>, then <action>.` solution.
4. Explanatory context moves to an existing detail, evidence, or boundary section when compressing it into a guardrail would lose meaning.
5. Duplicate intent is merged when old and new sections coexist.

The migration will not use a blanket heading rename because many old bullets combine rules, explanation, and recovery actions.

### Apply the Full Entrypoint Contract, but Only the Applicable Subpage Contract

Every active `SKILL.md` will have valid discovery frontmatter, `## Overview`, `## When to Use`, a near-top numbered `## Workflow` with a freeform fallback, and exactly one `## Guardrails` section. Description rewrites will retain manual-only or exact-trigger restrictions in both the description and `agents/openai.yaml` policy where applicable.

An active subpage is executable when the parent routes a command or procedure to it, or when the page contains its own `## Workflow`. Executable subpages receive a concise numbered workflow and a freeform fallback. Behavioral subpages receive strict Guardrails when they need prohibitions or requirements, and optional troubleshooting only when they describe recoverable failures. Explanatory subpages are inspected for old-template headings but do not receive artificial Overview, When-to-Use, Guardrails, or troubleshooting sections.

### Preserve Stable Layout and Semantics

The implementation will edit content in place. It will not rename files, public subcommands, manifest entries, callback stages, or reference paths. Existing output contracts, stop conditions, approval rules, resource checks, storage bindings, and canonical Isomer domain terms remain authoritative.

Before touching a dirty target file, implementation will inspect its current diff and apply a narrow patch to the working-tree version. It will not reset, restore, or replace unrelated user changes.

### Extend the Existing Validator Instead of Adding a Separate Tool

`scripts/validate_skillsets.py` will gain a generic manifest-aware template validation phase used by `pixi run validate-skills`. Focused unit tests will cover:

- Required entrypoint sections and discovery description shape.
- Numbered workflows and freeform fallbacks on entrypoints and executable subpages.
- Exactly one Guardrails section per entrypoint.
- No active `## Common Mistakes` headings.
- `DO NOT` or `MUST` prefixes on top-level Guardrails bullets.
- Two-level troubleshooting entries with the required conditional solution form when a troubleshooting section exists.
- Exclusion of provenance, migration, and passive-template zones.

The validator will report actionable diagnostics without treating every explanatory reference page as executable.

## Risks / Trade-offs

- **Semantic loss while shortening old bullets**: A mechanical conversion could erase evidence or safety context. Mitigation: classify each item and move supporting explanation instead of deleting it.
- **Trigger broadening from frontmatter rewrites**: Starting descriptions with `Use when` could weaken manual-only boundaries. Mitigation: preserve explicit-invocation conditions and keep `allow_implicit_invocation` unchanged.
- **False positives in passive material**: Historical source and templates intentionally preserve upstream wording. Mitigation: derive scope from the manifest and file-role exclusions, with unit fixtures for excluded zones.
- **False positives on reference pages**: Some pages document schemas or contracts rather than executable behavior. Mitigation: require the executable-page workflow contract only for routed command/procedure pages or pages that declare `## Workflow`.
- **Large review surface**: The change touches many Markdown files. Mitigation: migrate and validate by manifest group, keep semantic edits narrow, and review section-level diffs after each group.
- **Overlap with uncommitted work**: Existing system-skill edits can be overwritten accidentally. Mitigation: inspect current diffs before each affected file and patch the working-tree version in place.

## Migration Plan

1. Add failing validator fixtures for each current-template rule and each excluded file role.
2. Inventory active pages from the manifest and record all old-template and loose-Guardrails findings.
3. Migrate the 19 core skills and active subpages, preserving current uncommitted content.
4. Migrate the 22 DeepSci skills and active subpages without editing their `org/`, `migrate/`, or template assets.
5. Migrate the 14 Kaoju skills and pipeline command pages.
6. Run template validation after each group, then run the full repository lint, typecheck, and unit-test commands.
7. Review the final diff for trigger, command, link, output-contract, and domain-language drift.

Rollback is file-level through ordinary version-control review. Because this change alters packaged prose and validation only, no persisted data or runtime state migration is required.

## Open Questions

None. The guide history, packaged manifest, active/passive file roles, and current repository validation surfaces provide enough information to implement the migration without choosing new product behavior.
