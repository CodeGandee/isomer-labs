# State Specs

## Purpose

Generated durable bookkeeping contracts for the DeepResearch loop. One platform-level sqlite DB
(`runs/state.sqlite`) holds all quests; agents touch it only through harness commands.

## Contents

- `state-overview.md`: authority for entities, transitions, lifecycle flows, invariants, scheduling queries.
- `schema.sql`: sqlite schema (tables, enums, indexes; built-in `stage_catalog` seed).
- `invariants.toml`: named validation checks run by `harness state validate`.
- `seed.toml`: domain-neutral platform seed (registries + role/default templates).
- `records/`: JSON Schemas for `record apply` payloads (the only write path).
