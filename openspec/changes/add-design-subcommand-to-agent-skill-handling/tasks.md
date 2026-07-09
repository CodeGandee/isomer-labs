## 1. Skill Entrypoint Updates

- [x] 1.1 Update `imsight-agent-skill-handling/SKILL.md` frontmatter description to mention the `design` subcommand.
- [x] 1.2 Update `imsight-agent-skill-handling/SKILL.md` Subcommands table to include `design` with purpose and `references/design.md` load target.
- [x] 1.3 Update `imsight-agent-skill-handling/SKILL.md` Workflow step 2 to include `design` in the list of subcommands that resolve a target skill folder or task input.
- [x] 1.4 Update `imsight-agent-skill-handling/SKILL.md` Overview to describe `design` as a planning stage between `deep-inspect` and `create`.

## 2. Design Subcommand Reference

- [x] 2.1 Create `imsight-agent-skill-handling/references/design.md` with a `## Workflow` section.
- [x] 2.2 Define intent capture rules in `references/design.md`, mirroring `references/create.md` but without file-writing steps.
- [x] 2.3 Define the default multi-subcommand design rule and when to override it with a single-command design.
- [x] 2.4 Define the output location contract in `references/design.md`: explicit path, `IMSIGHT_SKILL_OUTPUT_DIR`, then `.imsight-arts/skill-designs/<slug>/design-overview.md`.
- [x] 2.5 Define the `design-overview.md` document template in `references/design.md`, adapted from `references/deep-inspect.md`.
- [x] 2.6 Define validation rules in `references/design.md` for the generated design document.
- [x] 2.7 Define the chat output contract in `references/design.md`.

## 3. Design Document Template Content

- [x] 3.1 Include Purpose, Proposed File Inventory, Concepts, High Level Process, Skill Call Graph, Formal Skill Process, Skill Process Explanation, Evidence Handoffs, and Open Questions sections.
- [x] 3.2 Include a draft `SKILL.md` section following the format rules from `references/create.md`.
- [x] 3.3 Include an example warning near any user/AI chat examples, consistent with the `create.md` guidance.

## 4. Validation and Testing

- [x] 4.1 Run any available skill validator on `imsight-agent-skill-handling` after edits. (No `skill-creator/scripts/quick_validate.py` found in the project; verified manually instead.)
- [x] 4.2 Verify that `SKILL.md` frontmatter, subcommand table, and workflow remain internally consistent.
- [x] 4.3 Verify that `references/design.md` has a `## Workflow` section and ends with a freeform fallback.
- [x] 4.4 Verify that `design` is reachable through the invocation contract (`use design`, task-only form, and `help` listing).

## 5. Documentation and Handoff

- [x] 5.1 Update `imsight-skills/README.md` Skill Index entry for `imsight-agent-skill-handling` if the description there needs to reflect the new subcommand.
- [x] 5.2 Run `openspec validate add-design-subcommand-to-agent-skill-handling --strict` and fix any artifact or spec issues.
- [ ] 5.3 Commit the OpenSpec change artifacts and the skill edits with a clear Conventional Commit message.
