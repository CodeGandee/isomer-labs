---
name: scout
description: Use when a quest needs problem framing, literature scouting, dataset or metric clarification, or baseline discovery before deeper work.
skill_role: stage
---

# Scout

Use this skill when the quest does not yet have a stable research frame.
The goal is to make the task frame concrete enough that a heavier stage can start with confidence.

## Match signals

Use `scout` when:

- the user goal is still ambiguous
- the dataset or split contract is unclear
- the primary metric is unclear
- no trustworthy baseline has been identified
- the paper or repo neighborhood is still thin
- the quest was resumed after a long pause and framing needs reconstruction
- the next stage is blocked by ambiguity rather than by implementation

Do not use `scout` when:

- the user already fixed the paper, baseline, dataset, metric contract, and scope
- the quest already has a validated baseline and is ready for ideation or execution
- the real blocker is execution or verification rather than framing

## One-sentence summary

Resolve only the minimum framing unknowns that change the next anchor, then stop once baseline or idea becomes durable and obvious.

## Control workflow

1. Reconstruct the current frame from durable state.
   Make the current task, metric contract, baseline status, and blockers explicit before searching.
2. Identify the minimum unknowns.
   Keep only the unknowns that materially block `baseline`, `idea`, or both.
3. Search only the unresolved neighborhood.
   Reuse memory and local evidence first, then search the smallest paper, repo, and benchmark surface that can change the next anchor.
4. Make the evaluation contract and baseline direction explicit.
   End with a small decision-facing baseline shortlist rather than a broad literature dump.
5. Record the next anchor or blocker and stop on clarity.
   The right output is a durable frame, not search exhaustion.

## AVOID / pitfalls

- Do not let `scout` become endless exploration.
- Do not keep searching once the next anchor is already clear.
- Do not guess the metric, split, or baseline identity when local evidence is still ambiguous.
- Do not ask the user ordinary technical questions before checking local evidence first.
- Do not repeat the same wide search from scratch when existing survey notes, memory, or durable quest files already narrow the space.
- Do not write long paper summaries that do not change the next stage.
- Do not inflate novelty when the apparent gap is already closed by straightforward scaling, standard engineering, or a strong recent paper.

## Constraints

- Before broad external search, check quest or global memory first with `memory.list_recent(...)` and `memory.search(...)`.
- When search tools are available, actively use them.
- If DeepXiv is declared available by the system prompt, prefer the DeepXiv route for paper-centric discovery and shortlist triage before broader open-web search.
- If DeepXiv is declared unavailable, stay on the legacy route: memory reuse, web discovery, and `artifact.arxiv(...)` for actual paper reads.
- When a specific arXiv paper must be read or summarized, use `artifact.arxiv(paper_id=..., full_text=False)` instead of defaulting to a raw PDF.
- Keep discovery in search tooling by default; use `artifact.arxiv(...)` only for actual paper reading, and set `full_text=True` only when needed.
- `scout` should normally hand off to `baseline` or `idea` as soon as the next move is decision-ready.

## Validation

Before `scout` can end, all applicable checks should be true:

- the task frame is explicit enough
- the evaluation contract is explicit enough
- at least one baseline direction is justified enough
- the next anchor is obvious enough to record durably, or the blocker is explicit enough to stop guessing

## Interaction discipline

Follow the shared interaction contract injected by the system prompt.
Only send a richer scout milestone when the framing ambiguity actually shrank or the next anchor became clear.
For ordinary active work, prefer a concise progress update once work has crossed roughly 6 tool calls with a human-meaningful delta, and do not drift beyond roughly 12 tool calls or about 8 minutes without a user-visible update.

## Tool discipline

- **Do not use native `shell_command` / `command_execution` in this skill.**
- **Any shell, CLI, Python, bash, node, git, npm, uv, or repo-inspection execution must go through `bash_exec(...)`.**
- **For git inspection inside the current quest repository or worktree, prefer `artifact.git(...)` before raw shell git commands.**
- **If scouting only needs durable quest context, prefer `artifact.read_quest_documents(...)`, `artifact.get_quest_state(...)`, and `memory.*` instead of shelling out.**

## Truth sources

Prefer the following sources in order:

1. user-provided task description and explicit constraints
2. durable quest files and artifacts
3. codebase and repository docs
4. primary papers, official repos, and benchmark docs
5. existing reusable baselines and quest/global memory
6. web-search results, often including arXiv and adjacent sources, used to fill gaps, verify provenance, or update recency

Do not let the scout stage rest on vague recollection alone.

## Non-negotiable rules

- Do not force a baseline route without comparing attach, import, and reproduce options.
- Do not rely on memory alone when primary sources or durable quest files exist.
- Search for disconfirming evidence, not only supportive evidence.
- If one of the core framing layers is still missing, say so explicitly instead of pretending the frame is complete.

The scout stage should usually establish four layers:

- task-definition layer
- evaluation-contract layer
- literature and repo neighborhood layer
- baseline-direction layer

## Preconditions and gate

Before spending time scouting, first verify whether the current quest already contains enough framing in:

- `brief.md`
- `plan.md`
- `status.md`
- `SUMMARY.md`
- baseline artifacts
- recent paper or knowledge memory cards

If the answer is already clear, exit quickly and move to the correct next anchor.

## Operational guidance

The main skill keeps the control surface in front.
For the longer search and handoff notes, read:

- `references/paper-triage-playbook.md`
- `references/literature-scout-template.md`
- `references/eval-contract-template.md`
- `references/baseline-shortlist-template.md`
- `references/operational-guidance.md`

Use them when:

- the paper and repo search needs a fuller playbook
- the evaluation contract or baseline shortlist should be written durably
- memory or artifact handling materially affects the route

## Blocked-state handling

Record a blocked state if scouting cannot proceed because:

- the quest objective is materially ambiguous
- the required code or paper source is missing
- multiple evaluation contracts conflict and the choice would change later conclusions
- all baseline candidates are too weak, broken, or poorly specified

A blocked scout result should state:

- what is missing
- why it matters
- which next anchor is blocked
- what concrete user choice or source is needed

Do not hide a blocked scout stage behind generic literature chatter.

## Exit criteria

Exit the scout stage once all of the following are true:

- the task frame is explicit
- the evaluation contract is explicit
- at least one baseline direction is justified
- the next anchor is obvious enough to record durably

If the stage relied on external search, the literature scouting report must also be durable before exit.

Typical next anchors:

- `baseline`
- `idea`
- remain in `scout` only if the remaining blocker is explicit and durable

A good scout pass makes the next anchor obvious or makes the blocker explicit enough that the system stops guessing.
