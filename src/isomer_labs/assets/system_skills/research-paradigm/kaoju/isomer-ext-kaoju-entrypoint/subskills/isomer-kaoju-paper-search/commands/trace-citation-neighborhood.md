# Trace Citation Neighborhood

## Workflow

1. Require resolved seed papers, `forward`, `backward`, or `bidirectional` direction, depth, node, per-node result, page, and resource bounds, research purpose, evidence-use intent, and normalized fields.
2. Default depth to one hop when the actor supplies no depth. Reject an unbounded or negative traversal request.
3. Maintain a frontier keyed by resolved provider identity and a visited set. Expand each identity at most once per applicable direction.
4. Fetch bounded forward or backward edges according to the selected direction, preserving each parent seed and hop depth.
5. Stop at every declared depth, node, per-node, page, provider, resource, or failure bound; retain the reached frontier and successful suboperations.
6. Normalize papers and provider-reported edges, record one logical traversal observation, and hand the bounded graph to the caller.

If the task does not map cleanly to these steps, use your native planning tool to build and execute a bounded frontier plan from the seeds, direction, traversal limits, and stop conditions.

## Bounds and Direction

One hop is the default and never implies permission for a second hop. `Forward` edges run from a citing paper to the expanded seed; `backward` edges run from the expanded seed to a cited paper. `Bidirectional` preserves those meanings rather than relabeling all edges relative to the root.

## Provider Request Intent

Compose only the selected approach's bounded citation and reference operations. Batch metadata lookup may fill normalized fields for already returned identities; it must not expand the frontier implicitly.

## Normalized Output

Return root seeds, visited identities, candidate papers, normalized endpoints, route direction, parent seed, hop depth, reached frontier, requested and applied bounds, pagination, partial failures, completeness, and continuation posture.

## Gates, Blockers, and Resume

Ambiguous seed identity blocks its expansion. Missing provider capability, tool, credential Gate, throttling, or one failed frontier operation preserves successful branches and marks the observation partial. Resume only from the recorded frontier with the same resolved bounds or a newly authorized bounded request. Handoff graph candidates to `discover`.
