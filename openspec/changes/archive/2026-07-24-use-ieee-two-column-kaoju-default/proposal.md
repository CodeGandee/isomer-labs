## Why

Kaoju currently ships a neutral one-column `article` fallback even though the Predictive Memory Survey established a working IEEE Transactions two-column template with a locally available class file and checked composition contract. Shipping that proven tree as `latex/main` gives newly initialized topics and fallback consumers the intended paper presentation without requiring each topic to rediscover or adopt the same venue stock.

## What Changes

- Replace the packaged Kaoju `latex/main` neutral article tree with the prepared IEEE Transactions journal tree used by the Predictive Memory Survey.
- Vendor the complete prepared template tree into the installed `isomer_labs` package, including `IEEEtran.cls`, the marker-based composition entrypoint, the retained upstream sample, its referenced figure asset, and source metadata, so the IEEE class and style do not depend on `tmp/`, another workspace, or an external checkout.
- Update the packaged-template manifest, digest, resource version, provenance, license posture, and use guidance to describe the IEEE two-column default accurately.
- Keep the generic MyST `content/main` default and the existing role-aware selection rules unchanged: ready topic-owned `latex/main` stock still wins, and existing paper snapshots or initialized topic stock are not rewritten.
- Extend package-resource, initialization, export, and paper-composition tests to prove that the installed fallback contains and uses the vendored IEEE style tree.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kaoju-paper-production`: Change the checked packaged LaTeX `main` requirement from a neutral article presentation to the self-contained IEEE Transactions two-column tree proven by the Predictive Memory Survey, while preserving topic-stock precedence and immutable snapshot behavior.

## Impact

The change affects Kaoju packaged assets under `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/`, their manifest and resource digest, package-data validation, writing-template initialization and fallback expectations, and related unit tests and skill guidance. New topics and workspaces without topic-owned LaTeX stock will observe the IEEE default; existing topic-owned templates and paper artifacts retain their recorded bytes and identities. The vendored `IEEEtran.cls` remains subject to its declared LaTeX Project Public License posture.
