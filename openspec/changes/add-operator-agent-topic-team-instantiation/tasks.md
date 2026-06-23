## 1. Domain Language and Template Inspection Foundations

- [x] 1.1 Update canonical domain language for Topic Team Specialization, Project Operator Session, Topic Service Agent, Topic Service Master, and their Service Request boundaries.
- [x] 1.2 Add a generic Topic Team Instantiation Packet model, parser, serializer, and validator that captures Topic Team Specialization input and output: template ref, topic refs, the fixed Topic Workspace-local Topic Agent Team Profile Bundle path, role bindings, policy refs, expected Artifacts, copied template material plan, proposed topic edits, approval state, bundle-local approval ref when approved, deferrals, Project Operator Session provenance, Topic Service Agent provenance, and validation refs.
- [x] 1.3 Add packet validation diagnostics for missing required fields, unresolved required placeholders, invalid deferrals, cross-topic refs, runtime truth, and secret-like fields.
- [x] 1.4 Extend Domain Agent Team Template inspection to expose placeholder catalogs, instantiation schema paths, copyable material declarations, role binding slots, Agent Workspace placeholders, and workflow stage ownership.
- [x] 1.5 Extend Domain Agent Team Template validation so `topic_instantiation_required` and placeholder catalogs are accepted at template layer.
- [x] 1.6 Add template-boundary validation that rejects concrete Topic Agent Team Profile Bundle, Agent Team Instance, launch, approval, credential, or Run truth inside template source material.
- [x] 1.7 Reject user-selected profile ids in launch-facing packet and bundle materialization paths; derive Topic Agent Team Profile identity from the selected Research Topic and fixed `<topic-workspace>/team-profile/` bundle path.

## 2. Topic Agent Team Profile Bundle Materialization

- [x] 2.1 Add a packet-backed profile bundle materialization API that writes or previews the Research Topic's Topic Agent Team Profile Bundle under `<topic-workspace>/team-profile/` from a validated instantiation packet, including `profile.toml`, packet metadata, copied topic-edited template material, approved topic edits, bundle-local approval provenance, validation outputs, and provenance refs.
- [x] 2.2 Update existing Topic Team Specialization preview output so synthetic Python defaults are labeled as preview or candidate material, not authoritative instantiation.
- [x] 2.3 Extend Topic Agent Team Profile validation to recognize profile bundle layout, packet provenance, copied material refs, and save-time versus launch-facing validation.
- [x] 2.4 Reject launch-facing profiles with unresolved required placeholders unless the linked packet explicitly defers them and reports launch blockers.
- [x] 2.5 Reject materialization or Project Manifest registration when a Topic Agent Team Profile Bundle path is outside the selected Topic Workspace or inside another Research Topic's Topic Workspace.
- [x] 2.6 Reject materialization or Project Manifest registration that would create a second active Topic Agent Team Profile Bundle for the same Research Topic.
- [x] 2.7 Add deterministic positive and negative packet fixtures for `deepsci-mini` profile bundle materialization, including copied material plans and topic edit proposals.

## 3. Project Operator and Topic Service Skills

- [x] 3.1 Create `isomer-project-aware` skill instructions for resolving the Isomer Project root, reading the Project Manifest, reading supplied topic prompts or topic files, listing Research Topics, locating or creating the selected Topic Workspace, and discovering Topic Service Agents.
- [x] 3.2 Create `isomer-service-request-route` skill instructions for opening bounded Service Requests from a Project Operator Session or Operator Agent to Topic Service Agents.
- [x] 3.3 Create `isomer-template-inspect` skill instructions for inspecting template manifest, placeholder catalog, role bindings, workflow stages, workspace contract, and diagnostics.
- [x] 3.4 Create `isomer-topic-context-resolve` skill instructions for resolving Research Topic Config, Effective Topic Context, Topic Workspace, Workspace Runtime readiness, and policy or binding refs.
- [x] 3.5 Create `isomer-placeholder-reconcile` skill instructions for mapping template placeholders to concrete values, copied material plans, proposed topic edits, or explicit deferrals in an instantiation packet.
- [x] 3.6 Create `isomer-topic-profile-draft` and `isomer-profile-review-approval` skill instructions for drafting reviewable profile bundle material, copied template material changes, proposed topic edits, launch blockers, and bundle-local approval provenance requests.
- [x] 3.7 Create `isomer-profile-materialize` and `isomer-team-launch-orchestrate` skill instructions for calling generic validators/materializers and routing launch requests through the Houmao adapter.
- [x] 3.8 Create Topic Service Agent skill instructions for topic environment readiness, work-agent setup, Topic Team Specialization support, copied material planning, topic edit drafting, Agent Team Instance monitoring, diagnostics, and support Artifact writing.
- [x] 3.9 Add research skill validation coverage for the new project-operator and Topic Service Agent skill files and their required references.

