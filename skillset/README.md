# Project Skills

Project-specific agent skills live in this directory. Use the subtree that matches the intended installation target.

| Subtree | Naming | Installation target |
| --- | --- | --- |
| `skillset/operator/` | `isomer-admin-<purpose>` | Project Operator Sessions and Operator Agents that operate project control surfaces. |
| `skillset/research-paradigm/` | `isomer-rsch-<purpose>` | Research-stage workers and research roles that perform reusable research method. |
| `skillset/service/` | `isomer-srv-<purpose>` | Service Team actors that perform bounded operational support. |

Operator/admin skills include module-level workflows such as `isomer-admin-topic-team-specialize`; local subcommands inside that module cover project awareness, Topic Team Specialization support, approval provenance, profile materialization, and team launch orchestration. Research-paradigm skills handle research method such as scouting, baseline work, ideation, experiments, analysis, writing, review, rebuttal, and finalization. Service skills handle support tasks such as topic environment setup, Agent Workspace setup support, diagnostics, monitoring, and support Artifact writing.

Do not install `isomer-admin-*` skills into ordinary research team members unless the role is explicitly an Operator Agent role. Do not place operator control-surface skills under `skillset/research-paradigm/`.
