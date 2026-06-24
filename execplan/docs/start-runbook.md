# Start Runbook — DeepResearch

Exact ordered commands to take the prepared package live. **Do not run until explicitly approved.**

## Legend
- 🟢 **READ-ONLY** — inspects only; safe to run anytime.
- 🟡 **STATE-MUTATING** — writes files / DB / overlay; reversible (see Rollback).
- 🔴 **LAUNCH-STARTING** — starts live processes / gateway / notifier.

## Render-path toolchain prerequisites (optional; affects output fidelity only)
The publication packs degrade gracefully if a tool is absent (they still record an artifact), but for
full-fidelity output install these in the **quest runtime environment**:
- **paper-latex** (`render report`): `pandoc` + a TeX engine (`xelatex`/`latexmk` + `bibtex`); without them the
  adapter emits `.tex`-only instead of a compiled PDF.
- **nature-paper2ppt** (`render slides`): `python-pptx` (real `.pptx`; falls back to a self-contained HTML deck
  if absent) and `PyMuPDF`/`fitz` (PDF figure extraction; skipped if absent — on-disk `runs/<q>/figures/` still used).
- **paper-plot / nature-figure / figure-polish** (`render plot|figure|polish`): `matplotlib` for vector figures
  (paper-plot falls back to stdlib SVG if absent).

## Variables (set once)
```bash
export PATH="/root/.local/bin:$PATH"
P=/home/linfeng/houmao_DeepScientist
HARNESS="$P/execplan/harness/bin/deepresearch"
QID=q1                                  # quest id for this run (clean slate: derive the next id from `state query cursor`; q1 if none exist yet)
SRC_REPO=/ABS/PATH/TO/PROJECT           # OPTIONAL operator source project to seed the quest repo (else git init fresh)
REPO="$P/runs/$QID/repo"                # quest.workspace_ref — PER-QUEST code repo, lives INSIDE the quest folder (created in Step 4). `outputs/` is unused legacy; never use it.
MAILROOT="$P/.houmao/mailbox"           # SHARED messaging infra (not per-quest); state DB runs/state.sqlite is also shared
now(){ date -u +%FT%TZ; }               # caller-supplied ISO-8601 timestamps
M(){ houmao-mgr project --project-dir "$P" "$@"; }
```

> **Runtime vs source-of-truth.** `execplan/` is the SOURCE OF TRUTH (skills, packs, harness, schemas, docs).
> `.houmao/` is RUNTIME/GENERATED except for `.houmao/agents/` (role/preset/skill templates), `houmao-config.toml`,
> and credentials under `.houmao/content/auth/`. Specifically `.houmao/runtime/homes/claude-brain-*` (per-launch
> agent home snapshots) and `.houmao/runtime/manifests/*` are regenerated from `.houmao/agents/` (which the
> launch installs from `execplan/skills/`) on every launch — **do not edit them by hand and never commit them**
> (`.houmao/.gitignore` is `*`). They accumulate across launches; to reclaim space, stop all agents and delete
> stale `.houmao/runtime/homes/claude-brain-*` snapshots plus their matching `.houmao/runtime/manifests/*.yaml`
> (keep `.houmao/runtime/sessions/`); the next launch rebuilds the homes. If a local launch behaves oddly,
> suspect a stale runtime home and purge it rather than editing it.

---

