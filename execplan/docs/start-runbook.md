# Start Runbook — DeepResearch

Exact ordered commands to take the prepared package live. **Do not run until explicitly approved.**

## Legend
- 🟢 **READ-ONLY** — inspects only; safe to run anytime.
- 🟡 **STATE-MUTATING** — writes files / DB / overlay; reversible (see Rollback).
- 🔴 **LAUNCH-STARTING** — starts live processes / gateway / notifier.

## Variables (set once)
```bash
export PATH="/root/.local/bin:$PATH"
P=/home/linfeng/houmao_DeepScientist
HARNESS="$P/execplan/harness/bin/deepresearch"
QID=q1                                  # first quest id
REPO=/ABS/PATH/TO/OPERATOR/REPO         # quest.workspace_ref — operator-owned git repo (REQUIRED)
MAILROOT="$P/.houmao/mailbox"
now(){ date -u +%FT%TZ; }               # caller-supplied ISO-8601 timestamps
M(){ houmao-mgr project --project-dir "$P" "$@"; }
```

---

## Pre-flight 🟢 (read-only gate — must pass before anything below)
```bash
python3 "$HARNESS" selfcheck            # ok=true, 33 record types, 32 invariants, deps ok
M status                                # overlay healthy
M skills list   | grep -c deepresearch- # 7
M profile list  | grep -c deepresearch- # 6
M agents list   | grep instances        # instances [] (nothing live yet)
test ! -f "$P/runs/state.sqlite" && echo "DB absent (expected)"
test -d "$REPO/.git" && echo "REPO is a git repo (required for Experimenter worktrees)"
```

---

## Step 1 — Replace the placeholder Claude credential 🟡 (secret)
```bash
# Option A: paste a key
M credentials claude set --name default --api-key "$ANTHROPIC_API_KEY"
# Option B: interactive vendor login into an isolated config home
# M credentials claude login --name default
```
Verify 🟢: `M credentials claude get --name default`  → `ANTHROPIC_API_KEY present:true`.
**Rollback:** restore placeholder →
`M credentials claude set --name default --api-key "PLACEHOLDER-REPLACE-BEFORE-LAUNCH"`

---

## Step 2 — Initialize the platform DB 🟡
```bash
"$HARNESS" state init                   # creates $P/runs/state.sqlite (27 tables, 11 stages)
```
Verify 🟢: `"$HARNESS" state validate`  → `ok:true, checked:32`.
**Rollback (pre-quest only):** `rm -f "$P/runs/state.sqlite"`

---

## Step 3 — Create the quest 🟡
> ⚠️ **Not the first quest?** Ensure no prior quest is still `running` (`single_active_quest` will reject
> `run_state=running` below otherwise) and refresh `shared/objective` for the new quest before proceeding.
```bash
AT=$(now)
"$HARNESS" record apply --validate-after-write --json '{
  "record_type":"quest.create","record_id":"'"$QID"'","at":"'"$AT"'",
  "title":"<QUEST TITLE>","objective_ref":"shared/objective",
  "acceptance_ref":"shared/objective/acceptance.md","workspace_ref":"'"$REPO"'",
  "max_rounds":24,"convergence_patience":3 }'

# Register the 6 participant instances (experimenter starts at fanout_default=1)
for pair in orchestrator:orchestrator scout-ideator:scout-ideator \
            experimenter-1:experimenter analyst:analyst writer:writer reviewer:reviewer; do
  inst=${pair%%:*}; role=${pair##*:}
  "$HARNESS" record apply --json '{"record_type":"participant.register",
    "record_id":"'"$QID"':'"$inst"'","at":"'"$(now)"'","quest_id":"'"$QID"'",
    "instance_id":"'"$inst"'","role":"'"$role"'","tool":"claude"}'
done

# Move the quest to running (single_active_quest enforces one at a time)
"$HARNESS" record apply --validate-after-write --json '{"record_type":"quest.update",
  "record_id":"'"$QID"'","at":"'"$(now)"'","run_state":"running","current_stage":"scope"}'
```
Verify 🟢: `"$HARNESS" state query cursor`  → quest running, current_stage scope.
**Rollback (pre-launch):** `rm -f "$P/runs/state.sqlite" && "$HARNESS" state init` (no row-delete command; re-init is the clean reset).

