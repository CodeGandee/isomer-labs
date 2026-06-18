# Auth posture and liveness watchdog (operator-control)

Depth behind op 6b (auth posture) and the liveness watchdog of `SKILL.md`.

## op 6b — auth posture (credential)

Agents use the `default` bundle's **long-lived OAuth token** (Pro/Max, `claude setup-token`) — it does **not**
expire on the ~5h interactive clock, so normal recovery never needs a re-login. Distinguish failures:
- A **`401 Invalid authentication credentials`** = the token is genuinely bad/lapsed → the **operator** re-runs
  `claude setup-token` + `credentials claude set --name default --oauth-token …`, then **relaunch agents fresh**
  (a bare relaunch reuses the home-cached token).
- A **`403 … quota …`** = a *third-party proxy* (`ANTHROPIC_BASE_URL`+`AUTH_TOKEN`) is shadowing the OAuth token
  in the launch env — **not** a subscription problem; relaunch with those scrubbed (`unset` / `env -u …`).

Never paste a token into a prompt. See `docs/credentials.md`.

## Liveness watchdog (heartbeat + parked-agent recovery)

- **Heartbeat:** keep the loop live without inbound mail by setting a *repeating* gateway reminder on the
  orchestrator that prompts it to run **deepresearch-orchestrator-tick** (the tick's step 2 then reconciles
  stalled handoffs). Via `houmao-agent-gateway`:
  `houmao-mgr agents single --agent-name orchestrator gateway reminders create --interval-seconds <N> \
  --prompt "Run deepresearch-orchestrator-tick: heartbeat reconcile (handoff query --stalled), then stop."`
  Pick `N` ≥ the shortest `result_due_at` window so a dead worker turn is retried within one or two beats.
- **Claude Code interstitials:** a parked TUI prompt (e.g. *"How is Claude doing this session? 1:Bad 2:Fine
  3:Good 0:Dismiss"*, trust/permission, or `/clear`-suggestion) blocks the agent's input so neither mail nor
  reminders advance it. Detect + safely dismiss with the operator helper `execplan/ops/loop-watchdog.sh`
  (read-only by default; `--apply` sends only the documented **dismiss/0** key to *known* interstitials —
  never a content answer). After dismissing, the agent's notifier/heartbeat resumes normally.