## Pre-flight 🟢 (read-only gate — must pass before anything below)
```bash
python3 "$HARNESS" selfcheck            # ok=true, 42 record types, 39 invariants, deps ok
M status                                # overlay healthy
M skills list   | grep -c deepresearch- # 21 (9 loop/control + 12 pack-wrapper skills; per-role install in agents/skill-bindings.toml)
# Skill-install reconcile gate — the catalog must match agents/skill-bindings.toml (source of truth). If the
# source gained skills without a re-install (e.g. a methodology port), `grep -c` is < 21 and launched agents
# silently miss them. Verify, and FIX with the same script (idempotent; drop --check to apply):
python3 "$P/execplan/ops/reconcile-skills.py" --check   # exit 0 = OK; exit 1 = drift (re-run without --check)
M profile list  | grep -c deepresearch- # 6
M agents list   | grep instances        # instances [] (nothing live yet)
test ! -f "$P/runs/state.sqlite" && echo "DB absent (expected)"
# REPO is created PER-QUEST under runs/$QID/repo in Step 4 (not pre-existing). If seeding from a source project,
# check it here instead: test -d "$SRC_REPO/.git" && echo "source project is a git repo"
# GPU posture: GPU confirmation is a PRE-LOOP requirement — confirmed per-quest in Step 3 (gpu confirm)
#   BEFORE the quest can move to running. The live loop never re-prompts for GPUs (Step 3 gate + Step 6 assert).
# credential posture: long-lived OAuth token present, NO proxy override, and NO model pin in the launch env.
# The shared `default` bundle holds ONLY the OAuth token (quest-independence) — the model is passed per-launch
# via $AGENT_MODEL at Step 6, never pinned on the bundle/profile. Expect no ANTHROPIC_MODEL in the bundle.
M credentials claude get --name default | grep -iE 'oauth.token|api.key'   # expect a long-lived OAuth token (or api-key)
env | grep -iE '^ANTHROPIC_(BASE_URL|AUTH_TOKEN)=' && echo "WARNING: proxy env set — will shadow the OAuth token; unset before launch" || echo "no proxy env (good)"
```

---

## Step 1 — Set the Claude credential 🟡 (secret) — **canonical: long-lived OAuth token (Pro/Max)**
The agents authenticate via the `default` credential bundle. The **canonical** auth is a **long-lived OAuth
token tied to your Claude.ai Pro/Max subscription** (`claude setup-token`) — it does **not** expire on the
~5 h interactive-login clock, so the loop runs unattended without re-login. **You** run these (the token is a
secret; never paste it into an agent/transcript):
```bash
# (A) CANONICAL — long-lived subscription OAuth token
claude setup-token                       # interactive; prints a long-lived CLAUDE_CODE_OAUTH_TOKEN (Pro/Max)
M credentials claude set --name default \
    --oauth-token '<TOKEN_FROM_setup-token>' \
    --clear-api-key --clear-auth-token --clear-config-dir   # bundle carries ONLY the long-lived OAuth token

# (B) alt — funded API key (Console billing; also non-expiring):
# M credentials claude set --name default --api-key 'sk-ant-...' --clear-oauth-token --clear-auth-token --clear-config-dir
```
Verify 🟢: `M credentials claude get --name default` → shows `CLAUDE_CODE_OAUTH_TOKEN present:true` and
**no** `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN` (no proxy) in the bundle.
> ⚠️ **No proxy shadowing.** If `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` are present in the *launch
> environment*, Claude Code uses that third-party endpoint and **ignores the OAuth token**. The launch steps
> below scrub them (`env -u …`); keep them unset in the shell/tmux that launches the agents.
**Renew:** `setup-token` tokens are long-lived (~1 year) — re-run (A) when it eventually lapses. After any
credential change, **relaunch agents fresh** (a bare `relaunch` reuses the old token cached in the agent home).
**Rollback:** restore placeholder → `M credentials claude set --name default --api-key "PLACEHOLDER-REPLACE-BEFORE-LAUNCH" --clear-oauth-token`

---

## Step 2 — Initialize the platform DB 🟡
```bash
"$HARNESS" state init                   # creates $P/runs/state.sqlite (36 tables, 13 stages)
```
Verify 🟢: `"$HARNESS" state validate`  → `ok:true, checked:39`.
**Rollback (pre-quest only):** `rm -f "$P/runs/state.sqlite"`

---

## Step 3 — Clarify + create the quest 🟡

### Step 3a — MANDATORY pre-launch ambiguity check 🟢 (do this FIRST, before writing any files)

> **ACTIVE — required companion step: research-contract expansion (skill `deepresearch-research-contract`).**
> *Before* writing `objective.md`/`acceptance.md`, expand the operator's minimal Objective/Acceptance into a
> deeper, domain-neutral scientific done-bar (falsifiable claim, mechanism, baseline/ablation, alternative
> ruled out, scope, scholarly positioning, traceability) using the rubric in
> `execplan/docs/research-contract.md`, then have the operator **approve / edit / trim** it (respect the
> over-hardening guardrails — minimal-sufficient, achievable, operator-trimmable). The approved expansion
> becomes the canonical brief written below, and **must** be recorded as a `kind='research-contract'`
> artifact (`runs/$QID/objective/contract.md`). The move to `running` is **hard-gated** on it — a sibling of
> the clarification, GPU, and Claude effort gates (see Step 3c). This step subsumes the ambiguity check
> below: do both, record both artifacts (`clarification` + `research-contract`).

