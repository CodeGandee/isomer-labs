#!/usr/bin/env python3
"""Query the Topic Team Specialization step dependency graph."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_STEP_FIELDS = {
    "id",
    "display_name",
    "kind",
    "predecessors",
    "requires",
    "produces",
    "recovery_conditions",
    "mutation_notes",
    "unrecoverable_blockers",
}


class GraphError(Exception):
    """Raised when the dependency graph is invalid or a query cannot be answered."""


def default_manifest_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "step-dependencies.json"


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GraphError(f"Manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GraphError(f"Manifest is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise GraphError("Manifest root must be a JSON object.")
    return data


def step_ids(manifest: dict[str, Any]) -> list[str]:
    steps = manifest.get("steps")
    if not isinstance(steps, dict):
        raise GraphError("Manifest must contain object field 'steps'.")
    return list(steps)


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    steps = manifest.get("steps")
    order = manifest.get("canonical_order")
    edges = manifest.get("edges")

    if not isinstance(manifest.get("version"), int):
        errors.append("Field 'version' must be an integer.")
    if not isinstance(order, list) or not all(isinstance(item, str) for item in order):
        errors.append("Field 'canonical_order' must be a list of step ids.")
        order = []
    if not isinstance(steps, dict):
        errors.append("Field 'steps' must be an object.")
        steps = {}
    if not isinstance(edges, list):
        errors.append("Field 'edges' must be a list.")
        edges = []

    step_keys = set(steps)
    order_set = set(order)
    if len(order) != len(order_set):
        errors.append("Field 'canonical_order' contains duplicate step ids.")
    missing_from_order = sorted(step_keys - order_set)
    extra_in_order = sorted(order_set - step_keys)
    if missing_from_order:
        errors.append(f"Steps missing from canonical_order: {', '.join(missing_from_order)}")
    if extra_in_order:
        errors.append(f"canonical_order contains unknown steps: {', '.join(extra_in_order)}")

    adjacency: dict[str, list[str]] = {key: [] for key in step_keys}
    for step_id, step in steps.items():
        if not isinstance(step, dict):
            errors.append(f"Step '{step_id}' must be an object.")
            continue
        missing_fields = sorted(REQUIRED_STEP_FIELDS - set(step))
        if missing_fields:
            errors.append(f"Step '{step_id}' missing fields: {', '.join(missing_fields)}")
        if step.get("id") != step_id:
            errors.append(f"Step '{step_id}' must declare matching id.")
        for list_field in ("requires", "produces", "recovery_conditions", "mutation_notes", "unrecoverable_blockers"):
            if not isinstance(step.get(list_field), list):
                errors.append(f"Step '{step_id}' field '{list_field}' must be a list.")
        predecessors = step.get("predecessors")
        if not isinstance(predecessors, list):
            errors.append(f"Step '{step_id}' field 'predecessors' must be a list.")
            continue
        for index, predecessor in enumerate(predecessors):
            if not isinstance(predecessor, dict):
                errors.append(f"Step '{step_id}' predecessor {index} must be an object.")
                continue
            predecessor_step = predecessor.get("step")
            if predecessor_step not in step_keys:
                errors.append(f"Step '{step_id}' references unknown predecessor '{predecessor_step}'.")
                continue
            adjacency.setdefault(predecessor_step, []).append(step_id)
            if not isinstance(predecessor.get("condition"), str) or not predecessor.get("condition"):
                errors.append(f"Step '{step_id}' predecessor '{predecessor_step}' needs a condition.")

    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"Edge {index} must be an object.")
            continue
        from_step = edge.get("from")
        to_step = edge.get("to")
        if from_step not in step_keys:
            errors.append(f"Edge {index} references unknown from step '{from_step}'.")
        if to_step not in step_keys:
            errors.append(f"Edge {index} references unknown to step '{to_step}'.")
        if not isinstance(edge.get("condition"), str) or not edge.get("condition"):
            errors.append(f"Edge {index} needs a condition.")

    errors.extend(cycle_errors(adjacency))
    return errors


def cycle_errors(adjacency: dict[str, list[str]]) -> list[str]:
    errors: list[str] = []
    state: dict[str, str] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        state[node] = "visiting"
        stack.append(node)
        for neighbor in adjacency.get(node, []):
            neighbor_state = state.get(neighbor)
            if neighbor_state == "visiting":
                cycle_start = stack.index(neighbor)
                errors.append("Dependency cycle: " + " -> ".join(stack[cycle_start:] + [neighbor]))
            elif neighbor_state is None:
                visit(neighbor)
        stack.pop()
        state[node] = "visited"

    for node in adjacency:
        if state.get(node) is None:
            visit(node)
    return errors


def require_valid(manifest: dict[str, Any]) -> None:
    errors = validate_manifest(manifest)
    if errors:
        raise GraphError("\n".join(errors))


def get_step(manifest: dict[str, Any], target: str) -> dict[str, Any]:
    steps = manifest["steps"]
    if target not in steps:
        raise GraphError(f"Unknown target step '{target}'.")
    return steps[target]


def predecessor_closure(manifest: dict[str, Any], target: str) -> set[str]:
    get_step(manifest, target)
    seen: set[str] = set()

    def visit(step_id: str) -> None:
        for predecessor in manifest["steps"][step_id]["predecessors"]:
            predecessor_id = predecessor["step"]
            if predecessor_id in seen:
                continue
            seen.add(predecessor_id)
            visit(predecessor_id)

    visit(target)
    return seen


def ordered_path(manifest: dict[str, Any], target: str, *, include_target: bool) -> list[str]:
    closure = predecessor_closure(manifest, target)
    if include_target:
        closure.add(target)
    order = manifest["canonical_order"]
    return [step_id for step_id in order if step_id in closure]


def emit(payload: Any, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    if isinstance(payload, list):
        for item in payload:
            print(f"- {item}")
        return
    print(payload)


def command_validate(manifest: dict[str, Any], *, as_json: bool) -> int:
    errors = validate_manifest(manifest)
    if as_json:
        emit({"valid": not errors, "errors": errors}, as_json=True)
    elif errors:
        for error in errors:
            print(error, file=sys.stderr)
    else:
        print("step-dependencies.json is valid")
    return 1 if errors else 0


def command_path(manifest: dict[str, Any], target: str, *, include_target: bool, as_json: bool) -> None:
    path = ordered_path(manifest, target, include_target=include_target)
    if as_json:
        emit({"target": target, "include_target": include_target, "path": path}, as_json=True)
        return
    mode = "inclusive" if include_target else "exclusive"
    print(f"{mode} path to {target}:")
    print(" -> ".join(path) if path else "(no predecessor steps)")


def command_list_field(manifest: dict[str, Any], target: str, field: str, *, as_json: bool) -> None:
    step = get_step(manifest, target)
    payload = {"target": target, field: step[field]} if as_json else step[field]
    emit(payload, as_json=as_json)


def command_explain(manifest: dict[str, Any], target: str, *, as_json: bool) -> None:
    step = get_step(manifest, target)
    predecessors = step["predecessors"]
    payload = {
        "target": target,
        "display_name": step["display_name"],
        "kind": step["kind"],
        "predecessors": predecessors,
        "requires": step["requires"],
        "produces": step["produces"],
        "recovery_conditions": step["recovery_conditions"],
        "mutation_notes": step["mutation_notes"],
        "unrecoverable_blockers": step["unrecoverable_blockers"],
    }
    if as_json:
        emit(payload, as_json=True)
        return
    print(f"{step['display_name']} ({target})")
    if predecessors:
        print("Predecessor steps:")
        for predecessor in predecessors:
            print(f"- {predecessor['step']}: {predecessor['condition']}")
    else:
        print("Predecessor steps: none")
    print("Requires:")
    for item in step["requires"]:
        print(f"- {item}")
    print("Produces:")
    for item in step["produces"]:
        print(f"- {item}")
    print("Unrecoverable blockers:")
    for item in step["unrecoverable_blockers"]:
        print(f"- {item}")


def add_common_query_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=default_manifest_path(),
        help="Path to step-dependencies.json. Defaults to the manifest next to this skill.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate the dependency manifest.")
    add_common_query_args(validate_parser)

    path_parser = subparsers.add_parser("path", help="Print a dependency path for a target step.")
    path_parser.add_argument("--target", required=True, help="Target subcommand id.")
    mode_group = path_parser.add_mutually_exclusive_group()
    mode_group.add_argument("--include-target", action="store_true", default=True, help="Include the target step.")
    mode_group.add_argument("--exclude-target", action="store_true", help="Stop before the target step.")
    add_common_query_args(path_parser)

    for command, help_text in (
        ("prereqs", "Print required predecessor artifacts or inputs."),
        ("produces", "Print produced artifacts or outputs."),
        ("blockers", "Print unrecoverable blockers."),
        ("explain", "Print a full explanation for one step."),
    ):
        query_parser = subparsers.add_parser(command, help=help_text)
        query_parser.add_argument("--target", required=True, help="Target subcommand id.")
        add_common_query_args(query_parser)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        manifest = load_manifest(args.manifest)
        if args.command == "validate":
            return command_validate(manifest, as_json=args.json)
        require_valid(manifest)
        if args.command == "path":
            include_target = not args.exclude_target
            command_path(manifest, args.target, include_target=include_target, as_json=args.json)
        elif args.command == "prereqs":
            command_list_field(manifest, args.target, "requires", as_json=args.json)
        elif args.command == "produces":
            command_list_field(manifest, args.target, "produces", as_json=args.json)
        elif args.command == "blockers":
            command_list_field(manifest, args.target, "unrecoverable_blockers", as_json=args.json)
        elif args.command == "explain":
            command_explain(manifest, args.target, as_json=args.json)
        else:
            parser.error(f"Unknown command {args.command}")
    except GraphError as exc:
        if getattr(args, "json", False):
            emit({"valid": False, "errors": str(exc).splitlines()}, as_json=True)
        else:
            print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
