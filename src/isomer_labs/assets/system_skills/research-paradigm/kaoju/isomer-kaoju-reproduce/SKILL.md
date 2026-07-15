---
name: isomer-kaoju-reproduce
description: Use when a user wants to test a genuine paper reproduction claim under a source-grounded fidelity contract; use only for reproduction and route ordinary trials and generated-data probes to isomer-kaoju-trial.
---

# Kaoju Reproduce

## Overview

Test one bounded paper reproduction claim while preserving upstream-faithful, adapted, repaired, failed, and blocked attempts as different evidence. Reproduction requires the paper's intended task, source identity, data semantics, evaluator, metrics, and a declared fidelity target.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use the legacy-compatible `kaoju:method-trial` result only for a genuine reproduction summary. `$isomer-kaoju-trial` owns trial plans, generated datasets, execution attempts, and trial results. Return a storage blocker rather than inventing persistence; keep material and raw-output bytes behind recorded refs.

## When to Use

Use only when the requested conclusion is genuine reproduction of a source claim and the intended evidence contract can be stated. Do not use for a source-only assessment, smoke test, ordinary code trial, generated-data probe, multi-method empirical comparison, silent environment repair, or unbounded optimization.

## Workflow

1. **Accept the reproduction contract**. Require the paper and code Source Identities, exact target claim, intended task, dataset and split, evaluator, metrics, source command or mapped implementation, fidelity target, resources, and stop conditions.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-reproduce --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Reject non-reproduction routes**. If intended data, evaluator, metric semantics, or an honest fidelity mapping is unavailable, route a bounded observation or generated-data `capability-probe` to `$isomer-kaoju-trial`; do not weaken the reproduction label.
4. **Check materials and data**. Query the Topic Dataset Manifest first; verify code, intended data, model, evaluator, prepared environment, license, access, and Gate posture.
5. **Freeze execution identity**. Pin paper, code revision, dataset, split, model, evaluator, environment lock, command or mapping, seeds, resources, expected raw outputs, and comparison tolerance.
6. **Delegate execution mechanics**. Use `$isomer-kaoju-trial` for the approved plan, durable wrapper, Service Requests, Execution Adapter Command Request, Run checkpoints, attempts, and result Artifacts. Use bounded-run guidance for resource-heavy work.
7. **Preserve fidelity evidence**. Keep upstream-faithful, adapted, repaired, failed, and blocked Runs separate with patches, logs, outputs, purpose, fidelity, input basis, and quality checks. A material repair requires a revised plan and human Gate.
8. **Interpret the reproduction claim**. Compare only compatible results to the exact paper claim. State reproduced, not reproduced, inconclusive, or blocked with the tolerance, deviations, depth, and limitations.
9. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-reproduce --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
10. **Return status**. Produce the reproduction summary, Trial Run and result refs, failures, limitations, and a resume point.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Reproduction Contract

Use the paper's intended task, data, split, evaluator, and metric semantics. Record deviations and their effect on comparability. An authorized patch creates a new repaired or adapted Run; it never changes the verdict of the upstream-faithful attempt. Reimplementation records the mapped specification, omissions, tests, and fidelity limits and cannot claim exact-command fidelity.

## Artifact Operations

Resolve `kaoju:method-trial` through `project artifacts describe`. Persist the compatibility reproduction summary only through `project artifacts put`; all active trial execution records belong to `$isomer-kaoju-trial` and its typed operations.

## Reference Routing

Use `$isomer-kaoju-shared` for evidence, lineage, Gate, owner, and terminal contracts. Use `$isomer-kaoju-acquire` for pinned materials, `$isomer-kaoju-trial` for preparation and execution, and `$isomer-misc-bounded-run-tips` before resource-heavy execution.

## Foundational Principle

Numbers carry the identity of the code, inputs, evaluator, environment, and execution route that produced them. Changing any of those may create useful evidence, but it creates different evidence.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The repair is trivial.” | Record the patch and run it as a separate repaired attempt. |
| “Synthetic inputs are close enough.” | Route to `$isomer-kaoju-trial` as a capability probe; do not call it reproduction. |
| “One successful output proves reproduction.” | Check the accepted metric, evaluator, quality, and paper-claim compatibility. |

## Red Flags

- A Run lacks immutable code, input, evaluator, or environment identity.
- An ordinary or generated-data trial is labeled reproduction.
- A failure disappears after a repaired Run succeeds.

## Guardrails

- DO NOT ask for a dataset before checking registered data. Query and validate the Topic Dataset Manifest first.
- DO NOT run setup commands outside the owner or resource boundary. Route them and retain logs.
- DO NOT call a smoke test a benchmark. Record the actual Run purpose and achieved depth.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
