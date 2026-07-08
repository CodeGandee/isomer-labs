# Project Skills

Project-specific agent skills live in this packaged asset directory. The repository-root `skillset/` path is an authoring view that links here for distributable skills while keeping `skillset/dev/` local-only.

Installed Isomer packages load official non-development skills from `isomer_labs.assets.system_skills`; runtime code should use package-resource helpers instead of deriving a repository checkout path.

`manifest.toml` is the packaged catalog for system-skill groups, optional system extensions, and callback insertion points. When a packaged skill starts or stops resolving User Skill Callbacks, update the manifest metadata along with the `SKILL.md` workflow text.

| Subtree | Naming | Installation target |
| --- | --- | --- |
| `skillset/operator/` | `isomer-op-<purpose>` | Project Operator Sessions and Operator Agents that operate project control surfaces. |
| `skillset/research-paradigm/` | `isomer-deepsci-<purpose>` production DeepSci research and companion skills | Research-stage workers and research roles that perform reusable research method. |
| `skillset/service/` | `isomer-srv-<purpose>` | Service Team actors that perform bounded operational support. |

Operator skills include the informed-user `isomer-op-entrypoint` dispatcher plus module-level workflows such as `isomer-op-topic-team-specialize`; local subcommands inside those modules cover help, guided and automatic specialization, project awareness, Topic Team Specialization support, approval provenance, profile materialization, and team launch orchestration. Production DeepSci research-paradigm skills handle the active core method such as scouting, baseline work, ideation, experiments, analysis, decision, finalization, optimization, science validity, writing, review, rebuttal, plotting, figure polishing, Nature data availability, Nature figures, paper-to-PPT conversion, and Nature-style prose polishing. Service skills handle support tasks such as topic environment setup, Agent Workspace setup support, diagnostics, monitoring, and support Artifact writing.

Do not install `isomer-op-*` skills into ordinary research team members unless the role is explicitly an Operator Agent role. Do not place operator control-surface skills under `skillset/research-paradigm/`.

## Namespace Convention

All Isomer system-skill names keep the `isomer-` product prefix. New names should use one of these responsibility prefixes:

| Prefix | Responsibility |
| --- | --- |
| `isomer-misc-<purpose>` | Public cross-domain helper interfaces that other Isomer skill families may call. These are not domain extensions. |
| `isomer-op-<purpose>` | User-facing operator skills for Project Operator Sessions and Operator Agents. |
| `isomer-srv-<purpose>` | Protected service-routed skills for bounded operational support. |
| `isomer-<extension-name>-<purpose>` | Domain extension skill families. The extension name identifies the concrete domain or methodology, such as `deepsci` for DeepScientist-derived research skills. |

Use `isomer-<extension-name>-<purpose>` for future extension families, for example `isomer-deepsci-scout` or a future `isomer-chem-*` family. Do not use `isomer-ext-*` as a generic extension bucket because extensions are named by their domain family. Keep `isomer-misc-*` for stable utility-like helper interfaces that are intentionally shared across domains.
