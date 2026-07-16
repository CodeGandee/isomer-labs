---
name: isomer-kaoju-compare
description: Use when named works need a theory comparison, an empirical Comparison Intent Document, or controlled actual-run comparison with fairness and uncertainty limits.
---

# Kaoju Compare

## Overview

Compare only on dimensions or measurements whose definitions and evidence are explicit. Theory mode remains source-grounded; empirical mode requires an accepted Comparison Intent Document and Proceed Decision.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `KAOJU:THEORY-COMPARISON`, `KAOJU:COMPARISON-MATRIX`, and `KAOJU:COMPARISON-RUN` exactly. Return a storage blocker rather than inventing a path, profile, direct Markdown state, or untracked JSON.

## When to Use

Use for theory comparison of selected works, preparation of an actual-run comparison plan, or execution of an accepted empirical comparison. Do not use for a broad survey, a single-method trial, ranking based only on reported headline numbers, or candidate preparation before user approval.

## Workflow

1. **Select comparison mode**. Require named candidate Source Identities, target question, accepted source evidence, and either theory intent or empirical intent.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-compare --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Derive the comparison contract**. Define domain-relevant dimensions or metrics, rationale, applicability, evaluator semantics, fairness rules, exclusions, and desired evidence depth; perform bounded reference discovery when the domain basis is unclear.
4. **Apply the intent checkpoint for empirical mode**. Present candidate readiness, prior-evidence reuse, acquisition, environment, reproduce or reimplement routes, datasets, metrics, resources, Gates, and unresolved choices; wait for a Proceed Decision.
5. **Build theory evidence or prepare eligible candidates**. In theory mode, inspect exact source locators; in empirical mode, query registered datasets first and route governed preparation.
6. **Execute empirical mode**. Run eligible candidates under the accepted Comparison Contract and retain Run, raw-output, environment, input, evaluator, adaptation, and quality-check refs.
7. **Assemble the matrix**. Report source cells or measurements, variability or uncertainty, contradictions, missing states, and `not-comparable` where normalization changes task or quality semantics.
8. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-compare --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
9. **Return status**. Produce a Theory Comparison Artifact or empirical Comparison Matrix with evidence refs, limits, failures, and a resume point.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Comparison Modes

### Theory Mode

Each dimension has a definition, relevance rationale, applicability rule, and source basis. Every candidate cell cites an exact source locator or records `not stated`, `not applicable`, `unclear`, or `disputed`. Its verification depth remains source-inspected, never empirical `compared`.

### Empirical Intent Mode

The Comparison Intent Document records what the user wants, candidate identity and readiness, existing reproduced evidence, required source, model and data acquisition, environment and reimplementation needs, metrics, evaluator, fairness, repetitions, uncertainty, resources, Gates, and unresolved decisions. Ask: “Do you want to clarify for more detail, or proceed?”

## Artifact Operations

Resolve `KAOJU:THEORY-COMPARISON`, `KAOJU:COMPARISON-MATRIX`, and `KAOJU:COMPARISON-RUN` through `ext kaoju bindings describe KAOJU:WHAT`. Persist accepted comparison outputs only through typed `project artifacts put` or binding-permitted `revise`; keep each execution attempt in a distinct immutable Run.

### Empirical Results Mode

Each measurement links to the Run, immutable inputs, environment, metric definition, evaluator, quality checks, adaptations, and raw outputs. Report dispersion or repeated-run limits; use `not-comparable` when fair normalization would erase meaningful task or quality differences.

## Reference Routing

Use `$isomer-kaoju-shared` for evidence, comparison Artifact, interaction, lineage, Gate, and terminal contracts. Use `$isomer-kaoju-examine` for missing source bases, `$isomer-kaoju-reproduce` for single-candidate readiness, and the applicable owner skills for data, environment, and execution.

## Foundational Principle

A complete-looking matrix is weaker than an honest sparse one if its cells hide missing evidence or incompatible semantics.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “These are standard comparison dimensions.” | Define and source why each dimension matters here. |
| “All papers report accuracy.” | Verify dataset, split, evaluator, preprocessing, and metric semantics. |
| “We can normalize incompatible candidates.” | Use `not-comparable` when normalization changes the studied task or quality. |

## Red Flags

- Empirical work begins before a Proceed Decision.
- Theory cells receive `compared` verification depth.
- A single number has no variability statement or reason it is unavailable.

## Operational Notes

- Start from the domain question and accepted source basis.
- Preserve their state.

## Guardrails

- DO NOT let source availability determine the dimensions.
- DO NOT rank unclear or disputed cells.
- DO NOT reuse old Runs without verifying their identities and Comparison Contract compatibility.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
