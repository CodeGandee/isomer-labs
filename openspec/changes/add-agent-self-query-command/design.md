## Context

Isomer already resolves Effective Topic Context and optional Effective Agent Context through `project context show`, semantic path commands, supported `ISOMER_*` environment variables, cwd matching, Workspace Runtime path plans, and Project Manifest defaults. That machinery is sufficient for lower-level commands, but it is not packaged as a worker-friendly self-description contract.

Coding agents may be launched into `topic.repos.main` as cwd. That cwd correctly selects the topic but intentionally does not imply an Agent Workspace. If the launch adapter injects `ISOMER_AGENT_INSTANCE_ID`, `ISOMER_AGENT_NAME`, `ISOMER_TOPIC_ACTOR_NAME`, or related refs, the agent still has to know which command and fields to inspect. It also lacks a simple way to discover the selected Pixi manifest and environment needed to run Python through Pixi.

The new command family should be a read-only, agent-facing set of small queries over existing discovery, context, path, runtime, and Pixi helpers. It should avoid a single large response by default.

## Goals / Non-Goals

**Goals:**

- Provide a `project self` command family for coding agents and Topic Actors to inspect selected slices of their process-local Isomer identity.
- Keep `project self show` small enough to use as a first command in `AGENTS.md` guidance.
- Work from Topic Main Development Repository cwd when launch-time environment identity is present.
- Report enough source metadata that callers can distinguish explicit selectors, environment inputs, cwd inference, recorded runtime refs, and manifest/default fallbacks.
- Include recognized Isomer environment inputs without leaking arbitrary process environment or secrets.
- Include safe follow-up commands, semantic paths, and Pixi execution hints only when the caller asks for those slices.
- Keep the command side-effect free and suitable for `AGENTS.md` guidance.

**Non-Goals:**

- Do not make environment variables durable truth; they remain process-local candidate refs.
- Do not grant filesystem access control or claim identity security.
- Do not mutate Workspace Runtime, manifests, Pixi files, `AGENTS.md`, or launch material.
- Do not replace `project context show`, `project paths get/list/explain`, `project topic-actors show`, or runtime/team inspection commands.
- Do not make `project self show` a full introspection dump.
- Do not expose credential values, API keys, tokens, passwords, or arbitrary env var dumps.

## Decisions

1. Add `project self` as a command family, with `show` as the small default entry point.

`self` is intentionally agent-facing and short enough for injected guidance. The family avoids making `context show` heavier, and it avoids `agent self`, which would be misleading for Topic Actor-only or operator-launched processes. Alternative considered: `project context self`; rejected because this is more than context resolution and should feel like the starting point for a worker process.

2. Make each subcommand return one small slice.

The planned subcommands are:

- `project self show`: minimal summary and available next queries.
- `project self identity`: Effective Topic Context headline, Topic Actor context, Effective Agent Context, and source metadata.
- `project self pixi`: selected Pixi manifest path, environment, binding source, and runnable command hints.
- `project self env`: recognized safe Isomer environment inputs, with values omitted by default unless a safe-value option is explicitly used.
- `project self paths <label>...`: only the requested semantic labels.
- `project self queries`: only safe follow-up query commands.

This is the main token-control decision: the agent asks for what it needs, and the CLI does not preload broad context. Alternative considered: a single `project self show --include identity,pixi,paths` command. That is rejected for the first implementation because it still encourages broad reads through one command; subcommands are easier for agents to select and easier to document.

3. Compose each slice from existing resolvers.

Each subcommand should call project discovery, Effective Topic Context resolution, and then only the extra resolvers it needs. For example, `identity` uses `resolve_effective_topic_actor_context(..., missing_is_error=False)` and `resolve_effective_agent_context(..., missing_is_error=False)`, while `paths` calls semantic path resolution only for requested labels. This keeps behavior aligned with lower-level commands and prevents a second identity resolver from drifting.

4. Treat missing agent identity as a warning-like self state, not a hard failure, when topic context is available.

An operator or Topic Actor may legitimately run from `topic.repos.main` without a formal Agent Instance. The JSON should set `ok` according to fatal diagnostics, but the payload should include `identity.agent.resolved=false` or `null` plus diagnostics or `self_status` entries that explain how to supply `ISOMER_AGENT_INSTANCE_ID`, `ISOMER_AGENT_NAME`, `--agent-instance`, or `--agent`.

5. Redact and whitelist environment reporting.

`project self env` should report only recognized Isomer identity/path/config inputs and whether recommended identity vars are missing. It must not dump arbitrary `os.environ`. The default output should be names, classes, presence, and influence, not values. Values for known non-secret identity/path refs may be shown only with an explicit safe-values option; known secret-like keys and credential env names must be omitted even if they start with `ISOMER_`.

6. Pixi hints should prefer resolved binding evidence over generic placeholders.

`project self pixi` should return `pixi.manifest_path`, `pixi.pixi_environment`, and command examples such as `pixi run --manifest-path <resolved> --environment <env> python ...` when possible. If multiple active Project-root Pixi environment bindings exist, the command should report candidates and avoid guessing a single default unless one binding is selected by existing Topic Workspace Pixi rules. If no Pixi target can be resolved, it should report a blocker-style diagnostic and point to `project doctor` or topic env setup.

7. Update topic-main guidance to point to small self queries.

The injected guidance should keep lower-level `context show` and `paths get` examples, but the first recommended query should become `isomer-cli --print-json project self show`, followed by query-only-what-you-need examples such as `project self identity`, `project self pixi`, and `project self paths <semantic-label>`. This directly answers the worker's “where do I start?” question without encouraging a large context dump.

## Risks / Trade-offs

- Self packet becomes too broad → Do not implement a broad self dump in the first version. Keep `show` tiny and route details to specific subcommands.
- Identity appears more authoritative than it is → Label the payload as process-local resolved identity and include source metadata. Documentation should repeat that this is not access control.
- Multiple Pixi bindings are ambiguous → Report all candidates and avoid inventing one runnable command when the manifest declares more than one active environment without a clear selected target.
- Environment reporting leaks secrets → Whitelist known safe names and never include arbitrary env vars or secret-like names.
- Command duplicates `context show` → Keep `context show` as raw context display and make `self show` a tiny worker-start packet that points to specific self subcommands for env, path, and Pixi details.
- Too many subcommands become hard to remember → The tiny `self show` response should list the available self subcommands and one-line purposes.

## Migration Plan

1. Add the command family and slice payloads while keeping existing commands unchanged.
2. Add tests for topic-main cwd with env identity, Agent Workspace cwd inference, missing agent identity, conflict diagnostics, recognized env reporting, requested path labels, and Pixi hint behavior.
3. Update the topic-main guidance template to recommend `project self show` first and detail subcommands only as needed.
4. Update docs and command-surface help.

Rollback is straightforward: remove the new command and guidance reference. Existing context/path commands remain the fallback.
