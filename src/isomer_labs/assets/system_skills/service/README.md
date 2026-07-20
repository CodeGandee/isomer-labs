# Protected Service Capabilities

Service capabilities retain `isomer-srv-<purpose>` logical identities, but their active bundles now live below `operator/isomer-op-entrypoint/subskills/`. This directory contains no independently installed service skills.

| Logical ID | Core Member Route | Responsibility |
| --- | --- | --- |
| `isomer-srv-topic-env-setup` | `isomer-op-entrypoint->topic-env` | Topic Workspace, Topic Main Development Repository, external repository projection, and environment predecessor readiness |
| `isomer-srv-agent-env-setup` | `isomer-op-entrypoint->agent-env` | Agent Workspace worktree creation and cwd proof after topic-level predecessors exist |
| `isomer-srv-resolve-pkg-repo` | `isomer-op-entrypoint->package-repo` | Bounded package repository and channel resolution |
| `isomer-srv-houmao-interop` | `isomer-op-entrypoint->houmao` | Bounded Isomer-facing Houmao adapter support |
| `isomer-srv-topic-service-agent-support` | `isomer-op-entrypoint->topic-service` | Topic Service Agent and optional Topic Service Master lifecycle support |

Normal user requests enter through `$isomer-op-entrypoint use <subcommand> to <task>` and an operator owner delegates service work. Service capabilities do not own Research Topics, Research Claims, Gates, Decision Records, research routing, or Agent Team Instance membership.
