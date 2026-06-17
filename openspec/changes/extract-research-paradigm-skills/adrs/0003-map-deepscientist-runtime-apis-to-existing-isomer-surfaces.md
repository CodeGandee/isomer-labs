# Map DeepScientist Runtime APIs to Existing Isomer Surfaces

## Status

accepted

## Context

DeepScientist skills are executable inside a DeepScientist runtime because they call tool APIs such as `artifact.*`, `memory.*`, `bash_exec(...)`, and DeepXiv or arXiv helpers. Isomer Labs has not settled equivalent concrete APIs for the research-paradigm skillset.

The migration goal is to extract research behavior, not to port DeepScientist runtime APIs.

## Decision

Do not port DeepScientist runtime APIs into the research-paradigm skills. Map each source API dependency to existing Isomer concepts, then mark any concrete operation surface as `yet-to-be-determined`.

| DeepScientist operation | Isomer framing |
| --- | --- |
| `artifact.confirm_baseline(...)` | Decision Record selecting or accepting baseline evidence, with Artifact and Evidence Item refs |
| `artifact.waive_baseline(...)` | Decision Record resolving a Gate or recording a justified exception |
| `artifact.submit_idea(...)` | Artifact describing a hypothesis or candidate direction; Decision Record when selected; Research Branch when work forks |
| `artifact.record_main_experiment(...)` | Run record, Artifact, Evidence Item, Research Claim update, and Provenance Record |
| `artifact.create_analysis_campaign(...)` | Analysis plan Artifact plus one or more Research Tasks, Runs, or Workflow Stages when execution is needed |
| `artifact.record_analysis_slice(...)` | Artifact and Evidence Item linked to the relevant Research Claim, Run, or reviewer concern |
| `artifact.submit_paper_outline(...)` | Artifact containing paper outline, scoped claims, evidence boundaries, and missing evidence |
| `artifact.submit_paper_bundle(...)` | Artifact bundle for report or manuscript material, with Evidence Item and Provenance refs |
| `artifact.interact(kind="decision_request", ...)` | Gate routed through the Operator Agent; Decision Record after resolution |
| `artifact.complete_quest(...)` | Decision Record resolving finalization and Research Thread lifecycle transition |
| `memory.*` | Finding, Evidence Item, Artifact, or prior durable context query; concrete query/write API is `yet-to-be-determined` |
| `bash_exec(...)` | Execution capability supplied by an Execution Adapter and Capability Binding; concrete command API is `yet-to-be-determined` |
| DeepXiv or `artifact.arxiv(...)` | Literature search and reading capability; provider and API are `yet-to-be-determined` |

The migrated skills should request durable evidence, decisions, execution, or literature capabilities in generic terms. They must not require the DeepScientist API names.

## Considered Options

- Port the DeepScientist APIs as an Isomer compatibility surface.
- Replace every API call with a guessed file path convention.
- Map behavior to existing Isomer records and capabilities, with concrete APIs deferred.

## Consequences

- The skills remain portable across future Isomer execution adapters.
- Concrete API design stays visible as a platform gap instead of being hidden in skill text.
- Validation must search for DeepScientist API names and confirm any remaining matches are provenance or explicit mapping only.
- The first implementation can preserve research exit criteria and durable-output expectations without claiming an API contract that does not exist yet.
