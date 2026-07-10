---
name: isomer-kaoju-reproduce
description: Use when a user wants first-hand numbers for one paper method through intended data, or a rough generated-data capability probe when the intended dataset is impractical.
---

# Kaoju Reproduce

## Overview

Run one bounded paper-method trial while preserving faithful, adapted, repaired, failed, and generated-input evidence as different outcomes. A capability probe explains behavior under its generated inputs; it is not reproduction.

## Workflow

1. **Accept the trial contract**. Require the paper and code Source Identities, route, target claim, inputs, evaluator, desired metrics, resources, and stop conditions.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-reproduce --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Check materials and data**. Query the Topic Dataset Manifest first; verify code, data or generation plan, model, evaluator, environment, license, access, and Gate posture.
4. **Freeze execution identity**. Pin paper, code revision, dataset or Generated Dataset Artifact, model, evaluator, environment, command, seeds, resources, and expected raw outputs.
5. **Route preparation and execution**. Use existing environment, provider, execution, and Gate owners; use bounded-run guidance for resource-heavy work.
6. **Preserve attempts**. Record upstream-faithful, adapted, repaired, failed, blocked, and probe Runs separately with patches, logs, outputs, purpose, fidelity, input basis, and quality checks.
7. **Interpret within scope**. Compare intended-data results only to compatible paper claims; describe generated-data results only as `capability-probe` evidence at no stronger than `executed` depth.
8. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-reproduce --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
9. **Return status**. Produce a Method Trial Artifact, Run and Finding refs, failures, limitations, and a resume point.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## When to Use

Use for one method when the user asks to obtain executable materials and see first-hand numbers, including an explicit generated-data rough probe. Do not use for a source-only assessment, a multi-method empirical comparison, silent environment repair, or an unbounded optimization campaign.

## Trial Routes

| Route | Contract |
| --- | --- |
| Intended data | Use the paper's intended task, data, split, evaluator, and metric semantics where available; report deviations and comparable paper numbers. |
| Generated data | Create a Generated Dataset Artifact with generator, schema, size, seeds, assumptions, checks, and limitations; label every resulting Run `capability-probe`. |

An authorized patch creates a new repaired or adapted Run. It does not change the verdict of the upstream-faithful attempt. Reimplementation records the mapped specification, omissions, tests, and fidelity limits.

## Reference Routing

Use `$isomer-kaoju-shared` for evidence, Generated Dataset Artifact, lineage, Gate, owner, and terminal contracts. Use `$isomer-kaoju-acquire` for pinned materials, the applicable environment skill for preparation, and `$isomer-misc-bounded-run-tips` before resource-heavy execution.

## Foundational Principle

Numbers carry the identity of the code, inputs, evaluator, environment, and execution route that produced them. Changing any of those may create useful evidence, but it creates different evidence.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The repair is trivial.” | Record the patch and run it as a separate repaired attempt. |
| “Synthetic inputs are close enough.” | Label them generated and limit the claim to capability under those inputs. |
| “One successful output proves reproduction.” | Check the accepted metric, evaluator, quality, and paper-claim compatibility. |

## Red Flags

- A Run lacks immutable code, input, evaluator, or environment identity.
- Paper numbers and generated-input numbers share an unlabeled table.
- A failure disappears after a repaired Run succeeds.

## Common Mistakes

- Asking for a dataset before checking registered data. Query and validate the Topic Dataset Manifest first.
- Running setup commands outside the owner or resource boundary. Route them and retain logs.
- Calling a smoke test a benchmark. Record the actual Run purpose and achieved depth.
