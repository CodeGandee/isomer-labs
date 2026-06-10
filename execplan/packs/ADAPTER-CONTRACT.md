# Knowledge-pack adapter contract

How a built-in optional `knowledge_pack` becomes a *real* adapter the harness consumes. `paper-plot` is
the reference implementation; future packs (`nature-figure`, `nature-data`, `nature-paper2ppt`, …) follow
the same shape, so the harness/contract never changes — only the pack contents do.

## Pack directory layout
```
execplan/packs/<name>/
  pack.toml          # manifest (entrypoint, kind, backs, formats, deps)
  adapter.py         # real implementation exposing the kind's entrypoint
  pack.md            # human description
  examples/          # optional sample input(s)/output(s)
```

## Registration + activation
- Declared in `specs/state/seed.toml` as a `knowledge_pack` row with `ref = "execplan/packs/<name>"`,
  **`enabled = 0` by default** (core stays domain-neutral).
- Activate by enabling it (so the resolver can pick it):
  `$HARNESS record apply --type knowledge_pack.register --json '{… "enabled": true …}'` (upsert), or flip
  `enabled = 1` in `seed.toml` before `state init`. Point `quest.domain` at it for domain-scoped selection.
- Resolution (`_resolve_pack`): among **enabled** packs of one `(domain, kind)` the lowest unique
  `priority` wins; `domain` falls back to `general`. If none enabled → the command runs its generic stub.

## Manifest (`pack.toml`)
```toml
name = "<name>"
kind = "compiler"            # compiler | template | runner | validator | reference | metric_vocab
backs = ["render plot"]      # harness commands this adapter serves
entrypoint = "adapter:render" # "<module>:<function>" relative to the pack dir
input_formats = ["csv", "json"]
output_format = "svg"
deps = []                    # extra Python deps ([] = stdlib only)
```

## Entrypoint signature (by kind)
The harness loads `<ref>/adapter.py` and calls the entrypoint named in `pack.toml`. Stable kwargs:

- **compiler** (`render plot|polish|slides`, `render figure`):
  ```python
  def render(*, command, input_path, out_path, params, quest_id) -> dict:
      # read input_path, write the artifact to out_path, return metadata
      return {"ok": True, "out_path": out_path, "format": "svg", "summary": "...", "meta": {...}}
  ```
- **template** (`manuscript polish|datastmt`):
  ```python
  def generate(*, command, input_path, out_path, params, quest_id) -> dict: ...
  ```

## Harness ↔ adapter boundary (rules)
- The **adapter** only reads `input_path` and writes `out_path`; it returns metadata. It must **not**
  touch the state DB, mail, gateway, or agents.
- The **harness** owns state: after a successful adapter call it records the result via
  `record apply --type artifact.record` (the existing write path), so invariants/idempotency still apply.
- On a missing/disabled pack, a missing `adapter.py`, or a missing entrypoint, the command falls back to
  its **generic stub** (records the artifact, `stub=true`) — never an error. Adapter exceptions are
  reported in the command envelope `diagnostics`, and the command exits non-zero (no partial state).
- Adapters should be deterministic and dependency-light; declare any non-stdlib `deps` in `pack.toml`.
