#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Controlla le capability locali richieste dal workflow video-to-scroll.

Il comando è read-only: non installa pacchetti e non modifica il progetto.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable


COMMANDS = (
    ("uv", ("--version",), "esecuzione isolata degli script BMad"),
    ("ffmpeg", ("-version",), "estrazione dei frame"),
    ("ffprobe", ("-version",), "durata e dimensioni del video"),
)
RUNTIME_FILES = (
    "_bmad/scripts/resolve_config.py",
    "_bmad/scripts/resolve_customization.py",
    "_bmad/scripts/memlog.py",
)


def _version(command: str, args: tuple[str, ...], runner: Callable[..., Any]) -> tuple[bool, str]:
    try:
        result = runner(
            [command, *args],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return False, str(exc)
    output = (result.stdout or result.stderr or "").strip()
    first_line = output.splitlines()[0] if output else "version non rilevata"
    return result.returncode == 0, first_line[:240]


def check_command(
    name: str,
    version_args: tuple[str, ...],
    purpose: str,
    *,
    which: Callable[[str], str | None] = shutil.which,
    runner: Callable[..., Any] = subprocess.run,
) -> dict[str, Any]:
    path = which(name)
    if path is None:
        return {
            "name": name,
            "purpose": purpose,
            "installed": False,
            "usable": False,
            "path": None,
            "version": None,
        }
    usable, version = _version(path, version_args, runner)
    return {
        "name": name,
        "purpose": purpose,
        "installed": True,
        "usable": usable,
        "path": path,
        "version": version,
    }


def check_runtime_files(project_root: Path) -> list[dict[str, Any]]:
    results = []
    for relative in RUNTIME_FILES:
        path = project_root / relative
        results.append({
            "path": relative,
            "installed": path.is_file(),
        })
    return results


def install_hints(system_name: str) -> list[str]:
    if system_name == "Darwin":
        return ["brew install uv ffmpeg"]
    if system_name == "Windows":
        return [
            "winget install --id=astral-sh.uv -e",
            "winget install --id=Gyan.FFmpeg.Shared -e",
        ]
    if system_name == "Linux":
        return [
            "sudo apt-get install ffmpeg  # Debian/Ubuntu",
            "installare uv tramite il package manager o la documentazione ufficiale della distribuzione",
        ]
    return ["installare uv, ffmpeg e ffprobe tramite il package manager ufficiale del sistema"]


def build_report(
    commands: list[dict[str, Any]],
    runtime_files: list[dict[str, Any]],
    *,
    system_name: str,
    project_root: Path,
) -> dict[str, Any]:
    missing = [
        item["name"]
        for item in commands
        if not item["installed"] or not item["usable"]
    ]
    missing.extend(
        item["path"] for item in runtime_files if not item["installed"]
    )
    status = "pass" if not missing else "missing"
    return {
        "schema": "grl-video-to-scroll/tool-preflight/v1",
        "status": status,
        "system": system_name,
        "project_root": str(project_root),
        "commands": commands,
        "runtime_files": runtime_files,
        "missing": missing,
        "install_commands": [] if status == "pass" else install_hints(system_name),
        "note": "read-only check; no installation was performed",
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Controlla uv, ffmpeg, ffprobe e il runtime BMad senza installare nulla."
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="radice del progetto da controllare (default: directory corrente)",
    )
    parser.add_argument("-o", "--output", type=Path, help="scrive il report anche in questo file")
    parser.add_argument("--verbose", action="store_true", help="scrive dettagli diagnostici su stderr")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        project_root = args.project_root.resolve()
        commands = [
            check_command(name, version_args, purpose)
            for name, version_args, purpose in COMMANDS
        ]
        runtime_files = check_runtime_files(project_root)
        report = build_report(
            commands,
            runtime_files,
            system_name=platform.system(),
            project_root=project_root,
        )
        rendered = json.dumps(report, ensure_ascii=False, indent=2)
        print(rendered)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered + "\n", encoding="utf-8")
        if args.verbose:
            print(f"controllate {len(commands)} comandi e {len(runtime_files)} file runtime", file=sys.stderr)
        return 0 if report["status"] == "pass" else 1
    except OSError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
