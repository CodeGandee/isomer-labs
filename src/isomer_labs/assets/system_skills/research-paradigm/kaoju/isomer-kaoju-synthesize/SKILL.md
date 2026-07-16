---
name: isomer-kaoju-synthesize
description: Use when an accepted Kaoju Audit Report and accepted survey evidence are ready for a Field Summary, Survey Delta, Claim Status Table, or Kaoju Dossier.
---

# Kaoju Synthesize

## Overview

Write the strongest survey conclusion supported by accepted evidence and no stronger. Preserve contradictions, failures, limitations, uncertainty, and unresolved questions as first-class outputs.

Before accepting durable output, read the shared artifact semantics and recording rules plus this skill's `artifact-bindings.md`. Use `KAOJU:RELATED-WORK-CATALOG`, `KAOJU:CLAIM-STATUS-TABLE`, `KAOJU:FIELD-SUMMARY`, and `KAOJU:KAOJU-DOSSIER` exactly. Return a storage blocker rather than inventing a path, profile, canonical Markdown file, or untracked JSON.

## When to Use

Use only after audit accepts the evidence for synthesis or narrows the claims explicitly. Do not use this skill to fill evidence gaps, discover new sources, execute code, repair Runs, or bypass a not-ready Audit Report.

## Workflow

1. **Accept audited inputs**. Require an accepted Audit Report, Survey Contract, accepted Artifact and Evidence Item refs, and the requested output view.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-synthesize --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Freeze claim boundaries**. Map each intended conclusion to accepted evidence, achieved depth, verdict, contradictions, and audit limits.
4. **Build the requested view**. Produce the Related-Work Catalog or delta, Field Summary, Claim Status Table, comparison view, reading path, or Kaoju Dossier from accepted refs.
5. **Calibrate language**. Distinguish source-stated, source-supported, executed, compared, inconclusive, contradicted, blocked, and not-comparable conclusions.
6. **Preserve lineage**. Link every derived section or table to its source Artifacts, Evidence Items, Runs, Findings, Decision Records, and Provenance Records.
7. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-synthesize --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
8. **Return status**. Report `complete`, `paused`, or `blocked` with output refs, coverage limits, unresolved questions, and a resume point when applicable.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## Output Contract

Every output states its Survey Contract boundary, evidence cutoff, `searched_through` limit, accepted input refs, achieved verification depths, important contradictions and failures, limitations, and unresolved frontier. Structured records require non-empty top-level `title` and `summary`.

The Claim Status Table gives each conclusion a status, depth, verdict, supporting and challenging evidence refs, Run or source locators, and limitations. The Kaoju Dossier assembles the catalog, field model, comparisons, first-hand Findings, failures, limitations, unresolved questions, and reading path without hiding their lineage.

## Artifact Operations

Resolve `KAOJU:FIELD-SUMMARY` and `KAOJU:KAOJU-DOSSIER` through `ext kaoju bindings describe KAOJU:WHAT`. Persist accepted synthesis only through typed `project artifacts put` or binding-permitted `revise`; let the service infer profile, semantic label, scope, and managed content locator.

## Reference Routing

Use `$isomer-kaoju-shared` for evidence, survey Artifact, lineage, and terminal contracts. Return a not-ready audit to the owning repair stage; use `$isomer-kaoju-audit` again after new evidence exists.

## Foundational Principle

Synthesis organizes accepted evidence; it does not manufacture missing evidence or erase inconvenient evidence.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “The reader needs a clear winner.” | Report the supported comparison, including ties and non-comparability. |
| “The missing work probably would not change the result.” | State the coverage gap and limit the conclusion. |
| “Failures belong in an appendix.” | Keep their effect visible wherever the affected claim appears. |

## Red Flags

- A final claim has no entry in the Claim Status Table.
- Audited limitations disappear from the summary.
- A generated-data capability probe is presented as benchmark reproduction.

## Operational Notes

- Build every section from the audited evidence set.
- Preserve the state and source basis.
- State the bounded search and remaining frontier.

## Guardrails

- DO NOT write from memory instead of accepted refs.
- DO NOT turn `unclear` or `disputed` into a neutral score.
- DO NOT claim the field is complete.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
