# Semantic Surface Plan

## Workflow

1. Resolve existing topic record labels for general Artifacts, Research Tasks, Runs, View Manifests, and logs.
2. Check whether the planned evidence, provenance, and package labels are implemented in this workspace. If they are missing, mark them as planned and blocked instead of treating them as available.
3. Identify placeholder needs that do not fit ordinary Artifacts or existing labels. Use `custom.*` labels only when the user or topic policy needs distinct location, retention, or provenance behavior.
4. Build DEEPSCI:RSCH-STORAGE-LABEL-PLAN with each semantic label, availability, intended placeholder kinds, current access command or blocker, and notes for later typed record commands.
5. Refuse hard-coded fallback paths when a semantic label is missing; create DEEPSCI:RSCH-WORKSPACE-BLOCKER-RECORD instead.

If the user's task does not map cleanly to these steps, use your native planning tool to separate available semantic labels from planned or blocked support before producing a plan.

## Required Label Groups

- Existing topic record labels: `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, `topic.records.views`, and `topic.records.logs`.
- Planned topic record labels: `topic.records.evidence`, `topic.records.provenance`, and `topic.records.packages`.
- Optional labels: `custom.datasets.*` or another `custom.*` label only when ordinary Artifact handling is not enough.

## Output Shape

For each label, report:

- semantic label
- resolved path or unavailable status
- source of resolution
- placeholder kinds that may use it
- producer skill or actor
- blocker or next action

Keep the semantic label as the authority even when generated links or convenience paths exist.
