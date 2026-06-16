# Paper Outline Patterns

Use these examples when repairing an outline that is too close to implementation notes.

## Pattern: Small Mechanism, Big Lesson

Use when the method is simple but the result suggests a reusable principle.

Bad outline:

- "We add a guard and rerun evidence collection."

Better outline:

- "The paper argues that extra evidence helps only when acquisition and update are separated. Acquisition expands coverage; the guard prevents unsupported changes."

Needed analyses:

- guard removed
- extra evidence without guard
- guard with no extra evidence
- failure cases where the guard rejects changes
- budget sensitivity

## Pattern: Targeted Repair

Use when aggregate gains are modest but a diagnosed subset improves.

Bad outline:

- "The method improves only a small subset, so results are weak."

Better outline:

- "Aggregate metrics hide evidence-insufficiency pockets. The method is framed as targeted evidence repair, not a universal evaluator improvement."

Needed analyses:

- define the deficient subset
- compare gains inside and outside the subset
- show examples of repaired cases
- show residual failures
- compare with a stronger or simpler repair baseline

## Pattern: Measurement Reframing

Use when the contribution is mostly how to measure or select data/evidence.

Bad outline:

- "We compute many scores and report which one correlates best."

Better outline:

- "The paper argues that the useful notion of diversity/evidence/quality is the one that predicts downstream generalization under matched scale and quality."

Needed analyses:

- controlled comparison
- correlation or ranking stability
- failure case of old measure
- proxy/model sensitivity
- downstream result using the measure

## Common Negative Examples

Bad:

- "The paper uses a selected outline, paper branch, and worktree."
- "The abstract states dual ports, 64+64, and rerun switches."
- "The method is the latest user requirement."
- "The analysis plan has two runs because those are the completed ones."

Better:

- "The paper uses a fixed comparison budget on a held-out benchmark."
- "Exact local serving settings are appendix reproducibility details."
- "The method is described as an evidence-acquisition and guarded-update procedure."
- "The analysis plan is chosen from reviewer questions: cause, robustness, stronger baselines, failure modes, and cost."

## Quick Checklist

- One-sentence idea: would a reader remember it?
- Evidence: can every claim point to a result?
- Scope: does the outline say where the claim stops?
- Analyses: would 4-8 checks answer likely reviewer questions?
- Language: can the text appear in a paper without explaining the agent workflow?
