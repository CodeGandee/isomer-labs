# Research Idea Decision Context Contract

Decision context is a read-only explanation of selection, deferral, closure, and reopening. Read one idea through `GET /api/topics/{topic_id}/ideas/{idea_id}/decisions` or one Decision Record through `GET /api/topics/{topic_id}/idea-decisions/{decision_record_id}`.

The response includes `mutated: false`, topic identity, the requested idea or decision id, `decisions`, involved `ideas`, decision-linked `transitions`, `reopen_history`, `index_revision`, and `diagnostics`. Each decision includes its stable `decision_record_id`, every explicitly recorded option, selected idea ids, `option_set_complete`, rationale, consequences, actor refs, decision time, supporting refs, transition refs, and `missing_fields`.

Each option includes `idea_id`, outcome, ordering, rationale, consequence, supporting refs, nested lightweight idea identity, and any directly linked disposition `reason_code`, `transition_ref`, and transition rationale. Option membership is authoritative. Generation siblings are not added unless the Decision Record recorded them as options.

Historical data may have no option set, an incomplete option set, or missing rationale. The response preserves available objects, sets `option_set_complete: false`, lists `missing_fields`, and emits `idea_decision_context_incomplete`. Clients show that diagnostic and do not invent alternatives or reasons. A closed idea keeps its closure transition and reason after a later reopen; the later transition also appears in `reopen_history`.
