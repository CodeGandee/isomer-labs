## 1. Entrypoint Routing Guidance

- [x] 1.1 Build a protected-member inventory from the packaged manifest and collect each member's frontmatter description, agent short description, `## When to Use` guidance, and explicit handoff boundaries for editorial reference.
- [x] 1.2 Replace the operator entrypoint's terse `Use For` cells with one context-aware `When to Route Here` sentence for each of its 20 protected members, preserving every existing identity and designator.
- [x] 1.3 Add one context-aware `When to Route Here` sentence for each of the DeepSci entrypoint's 21 protected members, including decisive distinctions among early research and publication-stage routes.
- [x] 1.4 Add one context-aware `When to Route Here` sentence for each of the Kaoju entrypoint's 13 protected members, including decisive distinctions among source-evidence, execution, and closeout routes.
- [x] 1.5 Review all 54 sentences against their protected sources to remove redundant parent context, direct metadata copies, independent-invocation wording, and conflicts with owner or handoff boundaries.

## 2. Validation

- [x] 2.1 Extend packaged-skill validation to locate each public entrypoint's protected-subskill table and match its rows to manifest-declared protected members.
- [x] 2.2 Validate the `When to Route Here` column, one populated substantive sentence per member, and unchanged member identity and internal designator coverage with file-specific diagnostics.
- [x] 2.3 Reject routing sentences that contain multiple logical sentences or equal the member's normalized frontmatter description or agent short description.
- [x] 2.4 Add unit fixtures for missing columns, missing or duplicate rows, empty or phrase-only guidance, multiple sentences, copied metadata, malformed identities, and valid context-aware guidance.

## 3. Shared Imsight Authoring Convention

- [x] 3.1 In the separate `houmao-agents` checkout, update the bundled Imsight style guide and skill-layout guidance to require one context-aware `When to Route Here` sentence for each direct subskill in its parent entrypoint.
- [x] 3.2 Update the Imsight `create` workflow and validation checklist to author and check complete parent routing sentences whenever a new skill bundles subskills.
- [x] 3.3 Update the Imsight `format` checks, automatic refactoring guidance, and final inspection to repair missing, phrase-only, redundant, or directly copied subskill routing descriptions.
- [x] 3.4 Update the Imsight design guidance and design-output template so proposed subskills record `When to Route Here` separately from invocation and private-resource justification.
- [x] 3.5 Inspect and validate the changed `imsight-agent-skill-handling` files within the Houmao worktree, run the available skill validator when present, and report the separate repository diff without staging it through Isomer.

## 4. Verification

- [x] 4.1 Add pack-specific assertions that all 20 operator, 21 DeepSci, and 13 Kaoju protected members have routing guidance and that representative overlapping routes remain distinguishable.
- [x] 4.2 Run `pixi run validate-skills` and resolve every protected-routing diagnostic.
- [x] 4.3 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` and record any unrelated pre-existing failures separately.
