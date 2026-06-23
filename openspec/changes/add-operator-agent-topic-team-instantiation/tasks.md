## 1. Packet and Template Inspection Foundations

- [ ] 1.1 Add a generic Topic Team Instantiation Packet model, parser, serializer, and validator that captures template ref, topic refs, role bindings, policy refs, expected Artifacts, approval state, deferrals, and provenance.
- [ ] 1.2 Add packet validation diagnostics for missing required fields, unresolved required placeholders, invalid deferrals, cross-topic refs, runtime truth, and secret-like fields.
- [ ] 1.3 Extend Domain Agent Team Template inspection to expose placeholder catalogs, instantiation schema paths, role binding slots, Agent Workspace placeholders, and workflow stage ownership.
- [ ] 1.4 Extend Domain Agent Team Template validation so `topic_instantiation_required` and placeholder catalogs are accepted at template layer.
- [ ] 1.5 Add template-boundary validation that rejects concrete Topic Agent Team Profile, Agent Team Instance, launch, approval, credential, or Run truth inside template source material.

## 2. Topic Agent Team Profile Materialization

- [ ] 2.1 Add a packet-backed profile materialization API that writes or previews a Topic Agent Team Profile from a validated Operator Agent packet.
- [ ] 2.2 Update existing profile specialization preview output so synthetic Python defaults are labeled as preview or candidate material, not authoritative instantiation.
- [ ] 2.3 Extend Topic Agent Team Profile validation to recognize packet provenance and distinguish save-time validation from launch-facing validation.
- [ ] 2.4 Reject launch-facing profiles with unresolved required placeholders unless the linked packet explicitly defers them and reports launch blockers.
- [ ] 2.5 Add deterministic positive and negative packet fixtures for `deepsci-mini` profile materialization.

## 3. Operator Agent Skills and Definition

- [ ] 3.1 Create `isomer-template-inspect` skill instructions for inspecting template manifest, placeholder catalog, role bindings, workflow stages, workspace contract, and diagnostics.
- [ ] 3.2 Create `isomer-topic-context-resolve` skill instructions for resolving Project Manifest, Research Topic Config, Effective Topic Context, Topic Workspace, Workspace Runtime readiness, and policy/binding refs.
- [ ] 3.3 Create `isomer-placeholder-reconcile` skill instructions for mapping template placeholders to concrete values or explicit deferrals in an instantiation packet.
- [ ] 3.4 Create `isomer-topic-profile-draft` and `isomer-profile-review-gate` skill instructions for drafting reviewable profile material and requesting approval.
- [ ] 3.5 Create `isomer-profile-materialize` and `isomer-team-launch-orchestrate` skill instructions for calling generic validators/materializers and routing launch requests through the Houmao adapter.
- [ ] 3.6 Add or update a Houmao-compatible Isomer Operator Agent definition that loads the instantiation skills and receives bounded Project/Topic context refs.
- [ ] 3.7 Add research skill validation coverage for the new Operator Agent skill files and their required references.

## 4. Runtime and Adapter Provenance

- [ ] 4.1 Extend Workspace Runtime records or linked metadata so Agent Team Instance creation can reference packet ref, approval ref, Operator Agent actor ref, and validation provenance.
- [ ] 4.2 Update Agent Team Instance creation to reject launch-facing requests from preview-only profiles unless an approved packet or equivalent explicit approval is present.
- [ ] 4.3 Record Operator Agent actor refs distinctly from team member Agent Instances and Service Agent Instances.
- [ ] 4.4 Update Houmao launch materialization and quick-launch preflight to reject template-only launch requests without approved profile/runtime material.
- [ ] 4.5 Update Houmao adapter command, payload, launch, inspect-live, stop, and reconcile records to preserve bounded Operator Agent provenance refs when present.
- [ ] 4.6 Ensure the Operator Agent's own Houmao managed-agent refs are distinguishable from research Agent Team Instance member refs.

## 5. UC-01 and deepsci-mini Acceptance

- [ ] 5.1 Update the UC-01 fixture or manual harness so `deepsci-mini` is first inspected as a Domain Agent Team Template and materialized through a deterministic Operator Agent packet.
- [ ] 5.2 Remove hardcoded UC-01 or `deepsci-mini` profile substitution from the UC-01 harness except in fixture data and assertion code.
- [ ] 5.3 Add tests proving the `deepsci-mini` packet materializes the expected lead, scout, and synthesis-reviewer role bindings without product-code special cases.
- [ ] 5.4 Add tests proving invalid `deepsci-mini` packets are rejected before Agent Team Instance creation or Houmao launch materialization.
- [ ] 5.5 Keep live Houmao Operator Agent launch optional and gated, while deterministic packet/profile/runtime tests pass without live Houmao.

## 6. CLI, Docs, and Roadmap

- [ ] 6.1 Update CLI help/docs for profile specialization preview versus packet-backed authoritative materialization.
- [ ] 6.2 Update Domain Agent Team Template docs to explain placeholder catalogs, `topic_instantiation_required`, and Operator Agent instantiation.
- [ ] 6.3 Update Houmao adapter docs to show Operator Agent orchestration above adapter launch mechanics.
- [ ] 6.4 Update UC-01 workflow docs and troubleshooting to run the Operator Agent packet path before team simulation or launch.
- [ ] 6.5 Update ROADMAP milestones so topic-team instantiation is agent-mediated and `deepsci-mini` is not described as directly instantiated by hardcoded product code.

## 7. Verification

- [ ] 7.1 Run `openspec validate add-operator-agent-topic-team-instantiation --strict`.
- [ ] 7.2 Run `openspec validate --all`.
- [ ] 7.3 Run `pixi run lint`.
- [ ] 7.4 Run `pixi run typecheck`.
- [ ] 7.5 Run `pixi run test`.
- [ ] 7.6 Run `pixi run validate-research-skills`.
- [ ] 7.7 Run the UC-01 manual harness and record that packet-backed profile materialization precedes Agent Team Instance creation.
- [ ] 7.8 Run `git diff --check` and confirm no generated `__pycache__`, temporary runtime files, or live Houmao state are tracked.
