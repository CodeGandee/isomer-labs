## Context

The Imsight skillset under `extern/orphan/houmao-agents/skillset/imsight-skills/` contains 13 skills. The skill-creation reference `imsight-agent-skill-handling/references/create.md` now defines `## Guardrails` as a required section written with "DO NOT ..." and "MUST ..." rules, and a separate `## Troubleshooting Guide` section for execution problems and recovery actions. However, most existing skills still use `## Common Mistakes`, and two skills (`imsight-autodev-master` and `imsight-autodev-slave`) contain both `## Guardrails` and `## Common Mistakes` with overlapping content. This inconsistency weakens the behavioral guidance agents receive when invoking these skills, and conflates prohibited behavior with recovery guidance.

## Goals / Non-Goals

**Goals:**

- Every Imsight skill in the target directory has exactly one `## Guardrails` section.
- All guardrail bullets follow the "DO NOT ..." or "MUST ..." format.
- Guardrail lists are sparse, concise, and limited to rules that protect the skill's design intent.
- Every skill has a `## Troubleshooting Guide` section containing nested problem-and-recovery guidance where execution problems exist.
- No `## Common Mistakes` headings remain in the skillset after the update.

**Non-Goals:**

- Changing skill frontmatter, workflow structure, subcommand structure, or bundled resources.
- Adding new functionality, scripts, or references.
- Updating the top-level `style-guide.md` or `README.md` unless they explicitly reference `Common Mistakes`.
- Running pressure tests or full skill validation suites.

## Decisions

- **Convert, do not just rename.** Existing `Common Mistakes` bullets will be rewritten as guardrails. Positive anti-patterns will be expressed as "DO NOT ..."; required behaviors implied by the mistakes will be expressed as "MUST ...".
- **Separate recovery guidance from guardrails.** Any `Common Mistakes` item that describes a problem and a recovery action rather than a design-intent violation will move to `## Troubleshooting Guide`.
- **Merge dual sections in autodev skills.** `imsight-autodev-master` and `imsight-autodev-slave` already have both sections. The two sections will be merged into a single `## Guardrails` section, removing duplicates and preserving unique intent.
- **Preserve nearby sections.** Sections such as `## Quality Bar`, `## Maintenance`, or `## When to Use` will remain unchanged unless their content clearly belongs under Guardrails or Troubleshooting Guide.
- **No mechanical blanket rename.** Each skill will be reviewed individually to ensure converted guardrails and troubleshooting entries still match the skill's actual design intent.

## Risks / Trade-offs

- **Loss of nuance** — Some `Common Mistakes` items include explanatory context that may be lost when compressed to "DO NOT ...". Mitigation: keep a short explanatory clause after the rule when the action alone is ambiguous, but stay within the concise bullet format.
- **Recovery guidance misclassified** — A problem-and-recovery item might be wrongly placed under Guardrails instead of Troubleshooting Guide. Mitigation: ask "Is this a prohibited/required behavior, or a fix for an execution problem?" for every bullet.
- **False positives** — A rule that is valid for one skill may be copied incorrectly to another. Mitigation: review each skill's workflow and purpose before finalizing its guardrails.
- **Scope creep** — It is tempting to also refactor workflow wording or add new sections while editing. Mitigation: restrict edits to the `## Guardrails`, `## Troubleshooting Guide`, and `## Common Mistakes` conversion.
