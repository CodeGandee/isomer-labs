# Claude effort / reasoning level (pre-launch selection)

When a quest's agents run on Claude (`participant.tool='claude'`), the operator must choose a **Claude effort
(reasoning) level** before launch. This is a mandatory pre-launch item, hard-gated like the clarification,
research-contract, and GPU gates (see `records.py::_effort_gate` and `start-runbook.md` Step 3c).

## How effort is applied (Houmao Claude provider)

The level is a non-negative **`reasoning_level` preset index**. At launch the Houmao Claude provider
(`houmao.agents.model_mapping_policy.project_reasoning_level`, `tool="claude"`) projects it into the agent
home's `settings.json` key **`effortLevel`** and appends **`--effort <value>`** to the Claude launch command.
A level that is unset injects nothing → Claude Code runs at its own default.

The level can be supplied two ways, and the provider projection is identical either way:
- **Persisted on the launch profile** (`profile set --reasoning-level <N>`; catalog
  `launch_profiles.reasoning_level`) — **template-level**: the value lives on the shared `deepresearch-*`
  profile and is inherited by **every** quest launched from it.
- **One-off launch override** (`agents launch --reasoning-level <N>`) — **quest-scoped**: applied to this
  launch only; the shared profile is never written.

> **Quest-independence rule (REQUIRED).** Per-quest settings must NOT mutate the predefined template. So apply
> effort with the **one-off launch override at Step 6**, NOT `profile set`. The shared profiles stay pristine
> (no `reasoning_level`), and each quest carries its own effort as a launch flag. Same applies to the model:
> pass `--model <id>` at launch rather than pinning it on the shared `default` credential bundle (which then
> holds only the OAuth token). The recorded `effort.md` + `artifact.record(kind="effort-selection")` remain the
> audit trail and satisfy the effort gate; only the *application mechanism* moves from profile/bundle to launch.

## Confirmed index → effort mapping

Verified by executing `houmao.agents.model_mapping_policy.resolve_reasoning_mapping(tool="claude", …)` against
the **installed** provider (do not assume; re-confirm if Houmao is upgraded):

| `reasoning_level` | `effortLevel` (settings.json) + `--effort` | Selection label |
|---|---|---|
| **unset (None)** | nothing injected — Claude's own default | **Standard / default** |
| `0` | **invalid — provider raises** "does not support reasoning level 0" | (never use) |
| `1` | `low` | (available via Custom) |
| `2` | `medium` | (available via Custom) |
| `3` | `high` | **High** |
| `4` | `max` — **only if the model name contains `opus-4-6`**; otherwise **saturates to `high`** | **Max / extended** |
| `≥5` | saturates to the highest available preset | — |

## Max / extended on this deployment

The provider gates the `max` preset behind `_claude_model_supports_max(model_name)`, which currently returns
true **only** when the model name contains `opus-4-6`. This box runs **Opus 4.8** with `model_name` unset, so:

- **`max` is NOT available here** — requesting level 4 saturates to `high` (`effective_level=3`, `saturated=True`).
- Do **not** force `--model …opus-4-6…` just to unlock `max` on a 4.8 runner (that would misname the model).
- Therefore **High (level 3) is the effective ceiling** on this deployment. Present "Max / extended" only as
  *unavailable on this runner (saturates to High)* until the installed Houmao provider learns the current
  model family. Re-run the probe after any Houmao upgrade.

## Standard / default

"Standard / default" means **pass no `--reasoning-level` at launch** (leave it unset), which
is distinct from level 0 (which errors). It yields Claude Code's built-in default effort.

## Operator options (Step 3c)

Structured choices, plus a free-form custom option. The chosen level becomes a **launch-time** flag
(`agents launch --reasoning-level <N>`), NOT a `profile set` — keep the shared profiles pristine:

- **Standard / default** → pass no `--reasoning-level` at launch (unset → Claude's default).
- **High** → launch all agents with `--reasoning-level 3` (`high`).
- **Max / extended** → only if supported (see above); otherwise shown as unavailable (saturates to High).
- **Role-specific** → choose a level per role; pass that role's `--reasoning-level <N>` on its launch command.
- **Other / custom** → explicit index (1=low, 2=medium, 3=high, 4=max) and/or a `--model` override at launch;
  the operator owns the trade-off.

The chosen level(s) are recorded to `runs/<q>/objective/effort.md` and as an
`artifact.record(kind="effort-selection")` (this is what satisfies the effort gate), and applied at launch to
all Claude roles unless the operator selects role-specific levels. The shared `deepresearch-*` profiles keep
`reasoning_level` **unset** so the choice never leaks into the next quest's template.

## Verifying it took effect (at the next real launch)

There is no `--dry-run`; confirm end-to-end at Step 6 by inspecting a launched agent's home `settings.json`
(`effortLevel` present at the chosen value) and the launch command (`--effort <value>`).
