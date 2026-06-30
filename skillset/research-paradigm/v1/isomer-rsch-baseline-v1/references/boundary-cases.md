# Boundary Cases

Use this reference when the baseline route is not blocked but the success boundary still feels fuzzy.

## Comparison-Ready but Not Paper-Repro-Ready

This is acceptable when the comparator is trustworthy enough for downstream comparison, the core metric contract is durable, and later work does not need to guess task, split, metric, comparator identity, or caveats.

It is not paper-repro-ready when exact source setup details remain partially unknown, broader variant tables or extra subtasks are missing, or the package is not reusable enough to support paper-facing claims.

## Trusted with Caveats

This is acceptable when the main comparator remains honest and usable, deviations are explicit, and the caveat does not silently change comparison meaning.

Examples include a verified local evaluation surface with one optional auxiliary metric unavailable, or a source-native execution route that differs from a generic environment tactic but better matches the package behavior.

This is not acceptable when the caveat hides a different dataset split, evaluator, metric direction, source identity, or evaluation protocol.

## Imported Metrics with Weak Provenance

Do not accept when a package contains a number but no evidence ties it to a real output, evaluator, source document, or Run record.

Possible next routes are verify-local-existing, reproduce from source, request provenance from the Operator Agent, or block with weak provenance.

## Local Path Exists but Comparator Is Unclear

Do not default into full reproduction immediately. First ask whether there is a concrete evaluation procedure, output location, split contract, and metric contract.

Escalate to reproduction only if those answers stay too ambiguous for honest comparison.

## Heavier Route Feels Cleaner but Not More Trustworthy

Do not replace a working comparison-ready comparator merely because a heavier route feels cleaner. The heavier route becomes justified only when it removes a named unresolved comparison risk.

## Repeated Failure with No New Evidence

Stop looping when the same command, import, package, data, environment, permission, or evaluation failure class appears again and no new evidence, code change, environment change, or route change has reduced uncertainty.

At that point, record the blocker, switch route, repair, waive, or route through decision.
