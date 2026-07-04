## Context

Isomer system skills are now packaged as stable interfaces, but users still need a low-friction way to inject topic- or project-specific instructions into those skills without editing packaged skill assets. The existing Research Operation Extension Point concept covers provider-neutral operation slots such as execution, literature search, gates, and skill availability. User Skill Callback is different: it is instruction material that a participating skill checks at a named stage of its own workflow.

The first rollout targets production `isomer-deepsci-*` top-level workflows because they have consistent `## Workflow` entrypoints and a clear need for domain-specific research guidance. The design stays generic so later operator, service, misc, or future `isomer-<extension-name>-<purpose>` skill families can opt in without renaming the mechanism.

## Goals / Non-Goals

**Goals:**

- Define User Skill Callback as a generic instruction-layer mechanism for packaged system skills.
- Support `begin` and `end` callback stages for top-level workflows.
- Provide a project-scoped CLI command group for registration, resolution, inspection, disabling, and validation.
- Keep callback registries outside packaged skill directories and connect them through Project or Research Topic refs.
- Support inline prompts, prompt files, and external skill directories as callback sources.
- Make callback resolution deterministic and safe to call from skill instructions.
- Add concise callback participation guidance to production `isomer-deepsci-*` skills in the initial implementation.

**Non-Goals:**

- Do not execute callbacks as code or provider operations.
- Do not make callback material a Research Operation Extension Point, Execution Adapter payload, Gate policy, or Skill Binding projection.
- Do not apply callbacks to every system skill family in the first rollout.
- Do not install external skill directories into the system skill manifest.
- Do not store secrets, runtime state, command outputs, or rich Artifact contents in callback registries.
- Do not add GUI support in this change.

## Decisions

### 1. Use `project skill-callbacks` as the CLI home

The command group should live under `isomer-cli project skill-callbacks` rather than `ext research`, `ext deepsci`, or a DeepSci-specific command. The callback mechanism applies to system skills generally, and Project discovery already provides the stable root needed to find Project Manifest refs, Research Topic Config refs, and managed callback content.

Alternative considered: place the commands under `isomer-cli ext deepsci`. That would match the first participating skill family, but it would encode the wrong scope and make later non-DeepSci adoption look like a compatibility hack.

### 2. Store registries as declarative refs, not inline instruction bodies

Project Manifest and Research Topic Config should carry User Skill Callback registry refs. The registry then stores callback metadata and source refs. Inline prompt input from the CLI is materialized into managed callback content, for example under `.isomer-labs/user-skill-callbacks/`, and the registry points at that file.

Example registry shape:

```toml
schema_version = "isomer-user-skill-callback-registry.v1"

[[callbacks]]
id = "deepsci-scout-begin-domain-prior"
skill = "isomer-deepsci-scout"
stage = "begin"
scope = "research_topic"
status = "active"
priority = 100
source_type = "prompt_file"
prompt_file = ".isomer-labs/user-skill-callbacks/deepsci-scout-begin-domain-prior.md"
```

This keeps config files small and keeps large instruction material out of fields that should remain declarative. It also lets validation check registry metadata separately from prompt content.

Alternative considered: embed callback prompt bodies directly in Research Topic Config. That is easy to author but conflicts with the existing rule that topic config stores refs and defaults, not runtime truth or rich material.

### 3. Support three source types with one source per callback

The first implementation should accept `--prompt`, `--prompt-file`, and `--skill-dir`. A callback record must have exactly one source type. `--prompt` is copied into managed project content. `--prompt-file` points to a readable Markdown or text prompt file. `--skill-dir` points to a directory with `SKILL.md`; the directory is treated as supplemental instruction material, not as an installed system skill.

Paths should resolve relative to the Project root by default. Paths outside the Project root are allowed only when the user passes an explicit flag such as `--allow-external-source`, and resolution output should clearly mark those callbacks as external.

Alternative considered: require all callback material to be copied into `.isomer-labs/`. Copying is safest for reproducibility, but users explicitly need to point at external skill directories. The explicit external-source flag keeps that power visible.

### 4. Resolve callbacks deterministically and read-only

