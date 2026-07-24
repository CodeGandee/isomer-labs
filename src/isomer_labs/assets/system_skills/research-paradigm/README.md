# Research Paradigm Public Packs

This subtree contains two optional public extension packs:

| Paradigm | Public Pack Path | Protected Inventory |
| --- | --- | --- |
| DeepSci | `deepsci/isomer-ext-deepsci-entrypoint/` | 21 `isomer-deepsci-*` logical capabilities below `subskills/` |
| Kaoju | `kaoju/isomer-ext-kaoju-entrypoint/` | 16 `isomer-kaoju-*` logical capabilities below `subskills/` |

DeepSci develops or evaluates a research route around a hypothesis and comparator. Kaoju maps and verifies existing literature, code, datasets, and models, including governed first-hand trials when a survey question requires them. Its protected paper-search member owns agent-direct provider retrieval and normalized provider-output observations, while discover retains survey strategy and selection. A task may hand accepted evidence between paradigms, but each retains its own process and evidence contract.

Users invoke only the public entrypoints:

```text
$isomer-ext-deepsci-entrypoint use hypothesis-pass to evaluate a selected idea
$isomer-ext-kaoju-entrypoint use landscape-pass to map a field
```

Task-only invocation may route to a protected member without exposing that member as a top-level host skill. Internal routing uses bare member designators such as `isomer-ext-deepsci-entrypoint->experiment` and `isomer-ext-kaoju-entrypoint->examine`. Public and nested command components always use `()` in object notation.

## Protected Bundle Ownership

Each protected member remains a self-contained skill bundle with its stable logical id and a `SKILL-MAIN.md` entrypoint. The public execution entrypoint resolves and loads only the selected member and its directly required local resources. Resources used by one capability belong inside that bundle. Shared family procedures route through the protected `shared` member. Data or machine services shared across several bundles remain package-owned and are queried through `isomer-cli ext <extension-id>`.

DeepSci traceability material may remain below a protected bundle in `migrate/`, `org/`, passive templates, provenance files, and license notices. Preserved source entrypoints use `SKILL-SOURCE.md`; nested traceability material must not introduce another discovery-named `SKILL.md`. Active runtime resources must remain directly linked and bundle-local.

Kaoju process, semantic, binding, schema, named-template, composition, migration, validation, build, and wiki resources remain under `isomer_labs.kaoju`. The public pack and protected `write` member query those services rather than copying their data.

## Identity and Installation

Protected logical ids remain callback, binding, provenance, and private-projection identities. The old `isomer-deepsci-pipeline` and `isomer-kaoju-pipeline` names are selection and callback-normalization aliases only. No compatibility folder is installed.

Install with `--extension deepsci` or `--extension kaoju`. Each selector installs core plus the complete selected extension pack. Refresh the agent host or start a new session before assuming the public entrypoint is live.
