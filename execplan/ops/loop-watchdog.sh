#!/usr/bin/env bash
# loop-watchdog.sh — DeepResearch liveness watchdog (conservative).
#
# Detects two stall sources and (only with --apply) performs the minimal safe nudge:
#   1. Stalled handoffs   — in-flight (sent|acked) past due  -> reported; the Orchestrator's
#                           heartbeat tick is what actually resends (this script does NOT mutate state).
#   2. Claude Code interstitials parked on an agent's TUI    — e.g. "How is Claude doing this session?",
#                           trust/permission, or /clear suggestion -> with --apply, sends ONLY the
#                           documented dismiss key (0) to KNOWN interstitials. Never a content answer.
#
# DEFAULT IS DRY-RUN (read-only). Nothing is sent without --apply.
# It never touches runs/state.sqlite, research data, mailbox messages, or git.
#
# Usage:
#   ops/loop-watchdog.sh                 # report only (read-only)
#   ops/loop-watchdog.sh --apply         # also dismiss known interstitials via tmux send-keys 0
#   ops/loop-watchdog.sh --quest-id q1   # scope the stalled-handoff check
set -euo pipefail

APPLY=0; QID=""
while [ $# -gt 0 ]; do case "$1" in
  --apply) APPLY=1;; --quest-id) QID="$2"; shift;; *) echo "unknown arg: $1" >&2; exit 2;;
esac; shift; done

SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # execplan/
P="$(cd "$SELF/.." && pwd)"                                # project root
HARNESS="$SELF/harness/bin/deepresearch"
NOW="$(date -u +%FT%TZ)"

# Known Claude Code interstitial signatures (substring match on the captured pane).
# Each maps to the SAFE dismissal keystroke. We only ever send "0" (Dismiss) or Escape — never 1/2/3
# (which would submit a content answer) and never Enter on a trust/permission prompt.
# NOTE: only genuine *blocking* modal prompts belong here. The "/clear to save N tokens" footer is
# benign (it shows on a normal idle prompt and does NOT block input) — do NOT match it, or healthy idle
# agents get mis-flagged.
INTERSTITIAL_PATTERNS=(
  "How is Claude doing this session?"     # session-feedback modal -> dismiss with 0
  "Do you trust the files in this folder?" # trust modal -> Escape (never auto-Enter a trust prompt)
)

echo "=== DeepResearch loop watchdog @ $NOW  (apply=$APPLY) ==="

echo "--- stalled handoffs (read-only; heartbeat tick resends, not this script) ---"
if [ -f "$P/runs/state.sqlite" ]; then
  python3 "$HARNESS" handoff query ${QID:+--quest-id "$QID"} --stalled --now "$NOW" \
    | python3 -c 'import sys,json; d=json.load(sys.stdin).get("data",{}); rows=d.get("stalled",[]);
print("  count:",d.get("count",0));
[print("   ",r.get("handoff_id"),r.get("status"),"->",r.get("action")) for r in rows]' \
    2>/dev/null || echo "  (handoff query unavailable)"
else
  echo "  (no state.sqlite — loop not initialized)"
fi

echo "--- parked interstitials on live agent panes ---"
found=0
for sess in $(tmux ls 2>/dev/null | grep -oE '^HOUMAO-[^:]+' || true); do
  pane="$(tmux capture-pane -p -t "$sess" 2>/dev/null || true)"
  hit=""
  for pat in "${INTERSTITIAL_PATTERNS[@]}"; do
    if printf '%s' "$pane" | grep -qE "$pat"; then hit="$pat"; break; fi
  done
  if [ -n "$hit" ]; then
    found=1
    echo "  PARKED: $sess  (matched: $hit)"
    if [ "$APPLY" = 1 ]; then
      # Send ONLY the safe dismiss: "0" then Escape. Never a content answer.
      tmux send-keys -t "$sess" "0" 2>/dev/null || true
      tmux send-keys -t "$sess" Escape 2>/dev/null || true
      echo "    -> dismissed (sent '0' + Escape)"
    else
      echo "    -> would dismiss with --apply (sends only '0' + Escape)"
    fi
  fi
done
[ "$found" = 0 ] && echo "  none detected"

echo "=== done ==="
