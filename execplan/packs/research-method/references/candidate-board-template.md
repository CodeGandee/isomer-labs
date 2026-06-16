# CANDIDATE_BOARD.md

| Candidate ID | Level | Parent | Strategy | Status | Expected Gain | Observed Result | Promote / Archive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cand-001 | brief | current-head | explore | proposed | Better tail accuracy | n/a | pending |
| cand-002 | impl | cand-001 | exploit | smoke_passed | Faster convergence | smoke ok | consider promote |

Notes:

- `Level` should be `brief` or `implementation`
- `Parent` may be a branch, idea id, run id, or candidate id
- `Strategy` should usually be one of `explore`, `exploit`, `fusion`, `debug`
- `Promote / Archive` should be a clear recommendation, not an empty placeholder
