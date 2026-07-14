# UC-01 Direction Selection and Next Direction Set Record

Status: accepted
Date: 2026-07-14
Related: none

The initial UC-01 draft assumed a single selected survey direction. In practice, a researcher may want to pursue several directions in parallel, or add a direction that was not in the system's initial proposal. The design must support multi-selection and custom-direction input, and it must keep a durable record of which directions are queued for exploration.

## Current Decision

- UC-01 allows the human to **select multiple directions**, **provide a new custom direction**, or **reject all and ask for a revised proposal**.
- The system records the accepted directions as a durable artifact with semantic id `kaoju:direction-set`.
- Each direction in the set carries its own scoped question, boundary, source classes, coverage date, expected depth, and deliverables.
- The `kaoju:direction-set` is the input to the next use case (online collection / discovery). It is not the same as the frozen `kaoju:survey-contract`; a contract may be created per direction or per combined direction set, depending on how tightly the directions are coupled.
- The system can report "next direction set to be explored" at any time by reading `kaoju:direction-set`.

## Affected Artifacts

- `usecases/uc-01-survey-direction-from-topic.md`: updated supported actions, main flow, durable outputs, and example prompt to cover multi-selection, custom directions, and the `kaoju:direction-set` record.
- `README.md`: added ADR link to artifact map.

## Refinement History

### 2026-07-14 - Initial Decision

- Instruction: "human can select multiple directions, or provide new one, system shall have durable records about 'the next direction set to be explored'"
- Applied changes:
  - Renamed and expanded the "Accept Or Refine Direction" supported action into "Select, Add, or Refine Directions".
  - Added `kaoju:direction-set` as a durable output.
  - Updated main flow to allow multi-select and custom direction input.
  - Updated example prompt/response to illustrate multi-selection and a custom direction.