The operator-facing agent MUST inspect the provided objective/prompt for unclear, underspecified, or
ambiguous parts **before** creating the quest, and confirm with the operator. This is **required**, not
optional: the move-to-running below is HARD-GATED on a recorded clarification artifact (the quest cannot
start without it). Walk **all 7 dimensions**; for each that is unclear, ask the operator with structured
multiple-choice options **plus** a free-form "Other/custom" choice (use the `AskUserQuestion` mechanism):

1. **Objective** — falsifiable/measured vs. open exploration; the precise question + scope.
2. **Acceptance** — metric target vs. coverage/process "done"; (offer to draft if undefined).
3. **GPU / devices** — allowed CUDA device set (mandatory; feeds the GPU start-gate).
4. **Domain** — `general` (default) / `nature` / `science` / custom.
5. **Workspace / repo** — seed `runs/$QID/repo` from a source project, or start empty.
6. **Budget** — `max_rounds`, `convergence_patience`, cost budget.
7. **Domain-specific constraints** — hardware/dtype/baseline must-haves, etc.

Outcome is one of: **(1) no blocking ambiguity** → record an explicit "reviewed, none blocking"
attestation; or **(2) clarifications received** → fold the operator's answers into `objective.md` /
`acceptance.md` before creation. Either way a `clarification.md` + `artifact.record(kind=clarification)`
is written below (audit trail).

