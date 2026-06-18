# Operational Guidance

Use this reference when the experiment route needs longer planning, resource, recording, or charting notes than the main control surface.

## Planning Surfaces

Use plan and checklist Artifacts only when they help control a non-trivial Run. Otherwise keep the Run contract small and move to the first decisive execution step.

Before substantial implementation work or a real main Run, create or update visible plan and checklist Artifacts from `references/plan-template.md` and `references/checklist-template.md`.

## Working Boundaries

Only modify the active Topic Workspace for this experiment line. Treat the accepted comparator as read-only. Keep durable outputs inside accepted Artifact surfaces and record durable outputs as experiment output Artifacts resolved by Workspace Path Resolution.

## Resource and Environment Rules

Respect explicit resource limits and record real environment or dependency constraints. Do not silently consume broader resources. Capture enough environment information that the Run can be reconstructed, and record unavailable environment-capture commands as gaps.

## Required Durable Outputs

A meaningful experiment pass should leave behind:

- Run contract Artifact.
- durable command, config, log, output, metric, and environment pointers.
- Run log Artifact or Evidence Item resolved by Workspace Path Resolution.
- metric records and evaluation summary.
- Research Claim update.
- Decision Record for next route.
- Provenance Records for inputs, execution, outputs, and manual decisions.

## Findings and Reuse

Use Findings to avoid repeating known failures or to preserve reusable experiment lessons. The canonical Run record belongs in Artifacts and Evidence Items, not only in conversation context.

## Recording Rules

Use progress records for long-running execution updates, Evidence Items for results, Decision Records for continue, Research Inquiry Relationship, analysis, write, reset, or stop decisions, and Gate Policy preflight plus Gates for governed expensive, risky, credentialed, private-data, external-upload, long-compute, destructive-change, or publication-facing actions. Use the accepted Artifact and Provenance recording API for durable record updates.

## Chart Notes

When connector-facing charts or milestone visuals are produced, keep them restrained and evidence-focused. Highlight the decisive delta, keep baseline or comparator styling neutral, and do not invent a chart schema inside this skill.

## Failure and Blocked Handling

Classify failed Runs as implementation, evaluation, environment, direction, data-contract mismatch, resource exhausted, numeric instability, external dependency blocked, or non-comparable metrics. Record what was attempted, where failure occurred, whether retry is justified, and the single best next action.
