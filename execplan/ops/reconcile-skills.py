#!/usr/bin/env python3
"""Reconcile the project overlay's installed skills to the source-of-truth bindings.

Root cause this fixes: `execplan/agents/skill-bindings.toml` + `execplan/skills/` are the
source of truth, but the overlay catalog (`.houmao/catalog.sqlite`) is only populated by an
explicit install. When skills are added to the source (e.g. the DeepScientist methodology
port) without re-running that install, a fresh pre-flight shows fewer skills than expected and
launched agents silently miss them. There was no committed, runnable installer — this is it.

What it does (idempotent):
  1. Registers every skill referenced in skill-bindings.toml that is not yet in the registry
     (`skills add --mode symlink`; `skills add` errors on duplicates, so we skip those).
  2. Binds each skill to the correct specialists per skill-bindings.toml
     (`specialist set --add-skill`; idempotent, safe to re-apply).
  3. Verifies every specialist's bound set matches the desired set and prints a summary.

Roles in [skills]: `all` is merged into every specialist; `operator` is setup-time only (its
skills are registered so the operator can invoke them, but not bound to a launched specialist).

Usage:
  python3 execplan/ops/reconcile-skills.py [--project-dir DIR] [--check]
    --project-dir  human-facing project dir holding .houmao/ (default: repo root above this file)
    --check        report drift and exit nonzero without mutating anything
"""
from __future__ import annotations
import argparse, sqlite3, subprocess, sys, tomllib
from pathlib import Path

NON_SPECIALIST_ROLES = {"all", "operator"}  # 'all' fans out to every specialist; 'operator' isn't launched


def load_bindings(skill_bindings_path: Path) -> dict[str, list[str]]:
    with skill_bindings_path.open("rb") as fh:
        return tomllib.load(fh)["skills"]


def read_catalog(catalog: Path):
    """Return (registered_skill_names, {specialist_name: set(bound_skill_names)})."""
    con = sqlite3.connect(f"file:{catalog}?mode=ro", uri=True)
    try:
        sp = {sid: name for sid, name in con.execute("SELECT id, name FROM skill_packages")}
        registered = set(sp.values())
        bound: dict[str, set[str]] = {}
        for name, preset_id in con.execute("SELECT name, preset_id FROM specialists"):
            rows = con.execute(
                "SELECT skill_package_id FROM preset_skill_packages WHERE preset_id=?", (preset_id,)
            )
            bound[name] = {sp[r[0]] for r in rows}
        return registered, bound
    finally:
        con.close()


def desired_bindings(bindings: dict[str, list[str]]) -> dict[str, set[str]]:
    """specialist_name -> set of skills it should carry (role list + the shared 'all' list)."""
    shared = set(bindings.get("all", []))
    out: dict[str, set[str]] = {}
    for role, skills in bindings.items():
        if role in NON_SPECIALIST_ROLES:
            continue
        out[f"deepresearch-{role}"] = set(skills) | shared
    return out


def referenced_skills(bindings: dict[str, list[str]]) -> set[str]:
    out: set[str] = set()
    for skills in bindings.values():
        out.update(skills)
    return out


def mgr(project_dir: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["houmao-mgr", "project", "--project-dir", str(project_dir), *args],
        capture_output=True, text=True,
    )


def main() -> int:
    here = Path(__file__).resolve()
    repo_root = here.parents[2]  # execplan/ops/this -> repo root
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project-dir", type=Path, default=repo_root)
    ap.add_argument("--check", action="store_true", help="report drift and exit nonzero without changing anything")
    args = ap.parse_args()

    project_dir: Path = args.project_dir.resolve()
    skills_dir = repo_root / "execplan" / "skills"
    skill_bindings = repo_root / "execplan" / "agents" / "skill-bindings.toml"
    catalog = project_dir / ".houmao" / "catalog.sqlite"

    for p in (skills_dir, skill_bindings, catalog):
        if not p.exists():
            print(f"ERROR: missing {p}", file=sys.stderr)
            return 2

    bindings = load_bindings(skill_bindings)
    want_registered = referenced_skills(bindings)
    want_bound = desired_bindings(bindings)
    registered, bound = read_catalog(catalog)

    to_register = sorted(want_registered - registered)
    to_bind = {s: sorted(sks - bound.get(s, set())) for s, sks in want_bound.items()}
    to_bind = {s: v for s, v in to_bind.items() if v}

    if not to_register and not to_bind:
        print(f"OK: overlay already matches skill-bindings.toml ({len(registered)} skills registered).")
        return 0

    print("DRIFT vs skill-bindings.toml:")
    if to_register:
        print(f"  missing registrations ({len(to_register)}): {', '.join(to_register)}")
    for spec, sks in to_bind.items():
        print(f"  {spec} missing bindings: {', '.join(sks)}")

    if args.check:
        print("\n--check: drift present, no changes made.")
        return 1

    # 1) register missing skills (verify each source has SKILL.md; skills add errors on duplicates)
    for name in to_register:
        src = skills_dir / name
        if not (src / "SKILL.md").is_file():
            print(f"  SKIP register {name}: no SKILL.md at {src}", file=sys.stderr)
            continue
        r = mgr(project_dir, "skills", "add", "--name", name, "--source", str(src), "--mode", "symlink")
        ok = r.returncode == 0
        print(f"  {'registered' if ok else 'FAILED   '} {name}" + ("" if ok else f": {r.stderr.strip().splitlines()[-1:] }"))
        if not ok:
            return 3

    # 2) bind missing skills (idempotent)
    for spec, sks in to_bind.items():
        for name in sks:
            r = mgr(project_dir, "specialist", "set", "--name", spec, "--add-skill", name)
            ok = r.returncode == 0
            print(f"  {'bound' if ok else 'FAILED'} {spec} += {name}" + ("" if ok else f": {r.stderr.strip()}"))
            if not ok:
                return 3

    # 3) verify
    registered2, bound2 = read_catalog(catalog)
    drift = False
    for spec, want in want_bound.items():
        got = bound2.get(spec, set())
        if got != want:
            drift = True
            print(f"VERIFY FAIL {spec}: missing {sorted(want - got)} extra {sorted(got - want)}", file=sys.stderr)
    if drift:
        return 4
    print(f"\nOK: reconciled. {len(registered2)} skills registered; all specialists match skill-bindings.toml.")
    for spec in sorted(want_bound):
        print(f"  {spec}: {len(bound2[spec])} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
