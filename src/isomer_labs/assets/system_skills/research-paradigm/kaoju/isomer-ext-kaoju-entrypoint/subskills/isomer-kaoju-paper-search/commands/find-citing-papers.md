# Find Citing Papers

## Workflow

1. Require one resolved target, an explicit inclusive date or year range when requested, result and page bounds, research purpose, evidence-use intent, and normalized fields.
2. Fetch papers reported as citing the target through the selected provider approach.
3. Apply supported provider-side date filters; otherwise retrieve only a bounded set and filter locally while recording that limitation.
4. Normalize each edge from the citing paper to the target, label the route `forward`, and preserve the target as parent seed.
5. Follow pagination until exhaustion or a declared bound, preserving successful pages when a later operation fails.
6. Record one complete, truncated, or partial observation and hand candidates to the requesting owner.

If the task does not map cleanly to these steps, use your native planning tool to build and execute a bounded forward-citation plan from the resolved target, filters, and stop conditions.

## Bounds and Direction

Direction is `forward`: the citing paper is the edge source and the requested target is the edge destination. Require and record requested and applied result and page bounds, including any provider maximum.

## Provider Request Intent

Request the target's inbound citation neighborhood with minimal cited-edge and candidate bibliographic fields. Provider contexts, intents, or influence labels remain optional metadata and never become full-text evidence.

## Normalized Output

Return the resolved target, citing candidates, normalized citing and cited paper keys, parent seed, pages and records inspected, filtering location, completeness, continuation posture, null or unresolved records, and provider provenance.

## Gates, Blockers, and Resume

An ambiguous target blocks traversal. Missing binding, tool, credential authorization, provider rejection, throttling, or page failure yields blocked or partial status. Resume from target selection, provider selection, or the recorded page continuation. Handoff to `discover`; route selected material through `acquire` and `examine` before claim-bearing use.
