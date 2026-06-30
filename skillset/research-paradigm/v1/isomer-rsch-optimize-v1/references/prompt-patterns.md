# Prompt Patterns

Use this reference when prompt shape affects candidate generation, plateau handling, fusion, or debug work.

## Common Skeleton

- introduction
- task description
- retrieved Findings and Evidence Items
- previous solution or previous line
- instructions
- stable response lead-in when needed
- explicit response format

## Reasoning Contract

- What is changing?
- Why is the current line limited?
- How should the change address the limitation?
- What must remain stable for comparability?
- What concrete next action follows?

## Plateau Pattern

When a line is stagnating, state the plateau, forbid trivial same-family tweaks when a deeper change is needed, and require a larger representational, architectural, objective, measurement, or route shift.

## Fusion Pattern

Identify the real strength of each source line, explain why strengths are complementary, avoid combining everything, and preserve the comparison surface.

## Debug Pattern

Restate the concrete error, state the likely root cause, require the minimal targeted fix, and preserve the original solution intent unless the bug proves the design invalid.

## Guardrail

A good optimize pass changes the frontier or stops a stale line. It does not generate activity without moving the incumbent or recording a stop decision.
