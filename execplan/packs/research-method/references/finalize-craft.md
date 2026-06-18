# Finalize Craft

Use this reference for the closure-protocol craft that complements the finalize gates.
md`. This is the prose the agent reads; the hard
finalize gates (manuscript coverage, outline validation, no-unmapped-analysis, bundle maturity,
etc.) are **enforced at the write path in `records.py`** — do not re-implement them here. Houmao
adaptation: durable closure rows are written with `$HARNESS record apply` (decision/report/quest
rows); the refreshed summary and resume packet live under `runs/<quest-id>/...`.

For the denser line-item checklist, also read `references/finalization-checklist.md` and
`references/resume-packet-template.md`.

## Stage purpose

The finalize stage should not pretend every line succeeded. It produces the most accurate final
state of the quest: what is supported, what is only partially supported, what failed, what
remains open, and whether the right move is stop, archive, publish, or continue later. Finalize
is the durable closure protocol that turns a long-running research graph into a recoverable
stopping point, a publishable handoff, or an honest continue-later checkpoint.

## Belief-change log

For every important outcome, classify it as one of: `supported`, `partially supported`,
`unsupported`, `deferred`. For each claim, record: claim text or id; evidence paths; key
caveats; whether it is safe to surface in summaries or papers.

If a claim was once believed and later weakened, preserve that downgrade history rather than
silently deleting it. Build a compact **belief-change log** for the most important claim
transitions, such as:

- `supported -> partial`
- `partial -> unsupported`
- `promising route -> abandoned`
- `draft-ready -> evidence-gap`

For each transition, record:

- what changed
- which evidence caused the change
- what the new recommendation is

## Limitations taxonomy

A final limitations and failure section should include these six categories:

1. data or split limitations
2. metric limitations
3. implementation limitations
4. robustness limitations
5. reproducibility risks
6. claims intentionally not made

Also preserve: failed branches that meaningfully changed the research direction; blocked items
that remain unresolved; confounders or comparability issues that weaken confidence; handoff
cautions for anyone resuming the quest later.

## Final recommendation structure

Choose the most honest next recommendation, such as: stop and archive; stop and publish;
continue later with a targeted experiment; continue later with a targeted analysis campaign;
reset the current line and revisit ideation.

The recommendation should include:

- the chosen action
- why that action is appropriate now
- what evidence most strongly supports it
- what would have to become true to justify a different recommendation

When deciding whether the quest is publish-ready or only archive-ready, be explicit about which
writing or validation gates have actually passed.

## Resume / handoff packet

If the quest may continue later, leave behind a compact restart packet that answers:

- where the strongest evidence is
- what the current accepted baseline is
- what the current preferred route is
- what the top blockers are
- what should be read first on resume
- what should not be repeated

This packet should be short, high-signal, and directly usable by a future agent turn. If later
continuation remains plausible, also write or refresh one compact checkpoint-style quest memory
card that mirrors the live resume packet, usually stating: current route; current active node
(live paper line, accepted bundle pair, or active continue-later checkpoint); node history
(which earlier nodes / report-decision pairs / closure paths were superseded); strongest
retained result or blocker; what not to reopen by default; next resume step; first files to
read; reopen conditions. Use `references/checkpoint-memory-template.md`.

## Blocked-finalize states

The hard finalize gates are enforced at the write path; this is the diagnostic vocabulary for
naming why finalize is premature. If finalization is premature, record one of these explicitly
and route back to the proper stage through `decision`:

1. `unresolved_major_claim`
2. `unresolved_write_gate`
3. `missing_proofing_or_submission_checks`
4. `unclear_final_recommendation`
5. `missing_handoff_packet`
6. `stale_summary_or_graph`
7. `unresolved_package_inventory`

For paper-like deliverables, do not finalize while any of these remain true: required main-text
outline items unresolved; completed analysis unmapped into the paper contract; the active paper
line still reports blocking open supplementary work; the paper contract rows still fail to
expose the main experiment or required analysis rows the manuscript depends on; manuscript
coverage does not report `submission_ready=true`; the academic-outline validator does not pass
for the selected outline; the manuscript-language validator reports main-text wording blockers;
the latest bundle is only a `draft_checkpoint` or `review_package`. (These are the same
conditions the write-path gate enforces; restated here so the agent can self-diagnose before
attempting the write.)

## Finalization-quality rules

Good finalization: distinguishes supported findings from hopes; preserves negative evidence;
names open questions honestly; leaves a clean state for later resumption; exposes whether
writing/proofing/submission gates passed or failed; makes reopen conditions explicit.

Weak finalization: overclaims unresolved work; hides failed branches; skips limitations; leaves
no clear recommendation; claims "done" without showing what is actually done; drops the package
or file inventory needed for resumption; ignores unmapped completed analysis that never entered
the paper contract.

## Required durable outputs

The finalize stage should usually leave behind: refreshed `SUMMARY.md`; refreshed `status.md`;
final report row; final decision row; refreshed Git graph; explicit limitations and next-step
recommendation; a final claim ledger or equivalent claim-status summary; a compact resume packet
or handoff packet when later continuation is plausible. Quest-specific closure state belongs in
files and DB rows first, not only in memory.
