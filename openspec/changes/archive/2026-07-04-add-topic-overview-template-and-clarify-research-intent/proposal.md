## Why

The `isomer-op-topic-creator` skill currently creates a lightweight `topic-overview.md` without a defined shape, and it has no user-facing way to refine an existing intent. A richer, standardized template already exists at `tests/topics/topic-template.md`. We need to make that template the canonical skeleton for `topic.intent.overview` and add an interactive clarification subcommand so users can fill gaps and sharpen an existing overview before proceeding to environment setup.

## What Changes

- Add `templates/topic-overview.md` to `skillset/operator/isomer-op-topic-creator/` (copied from `tests/topics/topic-template.md`).
- Update `create-research-intent` to populate `topic-overview.md` from the template, filling inferred sections and leaving empty headings for sections that need later input; strip the template's `> Example:` blocks from produced files.
- Add a new user-facing Misc subcommand `clarify-research-intent` with its own reference page; it loads the existing overview, scores each template section as Clear/Partial/Missing, asks one focused question at a time, presents options when meaningful, and updates the file directly.
- Update `SKILL.md`, `references/help.md`, `references/run-to.md`, and `references/fast-forward.md` to document the template and the new subcommand.
- Keep the default bare-topic dispatch stopping at `define-topic-env`; `clarify-research-intent` is never part of automatic flows.
- Update `scripts/validate_skillsets.py` to recognize `clarify-research-intent.md` and the new required terms.
- Mirror all skill changes into the packaged system-skill assets under `src/isomer_labs/assets/system_skills/operator/isomer-op-topic-creator/`.
- **Non-goal**: change `isomer-op-topic-team-specialize` or its `clarify-topic` behavior in this change.

## Capabilities

### New Capabilities

- None. The template is a skill-local artifact; the new subcommand is part of the existing Topic Creator capability.

### Modified Capabilities

- `topic-creator-skill`: requirements change for `create-research-intent` output shape and the addition of the `clarify-research-intent` subcommand.

## Impact

- `skillset/operator/isomer-op-topic-creator/` (new template, new reference page, updated SKILL and references).
- `scripts/validate_skillsets.py` (new allowed command and required-term checks).
- `src/isomer_labs/assets/system_skills/operator/isomer-op-topic-creator/` (mirrored packaged assets).
- Existing `topic-overview.md` files created before this change remain readable; `clarify-research-intent` will treat missing template sections as gaps and offer to fill them.
