#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Genera o modifica un'immagine con Gemini (Nano Banana, Imagen) o OpenAI (GPT Image).

Solo libreria standard: nessuna installazione, nessun SDK che cambia sotto i piedi.
Lo script non conosce quali modelli esistono e non ne inventa: il modello è sempre un
argomento esplicito, così un rinomino a monte non lo rende bugiardo.

Chiavi lette dall'ambiente, mai dagli argomenti (finirebbero nella cronologia della shell):
`GEMINI_API_KEY` o `GOOGLE_API_KEY` per Gemini, `OPENAI_API_KEY` per OpenAI.

Ogni immagine scritta ha accanto un sidecar `.provenance.json` con provider, modello,
prompt, riferimenti e ora UTC: un file senza provenienza non è riutilizzabile.

Esempi:

    # cosa verrebbe inviato, senza spendere
    uv run generate_image.py --provider gemini --model <modello> \\
        --prompt "..." --out out/scatto.png --dry-run

    # generazione
    uv run generate_image.py --provider openai --model <modello> \\
        --prompt "..." --size 1024x1024 --out out/scatto.png

    # editing con riferimenti (Gemini) o con maschera (OpenAI)
    uv run generate_image.py --provider gemini --model <modello> \\
        --prompt "..." --image rif1.png --image rif2.png --out out/v2.png
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
OPENAI_GENERATION_ENDPOINT = "https://api.openai.com/v1/images/generations"
OPENAI_EDIT_ENDPOINT = "https://api.openai.com/v1/images/edits"

EXTENSION_BY_MIME = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
}


class ImagingError(Exception):
    """Errore d'uso o di risposta: si stampa e si esce, senza traceback."""


# --------------------------------------------------------------------------- #
# Utilità
# --------------------------------------------------------------------------- #


def read_api_key(provider: str) -> str:
    names = ("GEMINI_API_KEY", "GOOGLE_API_KEY") if provider == "gemini" else ("OPENAI_API_KEY",)
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    joined = " o ".join(names)
    raise ImagingError(
        f"chiave API assente: imposta {joined} nell'ambiente. "
        "Non passarla come argomento: finirebbe nella cronologia della shell."
    )


def guess_mime(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    if not mime or not mime.startswith("image/"):
        raise ImagingError(f"{path}: tipo immagine non riconosciuto dall'estensione")
    return mime


def load_reference(path_value: str) -> tuple[Path, str, bytes]:
    path = Path(path_value)
    if not path.is_file():
        raise ImagingError(f"riferimento non trovato: {path}")
    return path, guess_mime(path), path.read_bytes()


def post_json(url: str, payload: dict, headers: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    for key, value in headers.items():
        request.add_header(key, value)
    return send(request)


def post_multipart(url: str, fields: list[tuple[str, str]], files: list[tuple[str, Path, str, bytes]], headers: dict) -> dict:
    boundary = f"----grl-imaging-{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for name, value in fields:
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        chunks.append(f"{value}\r\n".encode())
    for name, path, mime, data in files:
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(
            f'Content-Disposition: form-data; name="{name}"; filename="{path.name}"\r\n'.encode()
        )
        chunks.append(f"Content-Type: {mime}\r\n\r\n".encode())
        chunks.append(data)
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())

    request = urllib.request.Request(url, data=b"".join(chunks), method="POST")
    request.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    for key, value in headers.items():
        request.add_header(key, value)
    return send(request)


def send(request: urllib.request.Request) -> dict:
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:2000]
        raise ImagingError(f"HTTP {error.code} da {request.full_url}\n{detail}") from error
    except urllib.error.URLError as error:
        raise ImagingError(f"rete non raggiungibile: {error.reason}") from error
    except json.JSONDecodeError as error:
        raise ImagingError(f"risposta non JSON da {request.full_url}") from error


# --------------------------------------------------------------------------- #
# Costruzione della richiesta
# --------------------------------------------------------------------------- #


def build_gemini(args, references: list[tuple[Path, str, bytes]]) -> tuple[str, dict, dict]:
    parts: list[dict] = [{"text": args.prompt}]
    for _, mime, data in references:
        parts.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(data).decode()}})

    payload: dict = {"contents": [{"parts": parts}]}
    if args.config_json:
        payload["generationConfig"] = json.loads(args.config_json)

    url = GEMINI_ENDPOINT.format(model=args.model)
    return url, payload, {}


def build_openai(args, references: list[tuple[Path, str, bytes]]) -> tuple[str, dict | None, list, list]:
    if references or args.mask:
        fields = [("model", args.model), ("prompt", args.prompt), ("n", str(args.count))]
        if args.size:
            fields.append(("size", args.size))
        files = [("image[]", path, mime, data) for path, mime, data in references]
        if args.mask:
            mask_path, mask_mime, mask_data = load_reference(args.mask)
            files.append(("mask", mask_path, mask_mime, mask_data))
        return OPENAI_EDIT_ENDPOINT, None, fields, files

    payload: dict = {"model": args.model, "prompt": args.prompt, "n": args.count}
    if args.size:
        payload["size"] = args.size
    if args.config_json:
        payload.update(json.loads(args.config_json))
    return OPENAI_GENERATION_ENDPOINT, payload, [], []