> ⚠️ **Not the first quest?** Ensure no prior quest is still `running` (`single_active_quest` will reject
> `run_state=running` below otherwise). Each quest's brief is **per-quest** at `runs/$QID/objective/` — the
> previous quest's objective is untouched (no shared-slot overwrite).
```bash
AT=$(now)
# Per-quest objective: write the (EXPANDED + CLARIFIED — Step 3a, operator-approved) brief into
# runs/$QID/objective/ BEFORE quest.create (canonical source the agents read). The deeper done-bar from the
# research-contract expansion lands HERE. shared/objective/ is only an optional staging area.
mkdir -p "$P/runs/$QID/objective"
cp /ABS/PATH/TO/objective.md   "$P/runs/$QID/objective/objective.md"     # operator-approved EXPANDED brief
cp /ABS/PATH/TO/acceptance.md  "$P/runs/$QID/objective/acceptance.md"    # (deep done-bar; or hand-author here)

"$HARNESS" --validate-after-write record apply --json '{
  "record_type":"quest.create","record_id":"'"$QID"'","at":"'"$AT"'",
  "title":"<QUEST TITLE>","objective_ref":"runs/'"$QID"'/objective/objective.md",
  "acceptance_ref":"runs/'"$QID"'/objective/acceptance.md","workspace_ref":"'"$REPO"'",
  "max_rounds":24,"convergence_patience":3 }'

# Record the Step 3a ambiguity check (REQUIRED — the move-to-running gate refuses to start without it).
# clarification.md captures the 7-dimension review + resolutions (or the "no blocking ambiguity" attestation).
cat > "$P/runs/$QID/objective/clarification.md" <<'CLAR'
# Pre-launch clarification — <QID>
Reviewed dimensions: objective, acceptance, GPU/devices, domain, workspace/repo, budget/max_rounds, domain-constraints.
Outcome: <no-blocking-ambiguity | resolved>
Resolutions (option chosen / custom input per dimension):
- ...
CLAR
"$HARNESS" record apply --json '{"record_type":"artifact.record",
  "record_id":"'"$QID"':clarification","at":"'"$(now)"'","quest_id":"'"$QID"'",
  "kind":"clarification","ref":"runs/'"$QID"'/objective/clarification.md"}'

# Record the research-contract (REQUIRED — the move-to-running gate refuses to start without it). contract.md
# captures the original→expanded done-bar diff + rationale + the operator's approve/edit/trim decisions
# (skill deepresearch-research-contract; rubric in execplan/docs/research-contract.md).
cat > "$P/runs/$QID/objective/contract.md" <<'CONTRACT'
# Pre-launch research contract — <QID>
Original Objective/Acceptance (operator):
- ...
Expanded done-bar (rubric dimensions included; operator-approved):
- claim / mechanism / baseline+ablation / alternative-ruled-out / scope / scholarly-positioning / traceability: ...
Operator decisions (approve/edit/trim per block) + rationale:
- ...
CONTRACT
"$HARNESS" record apply --json '{"record_type":"artifact.record",
  "record_id":"'"$QID"':research-contract","at":"'"$(now)"'","quest_id":"'"$QID"'",
  "kind":"research-contract","ref":"runs/'"$QID"'/objective/contract.md"}'

# Register the 6 participant instances (experimenter starts at fanout_default=1)
for pair in orchestrator:orchestrator scout-ideator:scout-ideator \
            experimenter-1:experimenter analyst:analyst writer:writer reviewer:reviewer; do
  inst=${pair%%:*}; role=${pair##*:}
  "$HARNESS" record apply --json '{"record_type":"participant.register",
    "record_id":"'"$QID"':'"$inst"'","at":"'"$(now)"'","quest_id":"'"$QID"'",
    "instance_id":"'"$inst"'","role":"'"$role"'","tool":"claude"}'
done

# GPU confirmation — PRE-LOOP REQUIREMENT (operator confirms the allowed devices BEFORE the loop starts).
# Mandatory: the move-to-running below is HARD-GATED and will fail if no confirmed gpu_allocation exists.
# This is the only point the operator is asked about GPUs; the live loop never re-prompts.
"$HARNESS" gpu confirm --quest-id "$QID" --devices "0" --by "$USER" --at "$(now)"   # e.g. "0" or "0,1" (integer indices only)

### Step 3c — MANDATORY Claude effort selection (when any participant uses tool='claude')
# Claude-conditional pre-launch item, hard-gated like clarification/research-contract/GPU. Detect Claude:
#   the roster in agents/bindings.toml is all tool="claude" by default (so this applies); the _effort_gate
#   itself keys off participant.tool='claude' recorded in Step 3 above.
# If Claude is in use, ASK THE OPERATOR for an effort level (AskUserQuestion) — structured options + custom:
#   Standard/default | High | Max/extended (ONLY if supported — see below) | Role-specific | Other/custom
# CONFIRMED mapping (execplan/docs/claude-effort.md; verified against the installed Houmao Claude provider):
#   unset=Claude default · 1=low · 2=medium · 3=high · 4=max (ONLY if model name has 'opus-4-6', else
#   saturates to high) · level 0 is INVALID. On this Opus-4.8 box, Max is unavailable → High is the ceiling.
# QUEST-INDEPENDENCE RULE — do NOT mutate the shared template. Effort is applied as a LAUNCH-TIME override at
# Step 6 (`agents launch --reasoning-level <N>`), NOT via `profile set`. The shared deepresearch-* profiles stay
# pristine (reasoning_level UNSET) so this quest's choice never leaks into the next quest's template. Capture the
# choice as a var the Step 6 launch loop consumes (High = level 3; empty string = Standard/default → omit flag):
EFFORT_LEVEL=3
# IMPORTANT — reasoning_level does NOT pin a MODEL. Without a model pin Claude Code's per-process default can
# diverge (observed: Orchestrator=Opus 4.8 but specialists silently fell back to Sonnet 4.6). Pin the model the
# SAME quest-independent way: pass it at LAUNCH, NOT on the shared bundle — the `default` bundle keeps ONLY the
# OAuth token. Capture the model as a var the Step 6 launch loop consumes:
AGENT_MODEL=claude-opus-4-8                       # Opus 4.8=claude-opus-4-8, Sonnet 4.6=claude-sonnet-4-6
# (Record EFFORT_LEVEL + AGENT_MODEL in the quest's effort.md.) The operator CONFIRMS the live per-agent models
# at the Step 6c gate before the loop's first trigger. The effort GATE is satisfied by the effort-selection
# artifact below — NOT by any profile/bundle mutation.
# Audit: write the choice + resolved per-role levels, then record the gate token artifact.
cat > "$P/runs/$QID/objective/effort.md" <<'EFFORT'
# Claude effort selection — <QID>
Runner: claude (Opus 4.8).  Choice: <Standard|High|Max|Role-specific|Custom>.
Resolved reasoning_level per role: orchestrator=<N> scout-ideator=<N> experimenter=<N> analyst=<N> writer=<N> reviewer=<N>
Notes (saturation / model override, if any): ...
EFFORT
"$HARNESS" record apply --json '{"record_type":"artifact.record",
  "record_id":"'"$QID"':effort-selection","at":"'"$(now)"'","quest_id":"'"$QID"'",
  "kind":"effort-selection","ref":"runs/'"$QID"'/objective/effort.md"}'

### Step 3d — MANDATORY run-mode selection (auto | assistant) — fifth launch gate
# Ask the operator (AskUserQuestion) to choose the run mode BEFORE launch — orthogonal to execution_mode
# (drive cadence). This keys how strict the loop's self-completeness checks are:
#   auto      → the loop self-disposes; the research-completeness checklist HARD-GATES `complete` when the
#               contract is publication-grade (DEEPRESEARCH_COMPLETENESS_GATE_RIGOR, default 'publication').
#   assistant → advisory; the loop recommends continuation but the operator disposes (checks warn only).
# Also set rigor_level (scoping|standard|publication) for the contract (keys the completeness gate with the mode).
RUN_MODE=auto          # or: assistant
RIGOR=publication      # scoping | standard | publication
houmao-mgr ... # (operator confirms the choice)
"$HARNESS" record apply --json '{"record_type":"quest.update","record_id":"'"$QID"'","at":"'"$(now)"'",
  "autonomy_mode":"'"$RUN_MODE"'","rigor_level":"'"$RIGOR"'"}'
# (equivalently: `$HARNESS control set-mode --quest-id $QID --autonomy $RUN_MODE --at <ts>`)

# Move the quest to running. QUINTUPLE-GATED at not_started->running: refused unless ALL of (a) a confirmed
# gpu_allocation exists (GPU start-gate), (b) a kind='clarification' artifact exists (ambiguity-check gate),
# (c) a kind='research-contract' artifact exists (research-contract gate), (d) — when any
# participant has tool='claude' — a kind='effort-selection' artifact exists (Claude effort gate), AND (e) a
# run mode is chosen (quest.autonomy_mode IN auto/assistant — _autonomy_gate).
# single_active_quest also enforces one running quest at a time.
"$HARNESS" --validate-after-write record apply --json '{"record_type":"quest.update",
  "record_id":"'"$QID"'","at":"'"$(now)"'","run_state":"running","current_stage":"scope"}'
```
Verify 🟢: `"$HARNESS" gpu status --quest-id "$QID"` → `confirmed:true`; `"$HARNESS" state query cursor` → quest running, current_stage scope.
**Rollback (pre-launch):** `rm -f "$P/runs/state.sqlite" && "$HARNESS" state init` (no row-delete command; re-init is the clean reset).

