---
name: isomer-rsch-shared-v2
description: Use when a v2 Isomer research skill needs shared coordination rules, semantic handoff vocabulary, route discipline, or storage-binding cautions before conducting research work.
---

# Isomer Research Shared V2

## Overview

Shared defines the coordination contract for v2 research skills. It is not migrated from one upstream source skill; it exists to keep v2 skill handoffs, route decisions, placeholder usage, and storage-binding cautions consistent across the refactor-migrated skills.

## When to Use

Use this skill when:

- A v2 research skill needs the shared semantic placeholder registry.
- A handoff object needs a stable meaning before Isomer storage binding exists.
- Two v2 skills disagree about whether an object is evidence, a decision, a handoff, a run record, runtime state, a report, a draft, code, a dataset, or a figure.
- A route decision should be expressed in a common form before dispatching to another v2 skill.

Do not use this skill as a substitute for a domain skill such as scout, baseline, idea, optimize, experiment, analysis, science, decision, or finalize.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify the coordination question**. Name the handoff, route, placeholder, or storage-binding ambiguity that needs shared rules. Read `references/coordination-contract.md`.
2. **Check the semantic registry**. Read `references/semantic-placeholders.md` and choose the closest existing semantic object.
3. **Preserve skill ownership**. Route domain work back to the owning v2 skill; use shared only for vocabulary and coordination consistency. Read `references/coordination-contract.md`.
4. **Avoid premature storage binding**. Keep unresolved records semantic until an Isomer storage-binding pass assigns Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, path, or schema bindings. Read `references/semantic-placeholders.md` and `references/coordination-contract.md`.
5. **Return the coordination result**. State the chosen semantic object, owning producer, intended consumer, and any unresolved binding or route question. Read `references/coordination-contract.md`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the shared registry, the relevant v2 skill, and the user's request, then execute the plan.

## Common Mistakes

- Treating shared as the owner of research work rather than the owner of vocabulary consistency.
- Binding placeholders to paths, database rows, or Artifact kinds before a storage-binding pass.
- Inventing a new semantic object when an existing registry entry already fits.
- Letting a route decision hide the evidence or blocker that made the route justified.

## Reference Routing

Read `references/semantic-placeholders.md` whenever a v2 skill needs shared handoff vocabulary. Read `references/coordination-contract.md` whenever the question is about ownership, routing, unresolved storage binding, or handoff shape.
