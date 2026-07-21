# Latest Context Preflight

Use this preflight before a production DeepSci skill accepts durable research record work, refreshes an accepted record, or makes a durable route, claim, context, evidence, result, or publication-facing decision. It resolves the current Isomer topic state before the agent trusts prompt context, chat memory, older rendered prose, or remembered research state.

Standalone source-only reading may skip this preflight until the skill writes or refreshes accepted Isomer records. Plain generated files remain governed by Worker Output Policy; run this preflight before promoting or recording those files as accepted durable records.

## Command Ladder

1. Extract any prompt-selected Research Topic, Topic Actor, or Agent before consulting defaults. Run `isomer-cli --print-json project self location`, then run `isomer-cli --print-json project self check --scope topic --topic <prompt-topic>` for a named topic, `--scope topic-actor --topic <prompt-topic> --topic-actor <prompt-topic-actor>` for a named Topic Actor, or `--scope agent --topic <prompt-topic> --agent <prompt-agent>` for a named Agent. A prompt target is always an explicit selector; Project-root cwd and manifest defaults cannot replace it.
2. When a topic-scoped prompt names no Research Topic, run the applicable self check without a topic selector. Accept a valid stronger Effective Context source or Project Manifest default only when the result is nonconflicting, record its exact source as fallback evidence, and pin the returned Research Topic id as `<topic>` before continuing. A sole manifest actor does not establish active acting posture.
3. Stop before durable writes on `unresolved` or `conflict`, including disagreement between prompt target, active switch posture, explicit selector, or validated worker cwd. Record the conflicting sources and require a corrected selector, switch reset, or explicit scope decision. Do not choose from chat memory, sibling Topic Workspaces, another manifest default, or filesystem layout.
4. Resolve Effective Topic Context with `isomer-cli --print-json project context show --topic <topic>`. Treat the resolved Research Topic id, Research Topic Config path, Topic Workspace path, source metadata, and effective Topic Actor or Agent context as current stage evidence, while keeping ambient location, task target, manifest fallback, and acting posture distinct.
5. Discover safe follow-up commands with `isomer-cli --print-json project self queries` when additional selectors, paths, or diagnostic queries are needed. Do not infer topic identity from sibling directories, remembered context, or hard-coded paths.
6. Inspect Workspace Runtime with `isomer-cli --print-json project runtime inspect --topic <topic>` when the selected Research Topic has a Topic Workspace. Treat missing, invalid, stale, or contradictory runtime evidence as a blocker or route-to-bootstrap condition before accepted records are written.
7. Resolve semantic paths with `isomer-cli --print-json project paths get <semantic-label> --topic <topic>` and the pinned `--topic-actor <topic-actor>` or `--agent <agent>` selector when applicable. Use path-resolution output instead of constructing Topic Workspace, Topic Actor Workspace, Agent Workspace, or record paths by hand.
8. List stage-relevant records with `isomer-cli --print-json ext research records list --topic <topic> --semantic-id 'DEEPSCI:WHAT'` before using a prior context brief, contract, route decision, hypothesis, result, analysis finding, paper state, blocker, or on-demand view as current.
9. Inspect candidate records with `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` when payload fields, rendered review text, status, timestamps, active signals, supersession signals, or route metadata may affect the stage.

Every applicable topic- or worker-scoped command after alignment must retain the pinned `--topic <topic>` and applicable `--topic-actor <topic-actor>` or `--agent <agent>` selector, even when cwd changes. If the user or workflow intentionally changes Research Topic, Topic Actor, Agent, or operation scope, rerun the context alignment steps and create a new freshness verdict before using the new target.

## Freshness Verdict

Produce or feed a stage-local `DEEPSCI:LATEST-CONTEXT-SNAPSHOT` verdict before durable record work proceeds. The verdict can live inside the stage's first accepted context object, contract, paper state, route decision, blocker, or equivalent record; it does not require a standalone durable record.

The verdict must name:

- selected Research Topic and topic selectors used
- Research Topic Config source or source metadata
- Topic Workspace path or absence
- Workspace Runtime inspection status and blocker state
- effective Topic Actor or Agent context when available
- placeholder records checked and selected candidate record ids
- whether prompt-provided context matched durable context, refined it, conflicted with it, or implied a Research Topic scope change
- route taken when the current stage is no longer ready
- ambient location, task-selected target, manifest fallback, and active acting posture as separate evidence
- alignment verdict and any explicit-override or conflict diagnostics

## Conflict Routing

Treat prompt context as candidate context until the preflight confirms it against durable Isomer state. If prompt-provided context conflicts with the current Research Topic, route records, comparator basis, metric contract, paper state, blocker records, or runtime evidence, do not continue from memory.

When a typed topic-sensitive operation returns selected-context metadata, compare its Research Topic and Topic Workspace with the pinned target. A mismatch, not-found result, or context-conflict diagnostic triggers selector correction or renewed alignment against the same requested target. It does not authorize searching another Research Topic, falling back to another default, adding an alternate output path, or copying material into a worker workspace or Topic Main.

Route conflicts using the smallest responsible stage:

- use scout when the frame, dataset, metric, benchmark, or route is no longer concrete enough
- use baseline when comparator basis, metric contract, reproduction status, or accepted waiver changed
- use decision when competing ready records, route reversals, or user-sensitive tradeoffs need an explicit verdict
- use workspace-mgr when Topic Workspace, Topic Actor, Agent Workspace, placeholder binding, semantic surface, or runtime readiness is missing or stale
- use paper-outline when paper target, claim boundary, outline, or evidence-to-paper mapping changed
- record a blocker when no responsible route can proceed without missing setup, missing durable records, invalid runtime, or user input

## Duplicate Records

When `records list` returns several ready records for the same placeholder or semantic object, use the newest ready record only as the default candidate. Prefer explicit active, supersession, route, or decision metadata when present. If competing ready records conflict and no active record can be identified responsibly, route to decision or blocker handling instead of merging or silently choosing one.

Do not teach unavailable `--latest` or `--active` selectors as current behavior. Those selectors are deferred to graph-index follow-up work.

## Record Authority

When a durable record has both structured payload and on-demand Markdown view, treat the structured payload and record metadata as authoritative for machine-readable fields. Treat on-demand Markdown as review material unless the producing binding declares otherwise.

Worker output roots are for pre-promotion or operation-local plain files. A file under the resolved worker output root is not an accepted Artifact, Evidence Item, Run record, Decision Record, View Manifest, context brief, contract, route decision, or other durable research record until a separate accepted record or promotion action records it under the appropriate topic-owned surface.