---

## Step 4 — Materialize per-quest work roots + Experimenter worktree(s) 🟡
```bash
# artifact + work-root dirs (objective/ already seeded in Step 3). baseline/ is the per-quest canonical
# comparator+metric-contract path (Scout/Ideator writes it at the baseline stage). shared/ is NOT used as a
# canonical source — it is optional staging/templates only.
mkdir -p "$P/runs/$QID"/{objective,baseline,round-0,report/review,figures,refs,findings,exports,intake,mail,workspaces}
for r in orchestrator scout-ideator analyst writer reviewer; do
  mkdir -p "$P/runs/$QID/workspaces/$r"
done

# Per-quest code repo INSIDE the quest folder ($REPO = runs/$QID/repo). Seed from the operator's source
# project if provided, else start a fresh repo — either way the quest stays self-contained under runs/$QID/.
if [ -d "$SRC_REPO/.git" ]; then git clone "$SRC_REPO" "$REPO"; else mkdir -p "$REPO" && git -C "$REPO" init -q && git -C "$REPO" commit --allow-empty -qm "init quest $QID workspace"; fi

# Experimenter ISOLATED git worktree (fanout_default=1; repeat exp-2..exp-8 to scale to fanout_max=8)
git -C "$REPO" worktree add "$P/runs/$QID/workspaces/experimenter-1" -b "quest/$QID/exp-1"
"$HARNESS" record apply --json '{"record_type":"branch.record","record_id":"exp-1",
  "at":"'"$(now)"'","quest_id":"'"$QID"'","git_branch":"quest/'"$QID"'/exp-1",
  "worktree_ref":"runs/'"$QID"'/workspaces/experimenter-1","status":"active"}'

# (objective.md + acceptance.md were written to runs/$QID/objective/ in Step 3 — the per-quest canonical
#  brief, read-only to agents thereafter. shared/objective/ is optional staging/template only.)
```
Verify 🟢: `git -C "$REPO" worktree list` ; `"$HARNESS" state query branches` ; `ls "$P/runs/$QID/workspaces"`.
**Rollback (pre-launch / abandoning a route):**
```bash
git -C "$REPO" worktree remove "$P/runs/$QID/workspaces/experimenter-1" --force
git -C "$REPO" branch -D "quest/$QID/exp-1"          # NOTE: preserve-failed-routes — only delete pre-launch
rm -rf "$P/runs/$QID"
```

