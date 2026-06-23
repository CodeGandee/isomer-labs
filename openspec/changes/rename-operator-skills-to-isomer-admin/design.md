## Context

The repository currently has a clear naming contract for research-stage skills: `skillset/research-paradigm/` contains portable research method skills named `isomer-rsch-*`. The recent topic-team instantiation work added project-operator orchestration skills to that same subtree, including project awareness, service request routing, template inspection, topic context resolution, placeholder reconciliation, profile drafting, review and approval, profile materialization, and team launch orchestration.

Those skills are not ordinary research-stage skills. They are control-surface skills for a Project Operator Session or Operator Agent. Some of their outputs are also consumed by Topic Service Agents, but the installation target and authority boundary are different from scout, baseline, experiment, analysis, write, review, and other research-stage skills.

## Goals / Non-Goals

**Goals:**

- Create `skillset/operator/` as the home for Project Operator Session and Operator Agent skills.
- Rename operator-installable skills from `isomer-rsch-*` to `isomer-admin-*`.
- Keep `skillset/research-paradigm/` focused on reusable research-stage method skills.
- Keep Service Team-only support skills in `skillset/service/` with service naming, not operator/admin naming.
- Update validation so renamed skills have consistent folder names, frontmatter names, manifests, prompts, and references.
- Update team profiles, docs, tests, and fixtures so they refer to the new skill names.

**Non-Goals:**

- Do not create a durable Project Operator Agent profile in this change.
- Do not change Workspace Runtime, Topic Team Instantiation Packet, Topic Agent Team Profile Bundle, or Houmao adapter schemas beyond skill refs and documentation.
- Do not rewrite research-stage skill content unrelated to the moved operator skills.
- Do not remove Topic Service Agent support behavior; only separate its skill naming and installation target.

## Decisions

### Decision: Use `skillset/operator/` for Operator/Admin Skills

Operator-installable skills will live under `skillset/operator/`. This keeps the package boundary visible in the filesystem and makes it possible to validate, install, and document operator skills separately from research-stage skills.

Alternative considered: keep the files under `skillset/research-paradigm/` and only rename them. That would leave the installation target ambiguous and force research skill validation to understand operator-only exceptions.

### Decision: Use `isomer-admin-<purpose>` Names

The active skill folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` `display_name`, and default prompt will all use `isomer-admin-<purpose>` for operator/admin skills. The migration mapping is:

| Current skill | New operator skill |
| --- | --- |
| `isomer-rsch-project-aware` | `isomer-admin-project-aware` |
| `isomer-rsch-service-request-route` | `isomer-admin-service-request-route` |
| `isomer-rsch-template-inspect` | `isomer-admin-template-inspect` |
| `isomer-rsch-topic-context-resolve` | `isomer-admin-topic-context-resolve` |
| `isomer-rsch-placeholder-reconcile` | `isomer-admin-placeholder-reconcile` |
| `isomer-rsch-topic-profile-draft` | `isomer-admin-topic-profile-draft` |
| `isomer-rsch-profile-review-approval` | `isomer-admin-profile-review-approval` |
| `isomer-rsch-profile-materialize` | `isomer-admin-profile-materialize` |
| `isomer-rsch-team-launch-orchestrate` | `isomer-admin-team-launch-orchestrate` |

Alternative considered: use `isomer-op-*`. The word “admin” is more explicit about project control, mutation, approval, and launch-adjacent authority, while “op” is easy to confuse with generic operations or workflow stages.

### Decision: Keep Service Team Support Outside the Admin Namespace

`isomer-rsch-topic-service-agent-support` is a Topic Service Agent support skill, not an operator skill. It should move to a service-appropriate name, such as `isomer-srv-topic-service-agent-support`, under `skillset/service/`, while the existing `isomer-srv-env-setup` remains there.

Alternative considered: rename Topic Service Agent support to `isomer-admin-topic-service-agent-support`. That would mislabel a service actor as an admin actor and weaken the Project Operator Session versus Service Team boundary.

### Decision: Update Validation by Skillset

Research validation should continue to enforce `isomer-rsch-*` inside `skillset/research-paradigm/`. Operator validation should enforce `isomer-admin-*` inside `skillset/operator/`. Service validation should enforce service skill naming for service bundles. The existing `pixi run validate-research-skills` may be extended or complemented with a new repository command, but each validation error should identify the affected path and line.

Alternative considered: create one broad validation command with loose naming rules. That would make skill placement mistakes easier to miss.

### Decision: Preserve Compatibility Through Explicit Migration, Not Shims

Active docs, manifests, fixtures, and tests should switch to the new names. Avoid keeping duplicate old skill folders or active alias skills under `skillset/research-paradigm/`, because duplicate active skills would keep the namespace confusion alive. If migration notes are useful, keep them in docs or provenance, not as installable shims.

Alternative considered: keep old directories as compatibility shims. The project has recently been cleaning up compatibility shims, and active duplicate skill names would make installation and validation less deterministic.

## Risks / Trade-offs

- Existing references may be missed → Use `rg` for every old skill name and add validation that fails when moved operator skills still appear as active `isomer-rsch-*` refs.
- Topic Service Master may lose needed skills during renaming → Update its required skill list intentionally, using `isomer-admin-*` only when the service actor truly needs operator-admin behavior and `isomer-srv-*` for service-specific support.
- Validation command scope may become confusing → Document which command validates research, operator, and service skillsets, and expose a repository-level validation command when practical.
- Archived OpenSpec changes may still mention old names → Treat archived or provenance mentions as historical, while active docs, current changes, tests, templates, and manifests use the new names.

## Migration Plan

1. Create `skillset/operator/` and move operator-installable skill bundles into it with `isomer-admin-*` names.
2. Move Topic Service Agent-only support into `skillset/service/` with a service name.
3. Update frontmatter, manifests, prompts, README tables, team profile refs, fixtures, OpenSpec active specs, and tests.
4. Add or extend validation for research, operator, and service skillsets.
5. Run OpenSpec validation, skill validation, lint, typecheck, tests, and targeted topic-team instantiation tests.
