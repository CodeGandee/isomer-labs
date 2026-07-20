---
name: isomer-research-idea-recording
description: Use when an Isomer workflow creates, accepts, classifies, selects, defers, closes, reopens, explores, supports, refutes, revises, derives, merges, or archives durable research concepts and must record canonical Research Ideas, exact realizations, independent portfolio facets, decision options, transitions, generations, lineage, or atomic idea-bearing record effects.
---

# Research Idea Recording

## Overview

Record durable research concepts as a producer-neutral portfolio that Project Web, CLI queries, and later agents can interpret without parsing extension-specific prose. Keep concept identity, record identity, evidence, workflow state, and browser state separate.

Read `references/recording-contract.md` before accepting any idea-bearing output or changing canonical idea state.

## When to Use

Use this skill whenever a durable research concept is proposed, explored, selected, deferred, closed, reopened, supported, refuted, revised, derived, merged, or archived, or when an idea-bearing record promises canonical portfolio effects.

## Workflow

1. Apply the durable-concept test. Record a Research Idea only when the object is a research direction, hypothesis, mechanism, model, method concept, or other durable proposition that a user may compare, explore, select, defer, close, reopen, or derive from another concept.
2. Resolve current canonical state. Query the Topic Workspace database for matching `idea_id` values, aliases, latest Idea Realizations, generations, decision options, transitions, and lineage before writing.
3. Plan one acceptance operation. Identify every affected idea, exact object-valued source path, authored current facet, generation membership, decision option, justified transition, lineage edge, actor, rationale, and terminal result ref before the record write.
4. Use atomic structured effects when the profile promises idea recording. Put `research_idea_effects` in the structured payload with `atomic=true`; let record acceptance create the record and every promised canonical effect in one transaction.
5. Use explicit CLI mutations for standalone maintenance. Upsert initial facets, record exact realizations, add generations and lineage, maintain complete decision option sets, and use transition commands for later state changes.
6. Verify the accepted result. Inspect returned idea, realization, generation, lineage, decision-option, transition, and operation refs; query the affected ideas and decision context; run canonical validation before claiming completion.
7. Report uncertainty honestly. Use `unknown` when durable evidence does not justify a facet, preserve incomplete historical context as a diagnostic, and use preview before applying migration or repair.

If the request does not map cleanly to this workflow, use the native planning tool to build a bounded recording plan from the durable-concept test, authoritative record profile, current canonical portfolio state, and explicit actor intent, then execute only justified mutations or stop on a concrete blocker.

## Chat Response

Present normal chat responses in natural-language Markdown. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.

## Completion Boundary

Do not call an idea-bearing output accepted until the durable research record and all promised canonical effects have committed, the exact realization paths resolve to individual objects, the compatibility status matches the facets, and validation returns no errors. A Markdown file, rendered view, operation-set report, or chat claim is not canonical recording evidence.

Do not use the deprecated one-value `status` as the source of truth.

## Guardrails

- DO NOT infer canonical ideas, state, decisions, or lineage from Markdown.
- DO NOT use the deprecated one-value `status` as the source of truth.
- DO NOT treat generation membership as proof that a Decision Record considered every sibling.
- DO NOT change decision state because evidence changed, or evidence state because a decision changed, without an explicit transition for the affected facet.
- DO NOT create Research Ideas automatically for sources, datasets, repositories, claims, metrics, tasks, repair routes, paper sections, or implementation attempts unless an actor explicitly promotes a distinct durable concept.
- DO NOT create idea-level `revision_of` edges. Preserve identity for concept-stable revisions and add a new realization; create a new idea and justified concept-lineage edge only when the concept changes.