---

## Step 5 — Initialize + register the mailbox 🟡
```bash
M mailbox init
for inst in orchestrator scout-ideator experimenter-1 analyst writer reviewer; do
  M mailbox register --address "$inst@houmao.localhost" --principal-id "$inst" --yes
done
```
Verify 🟢: `M mailbox status` ; `M mailbox accounts`.
**Rollback:** `M mailbox unregister --address "<inst>@houmao.localhost"` (repeat) ; `M mailbox cleanup`.

---

## Step 6 — Launch agents 🔴 (LAUNCH-STARTING: live tmux sessions + per-agent gateway)
> **Launch-readiness gate** — the quest must already be `running` with GPUs confirmed (both established in
> Step 3; the start-gate refuses `running` without confirmation). Assert before launching:
> `"$HARNESS" gpu status --quest-id "$QID" | grep -q '"confirmed": true' || { echo "ABORT: GPUs not confirmed — run Step 3 gpu confirm"; }`
> Also confirm the Claude effort selection (Step 3c): the effort gate already blocked `running` without the
> artifact. Effort + model are applied as LAUNCH FLAGS (`$EFFORT_LEVEL` / `$AGENT_MODEL` → `$LAUNCH_OVERRIDES`),
> NOT on the profile/bundle. Verify the shared template stayed pristine and the vars are set:
> `houmao-mgr project --project-dir "$P" profile get --name deepresearch-orchestrator | grep -i reasoning`
> (expect NONE) and `echo "$EFFORT_LEVEL $AGENT_MODEL"` (expect both set). See `execplan/docs/claude-effort.md`.
>
> **Scrub the proxy env first**, so agents use the `default` long-lived OAuth token and are NOT silently
> routed through a third-party `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN` proxy:
> `unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_API_KEY` (and launch from this clean shell).
```bash
unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_API_KEY   # OAuth token must not be shadowed by a proxy
# Quest-scoped launch overrides (from Step 3c) — applied HERE, never on the shared profile/bundle, so the
# template stays quest-independent. Model always pinned at launch; effort flag omitted when EFFORT_LEVEL empty.
LAUNCH_OVERRIDES="--model $AGENT_MODEL"
[ -n "$EFFORT_LEVEL" ] && LAUNCH_OVERRIDES="$LAUNCH_OVERRIDES --reasoning-level $EFFORT_LEVEL"
# Orchestrator (root)
env -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_API_KEY \
  houmao-mgr project --project-dir "$P" agents launch --profile deepresearch-orchestrator --name orchestrator \
  $LAUNCH_OVERRIDES \
  --workdir "$P/runs/$QID/workspaces/orchestrator" \
  --mail-transport filesystem --mail-root "$MAILROOT" --gateway-background

# Specialists (experimenter uses its isolated worktree as workdir; add experimenter-2..N for fanout>1)
for pair in scout-ideator:scout-ideator experimenter:experimenter-1 \
            analyst:analyst writer:writer reviewer:reviewer; do
  prof=deepresearch-${pair%%:*}; inst=${pair##*:}
  env -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_API_KEY \
    houmao-mgr project --project-dir "$P" agents launch --profile "$prof" --name "$inst" \
    $LAUNCH_OVERRIDES \
    --workdir "$P/runs/$QID/workspaces/$inst" \
    --mail-transport filesystem --mail-root "$MAILROOT" --gateway-background
done
```
Notes: `$HARNESS` is exported on every profile, so the harness resolves regardless of `--workdir`. Gateway auto-attaches per agent (omit `--no-gateway`). **Verify the live auth posture:** `tr '\0' '\n' </proc/$(tmux list-panes -t "$(tmux ls|grep -oE 'HOUMAO-orchestrator-[0-9]+'|head -1)" -F '#{pane_pid}')/environ | grep -i ANTHROPIC` should show **no** `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN` (the agent uses the bundle's `CLAUDE_CODE_OAUTH_TOKEN`).
Verify 🟢: `M agents list` (6 live) ; `houmao-mgr agents single --agent-name orchestrator gateway status`.
**Rollback / stop:** `for inst in orchestrator scout-ideator experimenter-1 analyst writer reviewer; do M agents stop --name "$inst"; done`

---

## Step 6b — Attach notifier prompts to each live gateway 🔴 (requires Step 6 up)
```bash
# instance -> notifier file (experimenter-1 uses experimenter.md)
for pair in orchestrator:orchestrator scout-ideator:scout-ideator experimenter-1:experimenter \
            analyst:analyst writer:writer reviewer:reviewer; do
  inst=${pair%%:*}; role=${pair##*:}
  houmao-mgr agents single --agent-name "$inst" gateway mail-notifier enable \
    --appendix-file "$P/execplan/agents/notifier-prompts/$role.md"   # CONFIRM exact flag: `gateway mail-notifier --help`
done
```
Verify 🟢: `houmao-mgr agents single --agent-name orchestrator gateway mail-notifier status`.
**Rollback:** `houmao-mgr agents single --agent-name "<inst>" gateway mail-notifier disable`

---

## Step 6c — MANDATORY operator model-confirmation gate 🟢→🛑 (agents up, BEFORE the first trigger)
> **Why this exists.** Profiles set only `reasoning.level`, NOT a model name. Without a model pinned on the
> shared credential bundle, Claude Code's per-process default can diverge — observed: the Orchestrator
> resolved to Opus 4.8 while specialists silently fell back to **Sonnet 4.6**, violating the operator's
> Opus-4.8 effort choice. The loop must NOT start the research work until the operator confirms every agent
> is on the intended model.
>
> **Deterministic fix (quest-independent): pass the model at LAUNCH (Step 6), not on the shared bundle.**
> Each `agents launch` carries `--model claude-opus-4-8` via `$LAUNCH_OVERRIDES`, so every agent resolves the
> intended model without mutating the shared `default` bundle (which keeps ONLY the OAuth token). Verify on the
> live agent's TUI header below. Model ids: Opus 4.8 = `claude-opus-4-8`, Sonnet 4.6 = `claude-sonnet-4-6`,
> Haiku 4.5 = `claude-haiku-4-5-20251001`. (Legacy: pinning `--model` on the bundle also works but leaks the
> choice across all quests — disallowed by the quest-independence rule.)

Capture each live agent's ACTUAL resolved model from its TUI header and present the table to the operator
for explicit confirmation. The Step 7 trigger is **hard-gated** on this confirmation.
```bash
for inst in orchestrator scout-ideator experimenter-1 experimenter-2 analyst writer reviewer; do
  S=$(tmux ls 2>/dev/null | grep -oE "HOUMAO-$inst-[0-9]+" | head -1)
  hdr=$(tmux capture-pane -t "$S" -p -S -60 2>/dev/null | grep -iE 'Opus|Sonnet|Haiku|Fable|· Claude' | head -1 | tr -s ' ')
  printf "  %-16s %s\n" "$inst" "${hdr:-<no model header yet — agent still booting>}"
done
```
Outcome — present the per-agent model table and ask the operator (`AskUserQuestion`) to **confirm or abort**:
- **All agents on the intended model** (e.g. every row shows `Opus 4.8`) → operator confirms → proceed to Step 7.
- **Any mismatch** (e.g. a row shows `Sonnet 4.6`) → **STOP**. Do NOT send the trigger. Relaunch the affected
  agents fresh (Step 6) **with `$LAUNCH_OVERRIDES`** (`--model $AGENT_MODEL`) so they resolve the intended
  model — do NOT pin the model on the shared bundle (quest-independence rule; the bundle stays token-only).
  Re-check here. Record the confirmed model set in the quest's `effort.md` (or a `kind='model-confirmation'`
  note) for the audit trail.

