# Candidate Board

Use this reference when the active candidate pool needs one shared surface. The board should separate method briefs from implementation attempts.

## Template

| Candidate ID | Level | Parent | Strategy | Status | Expected Gain | Observed Result | Promote or Archive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cand-001 | brief | current head | explore | proposed | Better tail metric | none yet | pending |
| cand-002 | implementation | cand-001 | exploit | smoke passed | Faster convergence | smoke ok | consider promotion |

## Field Rules

- `Level` is `brief`, `durable_line`, or `implementation`.
- `Parent` may be a Research Inquiry Relationship, route id, Run id, or candidate id.
- `Strategy` should usually be `explore`, `exploit`, `fusion`, or `debug`.
- `Status` should be specific: proposed, held, promoted, smoke running, smoke passed, smoke failed, full evaluation running, succeeded, failed, archived, blocked, or stopped.
- `Promote or Archive` must be a clear recommendation, not an empty placeholder.

## Use Rule

If the board stops changing while attempts continue, route through frontier review instead of adding more near-duplicate attempts.
