# Search Papers

## Workflow

1. Accept the topic or metadata query, terminology variants supplied by the caller, explicit date or year range, filters, result and page bounds, research purpose, evidence-use intent, and normalized fields.
2. Choose relevance-oriented or bounded corpus-oriented search according to the caller's request. Do not let the provider choose the survey strategy.
3. Apply supported filters at the provider. Apply unsupported filters locally only over a declared bounded retrieved set and record the filtering location.
4. Follow pagination until provider exhaustion or the first declared result, page, resource, or failure bound.
5. Normalize retained and rejected-by-local-filter candidates, pages and records inspected, searched-through date, continuation posture, missing fields, and limitations.
6. Record one observation for the complete or partial logical query and hand candidates to the caller without making inclusion decisions.

If the task does not map cleanly to these steps, use your native planning tool to build and execute a bounded query plan from the supplied purpose, filters, bounds, and normalized output contract.

## Bounds and Direction

Direction is `non-citation`. Require result and page maxima; resolve relative dates before execution. Record both requested and applied bounds and mark output truncated whenever a bound stops an available continuation.

## Provider Request Intent

Request a paper query with minimal identity and bibliographic fields. Use a bulk or token-paginated operation only when the bounded purpose requires broader retrieval rather than relevance ranking.

## Normalized Output

Each candidate records its normalized paper key, available identifiers, title, authors, venue, publication date or year, locator, parent query, route, observation time, filtering posture, and missing fields.

## Gates, Blockers, and Resume

Missing binding, unavailable tool, credential Gate, invalid query, throttling, and pagination failure preserve a blocked or partial posture. Resume from the recorded continuation token or offset when policy and provider behavior permit. Handoff to `discover` for cross-source strategy and candidate disposition.
