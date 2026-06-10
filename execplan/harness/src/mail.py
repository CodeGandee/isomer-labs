"""email: templated-mail validate / render (jinja2) / schema lookup. Delivery is external."""
from __future__ import annotations
import json
import tomllib
import jsonschema
from jinja2 import Environment, FileSystemLoader

from paths import COMMS_TEMPLATES, COMMS_SCHEMAS, COMMS_RENDERERS

_TEMPLATES = None


def templates() -> dict:
    global _TEMPLATES
    if _TEMPLATES is None:
        reg = tomllib.loads(COMMS_TEMPLATES.read_text())
        _TEMPLATES = {t["schema_id"]: t for t in reg.get("template", [])}
    return _TEMPLATES


def resolve(schema_id_or_name: str) -> dict:
    reg = templates()
    if schema_id_or_name in reg:
        return reg[schema_id_or_name]
    for t in reg.values():
        if t["name"] == schema_id_or_name:
            return t
    raise KeyError(f"unknown mail family: {schema_id_or_name}")


def validate(payload: dict) -> None:
    sid = payload.get("meta", {}).get("schema_id")
    fam = resolve(sid)
    schema = json.load(open(COMMS_SCHEMAS / f"{fam['name']}.schema.json"))
    jsonschema.validate(payload, schema)


def render(payload: dict) -> str:
    sid = payload.get("meta", {}).get("schema_id")
    fam = resolve(sid)
    env = Environment(loader=FileSystemLoader(str(COMMS_RENDERERS)), keep_trailing_newline=True)
    return env.get_template(f"{fam['name']}.md.j2").render(**payload)
