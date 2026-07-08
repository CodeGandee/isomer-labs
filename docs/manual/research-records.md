# Research Records

Research records are durable, file-backed artifacts that describe ideas, decisions, diagnostics, experiments, papers, and other outputs from a topic. The SQLite index records where each payload lives and how artifacts relate, but the generated files remain the durable source material.

The GUI uses record metadata to build topic overview pages, idea lineage graphs, JSON inspectors, markdown previews, and artifact links. Agents should write records through the supported CLI or library APIs so the file index and relationship DAG stay consistent.

Records may contain more fields than the GUI currently displays. GUI data-contract schemas validate required fields and allow extra fields so newer agents can write richer payloads without breaking older viewers.
