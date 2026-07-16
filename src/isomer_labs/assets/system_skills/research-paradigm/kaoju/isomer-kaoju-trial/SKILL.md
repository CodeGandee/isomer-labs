---
name: isomer-kaoju-trial
description: Use when a Kaoju source-code method needs governed environment preparation, a task-critical smoke check, or one separately approved bounded code trial.
---

# Kaoju Trial

## Overview

Prepare a governed Pixi environment and run one approved bounded code trial while preserving exact source, environment, data, command, Gate, and attempt evidence.

Portfolio reminder: a method, wrapper, patch, environment, trial attempt, metric, or result is not a Research Idea. When an accepted terminal trial directly changes exploration or evidence assessment for an existing direction, invoke `$isomer-research-idea-recording` and record an explicit transition with the exact Artifact, Evidence Item, Finding, Research Task, and Run refs. Leave decision state unchanged without a separate decision.

## When to Use

Use for `prepare-code-run`, `run-code-trial`, bounded capability probes, and approved method trials. Use `$isomer-kaoju-reproduce` only when the claim is genuine reproduction and the stronger fidelity contract can be met.

## Workflow

1. **Resolve prerequisites**. Query Workspace Runtime by semantic id and scope for the registered repository semantic label, caller-observed immutable commit or digest, associated paper, accepted source digest, data posture, and current environment evidence. Never scan directories to guess durable state or infer repository identity from a checkout.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-trial --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Plan environment support**. Record `KAOJU:ENV-PREP-PLAN` with flexible dependency intent, task-critical path, candidate Pixi environments, risks, authorization, and expected smoke outputs.
4. **Open a Service Request**. Use `isomer-cli project service-requests create` and synchronous `dispatch` for Pixi, lock, smoke, or managed environment repair. Preserve the Service Request, command request, support Artifact, Gate, and Run refs. If repository source work is still required, return to `$isomer-kaoju-acquire`; its user-supplied or agent-selected repository commands run externally before verification, semantic registration, and Artifact recording.
5. **Require readiness evidence**. Accept `KAOJU:PIXI-ENV-REF` only with exact resolved packages and lock identity. Require a durable `KAOJU:SMOKE-RUN-SCRIPT`, `KAOJU:SMOKE-RUN-RESULT`, and successful task-critical observation before marking the environment ready.
6. **Plan the trial**. Record `KAOJU:METHOD-TRIAL-PLAN` with source, environment, data, wrapper, upstream entry point or smallest adaptation, evaluator, metrics, resources, fidelity target, limitations, and expected outputs. After approval, register the minimal wrapper itself as file-backed `KAOJU:METHOD-TRIAL-WRAPPER` state before execution.
7. **Pause at the human Gate**. Present the exact plan and wait. Rejection ends the Run without execution.
8. **Execute through the adapter**. Begin a new Run and send the approved command through the `code_trial` Research Operation Extension Point. Never use an ambient environment or make a source-tree, staged execution copy, or Local Tmp Surface the canonical wrapper or result.
9. **Record immutable outcomes**. Create distinct `KAOJU:METHOD-TRIAL-RUN` and `KAOJU:METHOD-TRIAL-RESULT` Artifacts with source commit, environment, data, logs, outputs, timing, resources, adaptations, checks, verdict, verification depth, and limitations.
10. **Classify retries**. An identical transient retry may proceed within the recorded attempt bound. Any dependency, lock, commit, patch, data, wrapper semantics, evaluator, metric, resource, canonical interpretation, or fidelity change requires a revised plan and another human Gate. Preserve every attempt.
11. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-trial --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
12. **Return terminal state**. Report completed refs, failures, blocker and Service Request refs, pending Gate, and the first incomplete stage as the resume point.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Artifact Operations

Resolve each contract with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`. Persist accepted output only through `project artifacts put` or `revise`; the service infers record kind, profile, semantic label, content mode, scope policy, and managed locator. Read `artifact-bindings.md`, `references/trial-contract.md`, `references/retry-and-repair.md`, and `$isomer-kaoju-shared` before mutation.

## Reference Routing

Use `$isomer-kaoju-shared` for evidence, Artifact, Gate, Service Request, execution request, lineage, and terminal contracts. Use `$isomer-kaoju-reproduce` only for a genuine reproduction claim.

## Operational Notes

- Record `purpose: capability-probe` and no stronger than executed verification depth.

## Guardrails

- DO NOT call random-data output a reproduction.
- DO NOT edit dependencies during an approved trial without revising the plan and Gate.
- DO NOT replace a failed faithful attempt with a repaired result.
- DO NOT treat smoke success as the code-trial verdict.

## Chat Response

Present normal chat responses in natural-language Markdown. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat. Lead with the outcome. Name every Run, Gate, Service Request, blocker, and resume ref that affects the result.
