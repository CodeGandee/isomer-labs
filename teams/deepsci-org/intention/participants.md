# Participants

This file describes the default Agent Roles in the `deepsci-org` Domain Agent Team Template. These are role definitions and topic-level binding slots, not concrete Agent Instances.

## Topology

- Topology intention: tree-loop.
- Root role: `deepsci-org-master`.
- Specialist roles: `deepsci-org-framer`, `deepsci-org-designer`, `deepsci-org-experimenter`, `deepsci-org-analyzer`, `deepsci-org-publisher`, and `deepsci-org-reviewer`.
- Routing rule: specialists return durable handoffs to `deepsci-org-master`; they do not recursively dispatch peers unless `{topic_agent_team_profile_id}` grants that authority through `{coordination_policy_ref}`.
- Runtime rule: a concrete `{agent_instance_id}` exists only after `{agent_team_instance_id}` is launched from `{topic_agent_team_profile_id}`.

## Topic-Level Binding Slots

| Agent Role | Agent Profile Placeholder | Capability Binding Placeholder | Skill Binding Projection Placeholder |
| --- | --- | --- | --- |
| `deepsci-org-master` | `{deepsci_org_master_agent_profile_ref}` | `{deepsci_org_master_capability_binding_ref}` | `{deepsci_org_master_skill_projection_ref}` |
| `deepsci-org-framer` | `{deepsci_org_framer_agent_profile_ref}` | `{deepsci_org_framer_capability_binding_ref}` | `{deepsci_org_framer_skill_projection_ref}` |
| `deepsci-org-designer` | `{deepsci_org_designer_agent_profile_ref}` | `{deepsci_org_designer_capability_binding_ref}` | `{deepsci_org_designer_skill_projection_ref}` |
| `deepsci-org-experimenter` | `{deepsci_org_experimenter_agent_profile_ref}` | `{deepsci_org_experimenter_capability_binding_ref}` | `{deepsci_org_experimenter_skill_projection_ref}` |
| `deepsci-org-analyzer` | `{deepsci_org_analyzer_agent_profile_ref}` | `{deepsci_org_analyzer_capability_binding_ref}` | `{deepsci_org_analyzer_skill_projection_ref}` |
| `deepsci-org-publisher` | `{deepsci_org_publisher_agent_profile_ref}` | `{deepsci_org_publisher_capability_binding_ref}` | `{deepsci_org_publisher_skill_projection_ref}` |
| `deepsci-org-reviewer` | `{deepsci_org_reviewer_agent_profile_ref}` | `{deepsci_org_reviewer_capability_binding_ref}` | `{deepsci_org_reviewer_skill_projection_ref}` |

## `deepsci-org-master`

- Purpose: own the whole team after launch, interpret the Research Topic, plan the route, dispatch bounded Research Tasks, collect handoffs, record Decisions and Gates, and close or park the loop.
- Required skills: `isomer-rsch-shared`, `isomer-rsch-decision`, `isomer-rsch-finalize`.
- Optional skills: `isomer-rsch-review` when the master must inspect a review handoff before opening a Gate.
- Hot context: `{research_topic_id}`, `{research_inquiry_id}`, `{workflow_stage_cursor_ref}`, `{gate_state_ref}`, `{decision_record_refs}`, `{handoff_refs}`, `{completion_watcher_contract_ref}`, and final closure state.
- Topic specialization: `{topic_agent_team_profile_id}` may tune default stage order, completion watchers, user interruption points, and automatic-mode limits.

## `deepsci-org-framer`

- Purpose: frame the problem, constrain the external search space, and establish the comparator context.
- Required skills: `isomer-rsch-shared`, `isomer-rsch-scout`, `isomer-rsch-baseline`.
- Optional skills: `isomer-rsch-science` for package or environment checks, `isomer-rsch-paper-outline` when the frame must state paper evidence needs early.
- Hot context: literature neighborhood, dataset and split contract, metric contract, comparator candidates, source identity, deviations, baseline evidence, and Baseline-Waiver Policy refs.
- Topic specialization: `{literature_provider_binding_ref}`, `{baseline_waiver_policy_ref}`, and `{deepsci_org_framer_capability_binding_ref}` decide how broad scouting and baseline repair can become.

