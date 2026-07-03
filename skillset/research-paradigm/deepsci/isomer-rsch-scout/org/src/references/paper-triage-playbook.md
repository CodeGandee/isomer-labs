# Paper Triage Playbook

Use this reference during `scout` when you need a more explicit process for building the paper and repo neighborhood.

## Search objective

The goal is not to collect many papers.
The goal is to map the smallest neighborhood that can justify:

- the task frame
- the evaluation contract
- the baseline shortlist

## Search order and reuse discipline

Before broad web search:

1. read recent quest `papers`, `knowledge`, and `decisions`
2. run `memory.search(...)` on task, benchmark, dataset, metric, split, and likely baseline names
3. search externally only for the missing pieces

Then search externally in this order:

1. arXiv for paper discovery
2. benchmark docs and official repos for contract truth
3. broader web search for provenance checks or follow-up references

## Retain only useful references

For each retained item, record:

- identifier or title
- why it matters
- whether it informs task framing, evaluation contract, baseline route, or later ideation

Reject references that do not materially change the next stage.

## Repo triage

When a paper has code, inspect:

- whether the repo is official or clearly linked
- whether the evaluation path is obvious
- whether dependencies are realistic
- whether the repo appears maintained enough to be usable

## Stop condition

Stop when:

- the strongest obvious references are mapped
- baseline candidates can be ranked credibly
- metric and split ambiguity are no longer the main blocker