---

## Step 7 — Send the first trigger 🔴 (start = nudge the Orchestrator once; loop self-sustains via self-wakeup)
```bash
houmao-mgr agents single --agent-name orchestrator prompt \
  --prompt "Run deepresearch-orchestrator-tick: begin quest $QID at stage scope. One bounded pass, then arm the durable self-wakeup."
```
After this the Orchestrator dispatches `scope` to scout-ideator and arms a `[self-wakeup]` on lane `main`; the mail-notifier drives all subsequent rounds. **Do not** send repeated prompts — the loop is now self-driven.

---

## Step 8 — First post-launch health checks 🟢 (read-only)
```bash
"$HARNESS" state validate                         # CLEAN (39 checks, 0 violations)
"$HARNESS" state query cursor                      # quest running; current_stage advancing past scope
"$HARNESS" wakeup list --quest-id "$QID"           # exactly one armed|delivered wakeup, lane main
"$HARNESS" handoff query --quest-id "$QID" --due   # dispatched handoff(s) to scout-ideator, status sent/acked
"$HARNESS" control status --quest-id "$QID"        # run_state running, pending handoffs sane
M agents list                                      # 6 live instances
houmao-mgr agents single --agent-name orchestrator gateway status        # gateway up
houmao-mgr agents single --agent-name orchestrator gateway mail-notifier status  # notifier enabled
M mailbox messages                                 # task-request delivered to scout-ideator
```
Healthy signal: `state validate` CLEAN, exactly one open self-wakeup, a `sent`/`acked` handoff to the first specialist, and no `failed` handoffs.

