## 1. Main Spec Updates

- [x] 1.1 Add the `research-execution-extension-contract` main spec with provider-neutral Research Operation Extension Points, Capability Binding and Skill Binding projection behavior, Execution Adapter Command Request, Gate policy preflight, scheduler boundaries, literature provider extension, baseline-waiver policy extension, and validation requirements.
- [x] 1.2 Update the `cli-topic-context-resolution` main spec so Research Topic Config and Effective Topic Context carry typed extension-point refs without storing secrets, runtime truth, provider payloads, command outputs, scheduler internals, or implementation bodies.
- [x] 1.3 Update the `research-paradigm-skills` main spec so the six resolved placeholders map to accepted Research Execution and Extension Contract terms and skills declare required extension points rather than host APIs or provider names.
- [x] 1.4 Update the `research-recording-contracts` main spec so execution choices, provider results, Gate policy preflight, baseline waivers, scheduler observations, and extension refs record through existing durable records.

## 2. Domain and Architecture Docs

- [x] 2.1 Update `.imsight-arts/project-explore` domain notes with Research Operation Extension Point, Execution Adapter Command Request, Skill Binding projection, scheduler policy, Gate policy, literature provider binding, and baseline-waiver policy terms.
- [x] 2.2 Update `context/` architecture and design notes that mention execution adapter command surface, topic config, Capability Binding, Skill Binding, literature providers, baseline waiver, scheduler policy, or cost/privacy Gates.
- [x] 2.3 Add concise Research Topic Config and Topic Agent Team Profile TOML examples that show topic-level extension defaults, role/stage capability availability, Skill Binding projections, and policy refs without embedding provider-specific command bodies, credentials, scheduler internals, command outputs, or provider payloads.

## 3. Shared Skill Contracts

- [x] 3.1 Update `skillset/research-paradigm/isomer-rsch-shared` shared guidance and the shared TBD registry so `api-execution-command`, `provider-literature-search`, `schema-skill-binding`, `policy-scheduler`, `policy-baseline-waiver`, and `policy-cost-privacy-gate` are removed as active open placeholders or mapped to accepted extension terms.
- [x] 3.2 Update every local `isomer-research-contract.md` copy under `skillset/research-paradigm/isomer-rsch-*` so execution, provider, scheduler, Skill Binding, baseline-waiver, and cost/privacy guidance matches the shared contract.
- [x] 3.3 Search the research-paradigm skillset for stale source terms and ensure DeepScientist, quest, Research Goal, Research Thread, Research Branch, Isomer Workspace, branch/worktree path terms, `workspace_mode`, `continuation_policy`, `auto_continue`, and `wait_for_user_or_resume` appear only as bounded provenance, source mapping, or migration notes.

## 4. Stage Skill Updates

- [x] 4.1 Update command-heavy skills so intake, baseline, optimize, experiment, analysis, science, paper-plot, figure-polish, write, review, rebuttal, and finalize route command, repository, package, notebook, HPC, build, render, export, service, or agent-launch behavior through Execution Adapter Command Requests.
- [x] 4.2 Update literature-facing skills so scout, idea, write, review, rebuttal, paper-outline, baseline, and decision use literature provider extension refs and record literature results as Artifacts, Findings, or Evidence Items according to evidence-use intent.
- [x] 4.3 Update baseline-facing skills so baseline, decision, optimize, experiment, analysis, review, rebuttal, and write require accepted baseline state, baseline-waiver policy refs, or explicit Gate/Decision Records before baseline-dependent promotion.
- [x] 4.4 Update policy-sensitive skill text so cost, credential use, private data, external upload, long compute, destructive changes, publication-facing output, and baseline waiver are governed by Gate policy preflight and not by ad hoc warnings.
- [x] 4.5 Update service and launch references so Service Requests, Service Agent Instance launches, and Agent Team Instance launches use Execution Adapter Command Requests for dispatch, preflight, monitoring, and recording while preserving their distinct domain records.

## 5. Validation

- [x] 5.1 Run `openspec validate define-research-execution-extension-contract` and fix any proposal, design, spec, or task formatting issues.
- [x] 5.2 Run repository searches for the six resolved placeholders and confirm no active guidance still treats them as open TBDs.
- [x] 5.3 Run repository searches for forbidden inline implementation patterns in generic topic context or skill docs, including credentials, provider payloads, command outputs, scheduler internals, and provider-specific command bodies.
- [x] 5.4 Confirm context-only literature provider output is recorded as provider-output Artifacts before any Finding or Evidence Item derivation, and confirm baseline waiver remains a separate policy ref that may open a Gate.
- [x] 5.5 Run `git diff --check` and any relevant documentation or lint checks available for this repository.

## 6. Review

- [x] 6.1 Review the final diff for terminology consistency with Research Topic, Research Inquiry, Research Task, Topic Workspace, Agent Workspace, Workspace Runtime, Run, Artifact, Evidence Item, Finding, Decision Record, Gate, Provenance Record, Workflow Stage Cursor, Operator Agent, Agent Team Instance, Capability Binding, and Execution Adapter.
- [x] 6.2 Confirm the implementation leaves research-specific details as explicit user-fillable extension points and does not introduce a default provider, command runner, scheduler, credential backend, literature provider, baseline registry, or artifact schema beyond the generic contracts.
