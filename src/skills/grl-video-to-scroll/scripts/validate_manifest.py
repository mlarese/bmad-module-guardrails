#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Valida un frame-manifest e i file locali che dichiara."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


SCHEMA = "grl-video-to-scroll/frame-manifest/v1"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_manifest(
    manifest_path: Path,
    *,
    root: Path | None = None,
    max_frames: int | None = None,
    max_bytes: int | None = None,
    require_files: bool = True,
) -> dict[str, Any]:
    """Restituisce un report serializzabile, senza modificare il manifest."""

    try:
        document = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "error", "errors": [f"manifest non leggibile: {exc}"], "warnings": []}
    if root is None:
        root = manifest_path.parent
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(document, dict):
        return {"status": "fail", "errors": ["il manifest deve essere un oggetto JSON"], "warnings": []}
    if document.get("schema") != SCHEMA:
        errors.append(f"schema inatteso: {document.get('schema')!r}")
    frames = document.get("frames")
    if not isinstance(frames, list) or not frames:
        errors.append("frames deve essere una lista non vuota")
        frames = []
    frame_count = document.get("frame_count")
    if not isinstance(frame_count, int) or isinstance(frame_count, bool):
        errors.append("frame_count deve essere un intero")
        frame_count = len(frames)
    elif frame_count != len(frames):
        errors.append(f"frame_count={frame_count} ma frames contiene {len(frames)} elementi")
    if max_frames is not None and len(frames) > max_frames:
        errors.append(f"troppi frame: {len(frames)} > {max_frames}")

    seen_files: set[str] = set()
    seen_indexes: set[int] = set()
    last_progress = -math.inf
    last_timestamp = -math.inf
    total_bytes = 0
    root_resolved = root.resolve()
    for position, frame in enumerate(frames):
        if not isinstance(frame, dict):
            errors.append(f"frame {position} non è un oggetto")
            continue
        index = frame.get("index")
        if index != position:
            errors.append(f"indice frame non consecutivo alla posizione {position}: {index!r}")
        if isinstance(index, int):
            if index in seen_indexes:
                errors.append(f"indice duplicato: {index}")
            seen_indexes.add(index)
        file_name = frame.get("file")
        if not isinstance(file_name, str) or not file_name:
            errors.append(f"file mancante al frame {position}")
            continue
        if file_name in seen_files:
            errors.append(f"file duplicato: {file_name}")
        seen_files.add(file_name)
        file_path = (root / file_name).resolve()
        try:
            file_path.relative_to(root_resolved)
        except ValueError:
            errors.append(f"percorso file fuori dalla radice: {file_name}")
            continue
        progress = frame.get("scroll_progress")
        if not isinstance(progress, (int, float)) or isinstance(progress, bool) or not math.isfinite(progress):
            errors.append(f"scroll_progress non valido al frame {position}")
        elif not 0 <= progress <= 1:
            errors.append(f"scroll_progress fuori range al frame {position}: {progress}")
        elif progress < last_progress:
            errors.append(f"scroll_progress non monotono al frame {position}")
        else:
            last_progress = progress
        timestamp = frame.get("timestamp_seconds")
        if not isinstance(timestamp, (int, float)) or isinstance(timestamp, bool) or not math.isfinite(timestamp):
            errors.append(f"timestamp non valido al frame {position}")
        elif timestamp < last_timestamp:
            errors.append(f"timestamp non monotono al frame {position}")
        else:
            last_timestamp = timestamp
        declared_bytes = frame.get("bytes")
        if not isinstance(declared_bytes, int) or isinstance(declared_bytes, bool) or declared_bytes < 0:
            errors.append(f"bytes non valido al frame {position}")
            declared_bytes = 0
        total_bytes += declared_bytes
        if require_files:
            if not file_path.is_file():
                errors.append(f"file frame mancante: {file_name}")
                continue
            actual_bytes = file_path.stat().st_size
            if actual_bytes != declared_bytes:
                errors.append(f"byte diversi per {file_name}: dichiarati {declared_bytes}, reali {actual_bytes}")
            expected_hash = frame.get("sha256")
            if not isinstance(expected_hash, str) or not expected_hash:
                errors.append(f"sha256 mancante per {file_name}")
            elif _sha256(file_path) != expected_hash:
                errors.append(f"sha256 diverso per {file_name}")
        else:
            warnings.append("file non controllati: modalità allow-missing-files")
    declared_total = document.get("total_bytes")
    if declared_total != total_bytes:
        errors.append(f"total_bytes={declared_total!r} ma la somma dei frame è {total_bytes}")
    if max_bytes is not None and total_bytes > max_bytes:
        errors.append(f"budget superato: {total_bytes} > {max_bytes} byte")
    status = "pass" if not errors else "fail"
    return {
        "status": status,
        "errors": errors,
        "warnings": sorted(set(warnings)),
        "manifest": str(manifest_path),
        "root": str(root),
        "frame_count": len(frames),
        "total_bytes": total_bytes,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Controlla struttura, file, hash e budget di un frame-manifest.")
    parser.add_argument("manifest", type=Path, help="manifest JSON da controllare")
    parser.add_argument("--root", type=Path, help="radice dei percorsi relativi (default: padre del manifest)")
    parser.add_argument("--max-frames", type=int, help="massimo numero di frame")
    parser.add_argument("--max-bytes", type=int, help="massimo peso cumulativo")
    parser.add_argument("--allow-missing-files", action="store_true", help="valida il piano senza richiedere file locali")
    parser.add_argument("-o", "--output", type=Path, help="scrive il report anche in questo file")
    parser.add_argument("--verbose", action="store_true", help="mostra il percorso radice su stderr")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.max_frames is not None and args.max_frames < 1:
        print(json.dumps({"status": "error", "error": "max-frames deve essere positivo"}), file=sys.stdout)
        return 2
    if args.max_bytes is not None and args.max_bytes < 0:
        print(json.dumps({"status": "error", "error": "max-bytes non può essere negativo"}), file=sys.stdout)
        return 2
    report = validate_manifest(
        args.manifest,
        root=args.root,
        max_frames=args.max_frames,
        max_bytes=args.max_bytes,
        require_files=not args.allow_missing_files,
    )
    if args.verbose:
        print(f"manifest root: {report.get('root', '<non disponibile>')}", file=sys.stderr)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    if report["status"] == "pass":
        return 0
    if report["status"] == "fail":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
