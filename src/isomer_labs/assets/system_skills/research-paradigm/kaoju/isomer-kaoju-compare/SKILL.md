---
name: isomer-kaoju-compare
description: Use when named works need a theory comparison, an empirical Comparison Intent Document, or controlled actual-run comparison with fairness and uncertainty limits.
---

# Kaoju Compare

## Overview

Compare only on dimensions or measurements whose definitions and evidence are explicit. Theory mode remains source-grounded; empirical mode requires an accepted Comparison Intent Document and Proceed Decision.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `kaoju:theory-comparison`, `kaoju:comparison-matrix`, and `kaoju:comparison-run` exactly. Return a storage blocker rather than inventing a path, profile, direct Markdown state, or untracked JSON.

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

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## When to Use

Use for theory comparison of selected works, preparation of an actual-run comparison plan, or execution of an accepted empirical comparison. Do not use for a broad survey, a single-method trial, ranking based only on reported headline numbers, or candidate preparation before user approval.

## Comparison Modes

### Theory Mode

Each dimension has a definition, relevance rationale, applicability rule, and source basis. Every candidate cell cites an exact source locator or records `not stated`, `not applicable`, `unclear`, or `disputed`. Its verification depth remains source-inspected, never empirical `compared`.

### Empirical Intent Mode

The Comparison Intent Document records what the user wants, candidate identity and readiness, existing reproduced evidence, required source, model and data acquisition, environment and reimplementation needs, metrics, evaluator, fairness, repetitions, uncertainty, resources, Gates, and unresolved decisions. Ask: “Do you want to clarify for more detail, or proceed?”

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

## Common Mistakes

- Letting source availability determine the dimensions. Start from the domain question and accepted source basis.
- Ranking unclear or disputed cells. Preserve their state.
- Reusing old Runs without verifying their identities and Comparison Contract compatibility.
