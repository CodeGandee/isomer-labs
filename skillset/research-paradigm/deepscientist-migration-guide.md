# Source Skill Migration Guide

This guide defines the general rules for migrating the upstream research skills into the Isomer Labs research-paradigm skillset. Resolve the source checkout from the repository's local orphan dependency area or the operator-provided source path. The goal is to preserve the original research method first, then adapt naming, placeholders, and storage binding later.

## Migration Goals

Migrate each skill from the source skill, not from an earlier Isomer adaptation. Earlier generationed skills remain useful historical references in git history, but a new migration must recover the original core logic directly.

Keep the first migration faithful and complete enough to execute the research process. Trimming, merging, and Isomer-specific simplification come after we can see the full source-derived process in the new skill.

## Source Lineage

The upstream source for this migration is the DeepScientist skill tree at `/home/huangzhe/workspace/code/isomer-labs/extern/orphan/DeepScientist/src/skills`. This section records provenance only; active migration instructions should continue to refer to source skills without depending on a fixed local checkout path.

## DeepScientist Harness

Many upstream DeepScientist skills assume a harness around the agent, especially the MCP-style `memory`, `artifact`, and `bash_exec` namespaces. Treat those harness calls as source behavior that must be understood during migration, not as ordinary Linux commands or final Isomer storage bindings.

For the first Isomer Labs implementation, the equivalent harness surface is the DeepScientist-flavored extension command family `isomer-cli ext deepsci ...`. Its initial role is compatibility: mock the DeepScientist command inputs and outputs, persist mock state in Isomer Workspace Runtime SQLite, and keep the migrated skills runnable while we replace individual source behaviors with real Isomer semantics.

Where an original source skill calls its DeepScientist MCP harness, the migrated skill should call the Isomer CLI extension harness instead. Treat `isomer-cli ext harness ...` as the generic Isomer harness intent; in the current DeepScientist-compatible implementation, spell concrete calls as `isomer-cli ext deepsci call <namespace.tool> --input-json <json-object>` so `memory.*`, `artifact.*`, and `bash_exec.bash_exec` preserve their source input and output shape.

When a source skill depends on `memory.*`, `artifact.*`, or `bash_exec.bash_exec`, preserve the intended research meaning in the migrated skill and use placeholders for produced or consumed research objects. Do not hard-code DeepScientist paths, quest directories, venv assumptions, or final Isomer storage labels in the skill text. Bind those placeholders to the Isomer storage system later, after the semantics are clear.

## Core Logic Rule

Every migrated skill must include the core logic of the original skill. Core logic means the purpose, trigger conditions, stage transitions, key judgments, required checks, refusal or stop conditions, and output meaning that make the original skill work.

Do not reduce a source skill to a slogan or a storage wrapper. If a source skill has a distinctive reasoning loop, decision rule, quality gate, or failure handling pattern, preserve it in the migrated skill even if the names and storage surfaces change later.

## Placeholder Rule

For handoffs and output artifacts, use semantic placeholders instead of real storage paths, filenames, database rows, or Isomer storage labels. A placeholder names what the research object means, not where it lives.

Use placeholders when a skill needs to hand off a research frame, comparator, hypothesis, result, analysis, route choice, final summary, or other reusable research object. Do not bind these objects to the storage system during the first migration pass.

Centralize placeholders in `skillset/research-paradigm/deepsci/isomer-rsch-shared/references/semantic-placeholders.md`. That registry should list each placeholder, explain what it means, name the producer skill, name the consumer skills, and state that storage binding is pending. This lets us bind stable semantics to the Isomer Labs storage layer later without rewriting every skill again.

## Internal Page Rule

The migrated skill must contain every file inside the original source skill directory. Copy internal pages, references, modes, scripts, templates, fixtures, and other support files first, then revise names and storage placeholders only where needed for the Isomer skill target.

The migrated entrypoint `SKILL.md` must reference the copied files in the proper places, following the original skill's entrypoint structure and link intent. If the original skill points readers or agents to a reference file during a workflow step, the migrated `SKILL.md` should point to the corresponding migrated file at that step.

If a source skill has multiple internal pages, references, modes, scripts, or executable subpages, keep all of them in the first migration. Preserve the page boundaries and links unless a link is broken or meaningless outside the source tree.

Trim later only after the migrated skill is readable, validated, and compared against the original source. Early trimming hides source logic and makes it harder to tell whether the migration is faithful.

## Skill Writing Rules

Follow the rules from `$imsight-agent-skill-handling create` when creating a migrated skill. Each `SKILL.md` must have valid YAML frontmatter with `name` and a `description` that starts with `Use when...`, then include `## Overview`, `## When to Use`, `## Workflow`, and `## Common Mistakes`.

Follow the rules from `$imsight-agent-skill-handling format` after drafting. Keep `## Workflow` near the top, write it as numbered steps, keep each step concise, move long detail into dedicated sections or references, and end with a fallback for tasks that do not map cleanly to the default steps.

Each migrated skill must include `agents/openai.yaml`. Set `interface.display_name` to the exact skill name, including the generation suffix. Use the same skill name in `interface.default_prompt` so OpenAI-facing metadata routes to the intended skill.

## Migration Workflow

1. **Copy the source skill directory**. Copy every file from `<original-skill>/` into `<new-skill-dir>/`, but copy the original entrypoint `SKILL.md` or `skill.md` to `<new-skill-dir>/skill-org.md` instead of overwriting the target entrypoint. Preserve subdirectories, references, scripts, templates, and support files exactly enough that the source skill can still be audited from the migrated directory.
2. **Rewrite the target entrypoint with Isomer terms**. Read `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` to understand canonical Isomer terms, then read `<new-skill-dir>/skill-org.md` and identify source terms that need replacement. Rewrite `<new-skill-dir>/SKILL.md` with Isomer terms while following `skill-org.md` logic as closely as possible, including the source skill's internal structure, workflow order, reference boundaries, and placement of links to copied files.
3. **Replace the harness calls**. Where `skill-org.md` calls the DeepScientist MCP harness, rewrite the migrated `SKILL.md` to call the Isomer CLI extension harness instead. Use the current DeepScientist-compatible form `isomer-cli ext deepsci call <namespace.tool> --input-json <json-object>` for `memory.*`, `artifact.*`, and `bash_exec.bash_exec`, and keep produced or consumed research objects as placeholders until storage binding is decided.
4. **Replace handoffs with placeholders**. Add or reuse entries in the central placeholder registry for every cross-skill research object.
5. **Format and validate**. Apply the `$imsight-agent-skill-handling create` and `$imsight-agent-skill-handling format` rules, then run the research skill validator before treating the migration as ready for review.

If a source concept has no clear Isomer equivalent, keep it as source-derived wording in the migrated skill and mark the naming question in the placeholder registry or a local note. Do not invent storage binding to make the migration look complete.