---

## Step 4 — Materialize per-quest work roots + Experimenter worktree(s) 🟡
```bash
# artifact + work-root dirs
mkdir -p "$P/runs/$QID"/{round-0,report/review,figures,refs,findings,exports,intake,mail,workspaces}
for r in orchestrator scout-ideator analyst writer reviewer; do
  mkdir -p "$P/runs/$QID/workspaces/$r"
done

# Experimenter ISOLATED git worktree (fanout_default=1; repeat exp-2..exp-4 to scale to fanout_max=4)
git -C "$REPO" worktree add "$P/runs/$QID/workspaces/experimenter-1" -b "quest/$QID/exp-1"
"$HARNESS" record apply --json '{"record_type":"branch.record","record_id":"exp-1",
  "at":"'"$(now)"'","quest_id":"'"$QID"'","git_branch":"quest/'"$QID"'/exp-1",
  "worktree_ref":"runs/'"$QID"'/workspaces/experimenter-1","status":"active"}'

# Seed shared/objective (operator provides the real brief; read-only to agents thereafter)
cp /ABS/PATH/TO/objective.md "$P/shared/objective/objective.md"
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
```bash
# Orchestrator (root)
M agents launch --profile deepresearch-orchestrator --name orchestrator \
  --workdir "$P/runs/$QID/workspaces/orchestrator" \
  --mail-transport filesystem --mail-root "$MAILROOT" --gateway-background

# Specialists (experimenter uses its isolated worktree as workdir)
for pair in scout-ideator:scout-ideator experimenter:experimenter-1 \
            analyst:analyst writer:writer reviewer:reviewer; do
  prof=deepresearch-${pair%%:*}; inst=${pair##*:}
  M agents launch --profile "$prof" --name "$inst" \
    --workdir "$P/runs/$QID/workspaces/$inst" \
    --mail-transport filesystem --mail-root "$MAILROOT" --gateway-background
done
```
Notes: `$HARNESS` is exported on every profile, so the harness resolves regardless of `--workdir`. Gateway auto-attaches per agent (omit `--no-gateway`).
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

## Step 7 — Send the first trigger 🔴 (start = nudge the Orchestrator once; loop self-sustains via self-wakeup)
```bash
houmao-mgr agents single --agent-name orchestrator prompt \
  --prompt "Run deepresearch-orchestrator-tick: begin quest $QID at stage scope. One bounded pass, then arm the durable self-wakeup."
```
After this the Orchestrator dispatches `scope` to scout-ideator and arms a `[self-wakeup]` on lane `main`; the mail-notifier drives all subsequent rounds. **Do not** send repeated prompts — the loop is now self-driven.

---

## Step 8 — First post-launch health checks 🟢 (read-only)
```bash
"$HARNESS" state validate                         # CLEAN (32 checks, 0 violations)
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
M skills remove --name deepresearch-<skill>        # repeat 7
# or, nuclear: rm -rf "$P/.houmao"
```

---

## Safety summary
- 🟢 Pre-flight, Step 8, and all `state query`/`status`/`validate`/`get`/`list` calls are read-only.
- 🟡 Steps 1–5 mutate credentials/DB/overlay/filesystem but start nothing live; each has a rollback.
- 🔴 Steps 6, 6b, 7 start live sessions, gateways, the notifier, and the loop. After Step 7 the loop is self-driving via self-wakeup — interact through operator-control / pause, not repeated prompts.
- Order matters: Steps 1→5 must complete before 6; 6b requires 6; 7 requires 6b + the mailbox; never run 6/7 with the placeholder credential still in place.
