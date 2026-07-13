# Ensure Topic Registration

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**:
   - If neither a concrete registered Research Topic ref nor `topic.intent.overview` from `resolve-topic-intent`, `init-topic`, or `clarify-topic` is available, refuse to run.
   - Explain that there is no topic material to register, and offer targeted fast-forward recovery through `resolve-topic-intent` when the original request contains enough topic substance.
2. Resolve registration inputs:
   - Resolve the Project root, Project Manifest, selected Research Topic id or candidate topic slug, candidate Topic Workspace directory, and topic overview.
   - Do not infer a topic from directory names, the current directory, a Project Manifest default, the registered id `default`, or a generic placeholder statement.
3. Recover the concrete Research Topic statement:
   - Use user input, `topic-overview.md`, or an already registered Research Topic Config.
   - If the statement is missing, generic, or unclear, stop with a blocker asking the user for the concrete research topic before any Project Config mutation.
4. Idempotently verify existing Project Manifest-backed registrations:
   - If the selected Research Topic and Topic Workspace are already registered and point to the intended topic material, state that registration is ready.
   - Carry forward the registered refs, and record that no mutation was needed.
5. If registration is missing, check path safety before mutation:
   - The candidate Topic Workspace directory must be project-scoped.
   - It must not be the Project Config directory, the Isomer-managed Houmao overlay, or another reserved project area.
   - It must not collide with a different registered Topic Workspace or unrelated project-owned path.
   - If any collision or unsafe path is found, stop with a blocker naming the conflicting path.
6. Create authoritative registration only when the topic statement and workspace path are clear:
   - Use a supported Isomer CLI/API surface, normally `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>`.
   - Capture the exact command or API evidence in `registration_command_evidence`.
7. Re-read the Project Manifest after creation:
   - If the Research Topic or Topic Workspace still is not registered, stop with a blocker.
   - Name the missing ref and the command or API surface that failed or is unavailable.
8. Verify the effective Topic Workspace Pixi binding accepted by `isomer-srv-topic-env-setup`:
   - Accepted forms are an explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` file target, an explicit directory target, or the implicit registered Topic Workspace directory default.
   - The implicit default is valid only when Pixi resolves it as a confined Topic Workspace Pixi workspace with environment `default`.
9. If Pixi cannot resolve the explicit or implicit binding target, report the blocker:
   - Explain that topic registration is blocked.
   - Explain that environment binding is blocked.
   - Name the target, binding source, and Pixi or confinement failure.
   - Do not hand-edit `.isomer-labs/manifest.toml` from this skill.
10. Report registration status, registered refs, command evidence, environment binding status, blockers, and the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded registration-assurance plan from the topic overview, Project Manifest, supported Isomer CLI/API surfaces, path safety rules, and downstream setup requirements, then execute only supported registration or verification steps.

## Prerequisite Artifacts

Required predecessor artifact or input:

- `topic.intent.overview` from `resolve-topic-intent` or `init-topic`, optionally revised by `clarify-topic`; or
- An explicit registered Research Topic ref whose registered config contains a concrete Research Topic statement.

If topic material is missing, refuse to run directly, explain that registration assurance needs a concrete topic statement and candidate Topic Workspace, and offer targeted fast-forward recovery to `ensure-topic-registration`. Use `python scripts/query_step_dependencies.py path --target ensure-topic-registration --include-target` for the inclusive default path and `python scripts/query_step_dependencies.py path --target ensure-topic-registration --exclude-target` for the exclusive path.

If the topic overview exists but does not contain a concrete topic statement, refuse to mutate Project Config and route to `clarify-topic`. Ask for the concrete Research Topic when the topic substance is missing or generic.

## Verification Targets

Verify the requested or derived Research Topic and candidate Topic Workspace against their Project Manifest-backed refs. Report registration as registered, provisional, blocked, or not checked, and summarize the command or API evidence. Describe the environment binding as active, implicit by default, blocked, or not checked, including its manifest and Pixi evidence when present. Name blockers that prevent authoritative registration or downstream service delegation.

## Supported Registration Surface

Use this command shape when a clear provisional topic seed should become authoritative Project state:

```bash
isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>
```

Use the effective Project root context expected by `isomer-cli project ...`. After the command succeeds, re-read the Project Manifest rather than trusting command output alone.

## Binding Gate

`setup-topic-env` depends on `isomer-srv-topic-env-setup`, and that service must receive a manifest-backed Research Topic and Topic Workspace. Before reporting success for this subcommand, check whether the Project Manifest has an active `topic_standalone_pixi_bindings.manifest_path_or_dir` entry or whether Pixi resolves the registered Topic Workspace directory as the implicit default binding accepted by `isomer-srv-topic-env-setup`.

If Pixi cannot resolve the effective target, report a blocker like this:

```text
topic_registration_status: blocked
environment_binding_status: blocked
manifest_path_or_dir: <topic-workspace>
binding_source: implicit-default
blocker: Pixi could not resolve the registered Topic Workspace directory as a confined Topic Workspace Pixi binding.
next_operator_action: run the environment setup or project-management command that creates a valid Topic Workspace Pixi manifest, or add an explicit manifest_path_or_dir binding through a supported surface when the target is not the Topic Workspace root.
```

## Guardrails

Do not hand-edit `.isomer-labs/manifest.toml` or Research Topic Config files.

Do not create a duplicate Research Topic or Topic Workspace when an existing Project Manifest-backed registration already matches the selected topic.

Do not register a topic from vague text, generic default topic statements, directory names, or unrelated workspace names.

Do not treat a provisional topic workspace seed as authoritative registration until the Project Manifest proves the Research Topic and Topic Workspace refs.

Do not call `isomer-srv-topic-env-setup` from this subcommand. Only verify or report the Topic Workspace Pixi binding that service setup needs.
