"""Filesystem layout for the DeepResearch harness.

Specs are resolved relative to this package (fixed); the state DB path is overridable for testing via
the global --db option or the DEEPRESEARCH_DB env var, defaulting to <loop-dir>/runs/state.sqlite.
"""
from __future__ import annotations
import os
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]          # .../execplan/harness
EXECPLAN_DIR = PKG_DIR.parent                          # .../execplan
LOOP_DIR = EXECPLAN_DIR.parent                         # loop dir (holds runs/)
SPECS_DIR = EXECPLAN_DIR / "specs"
AGENTS_DIR = EXECPLAN_DIR / "agents"
BO_REVIEWER_TOML = AGENTS_DIR / "bo-reviewer.toml"   # LLM-reviewer + UCB-like acquisition config (no secrets)
BO_REVIEWER_LOCAL_TOML = AGENTS_DIR / "bo-reviewer.local.toml"  # machine-LOCAL override (gitignored; not the product default)

SCHEMA_SQL = SPECS_DIR / "state" / "schema.sql"
INVARIANTS_TOML = SPECS_DIR / "state" / "invariants.toml"
SEED_TOML = SPECS_DIR / "state" / "seed.toml"
RECORDS_DIR = SPECS_DIR / "state" / "records"

COMMS_DIR = SPECS_DIR / "comms"
COMMS_TEMPLATES = COMMS_DIR / "templates.toml"
COMMS_SCHEMAS = COMMS_DIR / "schemas"
COMMS_RENDERERS = COMMS_DIR / "renderers"


def default_db() -> Path:
    return LOOP_DIR / "runs" / "state.sqlite"


def resolve_db(opt: str | None) -> Path:
    return Path(opt or os.environ.get("DEEPRESEARCH_DB") or default_db())
