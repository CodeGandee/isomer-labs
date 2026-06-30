# Project Skills

Project-specific agent skills live in this directory. Use the subtree that matches the intended installation target.

| Subtree | Naming | Installation target |
| --- | --- | --- |
| `skillset/operator/` | `isomer-admin-<purpose>` | Project Operator Sessions and Operator Agents that operate project control surfaces. |
| `skillset/research-paradigm/` | `isomer-rsch-<purpose>-v2` for active current research and companion skills; `isomer-rsch-<purpose>-v1` for preserved first-generation skills | Research-stage workers and research roles that perform reusable research method. |
| `skillset/service/` | `isomer-srv-<purpose>` | Service Team actors that perform bounded operational support. |

Operator/admin skills include module-level workflows such as `isomer-admin-topic-team-specialize`; local subcommands inside that module cover help, guided and automatic specialization, project awareness, Topic Team Specialization support, approval provenance, profile materialization, and team launch orchestration. Research-paradigm v2 skills handle the active core method such as scouting, baseline work, ideation, experiments, analysis, decision, finalization, optimization, science validity, writing, review, rebuttal, plotting, figure polishing, Nature data availability, Nature figures, paper-to-PPT conversion, and Nature-style prose polishing. Preserved v1 skills retain intake and older first-generation paper-facing guidance for compatibility. Service skills handle support tasks such as topic environment setup, Agent Workspace setup support, diagnostics, monitoring, and support Artifact writing.

Do not install `isomer-admin-*` skills into ordinary research team members unless the role is explicitly an Operator Agent role. Do not place operator control-surface skills under `skillset/research-paradigm/`.
