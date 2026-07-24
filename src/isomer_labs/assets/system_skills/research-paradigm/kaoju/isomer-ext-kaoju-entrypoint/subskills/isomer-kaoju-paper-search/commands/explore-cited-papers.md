# Explore Cited Papers

## Workflow

1. Require one resolved target, result and page bounds, optional inclusive date or year range, research purpose, evidence-use intent, and normalized fields.
2. Fetch papers reported in the target's reference list through the selected provider approach.
3. When the operation lacks a requested date filter, retrieve only a bounded set, filter locally, and record the filtering location and inspected population.
4. Normalize each edge from the target to the cited paper, label the route `backward`, and preserve the target as parent seed.
5. Follow pagination until exhaustion or a declared bound while retaining successful pages after a later partial failure.
6. Record one observation and hand candidates to the requesting owner without judging relevance or authority.

If the task does not map cleanly to these steps, use your native planning tool to build and execute a bounded backward-citation plan from the resolved target, filters, and stop conditions.

## Bounds and Direction

Direction is `backward`: the requested target is the edge source and each cited paper is the edge destination. Require and record requested and applied result and page bounds and mark locally filtered or bound-stopped output non-exhaustive.

## Provider Request Intent

Request the target's outbound reference neighborhood with minimal edge and candidate bibliographic fields. Do not infer that a listed reference supports, contradicts, or was materially used by the target.

## Normalized Output

Return target identity, cited candidates, normalized endpoints, parent seed, pagination, filtering location, completeness, continuation posture, missing fields, null or unresolved records, limitations, and provenance.

## Gates, Blockers, and Resume

Ambiguous target identity blocks traversal. Missing binding, unavailable tool, credential Gate, invalid target, throttling, or page failure yields blocked or partial status. Resume from target resolution or the recorded page continuation. Handoff candidates to `discover`; use `acquire` and `examine` for evidence work.