---

## Pause / stop / teardown (graded)

**Pause (no destroy)** 🟡 — idle the loop, keep all state:
```bash
"$HARNESS" control pause --quest-id "$QID" --at "$(now)"
```
Resume: `"$HARNESS" control resume --quest-id "$QID" --at "$(now)"` (add `--recovering` after a crash; the tick re-reads `wakeup list` + `handoff query --due`).

**Stop live agents** 🔴:
```bash
for inst in orchestrator scout-ideator experimenter-1 analyst writer reviewer; do
  houmao-mgr agents single --agent-name "$inst" gateway mail-notifier disable
  houmao-mgr agents single --agent-name "$inst" gateway detach
  M agents stop --name "$inst"
  houmao-mgr agents single --agent-name "$inst" cleanup
done
```

**Quest state reset** 🟡 (pre-meaningful-data): `rm -f "$P/runs/state.sqlite" && "$HARNESS" state init`

**Worktree/branch cleanup** 🟡 (only when abandoning pre-launch; otherwise keep branches — preserve-failed-routes):
```bash
git -C "$REPO" worktree remove "$P/runs/$QID/workspaces/experimenter-1" --force
git -C "$REPO" branch -D "quest/$QID/exp-1"
```

**Full overlay teardown** 🟡 (removes skills/specialists/profiles/credentials/mailbox):
```bash
M profile   remove --name deepresearch-<role>      # repeat 6
M specialist remove --name deepresearch-<role>     # repeat 6
M skills remove --name deepresearch-<skill>        # repeat 9
# or, nuclear: rm -rf "$P/.houmao"
```

---

## Safety summary
- 🟢 Pre-flight, Step 8, and all `state query`/`status`/`validate`/`get`/`list` calls are read-only.
- 🟡 Steps 1–5 mutate credentials/DB/overlay/filesystem but start nothing live; each has a rollback.
- 🔴 Steps 6, 6b, 7 start live sessions, gateways, the notifier, and the loop. After Step 7 the loop is self-driving via self-wakeup — interact through operator-control / pause, not repeated prompts.
- Order matters: Steps 1→5 must complete before 6; 6b requires 6; 7 requires 6b + the mailbox; never run 6/7 with the placeholder credential still in place.
