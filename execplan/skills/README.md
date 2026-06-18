# Skills

## Purpose

Generated skill packages for the deepresearch loop. The role → installed-skill map is
`../agents/skill-bindings.toml` (agent/mailbox identities live in `../agents/bindings.toml`).
Each skill is bounded (one event / one tick / one purpose), touches state ONLY through harness
commands (via `$HARNESS`), and is idempotent where applicable. Mail-received skills are entered
from Houmao notifier prompts after the separate notifier detects open mail.

Skill-invoked harness writes carry a `--via skill:<id>[/<action>]:<role>` stamp; the harness
enforces a per-role authority allowlist and records a `skill-invocation` audit artifact
(see `../harness/src/records.py`). Tier-A skills (read-only reference, additive render/manuscript
output) are safe for any role; stateful/gated actions stay in the loop/control skills below.

## Loop / control skills (9)

- `deepresearch-shared-guide/` — shared harness/comms usage conventions (installed in every agent).
- `deepresearch-on-task-request/` — specialist on-event handler for `deepresearch.email.task-request` (role-aware; per-stage detail in `actions/stage-work.md`).
- `deepresearch-on-receipt/` — orchestrator on-event handler for `deepresearch.email.receipt`.
- `deepresearch-on-task-result/` — orchestrator on-event handler for `deepresearch.email.task-result`.
- `deepresearch-on-self-wakeup/` — orchestrator on-event handler for `deepresearch.email.self-wakeup` (sole continuation root).
- `deepresearch-orchestrator-tick/` — orchestrator on-tick stage machine (reconcile / dispatch / terminate).
- `deepresearch-operator-control/` — operator lifecycle/mode/recovery control.
- `deepresearch-mentor/` — companion calibration (Houmao-native; reads the `mentor-standards` pack); installed in the orchestrator.
- `deepresearch-research-contract/` — **pre-launch (setup-time)** expansion of a minimal Objective/Acceptance
  into a deeper, operator-approved scientific done-bar; records the `research-contract` artifact the launch
  gate requires. Operator-run during the start-runbook (not mail-triggered; no agent binding).

## Pack-wrapper skills (12)

Thin triggers over the deterministic adapters/commands in `../packs/`; the pack is the source of truth.

Output / render (additive artifacts only):
- `deepresearch-figure/` — create or polish a figure (`actions/`: `plot` → paper-plot, `nature` → nature-figure, `polish` → figure-polish).
- `deepresearch-manuscript-aux/` — manuscript prose/data helpers (`actions/`: `polish` → nature-polishing, `datastmt` → nature-data).
- `deepresearch-paper-latex/` — compile a Markdown manuscript to a venue PDF (`render report`).
- `deepresearch-slides/` — build a real `.pptx` (HTML fallback) deck (`render slides`).

Reference-pack methodology lookups (read-only; surface a pack via `knowledge cards`/`knowledge query`):
- `deepresearch-ideation-rubric/`, `deepresearch-intake-rubric/`, `deepresearch-paper-craft/`,
  `deepresearch-review-craft/`, `deepresearch-rebuttal-craft/`, `deepresearch-research-method/`,
  `deepresearch-science-scipkg/`, `deepresearch-mentor-standards/`.

## Packs

See `../packs/`. The publication set (paper-latex, paper-plot, figure-polish, nature-*) and the
`science-scipkg` science/HPC reference pack are enabled by default; only `mentor-standards` ships disabled.
