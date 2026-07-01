## Context

The current v2 research-paradigm skills each keep a local `migrate/placeholders.md` registry. Those registries name durable handoff objects with a small shared set of placeholder kinds such as `evidence`, `report`, `handoff`, `decision`, `runtime state`, `draft`, `run record`, `figure`, and `code`. The shared v2 skill still says storage binding is unresolved, and the storage support plan identifies required semantic labels such as `topic.records.evidence`, `topic.records.provenance`, and `topic.records.packages`.

Topic Team Specialization prepares static team profile material and can prepare topic and agent environment readiness, but it does not produce a research-workflow bootstrap packet for v2 skills. The existing `isomer-admin-topic-workspace-mgr` is an operator topology helper and should remain separate from research placeholder and storage binding discipline.

## Goals / Non-Goals

**Goals:**

- Add `isomer-rsch-workspace-mgr-v2` as the v2 research skill that runs after Topic Team Specialization and full Topic Workspace initialization.
- Give the manager a placeholder registry that follows the same naming and table style used by the other v2 skills.
- Make the manager prepare or validate research storage semantic labels, placeholder binding decisions, agent access surfaces, and bootstrap readiness before ordinary v2 research skills write durable objects.
- Update validation so the new v2 skill is expected and its placeholder registry participates in the same checks as other v2 skills.

**Non-Goals:**

- Do not implement the future `project records` command family.
- Do not add new storage labels or runtime tables in this change.
- Do not make `isomer-rsch-workspace-mgr-v2` replace `isomer-admin-topic-workspace-mgr`, `isomer-srv-topic-env-setup`, or `isomer-srv-agent-env-setup`.
- Do not require a running Topic Service Master. The Project Operator Session or Operator Agent can perform the same bounded bootstrap work when the Topic Service Master is absent.

## Decisions

1. Create a research-paradigm v2 skill instead of expanding the operator workspace manager.

The new skill belongs in `skillset/research-paradigm/v2/` because its job is to prepare the research storage contract consumed by `isomer-rsch-*-v2` skills. The operator manager remains responsible for topology inspection, branch helpers, boundary summaries, and legacy diagnostics.

2. Use consistent semantic placeholders rather than per-directory conventions.

The manager will define placeholders such as `<RSCH_WORKSPACE_CONTEXT>`, `<RSCH_STORAGE_LABEL_PLAN>`, `<RSCH_PLACEHOLDER_BINDING_REGISTRY>`, `<RSCH_STORAGE_BOOTSTRAP_RECORD>`, `<RSCH_AGENT_ACCESS_PLAN>`, `<RSCH_BOOTSTRAP_VALIDATION_REPORT>`, and `<RSCH_WORKSPACE_BLOCKER_RECORD>`. These are durable objects, not hard-coded paths. Their `Kind` values will map through the storage item mapping already documented for v2 placeholders.

3. Treat planned labels as explicit blockers when platform support is missing.

The manager may verify existing labels immediately and report missing planned labels such as `topic.records.evidence`, `topic.records.provenance`, and `topic.records.packages`. It should not pretend those labels exist before the storage layer implements them. It can instead produce a label plan and bootstrap blocker that later platform work can resolve.

4. Make Topic Service Master optional.

When available, the Topic Service Master is the natural actor because it starts from the Topic Workspace cwd and manages topic-owned operational surfaces. When it is not started, the Project Operator Session or Operator Agent remains the fallback actor. The skill must name the actor in its bootstrap record and avoid implying that the Topic Service Master is required.

5. Keep validation small and deterministic.

Implementation should update the expected v2 skill list and tests rather than adding a new validator class. The existing placeholder, frontmatter, manifest, workflow, and reference checks should cover the new skill if it follows the same layout.

## Risks / Trade-offs

- Risk: The new skill could be mistaken for a runtime implementation of storage labels. Mitigation: state that it validates and plans labels, and reports blockers for missing platform support.
- Risk: The name overlaps with `isomer-admin-topic-workspace-mgr`. Mitigation: document the boundary in the skill entrypoint and storage plan.
- Risk: Agents may still write paths directly. Mitigation: make the manager produce a placeholder binding registry and agent access plan that tells later skills to use semantic labels and typed refs.
- Risk: Validation could become brittle if the expected v2 list changes often. Mitigation: keep this update aligned with the existing explicit list until the validator is later generalized.
