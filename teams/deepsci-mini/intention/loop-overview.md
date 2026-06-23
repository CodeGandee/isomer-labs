# Loop Overview: deepsci-mini

`deepsci-mini` is a small Domain Agent Team Template for the UC-01 headless vertical slice. It preserves DeepScientist practice as a compact, user-steered research loop: scout the topic, synthesize evidence into follow-up inquiry options, skeptically check claim strength, and return to the user for a Decision Record.

## Objective

- Enable a researcher to explore a new Research Topic without launching the full seven-role `deepsci-org` team.
- Produce durable UC-01 research state: source summaries, literature notes, claim candidates, Evidence Item candidates, review notes, inquiry options, View Manifest refs, a follow-up Research Inquiry Gate, a selected Research Inquiry, and a Decision Record.
- Keep the team simple enough for deterministic adapter simulation and optional live Houmao validation in Milestone 6.

## Template Lifecycle

| Isomer Layer | Meaning for `deepsci-mini` |
| --- | --- |
| Domain Agent Team Template | This reusable package, `{domain_agent_team_template_ref}`, with three default roles, manual-mode routing, Coordination Policy intent, and binding slots. |
| Topic Agent Team Profile | A derived topic profile inside `{topic_agent_team_profile_bundle_ref}`, specialized for `{research_topic_id}` with UC-01 constraints, expected Artifacts, policies, and bindings. |
| Agent Team Instance | `{agent_team_instance_id}`, the runtime team created from the profile with concrete Agent Instances and Agent Workspaces. |
| Run | `{run_id}`, a bounded execution attempt for `{research_task_id}` recorded through Workspace Runtime. |

## Participants

- `deepsci-mini-lead`: internal root role, owns routing, handoff normalization, Gates, Decision Records, and closeout.
- `deepsci-mini-scout`: gathers seed sources, related literature, benchmark or dataset notes, and candidate Evidence Items.
- `deepsci-mini-synth-reviewer`: clusters evidence into factor hypotheses, checks weak claims, and proposes follow-up Research Inquiry options.

## Operating Model

- Topology intention: `tree-loop`.
- Default Control Mode: manual.
- Work enters through `{research_topic_id}`, `{research_inquiry_id}`, `{research_task_id}`, and `{control_mode}` resolved from Effective Topic Context.
- The Project-facing Operator Agent may select this template, specialize it into the selected Research Topic's fixed Topic Agent Team Profile Bundle, launch `{agent_team_instance_id}`, and record task-routing changes, but `deepsci-mini-lead` remains the root role inside the team.
- Specialists own bounded Research Tasks and return durable handoffs to `deepsci-mini-lead`.
- The loop finishes when `deepsci-mini-lead` opens a follow-up-inquiry Gate and the Operator Agent records the selected Research Inquiry as a Decision Record.

```text
User / Operator Agent
        |
        v
deepsci-mini-lead
  |-- scout-handoff ---------> deepsci-mini-scout
  |                              returns source summaries, literature notes,
  |                              claim candidates, Evidence Item candidates
  |
  |-- synth-review-handoff --> deepsci-mini-synth-reviewer
                                 returns factor clusters, inquiry options,
                                 weak-claim notes, review notes
        |
        v
follow-up Research Inquiry Gate -> Decision Record
```

## Workspace Expectations

- `teams/deepsci-mini/` is an authoring package for the reusable template.
- `{project_manifest_ref}` is the discovery authority for Research Topics, Topic Workspaces, Domain Agent Team Templates, Topic Agent Team Profiles, and Agent Team Instances.
- `{topic_workspace_ref}` is the topic-level storage and runtime area for one Research Topic.
- `{workspace_runtime_ref}` records Research Inquiries, Research Tasks, Runs, handoffs, Artifacts, Evidence Items, Findings, Gates, Decision Records, View Manifests, and Provenance Records.
- Agent Workspaces live inside `{topic_workspace_ref}` for concrete `{agent_instance_id}` values; the template only states boundary rules.

## Constraints

- Keep `deepsci-mini` as a Domain Agent Team Template, not a concrete Topic Agent Team Profile or Agent Team Instance.
- Keep Houmao-native refs inside adapter payloads, manifests, or adapter tables.
- Do not promote claim candidates to supported Research Claims unless valid Evidence Item links exist.
- Manual Mode does not bypass Gates.
- The lead cannot close UC-01 without a follow-up Research Inquiry Gate and Decision Record.
- Generated loop material must not embed credentials, provider payloads, concrete project paths, live process ids, mailbox routes, or gateway routes.

## Open Questions

- Should the Milestone 6 UC-01 command expose `deepsci-mini` as the default only, or allow an experimental `--team-template deepsci-org` override for comparison?
