# Runtime and File Boundaries

Use this local reference when the Topic Team Specialization skill needs placement, ownership, or mutation rules.

## Topic Profile Placement

- Store topic-specific copied template material inside the selected Topic Workspace's Topic Agent Team Profile Bundle.
- Use `<topic-workspace>/team-profile/` as the fixed profile bundle root for one Research Topic.
- For `deepsci-mini`, use `<topic-workspace>/team-profile/execplan/` as the copied template root when the template declares `execplan` as copyable material.
- Place `team-specialization-guide.md` and `team-specialization-plan.md` inside the copied template root because they explain and govern that copied material.
- Do not edit Domain Agent Team Template source during Topic Team Specialization.
- Do not create a directory named `teams` under a Topic Workspace for topic-specific profiles.

## Runtime Boundaries

- Treat Workspace Runtime as the authority for Runs, handoffs, completion observations, Artifacts, Gates, View Manifests, and runtime validation state.
- Do not write command outputs, live process ids, provider payloads, scheduler internals, credentials, API keys, or secrets into Research Topic Config or Topic Agent Team Profile material.
- Do not treat runtime readiness as profile configuration. Report readiness as validation input or blocker.
- Use Project Manifest refs for discovery. Keep profile bundle body material inside the Topic Workspace.

## Service Boundaries

- Route environment readiness, dependency repair, diagnostics, copied material reconnaissance, and support Artifact writing through bounded Service Requests when operational support is needed.
- Keep Service Team outputs as support Artifacts or provenance inputs. Do not make Topic Service Agents research task handlers or Agent Team Instance members by default.
- Preserve Service Request scope, expected outputs, allowed file surfaces, validation obligations, approval posture, and provenance refs.

## Launch Boundaries

- Do not launch from Domain Agent Team Template material alone.
- Do not launch from preview-only Topic Agent Team Profile output.
- Launch requires an approved Topic Agent Team Profile Bundle, Workspace Runtime readiness, Agent Team Instance creation inputs, and Execution Adapter preflight.
