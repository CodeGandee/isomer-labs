## Context

The `isomer-op-topic-creator` skill is the front door for creating Research Topics for manual research. Its `create-research-intent` subcommand currently writes `topic.intent.overview` (`topic-overview.md`) as an ad hoc Markdown file covering the research topic, goals, scope, metrics, datasets, repositories, tools, assumptions, open questions, and source material. There is no canonical template and no user-facing subcommand to refine an existing intent interactively.

A rich research-topic template already exists at `tests/topics/topic-template.md`. It structures a topic as a mini research proposal with sections such as Abstract, Introduction and Background, Research Objective, Literature and Prior Work, Methodology and Research Design, Expected Outcomes, Additional Requirements, and Related Links. Making this template the canonical source skeleton for `topic-overview.md` gives later stages (topic env setup, actor setup, team specialization) a predictable, richer starting point.

## Goals / Non-Goals

**Goals:**
- Make `tests/topics/topic-template.md` the canonical template for `topic.intent.overview` inside the Topic Creator skill.
- Update `create-research-intent` to populate `topic-overview.md` from the template, stripping example blocks and leaving empty headings for sections it cannot fill.
- Add a user-facing `clarify-research-intent` subcommand that interactively refines an existing `topic-overview.md` by walking the template sections.
- Keep automatic flows (`fast-forward`, `run-to`, default bare dispatch) unchanged; `clarify-research-intent` is interactive-only.
- Keep validation and packaged system-skill assets consistent with the new skill files.

**Non-Goals:**
- Change `isomer-op-topic-team-specialize` or its `clarify-topic` behavior.
- Enforce that every template section must be filled before a topic can proceed.
- Introduce a new system-wide semantic label or storage profile.
- Migrate existing `topic-overview.md` files automatically.

## Decisions

### Template location: `templates/topic-overview.md` inside the skill dir

A dedicated `templates/` directory keeps templates separate from reference documentation and subcommand pages. The existing `_copy_resource_tree` helper in `isomer_labs.skills.system_assets` copies the entire skill directory, so the template will be included in packaged assets without extra code.

Alternative: place the template under `references/topic-overview-template.md`. Rejected because it would require either adding it to the validator's command list or adding a special-case exemption, and it conflates user-facing reference pages with internal templates.

### `create-research-intent` populates the full skeleton, leaving Additional Requirements as a placeholder

When creating or refreshing `topic-overview.md`, `create-research-intent` will write every template section heading. Sections it has substance for are filled; sections it lacks substance for are kept as empty headings. This gives users a complete, editable skeleton and makes `clarify-research-intent` scanning straightforward.

Exception: the `## Additional Requirements` section and its `### Preferences` and `### Constraints` subsections are always left in a placeholder state. These capture topic-specific user preferences and hard boundaries that are best supplied or confirmed by the user rather than inferred from the initial prompt. `clarify-research-intent` can later guide the user through filling them.

Alternative: write only filled sections. Rejected because an empty heading is a clearer signal of a gap than a missing section, and it matches the template's own structure.

### Strip `> Example:` blocks from generated files

The source template uses `> Example:` blocks as inline author guidance. These are helpful in the template but noisy in a concrete topic file. `create-research-intent` will omit them when populating the overview.

### `clarify-research-intent` is a Misc subcommand

It is interactive, so it belongs with `help`, `fast-forward`, `step-by-step`, `run-to`, `status`, and `repair` rather than with automatic procedural subcommands. It will not be a valid target for `run-to` and will not appear in `fast-forward` or `step-by-step` workflows.

### Clarification loop mirrors `clarify-topic` but stays template-scoped and human-in-the-loop

The new subcommand will use a coverage scan, a ranked question queue, one-question-at-a-time interaction, option tables for meaningful choices, and direct updates to `topic-overview.md`. This matches the proven pattern in `isomer-op-topic-team-specialize/references/clarify-topic.md`, but the scan categories are aligned with the Topic Creator template sections and the agent resolves gaps by asking the user rather than inferring answers.

Coverage categories for `clarify-research-intent`:

| Category | What to Check |
| --- | --- |
| Research Topic | Is the concrete research question or investigation intent specific enough to guide later work? |
| Abstract | Does the overview summarize what the topic studies, why it matters, and the expected result? |
| Introduction and Background | Is the practical or scientific context clear enough for an unfamiliar reader? |
| Research Objective | Are the primary and supporting objectives observable, and is the research gap explicit? |
| Literature and Prior Work | Are the anchoring papers, repositories, benchmarks, or standards named? |
| Methodology and Research Design | Is the planned approach, evidence source, and validation method described enough to start setup? |
| Expected Outcomes | Are the expected outputs and why they matter stated? |
| Additional Requirements | Are topic-specific preferences and constraints (`should`/`must`) captured? |
| Related Links | Are relevant references listed when known? |
| Open Questions | Do open questions affect scope, methodology, or setup rather than minor prose polish? |

For each Partial or Missing category, the agent adds a candidate question only when the answer would materially change `topic-overview.md` or determine whether later initialization stages can proceed. It ranks questions by impact and uncertainty, asks at most five per session, and keeps lower-priority ambiguity in `## Open Questions`.

Every question includes Motivation, Example, Proposed, and Implication. The user may answer with an option letter, `yes`, `proposed`, or a custom answer. The agent integrates accepted answers directly into the relevant template section and stops when the topic is actionable, the user signals completion, or the session question limit is reached.

### Validation updated in `scripts/validate_skillsets.py`

`clarify-research-intent.md` must be added to `TOPIC_CREATOR_COMMANDS` and `TOPIC_CREATOR_REFERENCE_REQUIRED_TERMS` so the skill validator recognizes the new reference page and enforces required content.

## Risks / Trade-offs

- **[Risk] Two clarification paths for the same file.** `isomer-op-topic-team-specialize/clarify-topic` and the new `clarify-research-intent` both edit `topic.intent.overview`.
  - **Mitigation:** Keep `clarify-research-intent` scoped to the Topic Creator template and the early initialization ladder; `clarify-topic` remains a team-specialization concern. Document the boundary in both skills.

- **[Risk] Existing overviews do not match the new template.** `clarify-research-intent` will see them as having many missing sections and may over-prompt.
  - **Mitigation:** `clarify-research-intent` ranks questions by impact and asks at most a bounded number per session; lower-priority gaps stay in `## Open Questions`.

- **[Risk] Packaged assets drift from skillset sources.** The validator currently checks `skillset/operator/isomer-op-topic-creator/`; the packaged copy under `src/isomer_labs/assets/system_skills/` must be kept in sync manually.
  - **Mitigation:** Mirror every skill file change into the packaged assets and run `pixi run test` before archiving.

## Migration Plan

No runtime migration is required. The change adds a template and a subcommand; existing topic overview files remain valid. After implementation:

1. Run `pixi run lint`.
2. Run `pixi run typecheck`.
3. Run `pixi run test`.
4. Run `python scripts/validate_skillsets.py`.
5. Run `openspec verify-change add-topic-overview-template-and-clarify-research-intent` after implementation.

Rollback: remove the new template and reference page, revert edits to `SKILL.md`, `help.md`, `run-to.md`, `fast-forward.md`, and `create-research-intent.md`, and revert validator updates.

## Open Questions

- Should the template's `> Example:` blocks be preserved anywhere, such as in a separate `templates/topic-overview-guide.md`, or are they only useful in `tests/topics/topic-template.md`?
- Should `finalize` later validate that `topic-overview.md` contains at least the `## Research Topic` and `## Research Objective` sections, or remain agnostic to section presence?
