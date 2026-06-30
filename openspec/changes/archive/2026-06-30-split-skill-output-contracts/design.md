## Context

Many Isomer skills now carry detailed output contracts because later skills need semantic labels, path sources, readiness evidence, and blockers. That detail is useful for handoff and audit, but it is too much for default chat output. The result is that a user sees long bookkeeping lists before they see the actual result.

The most affected skills are the large operator and service skills: topic team specialization, topic workspace management, project management, topic env setup, and agent env setup. Smaller misc and service skills should follow the same convention so agents learn one reporting pattern across the skillset.

This change excludes `skillset/research-paradigm/*` because those skills have their own research evidence and artifact reporting conventions.

## Goals / Non-Goals

**Goals:**

- Make default skill output easy for a user to skim.
- Preserve complete handoff and audit fields for agents, validators, and downstream skills.
- Use one convention across non-research-paradigm skills: **Essential Output** by default and **Complete Output** on request.
- Keep output contracts concise and structured with Markdown lists.
- Update validators and unit fixtures so future skill edits preserve the split.

**Non-Goals:**

- Do not change runtime CLI JSON contracts.
- Do not remove any durable evidence that downstream skills need.
- Do not redesign research-paradigm skill reporting.
- Do not require every small reference page to grow a large output section when the parent skill contract is enough.

## Decisions

1. **Use two output tiers instead of one flat field list.**

   Essential Output is the default chat report. It focuses on status, what happened, important paths, readiness, blockers, and next action. Complete Output is the full handoff/audit report and includes semantic path diagnostics, storage profiles, provenance refs, full command logs, full readiness matrices, detailed operation classification evidence, and complete blocker details.

   Alternative considered: keep one contract and tell agents to summarize. That leaves agents guessing which fields matter and does not give validators a stable shape to enforce.

2. **Let the user request complete output with natural language.**

   Skills should print Complete Output when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output. Otherwise, they should print Essential Output and mention that complete output is available when helpful.

   Alternative considered: add a rigid flag syntax to skill prompts. That is harder for natural-language skill use and not needed for chat-based operation.

3. **Keep Complete Output as structured handoff material, not polished prose.**

   Complete Output should stay field-oriented and JSON-friendly. Essential Output should be human-first and can be structured prose or a compact Markdown list.

   Alternative considered: make both tiers prose. That would improve readability but weaken downstream handoff and validation.

4. **Update parent skill output contracts first.**

   Parent `SKILL.md` output contracts should define the split. Reference pages can say they report through the parent output contract unless they have genuinely local output fields.

   Alternative considered: update every reference page with full essential/complete sections. That would create duplication and make later edits harder.

5. **Validate the convention, not every exact field.**

   Validators should require the presence of Essential Output, Complete Output, default essential behavior, complete-on-request wording, and a few capability-specific essential fields. They should avoid overfitting to the exact full bookkeeping list.

   Alternative considered: validate every complete field name. That repeats the current problem inside the validator and makes small contract evolution brittle.

## Risks / Trade-offs

- [Risk] Agents may omit useful audit detail from Complete Output while shortening contracts. → Mitigation: keep complete output field groups for semantic paths, evidence, commands, changed files, blockers, and next action.
- [Risk] Users may not know complete output exists. → Mitigation: essential reports should include a short note such as `Complete output available on request` when material detail was suppressed.
- [Risk] Existing validators may fail if exact old field lists disappear. → Mitigation: update validators and fixtures to enforce the tiered contract and key field groups instead of the old flat list.
- [Risk] Some small skills may not need both tiers. → Mitigation: still use the section names, but allow short complete output sections that add only evidence and debug detail beyond the essential fields.
- [Risk] Complete Output could become a second long unreadable contract. → Mitigation: group complete fields by purpose, such as identity, paths, evidence, operations, mutations, diagnostics, and next action.

## Migration Plan

1. Update the affected parent `SKILL.md` files outside `skillset/research-paradigm/*`.
2. For large output contracts, replace the flat field list with `### Essential Output` and `### Complete Output`.
3. For small output contracts, keep concise essential and complete sections rather than expanding them.
4. Update reference pages only where they explicitly describe output behavior that conflicts with the new split.
5. Update validators and unit fixtures.
6. Run skill validators and focused unit tests.