# --------------------------------------------------------------------------- #
# Lettura della risposta
# --------------------------------------------------------------------------- #


def extract_gemini(response: dict) -> list[tuple[bytes, str]]:
    images: list[tuple[bytes, str]] = []
    for candidate in response.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            blob = part.get("inlineData") or part.get("inline_data")
            if not blob:
                continue
            data = blob.get("data")
            if data:
                mime = blob.get("mimeType") or blob.get("mime_type") or "image/png"
                images.append((base64.b64decode(data), mime))
    if not images:
        raise ImagingError(
            "la risposta non contiene immagini. Cause tipiche: il modello indicato non produce "
            "immagini, oppure la configurazione delle modalità di risposta non le richiede "
            "(vedi --config-json). Risposta:\n"
            + json.dumps(response, ensure_ascii=False)[:1500]
        )
    return images


def extract_openai(response: dict) -> list[tuple[bytes, str]]:
    images: list[tuple[bytes, str]] = []
    for item in response.get("data", []):
        encoded = item.get("b64_json")
        if encoded:
            images.append((base64.b64decode(encoded), "image/png"))
        elif item.get("url"):
            raise ImagingError(
                "la risposta contiene un URL invece dei byte dell'immagine: scarica il file a "
                "parte oppure richiedi l'output codificato."
            )
    if not images:
        raise ImagingError(
            "la risposta non contiene immagini:\n" + json.dumps(response, ensure_ascii=False)[:1500]
        )
    return images


# --------------------------------------------------------------------------- #
# Scrittura
# --------------------------------------------------------------------------- #


def destination(base: Path, index: int, total: int, mime: str) -> Path:
    suffix = base.suffix or EXTENSION_BY_MIME.get(mime, ".png")
    stem = base.stem if base.suffix else base.name
    name = stem if total == 1 else f"{stem}-{index + 1}"
    return base.parent / f"{name}{suffix}"


def write_outputs(args, images: list[tuple[bytes, str]], references: list) -> list[Path]:
    base = Path(args.out)
    base.parent.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for index, (data, mime) in enumerate(images):
        path = destination(base, index, len(images), mime)
        if path.exists() and not args.overwrite:
            raise ImagingError(f"{path} esiste già: usa --overwrite per sostituirlo")
        path.write_bytes(data)
        provenance = {
            "provider": args.provider,
            "model": args.model,
            "prompt": args.prompt,
            "references": [str(p) for p, _, _ in references],
            "mask": args.mask,
            "size": args.size,
            "config_json": args.config_json,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "note": "immagine generata da un modello; verificare i marcatori di provenienza del fornitore prima della pubblicazione",
        }
        sidecar = path.with_suffix(path.suffix + ".provenance.json")
        sidecar.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(path)
    return written


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera o modifica un'immagine con Gemini o OpenAI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--provider", required=True, choices=("gemini", "openai"))
    parser.add_argument("--model", required=True, help="identificativo del modello, verificato sulla documentazione del fornitore")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--out", required=True, help="percorso del file da scrivere; con più immagini diventa nome-1, nome-2")
    parser.add_argument("--image", action="append", default=[], metavar="PATH", help="immagine di riferimento o da modificare, ripetibile")
    parser.add_argument("--mask", metavar="PATH", help="maschera per l'editing di un'area (solo openai)")
    parser.add_argument("--size", help="dimensione richiesta, nel formato accettato dal fornitore (solo openai)")
    parser.add_argument("--count", type=int, default=1, help="numero di immagini (default 1)")
    parser.add_argument("--config-json", help="configurazione grezza aggiuntiva in JSON, passata al fornitore così com'è")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="stampa la richiesta senza inviarla e senza spendere")
    args = parser.parse_args(argv)

    if args.mask and args.provider != "openai":
        parser.error("--mask è supportata solo con --provider openai")
    if args.count < 1:
        parser.error("--count deve essere almeno 1")
    return args


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        references = [load_reference(value) for value in args.image]

        if args.provider == "gemini":
            url, payload, extra_headers = build_gemini(args, references)
            fields: list = []
            files: list = []
        else:
            url, payload, fields, files = build_openai(args, references)
            extra_headers = {}

        if args.dry_run:
            summary = {
                "endpoint": url,
                "provider": args.provider,
                "model": args.model,
                "prompt": args.prompt,
                "references": [str(p) for p, _, _ in references],
                "mask": args.mask,
                "count": args.count,
                "size": args.size,
                "out": args.out,
                "sent": False,
            }
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0

        api_key = read_api_key(args.provider)
        if args.provider == "gemini":
            headers = {"x-goog-api-key": api_key, **extra_headers}
            response = post_json(url, payload, headers)
            images = extract_gemini(response)
        else:
            headers = {"Authorization": f"Bearer {api_key}"}
            if payload is not None:
                response = post_json(url, payload, headers)
            else:
                response = post_multipart(url, fields, files, headers)
            images = extract_openai(response)

        written = write_outputs(args, images, references)
        print(json.dumps({"written": [str(p) for p in written], "sent": True}, ensure_ascii=False, indent=2))
        return 0
    except ImagingError as error:
        print(f"errore: {error}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as error:
        print(f"errore: --config-json non è JSON valido ({error})", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
