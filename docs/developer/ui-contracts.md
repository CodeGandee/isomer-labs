# UI Contracts

GUI data contracts live under `docs/ui/contracts/`. Each page describes the required metadata that the backend and frontend depend on when showing topic overview, idea detail, graph, diagnostics, record inspection, and display paths.

Use schemas in `src/isomer_labs/` to validate required fields while allowing extra fields. Agents often write richer JSON than the GUI needs, so strict rejection of unknown fields would make the viewer brittle.

Contract pages are developer-facing. They should state the producer responsibility, the consumer expectation, and the fallback behavior when optional data is absent.

See [UI Contract Index](../ui/contracts/index.md).
