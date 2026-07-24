# Execution and Errors

## Resolve Time and Bounds

Resolve relative dates against the observation date before execution. For example, “the recent three years” observed on 2026-07-23 becomes the explicit inclusive year range 2024 through 2026 unless the actor specifies another interpretation.

Require a positive result bound and page bound for list actions. Citation-neighborhood traversal defaults to one hop and also requires positive node and per-node bounds. Record requested and applied values when a provider maximum narrows the request. Never raise a bound silently.

## Cycle and Frontier Control

Key the visited set by resolved provider identity. Expand each identity at most once for each direction, retain its parent seed and hop, and stop at the first depth, node, per-node, page, resource, provider, or user bound. Report the reached frontier and whether it can continue.

## External Tool Selection

Prefer an available provider-native tool when the binding approves it and its output can be normalized without losing pagination or provenance. Otherwise use a general-purpose CLI or bounded direct-HTTPS tool. Confirm URL encoding, body serialization, field projection, timeout, response-size, and output-file posture before execution.

Provider execution stays outside `isomer-cli`. `isomer-cli ext research literature` validates, records, indexes, and queries normalized Isomer-owned data only.

## Retry Classes

- Retry throttling, timeout, connection reset, and transient provider failures only within a declared retry and elapsed-time bound. Honor provider retry guidance when available and use bounded backoff.
- Do not retry invalid input, ambiguous identity, authentication failure, authorization failure, policy denial, or a missing resource without changing the applicable input or authorization.
- Preserve every successful page or frontier branch when a later operation fails. Record failed operation, attempt count, last status class, retry posture, and continuation point.
- Stop when retry would exceed cost, rate, elapsed-time, page, result, or user bounds.

## Safe Reporting

Sanitize terminal output before chat or recording. Do not record or show a credential, authorization header, signed locator, secret query value, private payload, prohibited raw response, or credential-bearing command. Report only safe status classes and provider messages.

Terminal status distinguishes:

- `complete`: provider exhaustion or a single bounded operation completed within all declared bounds;
- `truncated`: an available continuation remained when a bound stopped execution;
- `partial`: accepted results remain but one or more operations failed;
- `paused`: a resolvable clarification or Gate is pending;
- `blocked`: no in-scope provider, tool, permission, or external state can satisfy the action.

Record one normalized observation for complete, truncated, or useful partial provider output. Report the exact resume input or continuation posture.
