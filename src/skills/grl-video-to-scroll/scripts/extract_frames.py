#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Estrae frame da un file video locale e produce un manifest JSON.

Il comando è deliberatamente locale: non scarica, carica o pubblica sorgenti.
Richiede ffmpeg e ffprobe disponibili nel PATH. Le funzioni pure sono tenute
separate per permettere test senza un file video o un'installazione ffmpeg.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "grl-video-to-scroll/frame-manifest/v1"


class UserError(ValueError):
    """Errore di input che deve produrre exit code 1."""


def parse_timestamps(path: Path, duration: float, max_frames: int) -> list[float]:
    """Legge secondi decimali, rimuove duplicati e verifica il range."""

    if not path.is_file():
        raise UserError(f"file timestamp non trovato: {path}")
    result: list[float] = []
    seen: set[float] = set()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        try:
            value = float(line)
        except ValueError as exc:
            raise UserError(f"timestamp non numerico alla riga {line_number}: {raw!r}") from exc
        if not math.isfinite(value) or value < 0 or value > duration + 1e-6:
            raise UserError(
                f"timestamp fuori dal video alla riga {line_number}: {value}; durata={duration:.3f}"
            )
        value = min(value, duration)
        if value not in seen:
            result.append(value)
            seen.add(value)
    if not result:
        raise UserError("il file timestamp non contiene valori")
    if len(result) > max_frames:
        raise UserError(f"{len(result)} timestamp eccedono il massimo di {max_frames} frame")
    return result


def uniform_timestamps(duration: float, fps: float, max_frames: int) -> list[float]:
    """Crea un piano uniforme, sempre iniziando dal tempo zero."""

    if not math.isfinite(fps) or fps <= 0:
        raise UserError("fps deve essere un numero positivo")
    if duration <= 0:
        raise UserError("la durata del video deve essere positiva")
    values: list[float] = []
    index = 0
    while index < max_frames:
        timestamp = index / fps
        if timestamp > duration + 1e-6:
            break
        values.append(min(timestamp, duration))
        index += 1
    if not values:
        values = [0.0]
    return values


def make_progress(count: int) -> list[float]:
    """Distribuisce gli elementi sul progresso normalizzato 0..1."""

    if count < 1:
        return []
    if count == 1:
        return [0.0]
    return [round(index / (count - 1), 6) for index in range(count)]


def _run(command: list[str], *, verbose: bool = False) -> subprocess.CompletedProcess[str]:
    if verbose:
        print("$ " + " ".join(command), file=sys.stderr)
    return subprocess.run(command, check=True, text=True, capture_output=True)


