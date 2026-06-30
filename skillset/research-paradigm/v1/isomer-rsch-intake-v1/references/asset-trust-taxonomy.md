# Asset Trust Taxonomy

Use this taxonomy to classify existing assets before reuse. Trust is a route decision, not a file-existence check.

## Trust Levels

- accepted: provenance, metric or content role, and comparability are clear enough that later skills can rely on the asset without rerunning intake.
- usable-with-verification: the asset is likely relevant, but a bounded check must confirm provenance, metric, code path, draft role, or review status.
- reference-only: the asset is useful context but must not become active evidence for the current mainline.
- stale-or-conflicting: the asset conflicts with newer evidence, belongs to a superseded Research Inquiry Relationship, or uses an incompatible protocol.
- missing-context: the asset cannot be interpreted because its source, role, parameters, or relationship to the current Research Task is unclear.

## Paper-Facing Visibility

Classify paper or report assets separately from scientific trust:

- main-text-candidate: can support the central story if evidence and coverage checks pass.
- appendix-or-reproducibility: useful for methods, details, or reproducibility without carrying the main claim.
- comparator-or-negative-evidence: useful to explain rejected lines, failed variants, or baseline context.
- reference-only: useful background but not current evidence.
- internal-only: control evidence, notes, user instructions, or runtime traces that should not appear as scientific protocol without rewriting through a writing skill.

## Reuse Rules

- Existing baselines need metric contract, source, and comparability before acceptance.
- Existing main Runs need enough fields to show that the Run is genuinely the accepted result for the current Research Inquiry Relationship.
- Existing analysis outputs need slice question, comparison boundary, status, and claim impact.
- Existing outlines, drafts, or paper bundles need selected role, evidence support, and coverage state before they become active writing inputs.
- Review packages route to review or rebuttal work when reviewer comments define the real task.

## Common Failure Modes

- A draft from an older method is treated as current-method support.
- A promising result becomes a Research Claim without an Evidence Item.
- A command log or branch name is treated as scientific evidence rather than control provenance.
- A stale baseline is accepted because no one recorded why it was superseded.
- Intake reads the entire workspace even though one missing Gate or metric contract already explains the blocker.
