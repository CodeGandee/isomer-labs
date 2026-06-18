"""Reference-pack adapter: expose science package-routing cards.
Entrypoint: cards(*, query, quest_id) -> list[dict].

Surfaces BOTH:
  - the 8 curated generic-Python cards in catalog.json (rich use/example/notes), and
  - the full 169-package FermiLink-derived index in references/package-index.min.json
    (package_id/title/description/domains/tags/knowledge_url), normalized to the card shape.
Curated cards win on name collision. `query` filters by case-insensitive substring over the
whole card (name, description, domains, tags). See references/PROVENANCE.md for sourcing and
references/science-evidence-graph.md for how to record science evidence on the Houmao surface.
"""
from __future__ import annotations
import json
from pathlib import Path


def _curated():
    cat = Path(__file__).with_name("catalog.json")
    return json.loads(cat.read_text()) if cat.exists() else []


def _index_cards():
    idx = Path(__file__).with_name("references") / "package-index.min.json"
    if not idx.exists():
        return []
    pkgs = (json.loads(idx.read_text()) or {}).get("packages", [])
    out = []
    for p in pkgs:
        out.append({
            "name": p.get("package_id"),
            "domain": "science",
            "domains": p.get("domains", []),
            "use": p.get("description", ""),
            "title": p.get("title", ""),
            "tags": p.get("tags", []),
            "knowledge_url": p.get("knowledge_url", ""),
            "source": "fermilink-skilled-scipkg",
        })
    return out


def cards(*, query=None, quest_id=None):
    by_name = {}
    for c in _index_cards():          # 169 routing cards first
        if c.get("name"):
            by_name[c["name"]] = c
    for c in _curated():              # curated generic-Python cards override on collision
        if c.get("name"):
            by_name[c["name"]] = c
    data = list(by_name.values())
    if query:
        q = query.lower()
        data = [c for c in data if q in json.dumps(c, default=str).lower()]
    return data
