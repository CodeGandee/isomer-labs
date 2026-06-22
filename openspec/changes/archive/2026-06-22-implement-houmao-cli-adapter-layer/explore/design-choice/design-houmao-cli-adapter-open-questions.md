# Houmao CLI Adapter Open Questions

Date: 2026-06-22

## Reader and Scope
This note is for the implementer of `implement-houmao-cli-adapter-layer`. It clarifies the open questions in the change design before implementation starts.

## Open-Question Map
| Priority | Question | Resolution | Evidence |
| --- | --- | --- | --- |
| Important | What exact Houmao CLI argv should seed the adapter command catalog? | Use Houmao’s public CLI with top-level `--print-json`. Project-scoped operations select the overlay through `project --project-dir <dir>`. Material creation uses `project specialist create` and `project profile create`. Launch, inspect, list, and stop use `project agents launch`, `project agents get`, `project agents list`, and `project agents stop`. Global read-only preflight can use `agents global list` and `system-skills list`. | Houmao script entry point in `/home/huangzhe/workspace/code/houmao/pyproject.toml`; output style in `/home/huangzhe/workspace/code/houmao/src/houmao/srv_ctrl/commands/output.py`; project group and project-dir option in `/home/huangzhe/workspace/code/houmao/src/houmao/srv_ctrl/commands/project.py`; project specialist/profile/agents commands in `/home/huangzhe/workspace/code/houmao/src/houmao/srv_ctrl/commands/project_easy.py`; executable help from `pixi run houmao-mgr ... --help`. |
| Blocker | Should this focused change include any handoff primitive? | No. Keep this focused change to launch materialization, quick launch, inspect-live, stop, and reconciliation hooks. Full handoff dispatch, Signal Observation ingestion, and Operator Agent normalization remain in the broader `implement-milestone-5-houmao-execution-adapter` change. | User selected Option A during exploration; the broad Milestone 5 plan already owns `handoffs dispatch`, `handoffs observe`, and `handoffs normalize`. |

## Resolved Design Choice
The adapter-layer implementation should be a narrow launch foundation. It should make Houmao-backed Agent Team Instances launchable and inspectable from Isomer while preserving the direct `houmao-mgr` workflow and manifest reconciliation path. It must not pull in Run-level handoff routing or completion normalization.

## Command Catalog Seed
The implementation should confirm these commands against the local checkout during task 1.1 and then encode them in a small command catalog:

| Purpose | Command Shape |
| --- | --- |
| Version probe | `houmao-mgr --version` |
| JSON output style | `houmao-mgr --print-json <command> ...` |
| System skill probe | `houmao-mgr --print-json system-skills list` |
| Project overlay status | `houmao-mgr --print-json project --project-dir <dir> status` |
| Project specialist creation | `houmao-mgr --print-json project --project-dir <dir> specialist create --name <specialist> --tool <tool> ...` |
| Project profile creation | `houmao-mgr --print-json project --project-dir <dir> profile create --name <profile> --specialist <specialist> ...` |
| Per-Agent Instance launch | `houmao-mgr --print-json project --project-dir <dir> agents launch --profile <profile> --name <agent-instance-name> ...` |
| Project-scoped listing | `houmao-mgr --print-json project --project-dir <dir> agents list` |
| Project-scoped inspection | `houmao-mgr --print-json project --project-dir <dir> agents get --name <agent-instance-name>` |
| Project-scoped stop | `houmao-mgr --print-json project --project-dir <dir> agents stop --name <agent-instance-name>` |
| Global registry probe | `houmao-mgr --print-json agents global list --state all` |

## Deferred Work
Manual handoff dispatch, observation ingestion, and Operator Agent normalization should remain deferred to `implement-milestone-5-houmao-execution-adapter`. The focused adapter-layer change may record backend observations as adapter inspection snapshots or manifest reconciliation inputs, but it should not accept handoff completion or update Run status.
