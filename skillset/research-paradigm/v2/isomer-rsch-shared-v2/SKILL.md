---
name: isomer-rsch-shared-v2
description: Use when a v2 Isomer research skill needs the shared core process, semantic placeholder rules, or generation boundary before conducting research work.
---

# Isomer Research Shared V2

## Overview

This skill defines the v2 research-method contract. V2 skills keep the research process visible first and use semantic placeholders for research objects whose storage binding is intentionally deferred.

## When to Use

Use this skill before or during any `isomer-rsch-*-v2` skill when you need the core loop, shared placeholder meanings, or v2 boundaries. Do not use it to decide filesystem layout, record schemas, execution adapters, or storage labels.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Name the research stage**. Locate the work within `Frame -> Comparator -> Hypothesis -> Experiment -> Analysis -> Decision -> Finalize`.
2. **Load placeholder meanings**. Read `references/semantic-placeholders.md` when a v2 skill mentions any `[[rsch-object:<id>]]` placeholder.
3. **Keep semantics before storage**. Describe what the research object means, what it must contain, and which skill should consume it; do not bind it to implementation storage.
4. **Route by research need**. Pick the next v2 skill from the stage that would change the research state, not from bookkeeping availability.
5. **Preserve uncertainty**. Keep failed, null, weak, contradictory, or blocked results visible in the appropriate semantic output.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the v2 core loop, the placeholder registry, and the user's request, then execute the plan.

## Reference Routing

- `references/semantic-placeholders.md` for registered v2 placeholders, their meanings, producer skills, consumer skills, and storage-binding status.

## Core Loop

The default v2 research loop is `Frame -> Comparator -> Hypothesis -> Experiment -> Analysis -> Decision -> Finalize`. `isomer-rsch-optimize-v2` overlays the hypothesis, experiment, and analysis portion when candidate search is the main work. `isomer-rsch-science-v2` supports any stage that needs scientific computation or validity checks.

## Placeholder Rule

Use `[[rsch-object:<id>]]` when a skill needs to name a reusable research object. The placeholder means "this research object has semantics we must define"; it does not mean "write this object to a particular platform surface."

## Guardrails

- Do not replace research judgment with bookkeeping language.
- Do not treat a placeholder as proven or complete merely because it has a name.
- Do not hide uncertainty, failed results, or missing comparator information.
- Do not add new placeholder ids without also defining them in the registry.

## Source Lineage

The v2 loop distills the core process from the local DeepScientist skill analysis under `context/explore/deepscientist-skill-analysis/`. That path is maintainer provenance, not a runtime dependency for using this skill.
