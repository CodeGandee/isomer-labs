"""Small package-owned HTTP launcher for the Kaoju survey viewer."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Launch the package-owned Kaoju survey viewer.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--pid-file", type=Path, required=True)
    parser.add_argument("--log-file", type=Path, required=True)
    parser.add_argument("--serve", action="store_true", help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve(strict=True)
    if args.serve:
        return _serve(root, args.host, args.port, args.pid_file)
    args.pid_file.parent.mkdir(parents=True, exist_ok=True)
    args.log_file.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "isomer_labs.kaoju.viewer_server",
        "--root",
        str(root),
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--pid-file",
        str(args.pid_file),
        "--log-file",
        str(args.log_file),
        "--serve",
    ]
    with args.log_file.open("a", encoding="utf-8") as log:
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline:
        if process.poll() is not None:
            print(json.dumps({"ok": False, "pid": process.pid, "returncode": process.returncode, "log_file": str(args.log_file)}))
            return 1
        if _connectable(args.host, args.port):
            print(json.dumps({"ok": True, "pid": process.pid, "host": args.host, "port": args.port, "log_file": str(args.log_file)}))
            return 0
        time.sleep(0.05)
    process.terminate()
    print(json.dumps({"ok": False, "pid": process.pid, "reason": "startup_timeout", "log_file": str(args.log_file)}))
    return 1


def _serve(root: Path, host: str, port: int, pid_file: Path) -> int:
    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    server = ThreadingHTTPServer((host, port), handler)
    pid_file.write_text(str(os.getpid()) + "\n", encoding="utf-8")
    try:
        server.serve_forever()
    finally:
        server.server_close()
        pid_file.unlink(missing_ok=True)
    return 0


def _connectable(host: str, port: int) -> bool:
    selected = "127.0.0.1" if host in {"0.0.0.0", "::"} else host
    try:
        with socket.create_connection((selected, port), timeout=0.1):
            return True
    except OSError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
