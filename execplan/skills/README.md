# Skills

## Purpose

Generated skill packages for the DeepResearch loop, installed into agents per `../agents/bindings.toml`.
Each skill is bounded (one event / one tick / one purpose), touches state ONLY through harness commands
(via `$HARNESS`), and is idempotent where applicable. Mail-received skills are
entered from Houmao notifier prompts after the separate notifier detects open mail.

## Contents

- `deepresearch-shared-guide/` — shared harness/comms usage conventions (installed in every agent).
- `deepresearch-on-task-request/` — specialist on-event handler for `deepresearch.email.task-request` (role-aware).
- `deepresearch-on-receipt/` — Orchestrator on-event handler for `deepresearch.email.receipt`.
- `deepresearch-on-task-result/` — Orchestrator on-event handler for `deepresearch.email.task-result`.
- `deepresearch-on-self-wakeup/` — Orchestrator on-event handler for `deepresearch.email.self-wakeup`.
- `deepresearch-orchestrator-tick/` — Orchestrator on-tick stage machine (reconcile / dispatch / terminate).
- `deepresearch-operator-control/` — operator lifecycle/mode/recovery control.
- `deepresearch-mentor/` — companion calibration (ported DeepScientist mentor); installed in the Orchestrator.

Publication/domain extension behavior is delivered via stages (`outline`, `rebuttal`), harness extension
commands (`render plot|polish|slides`, `manuscript polish|datastmt`, `knowledge query`), and built-in
`knowledge_pack`s (see `../packs/`; the publication set is enabled by default, the `science-scipkg` +
`mentor-standards` reference packs are disabled).
