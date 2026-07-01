---
name: isomer-rsch-workspace-mgr-v2
description: Use after Topic Team Specialization has written the final topic summary and Topic Workspace initialization is ready to prepare v2 research placeholder binding, semantic record surfaces, agent access posture, and bootstrap readiness before ordinary v2 research skills write durable outputs.
---

# Isomer Research Workspace Mgr V2

## Overview

Workspace manager prepares the research-facing contract that v2 skills use after the topic team is specialized. It first detects Topic Workspace readiness from the final topic-team summary and a small set of fresh semantic checks, then verifies that the selected Research Topic, Topic Workspace, Workspace Runtime, topic-team profile material, and Agent Workspace context are ready enough for research placeholder outputs to land in durable topic-owned surfaces or become explicit blockers.

Placeholder definitions live in `migrate/placeholders.md`.

## When to Use

Use this skill when:

- Topic Team Specialization has produced `isomer-topic-summary.md` and the team is about to start ordinary v2 research work.
- A Topic Service Master, Project Operator Session, or Operator Agent needs to verify where v2 placeholder outputs should be routed.
- Working agents need an access plan for `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.links`.
- A v2 research skill is blocked because semantic record surfaces, placeholder binding, generated links, or pre-promotion rules are unclear.

Do not use this skill when:

- The task is only operator topology inspection, branch helper work, or legacy diagnostics. Use `isomer-admin-topic-workspace-mgr` for that boundary.
- The selected Topic Workspace lacks `isomer-topic-summary.md`, has only provisional registration evidence, or reports blocked/not-checked topic-team validation. Route back to `isomer-admin-topic-team-specialize` or the relevant setup service first.
- Topic environment setup, Topic Main Development Repository setup, projection materialization, or Agent Workspace cwd proof has not completed. Route that work to the setup services first.
- The user is asking for domain research work such as scouting, baseline selection, idea generation, experiment execution, analysis, writing, review, rebuttal, or finalization.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Confirm bootstrap entry**. Build <RSCH_WORKSPACE_CONTEXT> from minimal readiness signals: final topic summary, registered topic and workspace refs, topic-team validation status, Workspace Runtime readiness, topic-team profile material, Agent Workspace context, and actor identity. Read `references/bootstrap-workflow.md`.
2. **Inspect semantic surfaces**. Build <RSCH_STORAGE_LABEL_PLAN> by checking existing topic record labels, planned evidence/provenance/package labels, optional `custom.*` needs, and missing support. Read `references/semantic-surface-plan.md`.
3. **Bind v2 placeholders by kind**. Produce <RSCH_PLACEHOLDER_BINDING_REGISTRY> from the v2 placeholder kind table and the active skill set, preserving exact placeholder names as metadata. Read `references/placeholder-binding-registry.md`.
4. **Prepare agent access**. Produce <RSCH_AGENT_ACCESS_PLAN> for working-agent pre-promotion surfaces, generated conveniences, and promotion boundaries. Read `references/agent-access-plan.md`.
5. **Record bootstrap result**. Produce <RSCH_STORAGE_BOOTSTRAP_RECORD> when the contract is usable, <RSCH_BOOTSTRAP_VALIDATION_REPORT> for readiness checks, or <RSCH_WORKSPACE_BLOCKER_RECORD> when required support is missing. Read `references/validation-and-blockers.md`.
6. **Return next route**. Hand control to the selected v2 research skill only after the bootstrap outputs name durable semantic targets or explicit blockers.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/bootstrap-workflow.md` for minimal Topic Workspace readiness detection, entry conditions, actor fallback, and the post-specialization sequence.
- `references/semantic-surface-plan.md` for existing topic record labels, planned evidence/provenance/package labels, and `custom.*` escalation.
- `references/placeholder-binding-registry.md` for mapping v2 placeholder kinds to semantic targets while preserving placeholder names.
- `references/agent-access-plan.md` for Agent Workspace pre-promotion surfaces, generated links, and promotion boundaries.
- `references/validation-and-blockers.md` for readiness checks, bootstrap reports, validation output, and blocker records.

## Cross-Step Quality Gates

### Metrics

- Readiness-signal coverage: fraction of final topic summary, registered topic and workspace refs, topic-team validation status, Workspace Runtime readiness, topic-team profile material, Agent Workspace context, and actor identity checked before bootstrap; higher is better.
- Unbound placeholder-kind count: number of v2 placeholder kinds that lack a semantic target, access rule, planned support label, or explicit blocker in <RSCH_PLACEHOLDER_BINDING_REGISTRY>; lower is better.

### Checks

- Entry check: <RSCH_WORKSPACE_CONTEXT> confirms the Topic Workspace is post-specialization-ready using the minimal readiness signals rather than broad fragile file detection.
- Surface check: <RSCH_STORAGE_LABEL_PLAN> distinguishes existing labels, planned labels, optional `custom.*` needs, and missing support.
- Binding check: <RSCH_PLACEHOLDER_BINDING_REGISTRY> maps v2 placeholder kinds to semantic targets while preserving exact placeholder names as metadata.
- Access check: <RSCH_AGENT_ACCESS_PLAN> tells working agents where pre-promotion outputs belong and how to cite durable semantic refs.
- Validation check: <RSCH_BOOTSTRAP_VALIDATION_REPORT> states whether the v2 research loop can start, or <RSCH_WORKSPACE_BLOCKER_RECORD> names what must be prepared first.
- Route check: the next v2 research skill is invoked only after durable semantic targets or explicit blockers are recorded.

## Exit Criteria

This skill can end only when all applicable checks are true:

- <RSCH_WORKSPACE_CONTEXT> identifies the Topic Workspace, final topic summary, actor, runtime readiness, topic-team profile material, and Agent Workspace context used for bootstrap.
- <RSCH_STORAGE_LABEL_PLAN> distinguishes existing semantic labels, planned labels, optional `custom.*` labels, and missing support.
- <RSCH_PLACEHOLDER_BINDING_REGISTRY> maps v2 placeholder kinds to semantic targets without forcing hard-coded paths.
- <RSCH_AGENT_ACCESS_PLAN> tells working agents where pre-promotion outputs belong and how durable refs should be cited.
- <RSCH_BOOTSTRAP_VALIDATION_REPORT> says the v2 research loop can start, or <RSCH_WORKSPACE_BLOCKER_RECORD> states what must be prepared first.

## Common Mistakes

- Treating this skill as a replacement for Topic Team Specialization or environment setup.
- Treating `isomer-admin-topic-workspace-mgr` as the owner of v2 placeholder binding.
- Requiring a Topic Service Master when the Project Operator Session or Operator Agent can perform the same bounded bootstrap work.
- Inventing hard-coded paths when a semantic label, typed ref, or blocker is required.
- Letting working agents cite generated links instead of semantic labels and typed refs.