## `deepsci-org-designer`

- Purpose: convert the accepted frame into a falsifiable route and manage algorithm-first optimization when needed.
- Required skills: `isomer-rsch-shared`, `isomer-rsch-idea`, `isomer-rsch-optimize`.
- Optional skills: `isomer-rsch-scout` for narrow literature checks that change idea selection.
- Hot context: current board, accepted comparator, objective contract, candidate frontier, selected route, rejected alternatives, fusion ideas, and stop conditions.
- Topic specialization: `{topic_agent_team_profile_id}` may decide whether this role runs a small idea board, a larger optimization frontier, or a branch-comparison plan across multiple Agent Team Instances.

## `deepsci-org-experimenter`

- Purpose: implement selected routes and run main evidence-bearing Runs.
- Required skills: `isomer-rsch-shared`, `isomer-rsch-experiment`, `isomer-rsch-science`.
- Optional skills: `isomer-rsch-analysis` for tiny post-run checks that do not justify a separate analyzer handoff.
- Hot context: code, environment, commands, Run contract, logs, outputs, metrics, reproducibility facts, failure modes, and Provenance Records.
- Topic specialization: `{deepsci_org_experimenter_capability_binding_ref}` should provide command execution, repository inspection, package management, notebook execution, HPC job, or other Research Operation Extension Point refs only when the topic permits them.
- Parallelism: `{topic_agent_team_profile_id}` may fan this role out across multiple Agent Instances when `{research_task_id}` defines isolation, merge rules, and governed-resource limits.

## `deepsci-org-analyzer`

- Purpose: run follow-up evidence work after a main result and protect the team from overgeneralizing one Run.
- Required skills: `isomer-rsch-shared`, `isomer-rsch-analysis`, `isomer-rsch-science`.
- Optional skills: `isomer-rsch-paper-plot`, `isomer-rsch-figure-polish` for analysis-facing result displays.
- Hot context: parent result, parent Research Claim, slice definitions, comparability verdicts, analysis findings, claim updates, and caveats.
- Topic specialization: `{topic_agent_team_profile_id}` may define default slice templates, robustness checks, ablation budgets, and analysis-facing Artifact Format Profile refs.
- Parallelism: this role may fan out across independent slices when each slice has a parent claim, fixed conditions, comparability boundary, and evidence path expectation.

## `deepsci-org-publisher`

- Purpose: own report, paper, figure, and presentation surfaces without changing research truth.
- Required skills: `isomer-rsch-shared`, `isomer-rsch-paper-outline`, `isomer-rsch-write`, `isomer-rsch-paper-plot`, `isomer-rsch-figure-polish`.
- Optional skills: source DeepScientist companions `nature-data`, `nature-figure`, `nature-paper2ppt`, and `nature-polishing`, or future Isomer equivalents, only when `{topic_agent_team_profile_id}` needs those publication surfaces.
- Hot context: paper contract, claim-evidence map, outline, draft, bibliography, figure inventory, bundle status, data availability expectations, and publication Gates.
- Topic specialization: `{artifact_format_profile_ref}`, `{publication_surface_ref}`, and `{deepsci_org_publisher_skill_projection_ref}` decide whether the output is an internal report, paper draft, figure bundle, slide deck, or venue-specific package.

## `deepsci-org-reviewer`

- Purpose: provide a separate skeptical audit surface and route rebuttal pressure.
- Required skills: `isomer-rsch-shared`, `isomer-rsch-review`, `isomer-rsch-rebuttal`, `isomer-rsch-analysis`.
- Optional skills: `isomer-rsch-scout` for novelty benchmarking and comparator-paper checks.
- Hot context: draft, claim-evidence map, novelty benchmark, reviewer items, revision log, missing-evidence inventory, and likely rejection routes.
- Topic specialization: `{coordination_policy_ref}` should state whether the reviewer can use broad Peer Read Access or only promoted Artifacts and declared handoff bundles.
