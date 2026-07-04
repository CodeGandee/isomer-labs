## Context

The Topic Creator skill currently uses a research-proposal-style template with sections such as Abstract, Introduction and Background, Research Objective, Literature and Prior Work, Methodology and Research Design, Expected Outcomes, Additional Requirements, and Related Links. The source file `tests/topics/topic-template.md` has been rewritten into a lighter, directive-focused template with sections `Research Topic`, `Motivation`, `Topic Breakdown` (`Do's`/`Don'ts`), `Expected Outcome`, and `Related Links`.

Because `tests/topics/topic-template.md` is the intended source of truth, the skill's bundled template and the subcommands that read and write `topic.intent.overview` must follow it.

## Goals / Non-Goals

**Goals:**
- Replace the skill's `templates/topic-overview.md` with the updated `tests/topics/topic-template.md` content.
- Update `create-research-intent` to populate the new sections and strip the updated `> Example:` blocks.
- Update `clarify-research-intent` coverage categories to match the new template.
- Keep validation and tests passing.

**Non-Goals:**
- Change the default bare dispatch target (still `define-topic-env`).
- Add new subcommands or semantic labels.
- Migrate existing overview files.

## Decisions

### Replace the template in place

The skill template is a direct copy of `tests/topics/topic-template.md`. We overwrite rather than version because the skill is expected to track the latest source template.

### Keep example blocks in the source but strip them on population

`tests/topics/topic-template.md` uses `>` blocks as inline examples. `create-research-intent` will strip any line starting with `>` when writing a concrete overview, just as it did with the old `> Example:` blocks.

### Update coverage scan categories

`clarify-research-intent` will scan: Research Topic, Motivation, Topic Breakdown (Do's and Don'ts), Expected Outcome, Related Links.

## Risks / Trade-offs

- **[Risk] Existing overviews use the old section names.** `clarify-research-intent` will see all new-template sections as Missing for old files.
  - **Mitigation:** This is expected; the subcommand is interactive and will ask the user to fill gaps only when they invoke it.

## Migration Plan

1. Overwrite the skill template.
2. Update `create-research-intent.md`, `clarify-research-intent.md`, `SKILL.md`, `help.md`.
3. Update `scripts/validate_skillsets.py` and unit test fixtures.
4. Run `pixi run lint`, `pixi run typecheck`, `pixi run test`.

Rollback: restore the previous template and revert the reference page edits.

## Open Questions

- Should `clarify-research-intent` treat empty `Do's`/`Don'ts` subsections as one gap or two separate gaps?
