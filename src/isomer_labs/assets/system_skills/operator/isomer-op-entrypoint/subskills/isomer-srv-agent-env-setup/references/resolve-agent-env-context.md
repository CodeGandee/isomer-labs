# Resolve Agent Env Context

Use this subcommand to resolve the Project, Research Topic, Topic Workspace, Topic Workspace Pixi binding, topic semantic labels, and invocation provenance posture before any Agent Workspace environment setup mutation.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Project root | Use the provided path or current working directory; confirm `.isomer-labs/manifest.toml` exists. |
| Research Topic or Topic Workspace selector | Read a `research_topic_id`, Topic Workspace ref, or Topic Workspace path from the prompt or Project Manifest context. If several topics remain plausible, ask the user which one to use. |
| Requester and confirmation source | Record Project Operator Session, Operator Agent, Service Request ref, or direct prompt source when available. Direct mutation later requires explicit mutation confirmation or Service Request authorization. |
| Optional Service refs | Record Service Request refs, support Artifact refs, and Provenance refs when present. Missing refs do not block direct setup. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Resolve the Project root** from the prompt or current working directory. Confirm `.isomer-labs/manifest.toml` exists.
2. **Resolve the Research Topic and Topic Workspace** through Project Manifest-backed context. Do not select a Topic Workspace by scanning sibling directories.
3. **Resolve the Topic Workspace Pixi binding**:
   - Use an active `topic_standalone_pixi_bindings.manifest_path_or_dir` entry when present.
   - Otherwise use the registered Topic Workspace directory as the implicit default target.
   - Record `manifest_path_or_dir`, `manifest_path`, `pixi_environment`, and binding source.
4. **Resolve topic semantic labels before mutation**:
   - Required labels are `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.agents_root`, `topic.records`, `topic.runtime`, `topic.env.topic_setup_target_spec`, `topic.intent.agent_env_requirements`, and `topic.env.agent_setup_target_spec`.
   - Record each semantic label, resolved path, storage profile, source, source detail, diagnostic, and blocker.
5. **Confirm path boundaries**:
   - The Topic Workspace and resolved setup labels must be inside the selected Project root unless a later accepted external-root policy explicitly permits the binding.
6. **Record invocation posture**:
   - Report who requested the work, how authorization was confirmed, any Service Request, support Artifact, or Provenance refs, and whether the invocation is read-only or authorized to mutate.
7. **Report resolved context** using the parent Essential Output by default and Complete Output when requested:
   - Stop with blockers for missing Project Manifest, unknown Research Topic, missing Topic Workspace, unresolved Pixi binding, semantic label blockers, unsafe paths, or missing mutation confirmation for mutating follow-up steps.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from Project Manifest evidence, semantic label requirements, invocation posture, and the parent guardrails, then execute the plan.

## Resolved Context

Carry these values to later subcommands:

| Value | Meaning |
| --- | --- |
| `project_root` | The Isomer Project root containing `.isomer-labs/manifest.toml`. |
| `research_topic_id` | The selected Research Topic id. |
| `topic_workspace_dir` | The Project Manifest-declared Topic Workspace directory. |
| `topic_workspace_pixi_binding` | `manifest_path_or_dir`, `manifest_path`, `pixi_environment`, and binding source. |
| `semantic_paths` | Resolved labels, paths, storage profiles, sources, source details, diagnostics, and blockers for `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.agents_root`, `topic.records`, `topic.runtime`, `topic.env.topic_setup_target_spec`, `topic.intent.agent_env_requirements`, and `topic.env.agent_setup_target_spec`. |
| `requester` | Project Operator Session, Operator Agent, Service Request ref, or explicit blocker. |
| `confirmation_source` | Direct mutation confirmation, Service Request authorization, or read-only invocation. |
| `service_request_refs` | Optional Service Request refs when available. |
| `support_artifact_refs` | Optional support Artifact refs when available. |
| `provenance_refs` | Optional Provenance refs when available. |

## Operational Contract

- Record missing Service Request, support Artifact, or Provenance refs without blocking direct Project Operator Session setup.

## Guardrails

- DO NOT create files from this subcommand.
- DO NOT infer Pixi bindings from names.
- DO NOT treat Project-root Pixi as the Topic Workspace execution environment.
- DO NOT proceed to mutating subcommands when required context values are missing.