def probe_video(path: Path) -> dict[str, Any]:
    """Legge durata e dimensioni del primo stream video con ffprobe."""

    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate:format=duration",
        "-of",
        "json",
        str(path),
    ]
    try:
        completed = _run(command)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "ffprobe ha rifiutato il file").strip()
        raise UserError(f"video non leggibile: {detail}") from exc
    try:
        data = json.loads(completed.stdout)
        stream = data["streams"][0]
        duration = float(data["format"]["duration"])
        width = int(stream["width"])
        height = int(stream["height"])
    except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise UserError("ffprobe non ha restituito durata e dimensioni video valide") from exc
    if duration <= 0 or width <= 0 or height <= 0:
        raise UserError("video con durata o dimensioni non valide")
    return {
        "duration_seconds": round(duration, 6),
        "width": width,
        "height": height,
        "frame_rate": stream.get("r_frame_rate"),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _probe_image(path: Path) -> tuple[int | None, int | None]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-of",
        "json",
        str(path),
    ]
    try:
        completed = _run(command)
        stream = json.loads(completed.stdout)["streams"][0]
        return int(stream["width"]), int(stream["height"])
    except (subprocess.CalledProcessError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        return None, None


def _relative_path(path: Path, root: Path) -> str:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise UserError(f"il frame {path} deve stare sotto la radice del manifest {root}") from exc
    return relative.as_posix()


def build_manifest(
    *,
    source: Path,
    source_info: dict[str, Any],
    frame_paths: Iterable[Path],
    timestamps: list[float],
    root: Path,
    sampling: dict[str, Any],
    width_limit: int,
    image_format: str,
    quality: int,
) -> dict[str, Any]:
    """Costruisce un manifest senza percorsi assoluti."""

    paths = list(frame_paths)
    if len(paths) != len(timestamps):
        raise UserError(f"frame prodotti ({len(paths)}) diversi dal piano ({len(timestamps)})")
    progress = make_progress(len(paths))
    frames: list[dict[str, Any]] = []
    for index, (path, timestamp, scroll_progress) in enumerate(zip(paths, timestamps, progress)):
        if not path.is_file():
            raise UserError(f"frame mancante: {path}")
        width, height = _probe_image(path)
        item: dict[str, Any] = {
            "index": index,
            "file": _relative_path(path, root),
            "timestamp_seconds": round(timestamp, 6),
            "scroll_progress": scroll_progress,
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        if width is not None and height is not None:
            item["width"] = width
            item["height"] = height
        frames.append(item)
    return {
        "schema": SCHEMA,
        "source_file": source.name,
        "source_sha256": _sha256(source),
        "source_duration_seconds": source_info["duration_seconds"],
        "source_width": source_info["width"],
        "source_height": source_info["height"],
        "sampling": sampling,
        "output": {"format": image_format, "width_limit": width_limit, "quality": quality},
        "frame_count": len(frames),
        "total_bytes": sum(frame["bytes"] for frame in frames),
        "frames": frames,
    }


def _scale_filter(width: int) -> str:
    return f"scale={width}:-2:force_original_aspect_ratio=decrease"


def _quality_options(image_format: str, quality: int) -> list[str]:
    if image_format == "webp":
        return ["-c:v", "libwebp", "-q:v", str(quality)]
    if image_format == "jpg":
        # ffmpeg qscale: 2 is high quality, 31 is low quality.
        qscale = max(2, min(31, round(31 - (quality - 1) * 29 / 99)))
        return ["-q:v", str(qscale)]
    compression = max(0, min(9, round((100 - quality) * 9 / 99)))
    return ["-compression_level", str(compression)]


def _extract_one(
    source: Path,
    destination: Path,
    timestamp: float,
    *,
    width: int,
    image_format: str,
    quality: int,
    verbose: bool,
) -> None:
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        f"{timestamp:.6f}",
        "-i",
        str(source),
        "-frames:v",
        "1",
        "-vf",
        _scale_filter(width),
        *_quality_options(image_format, quality),
        str(destination),
    ]
    try:
        _run(command, verbose=verbose)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "ffmpeg ha rifiutato il frame").strip()
        raise UserError(f"estrazione fallita a {timestamp:.3f}s: {detail}") from exc


def _extract_fps(
    source: Path,
    output_dir: Path,
    *,
    fps: float,
    max_frames: int,
    width: int,
    image_format: str,
    quality: int,
    verbose: bool,
) -> list[Path]:
    pattern = output_dir / f"frame-%05d.{image_format}"
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(source),
        "-vf",
        f"fps={fps:g},{_scale_filter(width)}",
        "-frames:v",
        str(max_frames),
        "-start_number",
        "0",
        *_quality_options(image_format, quality),
        str(pattern),
    ]
    try:
        _run(command, verbose=verbose)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "ffmpeg ha rifiutato il campionamento").strip()
        raise UserError(f"campionamento fps fallito: {detail}") from exc
    return sorted(output_dir.glob(f"frame-*.{image_format}"))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Estrae frame da un video locale con ffmpeg e produce un manifest JSON."
    )
    parser.add_argument("video", type=Path, help="file video locale autorizzato")
    parser.add_argument("--output", required=True, type=Path, help="cartella di output dei frame")
    sampling = parser.add_mutually_exclusive_group(required=True)
    sampling.add_argument("--timestamps", type=Path, help="file con un timestamp in secondi per riga")
    sampling.add_argument("--fps", type=float, help="campionamento uniforme in frame al secondo")
    parser.add_argument("--max-frames", type=int, default=48, help="numero massimo di frame (default: 48)")
    parser.add_argument("--width", type=int, default=1600, help="larghezza massima, senza upscale (default: 1600)")
    parser.add_argument("--format", dest="image_format", choices=("jpg", "webp", "png"), default="webp")
    parser.add_argument("--quality", type=int, default=80, help="qualità da 1 a 100 (default: 80)")
    parser.add_argument("--manifest", type=Path, help="percorso del manifest (default: cartella padre/frame-manifest.json)")
    parser.add_argument("--dry-run", action="store_true", help="produce solo il piano JSON, senza creare frame")
    parser.add_argument("--verbose", action="store_true", help="scrive i comandi ffmpeg su stderr")
    return parser


