## Why

The production DeepSci research skills (`isomer-deepsci-scout`, `baseline`, `idea`, `experiment`, `analysis`, `write`, etc.) are fine-grained single-step tools with explicit artifact handoffs. Today the user or an external controller must decide which skill to invoke next after every stage boundary. This creates friction for recurring multi-step procedures such as "run a full empirical pass" or "turn a result into a paper." A thin orchestration skill that executes named linear recipes once, with automatic artifact handoffs and a terminal report, makes the common paths easier to use without weakening each skill's gate discipline.

## What Changes

- Add a new production DeepSci research skill `isomer-deepsci-pipeline` under `skillset/research-paradigm/deepsci/isomer-deepsci-pipeline/`.
- Define a small catalog of linear pipeline passes as self-contained subcommand pages under `commands/`.
- The skill executes one pass end-to-end, passing artifacts from stage to stage automatically.
- The skill pauses and reports when a stage emits a blocker or a route the recipe cannot satisfy.
- The skill produces a `pipeline-terminal-report` that an external controller can use to decide the next macro action (loop, stop, or run another pipeline).
- Update the `research-paradigm-skills` spec to recognize `isomer-deepsci-pipeline` as an allowed production DeepSci skill folder.
- No existing skill behavior changes; this is a pure orchestration layer.

## Capabilities

### New Capabilities
- `isomer-deepsci-pipeline`: Single-pass orchestration of named production DeepSci skill sequences with automatic artifact handoffs, pause-on-blocker semantics, and a terminal report for external control.

### Modified Capabilities
- `research-paradigm-skills`: Add `isomer-deepsci-pipeline` to the canonical list of production DeepSci research-stage skill folders and to the shared research contract.

## Impact

- New skill folder and provenance material under `skillset/research-paradigm/deepsci/isomer-deepsci-pipeline/`.
- New pass subcommand pages under that skill's `commands/` directory.
- Update to `openspec/specs/research-paradigm-skills/spec.md`.
- No changes to existing `isomer-deepsci-*` skill workflows or semantic-placeholder registry.
