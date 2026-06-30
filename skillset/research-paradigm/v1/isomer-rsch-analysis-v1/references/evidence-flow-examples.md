# Evidence Flow Examples

Use this reference when the evidence question is clear but the exact Artifact sequence is not. These are examples, not the only legal routes.

Provenance: see `provenance.md`.

Hard rule: once a supplementary slice is launched as analysis campaign work, its state must become a durable Artifact, Evidence Item, Finding, Decision Record, or Gate update through the accepted Artifact and Provenance recording API.

## 1. One Launched Supplementary Slice

Use when one extra experiment is enough but lineage or reviewability matters.

Typical sequence:

1. Resolve parent Artifact, Research Claim, or Run ids through the host Artifact or Provenance Record surface.
2. Create or update a durable campaign Artifact with one slice.
3. Run the slice in the assigned Agent Workspace, Workspace Runtime, or other isolated execution surface.
4. Record a slice Evidence Item with status, evidence path, claim update, comparability verdict, caveat, and next action.
5. Record the route implication as a Decision Record or next-stage handoff.

Good:

- one-slice campaign still gives durable lineage and review visibility

Bad:

- running the slice locally and only mentioning the result in chat

## 2. Multi-Slice Evidence Package

Use when several slices together answer one evidence question.

Typical sequence:

1. Define the currently justified slice frontier.
2. Create or update a durable campaign Artifact.
3. Execute slices one by one in their assigned execution surfaces.
4. After each launched slice, record a slice Evidence Item.
5. Aggregate only after slice-level evidence exists.

Good:

- summary comes after slice records, not before

Bad:

- pretending planned slices count as evidence before they run

## 3. Writing-Facing Slice

Use when the slice directly supports a report, paper, review, or rebuttal contract.

Typical sequence:

1. Recover or inspect the selected outline, evidence ledger, report matrix, section notes, claim ids, table ids, reviewer item, or rebuttal item.
2. Create or update a campaign Artifact with available writing-facing mapping fields.
3. Run the slice.
4. Record the slice Evidence Item.
5. Write back to the evidence ledger, section notes, report matrix, reviewer item, or rebuttal package.

Good:

- slice is durable and also write-backable

Bad:

- slice is completed but the report or paper contract still looks missing

## 4. Failed or Infeasible Slice

Use when the slice cannot complete honestly.

Typical sequence:

1. Stop, supersede, or mark the slice when blocked.
2. Keep the real blocker visible.
3. Record a non-success slice Evidence Item.
4. Route to redesign, decision, experiment, idea, write, stop, or blocker.

Good:

- non-success still becomes durable evidence

Bad:

- silently replacing a failed slice with a different slice and only reporting the later success

## 5. Read-Only Bounded Audit

Use when no slice is launched and the answer comes from existing outputs, tables, logs, Artifacts, Evidence Items, Findings, or files.

Typical sequence:

1. Inspect the existing evidence.
2. Leave a durable report, Finding, Decision Record, or Gate update.
3. Do not pretend this was a launched campaign slice.

Good:

- this avoids unnecessary campaign overhead

Bad:

- skipping durable slice recording for a real launched supplementary run and calling it a read-only audit afterward

Use Agent Workspace resolved by Workspace Path Resolution for assigned execution surfaces.