`isomer-cli --print-json project skill-callbacks resolve --skill <name> --stage <begin|end>` should not mutate files. It should load Project and, when selected, Effective Topic Context; collect active registries; filter by exact system skill name and stage; and return ordered callback items.

Resolution order:

1. Topic-scoped callbacks before project-scoped callbacks.
2. Lower numeric priority before higher numeric priority within the same scope, unless implementation chooses the inverse and documents it consistently.
3. Stable callback id as the final tie breaker.

Resolve output should include callback id, skill, stage, scope, priority, status, source type, source summary, resolved instruction refs, and diagnostics. Prompt sources may return normalized instruction text when safe. Skill directory sources should return the resolved `SKILL.md` path and instruct the agent to read it as supplemental guidance.

Alternative considered: let participating skills read registry files directly. That would duplicate parsing rules in skill prose and make provider agents handle TOML, path bounds, and redaction inconsistently.

### 5. Treat callback guidance as workflow order, not authority elevation

The phrase “follow callback instructions first” means stage order. A `begin` callback runs before workflow step 1, and an `end` callback runs before final completion. It does not make callback material higher priority than system policy, developer instructions, the owning skill, the current user request, Gates, validation, or Isomer domain constraints.

Participating skill wording should be explicit: resolve callbacks, follow returned instructions within this skill's constraints, and report any conflict that changes the workflow.

Alternative considered: treat registered callbacks as durable user preferences that override later prompts. That would be surprising for agents and unsafe for shared Projects because the current invocation must remain the active user intent.

### 6. Make skill-family participation explicit and validated

The generic registry can store callbacks for any active system skill name, but only participating skills are expected to resolve and apply them. The first implementation should add a concise User Skill Callback reminder to production `isomer-deepsci-*` `SKILL.md` files and update the DeepSci validation harness to check for the reminder.

The reminder should be a small shared pattern near the top-level workflow, not a large duplicated callback manual. Detailed CLI behavior belongs in docs and validator tests.

Alternative considered: make all skills implicitly callback-aware through a global agent instruction. That would be too broad, hard to validate, and less clear than opt-in participation.

## Risks / Trade-offs

- Callback conflicts can be subtle → Mitigation: resolution and participating-skill prose must say callbacks are supplemental instructions and must report conflicts with owning-skill constraints or current user intent.
- External skill directories can drift or disappear → Mitigation: validation reports missing paths, resolve emits diagnostics, and external sources require an explicit registration flag.
- Inline prompts may accidentally include secrets → Mitigation: reuse existing secret-like field validation patterns and redact diagnostic values.
- Registry priority could become overdesigned → Mitigation: keep v1 priority numeric, deterministic, and optional with a default value.
- Project-level callbacks could affect too many workflows → Mitigation: exact system skill and stage matching is required in v1, and topic-scoped callbacks sort before project-scoped callbacks when a topic is selected.
- DeepSci skill edits could become repetitive → Mitigation: use a concise shared wording pattern and enforce it with validation rather than copying a full manual into each skill.

## Migration Plan

1. Add callback registry data structures and validation helpers without changing existing Project or Research Topic behavior when no callback refs exist.
2. Add `isomer-cli project skill-callbacks` commands with JSON outputs and deterministic diagnostics.
3. Extend Project Manifest and Research Topic Config parsing to expose callback registry refs as optional declarative refs.
4. Add DeepSci skill callback participation text and update the DeepSci validation harness.
5. Add unit tests for registry parsing, CLI command behavior, path policy, source validation, resolve ordering, and conflict-safe output.
6. Run `pixi run validate-skills`, `pixi run validate-research-skills`, `pixi run lint`, `pixi run typecheck`, and `pixi run test`.

Rollback is simple for projects that do not register callbacks because the feature is optional. For a project that has callback refs, removing the refs or disabling the callback records returns participating skills to normal behavior.

## Open Questions

- Should project-level registry refs live in a repeated Project Manifest table or in a compact refs section if the manifest gains one later?
- Should `resolve` include prompt file text by default, or should it return paths by default and require a flag for embedded instruction text?
- Should wildcard skill matching exist later for all skills in a family, or should v1 exact skill matching remain the long-term rule?
