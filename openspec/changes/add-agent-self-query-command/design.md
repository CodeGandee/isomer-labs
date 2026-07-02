## Context

Isomer already resolves Effective Topic Context and optional Effective Agent Context through `project context show`, semantic path commands, supported `ISOMER_*` environment variables, cwd matching, Workspace Runtime path plans, and Project Manifest defaults. That machinery is sufficient for lower-level commands, but it is not packaged as a worker-friendly self-description contract.

Coding agents may be launched into `topic.repos.main` as cwd. That cwd correctly selects the topic but intentionally does not imply an Agent Workspace. If the launch adapter injects `ISOMER_AGENT_INSTANCE_ID`, `ISOMER_AGENT_NAME`, `ISOMER_TOPIC_ACTOR_NAME`, or related refs, the agent still has to know which command and fields to inspect. It also lacks a simple way to discover the selected Pixi manifest and environment needed to run Python through Pixi.

The new command should be a read-only, agent-facing aggregation over existing discovery, context, path, runtime, and Pixi helpers.

## Goals / Non-Goals

**Goals:**

- Provide one command, `project self show`, for coding agents and Topic Actors to inspect their process-local Isomer identity.
- Work from Topic Main Development Repository cwd when launch-time environment identity is present.
- Report enough source metadata that callers can distinguish explicit selectors, environment inputs, cwd inference, recorded runtime refs, and manifest/default fallbacks.
- Include recognized Isomer environment inputs without leaking arbitrary process environment or secrets.
- Include safe follow-up commands and selected semantic paths so agents can discover detailed paths without hardcoding.
- Include Pixi execution hints when a Project-root or standalone Topic Workspace Pixi target can be resolved.
- Keep the command side-effect free and suitable for `AGENTS.md` guidance.

**Non-Goals:**

- Do not make environment variables durable truth; they remain process-local candidate refs.
- Do not grant filesystem access control or claim identity security.
- Do not mutate Workspace Runtime, manifests, Pixi files, `AGENTS.md`, or launch material.
- Do not replace `project context show`, `project paths get/list/explain`, `project topic-actors show`, or runtime/team inspection commands.
- Do not expose credential values, API keys, tokens, passwords, or arbitrary env var dumps.

## Decisions

1. Add `project self show` as the public command.

`self` is intentionally agent-facing and short enough for injected guidance. It avoids making `context show` heavier, and it avoids `agent self`, which would be misleading for Topic Actor-only or operator-launched processes. Alternative considered: `project context self`; rejected because this is more than context resolution and should feel like the starting point for a worker process.

2. Build the self packet by composing existing resolvers.

The command should call project discovery, Effective Topic Context resolution, `resolve_effective_topic_actor_context(..., missing_is_error=False)`, `resolve_effective_agent_context(..., missing_is_error=False)`, semantic path resolution for a small curated set, and Pixi binding helpers. This keeps the command aligned with lower-level behavior and prevents a second identity resolver from drifting.

3. Treat missing agent identity as a warning-like self state, not a hard failure, when topic context is available.

An operator or Topic Actor may legitimately run from `topic.repos.main` without a formal Agent Instance. The JSON should set `ok` according to fatal diagnostics, but the payload should include `identity.agent.resolved=false` or `null` plus diagnostics or `self_status` entries that explain how to supply `ISOMER_AGENT_INSTANCE_ID`, `ISOMER_AGENT_NAME`, `--agent-instance`, or `--agent`.

4. Redact and whitelist environment reporting.

The command should report only recognized Isomer identity/path/config inputs and whether recommended identity vars are missing. It must not dump arbitrary `os.environ`. Values for known non-secret identity/path refs may be shown; known secret-like keys and credential env names must be omitted even if they start with `ISOMER_`.

5. Pixi hints should prefer resolved binding evidence over generic placeholders.

When possible, return `pixi.manifest_path`, `pixi.pixi_environment`, and command examples such as `pixi run --manifest-path <resolved> --environment <env> python ...`. If multiple active Project-root Pixi environment bindings exist, the command should report them and avoid guessing a single default unless one binding is selected by existing Topic Workspace Pixi rules. If no Pixi target can be resolved, it should report a blocker-style diagnostic and point to `project doctor` or topic env setup.

6. Update topic-main guidance to point to the new command first.

The injected guidance should keep lower-level `context show` and `paths get` examples, but the first recommended query should become `isomer-cli --print-json project self show`. This directly answers the worker's “who am I?” question.

## Risks / Trade-offs

- Self packet becomes too broad → Keep the first implementation curated: identity, recognized env, Pixi hint, selected semantic paths, and follow-up commands only.
- Identity appears more authoritative than it is → Label the payload as process-local resolved identity and include source metadata. Documentation should repeat that this is not access control.
- Multiple Pixi bindings are ambiguous → Report all candidates and avoid inventing one runnable command when the manifest declares more than one active environment without a clear selected target.
- Environment reporting leaks secrets → Whitelist known safe names and never include arbitrary env vars or secret-like names.
- Command duplicates `context show` → Keep `context show` as raw context display and make `self show` a worker-start packet that composes context with env, path, and Pixi summaries.

## Migration Plan

1. Add the command and payload while keeping existing commands unchanged.
2. Add tests for topic-main cwd with env identity, Agent Workspace cwd inference, missing agent identity, conflict diagnostics, recognized env reporting, and Pixi hint behavior.
3. Update the topic-main guidance template to recommend `project self show` first.
4. Update docs and command-surface help.

Rollback is straightforward: remove the new command and guidance reference. Existing context/path commands remain the fallback.
