## Why

Kaoju currently jumps straight from a user prompt to an artifact-producing survey procedure. Operators often need an intermediate, read-only planning discussion to agree on scope, evidence strategy, and the right command before any durable work begins. An explore-oriented helper keeps that discussion in memory, asks targeted questions, and only proceeds after explicit consent.

## What Changes

- Add a new protected Kaoju member `isomer-kaoju-explore` below `isomer-ext-kaoju-entrypoint`.
- Expose one new public entrypoint command `explore` that delegates interactive planning to the new subskill.
- The explore subskill maintains an in-memory coverage map and asks up to five clarification questions; it writes no files, artifacts, Runs, Gates, or Service Requests by default.
- On consent, the entrypoint command routes to the selected Kaoju command or procedure and executes it.
- Add an `exploration_procedures` category to the checked Kaoju process contract so the new command sits beside `survey_intents` and `compatibility_procedures` instead of being forced into either bucket.
- Update the Kaoju welcome command map to list the new `explore` command.

## Capabilities

### New Capabilities
- `kaoju-explore-subskill`: Behavior, output contract, guardrails, and subcommand structure for the new interactive planning helper.

### Modified Capabilities
- `kaoju-research-extension`: The Kaoju public pack gains one protected member (`isomer-kaoju-explore`) and one public command (`explore`). The process contract and manifest inventory counts change accordingly.

## Impact

- `src/isomer_labs/kaoju/resources/survey-process.v2.json`
- `src/isomer_labs/kaoju/contracts.py`
- `src/isomer_labs/assets/system_skills/manifest.toml`
- `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/SKILL.md`
- `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/commands/explore.md` (new)
- `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/subskills/isomer-kaoju-explore/` (new)
- `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-welcome/references/show-command-map.md`
- Unit tests that lock the Kaoju contract and system-skill inventory counts.
