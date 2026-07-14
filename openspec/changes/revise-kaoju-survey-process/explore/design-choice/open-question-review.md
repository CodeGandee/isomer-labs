# Kaoju Survey-Process Open-Question Review

Status: Complete
Date: 2026-07-14

## Scope

This review covers active product and architecture questions in `context/features/2026-07-14-kaoju-survey-process-usecases` and the OpenSpec change `revise-kaoju-survey-process`. The accepted use cases and ADRs remain constraints. Suggestion files supplied design input but did not override those constraints or the canonical Isomer domain language.

## Reviewed Decisions

| Review | Selected Option | Decision |
| --- | --- | --- |
| 1. Repair and retry autonomy | A | After an approved build or trial action, bounded identical transient retries and non-material repairs may run automatically. Material changes require a revised plan and human Gate, and every attempt remains a separate Run. |
| 2. Service Request dispatch | B | The first release provides synchronous-only dispatch. It creates durable request records before work, waits for completion or timeout, always returns a stable request ref, and uses status reconciliation after interruption. |
| 3. Paper and template lifecycle | A | Paper structure adapts through typed MyST profiles; figures and tables are separate Artifacts; exports have explicit revision and conflict behavior; grounded orphan removal requires confirmation; TeX templates use compatibility fingerprints. |
| 4. Discovery and source acquisition | A | Three directions plus custom input is the default; current-host capability only annotates empirical feasibility; blocked reading items trigger bounded backfill; repositories use shallow-first acquisition; associated-paper discovery is automatic but not authoritative; visual extraction is claim-driven and provisional until verified. |
| 5. Wiki export and viewer update | B | Wiki and viewer targets default inside the Topic Workspace with optional overrides. JSON is the canonical manifest. Recognized managed files refresh in place through staged writes, unrecognized files remain untouched, and each refresh records a changelog and a new durable Artifact revision. |

## Questions Resolved from Accepted Evidence

- Human researchers are the users; Topic Actors are the canonical topic-local worker identities used for human-orchestrated execution.
- `isomer-kaoju-pipeline` remains a thin intent router. Capability skills own research judgment, and typed `isomer-cli` services own deterministic operations.
- UC-01 through UC-10 cover the requested lifecycle. Further behavior should refine those use cases unless it introduces a distinct actor goal.
- New Kaoju record support enters through the versioned binding registry, Artifact Format Profiles, validators, and migrations. Agents do not invent partial runtime schemas.
- Environment refs retain flexible intent constraints and record exact resolved versions plus lock identity.
- Smoke scripts are file-backed Artifacts on resolved owner-preserved record surfaces. Source-tree and Local Tmp Surface copies are not canonical.
- Trials always record a minimal durable wrapper. The wrapper invokes a compatible upstream command when possible and records the smallest necessary adaptation otherwise.

## Deferred Implementation Selections

Two technical selections require implementation-time evidence rather than another product decision:

- Task 1.3 selects and locks a Python 3.11-compatible MyST parser after compatibility validation.
- Task 1.4 completes viewer license and provenance review, then either bundles the accepted implementation or uses an independently implemented compatible viewer.

Neither selection changes the approved behavioral contracts.

## Result

No active product-level open questions remain in the reviewed use cases or OpenSpec design. The synchronized specification remains strict-validation clean. Implementation can proceed through the tasks in [tasks.md](../../tasks.md), subject to the two evidence-based selections above.
