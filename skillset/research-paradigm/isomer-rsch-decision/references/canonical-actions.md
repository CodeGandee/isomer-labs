# Canonical Actions

Use these action labels to keep Decision Records legible. They are labels for research route outcomes, not runtime commands.

| Action | Use when | Typical next output |
| --- | --- | --- |
| continue | The active route remains valid and only needs the next bounded step. | Workflow Stage handoff |
| launch_experiment | A selected route needs one main Run. | experiment handoff |
| launch_analysis | A main result needs focused follow-up evidence. | analysis handoff |
| branch | A new Research Branch should be opened or recommended. | Decision Record and branch rationale |
| prepare_branch | A plausible branch needs a brief or feasibility check before activation. | idea or optimize handoff |
| activate_branch | A prepared branch becomes the active mainline. | current-board update |
| reuse_baseline | Existing comparator evidence should remain active. | baseline handoff or acceptance note |
| attach_baseline | An existing comparator should be linked, verified, or accepted. | baseline handoff |
| publish_baseline | A baseline state is ready for downstream use. | Decision Record or Gate |
| write | Evidence is ready for report, paper, or summary drafting. | write handoff |
| review | A substantial draft or package needs skeptical audit. | review handoff |
| finalize | Closure, pause, publication, or archive is justified. | finalize handoff |
| iterate | The current stage should continue with a bounded correction. | stage-local plan |
| reset | The current line is invalid enough to restart a route. | Decision Record and new scout or idea route |
| stop | The current objective should end or be parked. | Gate or finalization handoff |
| request_operator_gate | The route depends on human preference, scope, cost, privacy, safety, finality, or a missing user-held source. | Gate through the Operator Agent |

Choose the smallest action that resolves the state. If an action would imply a concrete API, schema, storage layout, or scheduler behavior, describe the intended record and use a TBD placeholder such as `[[tbd-surface:schema-decision-record]]` only when the concrete surface must be named.
