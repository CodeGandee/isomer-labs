# Baseline Pressure Scenario: Houmao Loop Customization Guidance

## Setup

You are the Isomer Labs Project Operator Agent. You have access to the project root at `/data/huangzhe/code/isomer-labs`. The user asks:

> "I want to run the DeepScientist research team template under Houmao management for a new research topic. Explain how the Houmao agent loop works and what I should customize so that DeepScientist's stage skills (scout, baseline, idea, experiment, write, finalize) are executed by Houmao-managed agents instead of the native DeepScientist runner. List the exact customization points and file paths, and tell me whether each stage skill maps to a Houmao role, recipe, preset, specialist, launch profile, or loop package."

## Constraints

- Answer using only the local source code at `extern/orphan/houmao` and `extern/orphan/DeepScientist`.
- Do not use prior training knowledge about Houmao or DeepScientist.
- Produce a concise markdown report with:
  1. A one-paragraph summary of the Houmao agent loop.
  2. A table mapping each DeepScientist stage skill to the correct Houmao customization concept and file path.
  3. A list of concrete files an Isomer operator would edit to add a new stage skill.

## Success Criteria

- The report correctly identifies that Houmao's loop is a gateway-driven request queue plus TUI-tracking lifecycle kernel.
- The report correctly distinguishes Houmao roles, recipes/presets, specialists, launch profiles/dossiers, and loop packages.
- The report points to real paths such as `extern/orphan/houmao/src/houmao/agents/realm_controller/gateway_service.py`, `extern/orphan/houmao/.houmao/agents/presets/`, `extern/orphan/DeepScientist/src/skills/*/SKILL.md`, etc.
- The report does not conflate DeepScientist's single PI-agent stage-skill model with Houmao's multi-agent role/recipe model.

## Pressures

- Domain terminology overload: Houmao and DeepScientist use overlapping words (role, skill, loop) for different things.
- File navigation burden: the answer requires reading across two external checkouts.
- Time constraint: the user expects a concise, actionable answer, not a long exploration.
