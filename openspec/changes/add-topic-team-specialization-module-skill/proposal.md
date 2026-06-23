## Why

The operator skillset now has too many fine-grained `isomer-admin-*` skills that behave like exposed helper functions instead of coherent operator workflows. Topic Team Specialization especially needs a single module-level skill that understands a Domain Agent Team Template, copies its material into the Topic Workspace profile bundle, guides adaptation through durable guide and plan files, and leaves an auditable final report.

## What Changes

- Add a combined operator/admin skill, `isomer-admin-topic-team-specialize`, for Domain Agent Team Template understanding and topic-specific adaptation.
- Treat the skill as a module-level operator function that covers template copy, guide discovery or synthesis, specialization planning, adaptation, and final reporting.
- Require topic-specialized copied material to live inside the selected Topic Workspace's Topic Agent Team Profile Bundle, not in the Domain Agent Team Template source and not in a Topic Workspace `teams/` directory.
- Introduce `team-specialization-guide.md` as the template-understanding guide. If the copied template material already contains this file, the operator reads it first; otherwise the operator synthesizes it from copied material and marks it clearly as generated.
- Introduce `team-specialization-plan.md` as the topic adaptation plan. It must include a checklist or task list before adaptation and a `Final Report` section after adaptation.
- Make `isomer-admin-topic-team-specialize` the preferred operator entrypoint for the workflow that previously required separate calls to template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, and related planning skills.
- Preserve lower-level validation, materialization, approval, and launch boundaries: the module skill may prepare packet/profile inputs, but generic validators and approval/materialization skills still own authoritative writes.

## Capabilities

### New Capabilities
- `topic-team-specialization-module-skill`: Defines the `isomer-admin-topic-team-specialize` operator skill, its template guide and specialization plan artifacts, copied template material workflow, generated-guide rule, final report rule, and boundaries with packet/profile validation.

### Modified Capabilities
- None.

## Impact

- Affected skill directories: `skillset/operator/`, especially the operator README and the new `isomer-admin-topic-team-specialize` skill bundle.
- Affected template material: Domain Agent Team Templates such as `teams/deepsci-mini` should include or support generation of `team-specialization-guide.md`.
- Affected topic profile material: Topic Agent Team Profile Bundles should contain copied/adapted template material plus `team-specialization-guide.md` and `team-specialization-plan.md`.
- Affected validation/docs: operator skill validation should recognize the module skill, and docs should describe when to use the module skill instead of calling fine-grained skills directly.
- Affected future cleanup: after this module skill lands, some fine-grained `isomer-admin-*` skills can become internal references, helper sections, or candidates for removal in a later consolidation change.
