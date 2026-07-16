# Research Idea Portfolio Workflow Use Cases

These use cases capture the user-perspective questions and actions that motivated `add-research-idea-portfolio-workflow`.

## Index

| ID | Use Case | Status | Primary User Question |
| --- | --- | --- | --- |
| [UC-01](uc-01-browse-and-filter-the-research-idea-portfolio.md) | Browse and Filter the Research Idea Portfolio | Proposed | What ideas were proposed, which were explored, and which remain open? |
| [UC-02](uc-02-trace-an-ideas-ancestry-and-descendants.md) | Trace an Idea's Ancestry and Descendants | Proposed | Which explored ideas derive from this idea? |
| [UC-03](uc-03-review-why-an-idea-was-selected.md) | Review Why an Idea Was Selected | Proposed | Why was this idea selected over the alternatives? |
| [UC-04](uc-04-review-and-reconsider-deferred-or-closed-ideas.md) | Review and Reconsider Deferred or Closed Ideas | Proposed | Which ideas were deferred or closed, and why? |
| [UC-05](uc-05-redirect-exploration-to-another-idea.md) | Redirect Exploration to Another Idea | Proposed | How can I tell the research actor to explore this idea instead? |

## Notes

- UC-01 through UC-04 are read-only Project Web inspection workflows. They do not change Workspace Runtime or canonical Research Idea state.
- UC-05 is an explicit mutating workflow. It records the user's decision and routes a durable task through the Project Operator to the configured topic research actor.
- These focused workflows extend the earlier broad live-lineage and idea-content use cases under `context/features/2026-07-06-topic-idea-iteration-map/`; they do not replace the existing node-content preview behavior.
- The feature baseline is [proposal.md](../proposal.md), with state vocabulary and boundaries defined in [design.md](../design.md).