def _error(message: str, *, status: str = "error") -> dict[str, str]:
    return {"status": status, "error": message}


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if not args.video.is_file():
            raise UserError(f"video non trovato: {args.video}")
        if args.max_frames < 1:
            raise UserError("max-frames deve essere positivo")
        if args.width < 2:
            raise UserError("width deve essere almeno 2")
        if not 1 <= args.quality <= 100:
            raise UserError("quality deve essere fra 1 e 100")
        if shutil.which("ffprobe") is None or shutil.which("ffmpeg") is None:
            raise RuntimeError("capability mancante: servono ffprobe e ffmpeg nel PATH")
        info = probe_video(args.video)
        if args.timestamps:
            timestamps = parse_timestamps(args.timestamps, info["duration_seconds"], args.max_frames)
            sampling = {"mode": "timestamps", "count": len(timestamps)}
        else:
            if args.fps is None:
                raise UserError("specificare timestamps oppure fps")
            timestamps = uniform_timestamps(info["duration_seconds"], args.fps, args.max_frames)
            sampling = {"mode": "fps", "fps": args.fps, "planned_count": len(timestamps)}

        manifest_path = args.manifest or args.output.parent / "frame-manifest.json"
        plan = {
            "status": "dry_run" if args.dry_run else "planned",
            "video": args.video.name,
            "duration_seconds": info["duration_seconds"],
            "source_width": info["width"],
            "source_height": info["height"],
            "sampling": sampling,
            "timestamps": timestamps,
            "output": str(args.output),
            "format": args.image_format,
            "width_limit": args.width,
            "quality": args.quality,
            "manifest": str(manifest_path),
        }
        if args.dry_run:
            print(json.dumps(plan, ensure_ascii=False, indent=2))
            return 0

        args.output.mkdir(parents=True, exist_ok=True)
        if args.timestamps:
            frame_paths: list[Path] = []
            for index, timestamp in enumerate(timestamps):
                destination = args.output / f"frame-{index:05d}.{args.image_format}"
                _extract_one(
                    args.video,
                    destination,
                    timestamp,
                    width=args.width,
                    image_format=args.image_format,
                    quality=args.quality,
                    verbose=args.verbose,
                )
                frame_paths.append(destination)
        else:
            frame_paths = _extract_fps(
                args.video,
                args.output,
                fps=args.fps,
                max_frames=args.max_frames,
                width=args.width,
                image_format=args.image_format,
                quality=args.quality,
                verbose=args.verbose,
            )
            timestamps = [min(index / args.fps, info["duration_seconds"]) for index in range(len(frame_paths))]
            sampling["actual_count"] = len(frame_paths)

        if not frame_paths:
            raise UserError("ffmpeg non ha prodotto frame")
        manifest = build_manifest(
            source=args.video,
            source_info=info,
            frame_paths=frame_paths,
            timestamps=timestamps,
            root=manifest_path.parent,
            sampling=sampling,
            width_limit=args.width,
            image_format=args.image_format,
            quality=args.quality,
        )
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "ok", "manifest": str(manifest_path), **manifest}, ensure_ascii=False, indent=2))
        return 0
    except UserError as exc:
        print(json.dumps(_error(str(exc), status="fail"), ensure_ascii=False), file=sys.stdout)
        return 1
    except (RuntimeError, OSError) as exc:
        print(json.dumps(_error(str(exc)), ensure_ascii=False), file=sys.stdout)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
