# System Skill Index

## Workflow

1. Match the user's task to one system skill family: operator, service, or misc. Use [extension-skill-index.md](extension-skill-index.md) for DeepSci and other domain-extension work.
2. Prefer the active operator owner skill for user-facing Project, Topic, actor, agent, Toolbox, team, and routing tasks.
3. Treat service skills as delegated support routes from owner workflows unless the user explicitly invokes the service skill by name.
4. Treat misc skills as explicit helper interfaces, not default owner workflows.
5. Return the selected skill name, direct invocation shape, owner boundary, and any prerequisite context needed before proceeding.

If the user's task does not map cleanly to these steps, use your native planning tool to build a skill-selection plan from the active system skills, the user's task, and owner-boundary constraints, then execute the plan or report the missing decision.

## Operator Skills

| Intent | Skill | Route Shape |
| --- | --- | --- |
| Read-only welcome, supported paths, first-run option menu, or owner-skill recommendations. | `isomer-op-welcome` | `Use $isomer-op-welcome show-options`, `choose-path`, `show-skill-map`, or `next-step`. |
| Project init, validation, doctor diagnostics, cleanup, content-root relocation, topic listing, context, runtime readiness, or Project-level routing. | `isomer-op-project-mgr` | `Use $isomer-op-project-mgr <subcommand>`. |
| Project Web GUI lifecycle, GUI Backend launch or status, cache-mode debugging, GUI refresh, recent-errors inspection, backend API reference, or GUI troubleshooting. | `isomer-op-gui-mgr` | `Use $isomer-op-gui-mgr help`, `launch`, `status`, `api-reference`, `refresh-records`, or `troubleshoot`. |
| Blank or partial Research Topic setup, manual-research-ready Topic Workspace, topic intent, Topic Actor preparation, or final readiness summary. | `isomer-op-topic-creator` | `Use $isomer-op-topic-creator run-to <target>`, `fast-forward`, `step-by-step`, `status`, or `repair`. |
| Initialized Research Topic storage, Topic Actors, actor workspaces, packages, environment verification, reset checkpoints, branch helpers, or diagnostics. | `isomer-op-topic-mgr` | `Use $isomer-op-topic-mgr <subcommand>`. |
| Switch the Project Operator to act as or on behalf of a selected Topic Actor or Agent workspace cwd. | `isomer-op-switch-identity` | `Use $isomer-op-switch-identity switch`, `act-as`, `status`, or `reset`. |
| Project-local Toolbox creation, conversion, install, inspection, update, disable, uninstall, callback insertion, insertion-point discovery, Runtime Params, or effective-state diagnostics. | `isomer-op-toolbox-mgr` | `Use $isomer-op-toolbox-mgr help` or a specific Toolbox subcommand. |
| Domain Agent Team Template adaptation, Topic Team Specialization, static team validation, profile approval, materialization, or launch-facing preparation. | `isomer-op-topic-team-specialize` | `Use $isomer-op-topic-team-specialize fast-forward`, `step-by-step`, or a procedural subcommand. |
| Informed-user dispatch from a concrete task to a system skill or CLI family. | `isomer-op-entrypoint` | Parse, route, and proceed with the selected skill or CLI family. |

`isomer-op-welcome` is read-only orientation. `isomer-op-entrypoint` is route-and-proceed dispatch.

## Service Skills

| Intent | Skill | Boundary |
| --- | --- | --- |
| Topic Workspace environment setup, topic-main readiness, external repos, projections, and verification materialization. | `isomer-srv-topic-env-setup` | Delegated by Topic Creator, Topic Manager, or Topic Team Specialization after manifest-backed topic refs exist. |
| Agent Workspace worktree creation and cwd proof. | `isomer-srv-agent-env-setup` | Delegated by Topic Team Specialization or Topic Manager after topic-main predecessor evidence and authoritative Agent Names exist. |
| Houmao loop, adapter, mailbox, gateway, launch material, and runtime support. | `isomer-srv-houmao-interop` | Bounded internal provider support through Isomer CLI skill-context, Project Manager, Topic Service Agent support, or Topic Team Specialization. |
| Package repository resolution. | `isomer-srv-resolve-pkg-repo` | Bounded service support for package or repo resolution. |
| Topic service agent support, including explicit Topic Service Master prepare, launch, inspect, stop, and repair lifecycle routes. | `isomer-srv-topic-service-agent-support` | Bounded service-team support, not a normal first-click owner route. Houmao remains an internal integration provider. |

## Misc Skills

| Intent | Skill | Boundary |
| --- | --- | --- |
| Bounded command-run planning for risky or heavy operations. | `isomer-misc-bounded-run-tips` | Helper guidance consulted by setup or verification workflows. |
| NVIDIA tooling guidance. | `isomer-misc-nvidia-tools` | Explicit helper guidance when GPU tooling is relevant. |
| Package-specific routing rules. | `isomer-misc-pkg-specifics` | Helper guidance before generic package handling. |
| Named installable toolset contract such as paper-writing, paper-figures-python, paper2ppt, cuda-build, torch-gpu, or topic-python-starter. | `isomer-misc-tool-packs` | Explicitly requested helper only; not automatic package mutation. |

Project-local Toolbox callback, insertion-point, Runtime Param, and registration management routes to `isomer-op-toolbox-mgr`, not to `isomer-misc-tool-packs`.

Do not route active work to retired operator compatibility skills or old admin names.
