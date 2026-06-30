## 1. Skill Entrypoint Policy

- [x] 1.1 Add a shared targeted fast-forward recovery section to `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md`.
- [x] 1.2 Define inclusive targeted fast-forward as the default mode that runs missing predecessor stages and then the selected subcommand.
- [x] 1.3 Define exclusive targeted fast-forward as the alternative mode that runs missing predecessor stages and stops before the selected subcommand.
- [x] 1.4 Distinguish targeted fast-forward from the existing full `fast-forward` mode that runs through `finalize-topic-team`.
- [x] 1.5 Update the missing-predecessor guardrail so blocked subcommands offer targeted recovery instead of only refusing and naming earlier commands.

## 2. Subcommand Recovery Wording

- [x] 2.1 Update `references/fast-forward.md` to describe targeted fast-forward inputs, target bounds, inclusive default behavior, and exclusive stop-before-target behavior.
- [x] 2.2 Update prerequisite failure text in `references/adapt-team-template.md` to offer targeted fast-forward recovery when topic intent or registration evidence is missing.
- [x] 2.3 Update prerequisite failure text in `references/setup-topic-env.md` to offer targeted fast-forward recovery when registration, binding, or topic env source intent is missing and recoverable.
- [x] 2.4 Update prerequisite failure text in `references/resolve-topic-env-gate.md` and `references/resolve-agent-env-gate.md` to offer targeted recovery for missing predecessor context while preserving clarification blockers.
- [x] 2.5 Update prerequisite failure text in `references/setup-agent-workspace.md` to offer targeted fast-forward recovery for missing registration, topic env evidence, specialization scope, or agent env source intent when recoverable.
- [x] 2.6 Update prerequisite failure text in `references/clarify-topic-team.md`, `references/validate-topic-team.md`, and `references/finalize-topic-team.md` to offer targeted fast-forward recovery when missing predecessors can be produced by the canonical flow.

## 3. User-Facing Examples and Consistency

- [x] 3.1 Add a concise operator response pattern that lists missing prerequisites, the inclusive default path, the exclusive alternative, and the stop option.
- [x] 3.2 Ensure direct natural-language `specialize <team-path> over topic <topic>` requests still route to full `fast-forward`, not to targeted recovery or `adapt-team-template`.
- [x] 3.3 Ensure targeted recovery stops on the same clarification or safety blockers as the normal flow instead of inventing topic substance, runnable requirements, Agent Names, or readiness criteria.

## 4. Validation

- [x] 4.1 Run `openspec validate add-targeted-fast-forward-recovery --strict`.
- [x] 4.2 Run `pixi run python scripts/validate_skillsets.py --scope operator`.
- [x] 4.3 Run `pixi run python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skillset/operator/isomer-admin-topic-team-specialize`.
- [x] 4.4 Run `pixi run python scripts/validate_docs.py` if Markdown structure or generated docs are touched.
