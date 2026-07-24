# Resolve Paper

## Workflow

1. Accept one stable identifier, publication URL, title, or metadata description plus research purpose, evidence-use intent, required normalized fields, and a result bound.
2. Prefer direct identity resolution for a supported stable identifier. For title or metadata input, run a bounded match and preserve every plausible candidate.
3. Stop before traversal when several candidates remain plausible. Return the ambiguity with distinguishing identifiers, authors, venue, year, and locators rather than selecting by provider rank.
4. Normalize the requested identifier, resolved provider identity, DOI, arXiv id, provider-qualified id, title, authors, venue, publication date or year, locator, missing fields, observation time, and provenance.
5. Record one observation for the resolution attempt, including unresolved or ambiguous posture, then hand a resolved target to the requesting owner.

If the task does not map cleanly to these steps, use your native planning tool to build and execute a bounded resolution plan from the supplied identity, required fields, and result contract.

## Bounds and Direction

Direction is `non-citation`. Require a candidate bound for title or metadata matching and a page bound for any paginated match. Record requested and applied bounds, including any provider maximum. A stable-identifier detail lookup remains one bounded target operation.

## Provider Request Intent

Request target detail or a narrow title or metadata match through the selected approach. Ask only for fields needed to distinguish identity and satisfy the normalized result contract.

## Normalized Output

Return one target with requested and resolved identifiers, or a bounded ambiguity or unresolved record. Never invent a DOI, publication date, author, or venue when the provider omits it.

## Gates, Blockers, and Resume

Missing Literature Provider Binding, unavailable external tooling, required credential approval, invalid identifier, and unresolved ambiguity pause or block execution. Resume at provider selection, bounded matching, actor selection, or recording. Handoff resolved identity to `discover` for disposition or `acquire` for material access.
