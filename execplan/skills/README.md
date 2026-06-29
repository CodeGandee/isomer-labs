# Skills

## Purpose

Skill packages for the deepresearch loop. The role → installed-skill map is
`../agents/skill-bindings.toml` (agent/mailbox identities live in `../agents/bindings.toml`).
Each skill is bounded (one event / one tick / one purpose), touches state ONLY through harness
commands (via `$HARNESS`), and is idempotent where applicable. Mail-received skills are entered
from Houmao notifier prompts after the separate notifier detects open mail.

Skill-invoked harness writes carry a `--via skill:<id>[/<action>]:<role>` stamp; the harness
enforces a per-role authority allowlist and records a `skill-invocation` audit artifact
(see `../harness/src/records.py`). Tier-A skills (read-only reference, additive render/manuscript
output) are safe for any role; stateful/gated actions stay in the loop/control skills below.

## Skill format

Every skill is **self-contained**: it carries everything an agent needs to execute it inside its own
folder, with no dependency on another skill's files or on any external content source. Long material
lives under that skill's own `references/` folder (linked from the workflow); shorter material is
inlined. The only outward pointers that remain are runtime commands an agent invokes — e.g.
`$HARNESS render`, `$HARNESS knowledge`, `$HARNESS record apply`, and the config paths an operator
skill acts on — which are called, not copied.

Each `SKILL.md` follows the same structure:

- frontmatter `name` (matching the folder) and a `description` that starts with `Use when …` and
  states triggering conditions only;
- `## Overview` — the skill's purpose in 1–2 sentences;
- `## When to Use` — triggers plus an explicit "when NOT to use" note;
- `## Workflow` — numbered steps ending with a freeform native-planning fallback;
- `## Common Mistakes` — guardrails and the failure modes to avoid;
- plus any domain detail sections (Inputs, Commands, Gates, Audit/Boundaries, …) the skill needs.

## Loop / control skills (10)

- `deepresearch-shared-guide/` — shared harness/comms usage conventions (installed in every agent).
- `deepresearch-on-task-request/` — specialist on-event handler for `deepresearch.email.task-request`
  (role-aware; per-stage detail in `references/stage-work.md`).
- `deepresearch-on-receipt/` — orchestrator on-event handler for `deepresearch.email.receipt`.
- `deepresearch-on-task-result/` — orchestrator on-event handler for `deepresearch.email.task-result`.
- `deepresearch-on-self-wakeup/` — orchestrator on-event handler for `deepresearch.email.self-wakeup`
  (sole continuation root).
- `deepresearch-orchestrator-tick/` — orchestrator on-tick stage machine (reconcile / dispatch /
  terminate; finalize/dispatch detail in `references/finalize-and-dispatch.md`).
- `deepresearch-operator-control/` — operator lifecycle/mode/recovery control.
- `deepresearch-mentor/` — companion calibration (Houmao-native); installed in the orchestrator.
- `deepresearch-llm-reviewer/` — independent surrogate evaluator for the idea-level BO loop; scores
  candidate moves into `bo_review` valuations. Bound to the BO-reviewer role.
- `deepresearch-research-contract/` — **pre-launch (setup-time)** expansion of a minimal
  Objective/Acceptance into a deeper, operator-approved scientific done-bar; records the
  `research-contract` artifact the launch gate requires. Operator-run during the start-runbook
  (not mail-triggered; no agent binding).

## Publication / render skills (4)

Additive-output skills that produce figures, decks, manuscripts, and prose helpers by invoking a
`$HARNESS render` (or manuscript) command. The agent-facing material each one needs — contracts,
checklists, layout procedure — is carried in its own `references/` folder; the heavy rendering work
is done by the runtime command, which is backed by an internal adapter the agent does not touch.

- `deepresearch-figure/` — create or polish a figure (`actions`: `plot`, `nature`, `polish`;
  figure/QA/polish checklists under `references/`).
- `deepresearch-manuscript-aux/` — manuscript prose/data helpers (`actions`: `polish`, `datastmt`).
- `deepresearch-paper-latex/` — compile a Markdown manuscript to a venue PDF (`render report`).
- `deepresearch-slides/` — build a real `.pptx` (HTML fallback) deck (`render slides`; deck
  procedure under `references/`).

## Methodology / reference skills (8)

Read-only skills that carry their methodology craft in-folder and surface it for a stage. The same
material is also discoverable at runtime through `$HARNESS knowledge cards` / `$HARNESS knowledge
query`; these skills change no quest state.

- `deepresearch-ideation-rubric/`, `deepresearch-intake-rubric/`, `deepresearch-paper-craft/`,
  `deepresearch-review-craft/`, `deepresearch-rebuttal-craft/`, `deepresearch-research-method/`,
  `deepresearch-science-scipkg/`, `deepresearch-mentor-standards/`.

The loop's methodology contract binds each worker stage to a required reference: an agent must
consult it via `$HARNESS knowledge cards`, produce the stage's typed record, and report
`methodology_used[]` so `$HARNESS methodology check` can resolve `applied_as`. See
`deepresearch-shared-guide/references/methodology.md` for the required-by-stage binding table.
