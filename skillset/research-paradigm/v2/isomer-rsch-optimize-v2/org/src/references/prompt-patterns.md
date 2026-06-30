# Optimization Prompt Patterns

These prompt structures are worth preserving across optimize subroutines.

## Common skeleton

- Introduction
- Task description
- Memory
- Previous solution or previous line
- Instructions
- assistant_prefix when a stable response lead-in reduces drift
- Explicit response format

## Common reasoning contract

- WHAT is changing?
- WHY is the current line limited?
- HOW should the change address the limitation?
- KEEP UNCHANGED: what must remain stable for comparability?
- NEXT ACTION: what concrete step follows this prompt?

## Plateau pattern

When the line is stagnating:

- explicitly state that the current approach has plateaued
- forbid trivial hyperparameter-only tweaks when a deeper change is needed
- require a larger representational or architectural shift

## Fusion pattern

When combining lines:

- identify the real strength of each source line
- explain why those strengths are complementary
- avoid combining everything
- preserve the comparison surface

## Debug pattern

For debugging:

- restate the concrete error
- state the likely root cause
- require the minimal targeted fix
- preserve the original solution intent unless the bug proves the design invalid

A good optimize pass changes the frontier or stops a stale line; it does not keep generating activity without moving the incumbent.