## 4. Houmao Topic Service Agent Definition and Adapter Provenance

- [x] 4.1 Add or update a Houmao-compatible Topic Service Agent definition that loads topic-specific Service Team skills and receives bounded Project/Topic context refs.
- [x] 4.2 Add a Topic Service Master posture or Agent Profile when one topic-scoped service actor should coordinate multiple Service Requests or subordinate Service Agent Instances.
- [x] 4.3 Extend Workspace Runtime records or linked metadata so Agent Team Instance creation can reference profile bundle ref, packet ref, bundle-local approval ref, project operator actor/session ref, Topic Service Agent refs, and validation provenance.
- [x] 4.4 Update Agent Team Instance creation to reject launch-facing requests from preview-only profiles unless an approved packet with validated approval provenance is present.
- [x] 4.5 Record project operator provenance distinctly from team member Agent Instances and Service Agent Instances.
- [x] 4.6 Update Houmao launch materialization and quick-launch preflight to reject template-only launch requests without approved profile bundle/runtime material.
- [x] 4.7 Update Houmao adapter command, payload, launch, inspect-live, stop, and reconcile records to preserve bounded project operator and Topic Service Agent provenance refs when present.
- [x] 4.8 Ensure Topic Service Agent managed-agent refs are distinguishable from research Agent Team Instance member refs.

## 5. UC-01 and deepsci-mini Acceptance

- [x] 5.1 Update the UC-01 fixture or manual harness so `deepsci-mini` is first inspected as a Domain Agent Team Template and materialized through a deterministic project-operator and Topic Service Agent packet path before any live Houmao Topic Service Agent path is required.
- [x] 5.2 Remove hardcoded UC-01 or `deepsci-mini` profile substitution from the UC-01 harness except in fixture data and assertion code.
- [x] 5.3 Add tests proving the `deepsci-mini` packet materializes the expected profile bundle, copied specialized template material, topic edits, and lead, scout, and synthesis-reviewer role bindings without product-code special cases.
- [x] 5.4 Add tests proving invalid `deepsci-mini` packets are rejected before Agent Team Instance creation or Houmao launch materialization.
- [x] 5.5 Keep live Houmao Topic Service Agent launch optional and gated, while deterministic packet, profile bundle, and runtime tests pass without live Houmao.

## 6. CLI, Docs, and Roadmap

- [x] 6.1 Update CLI help/docs for Topic Team Specialization preview versus packet-backed authoritative profile bundle materialization.
- [x] 6.2 Update CLI help/docs so `--profile-id` is preview-only or removed from authoritative materialization paths; launch-facing profile identity is derived from the selected Research Topic and `team-profile/` bundle.
- [x] 6.3 Update Domain Agent Team Template docs to explain placeholder catalogs, `topic_instantiation_required`, and project-operator plus Topic Service Agent instantiation.
- [x] 6.4 Update Houmao adapter docs to show Topic Service Agent launch and project-operator orchestration above adapter launch mechanics.
- [x] 6.5 Update UC-01 workflow docs and troubleshooting to run the project-operator and Topic Service Agent packet path before team simulation or launch.
- [x] 6.6 Update ROADMAP milestones so topic-team instantiation is agent-mediated and `deepsci-mini` is not described as directly instantiated by hardcoded product code.

## 7. Verification

- [x] 7.1 Run `openspec validate add-operator-agent-topic-team-instantiation --strict`.
- [x] 7.2 Run `openspec validate --all`.
- [x] 7.3 Run `pixi run lint`.
- [x] 7.4 Run `pixi run typecheck`.
- [x] 7.5 Run `pixi run test`.
- [x] 7.6 Run `pixi run validate-research-skills`.
- [x] 7.7 Run the UC-01 manual harness and record that packet-backed profile bundle materialization precedes Agent Team Instance creation.
- [x] 7.8 Run `git diff --check` and confirm no generated `__pycache__`, temporary runtime files, or live Houmao state are tracked.
