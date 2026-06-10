"""Reference-pack adapter: expose catalog cards. Entrypoint: cards(*, query, quest_id) -> list[dict].
Reads catalog.json colocated with this adapter; filters by `query` substring when given.
"""
from __future__ import annotations
import json
from pathlib import Path


def cards(*, query=None, quest_id=None):
    cat = Path(__file__).with_name("catalog.json")
    data = json.loads(cat.read_text()) if cat.exists() else []
    if query:
        q = query.lower()
        data = [c for c in data if q in json.dumps(c).lower()]
    return data
