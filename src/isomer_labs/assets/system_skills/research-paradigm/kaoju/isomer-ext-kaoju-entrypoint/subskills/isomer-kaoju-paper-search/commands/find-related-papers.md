# Find Related Papers

## Workflow

1. Require one or more resolved positive seeds, optional resolved negative seeds, result bound, filters, research purpose, evidence-use intent, and normalized fields.
2. Verify that the selected provider approach supports adjacent-paper retrieval for the supplied seed posture.
3. Request a bounded recommendation or similarity result. Do not reinterpret the result as a citation edge.
4. Apply unsupported date or metadata filters locally over the bounded returned set and record the filtering location.
5. Normalize every candidate with its positive and negative seed context, non-citation route, provider rank when available, missing fields, limitations, and observation time.
6. Record one complete, truncated, or partial observation and hand candidates to the caller for selection.

If the task does not map cleanly to these steps, use your native planning tool to build and execute a bounded adjacency plan from the seed set, filters, and result contract.

## Bounds and Direction

Direction is `non-citation`. Require a requested result maximum, record the applied provider maximum, and preserve any difference. A single bounded recommendation response without a continuation mechanism is not evidence of exhaustive adjacency.

## Provider Request Intent

Request provider-native adjacent-paper recommendations for one seed or a positive and negative seed set. Ask only for normalized identity and bibliographic fields needed downstream.

## Normalized Output

Return seed identities, candidate paper keys and metadata, parent seed set, route, filters, retained count, provider and access method, completeness, limitations, and continuation posture. Do not create citation edges for recommendation results.

## Gates, Blockers, and Resume

Unresolved seeds, missing provider support, unavailable tool, credential Gate, invalid seed set, or provider failure yields blocked or partial status. Resume from seed resolution or provider selection. Handoff to `discover` for relevance, version-family, inclusion, duplicate, and priority judgments.
