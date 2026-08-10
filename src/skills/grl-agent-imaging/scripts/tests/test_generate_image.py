#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest"]
# ///
"""Test di generate_image.py.

Nessun test esegue una chiamata di rete: si verificano la costruzione della richiesta,
la lettura della risposta, la scrittura dei file e i rifiuti che proteggono la spesa.
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generate_image import (  # noqa: E402
    ImagingError,
    build_gemini,
    build_openai,
    destination,
    extract_gemini,
    extract_openai,
    main,
    parse_args,
    read_api_key,
    write_outputs,
)

PIXEL = b"\x89PNG\r\n\x1a\n-finto-"


def png(tmp_path: Path, name: str = "rif.png") -> Path:
    path = tmp_path / name
    path.write_bytes(PIXEL)
    return path


# --------------------------------------------------------------------------- #
# Argomenti
# --------------------------------------------------------------------------- #


def test_modello_obbligatorio():
    with pytest.raises(SystemExit):
        parse_args(["--provider", "gemini", "--prompt", "x", "--out", "o.png"])


def test_maschera_solo_openai():
    with pytest.raises(SystemExit):
        parse_args(
            ["--provider", "gemini", "--model", "m", "--prompt", "x", "--out", "o.png", "--mask", "m.png"]
        )


def test_count_positivo():
    with pytest.raises(SystemExit):
        parse_args(
            ["--provider", "openai", "--model", "m", "--prompt", "x", "--out", "o.png", "--count", "0"]
        )


# --------------------------------------------------------------------------- #
# Costruzione della richiesta
# --------------------------------------------------------------------------- #


def test_gemini_include_riferimenti_inline(tmp_path: Path):
    args = parse_args(
        [
            "--provider", "gemini", "--model", "un-modello", "--prompt", "una borraccia",
            "--out", str(tmp_path / "o.png"), "--image", str(png(tmp_path)),
        ]
    )
    url, payload, _ = build_gemini(args, [(png(tmp_path), "image/png", PIXEL)])

    assert "un-modello:generateContent" in url
    parts = payload["contents"][0]["parts"]
    assert parts[0]["text"] == "una borraccia"
    assert base64.b64decode(parts[1]["inline_data"]["data"]) == PIXEL


def test_gemini_config_grezza_passa_invariata(tmp_path: Path):
    args = parse_args(
        [
            "--provider", "gemini", "--model", "m", "--prompt", "x", "--out", str(tmp_path / "o.png"),
            "--config-json", '{"responseModalities": ["IMAGE"]}',
        ]
    )
    _, payload, _ = build_gemini(args, [])
    assert payload["generationConfig"] == {"responseModalities": ["IMAGE"]}


def test_openai_senza_riferimenti_usa_generations(tmp_path: Path):
    args = parse_args(
        ["--provider", "openai", "--model", "m", "--prompt", "x", "--out", str(tmp_path / "o.png"), "--size", "1024x1024"]
    )
    url, payload, fields, files = build_openai(args, [])
    assert url.endswith("/images/generations")
    assert payload["size"] == "1024x1024"
    assert not fields and not files


def test_openai_con_maschera_usa_edits(tmp_path: Path):
    mask = png(tmp_path, "mask.png")
    reference = png(tmp_path, "base.png")
    args = parse_args(
        [
            "--provider", "openai", "--model", "m", "--prompt", "x", "--out", str(tmp_path / "o.png"),
            "--image", str(reference), "--mask", str(mask),
        ]
    )
    url, payload, fields, files = build_openai(args, [(reference, "image/png", PIXEL)])
    assert url.endswith("/images/edits")
    assert payload is None
    assert dict(fields)["prompt"] == "x"
    assert [name for name, *_ in files] == ["image[]", "mask"]


# --------------------------------------------------------------------------- #
# Lettura della risposta
# --------------------------------------------------------------------------- #


def test_estrae_immagine_gemini_in_entrambe_le_forme():
    encoded = base64.b64encode(PIXEL).decode()
    response = {
        "candidates": [
            {"content": {"parts": [
                {"text": "ecco"},
                {"inlineData": {"mimeType": "image/png", "data": encoded}},
                {"inline_data": {"mime_type": "image/webp", "data": encoded}},
            ]}}
        ]
    }
    assert extract_gemini(response) == [(PIXEL, "image/png"), (PIXEL, "image/webp")]


def test_gemini_senza_immagini_spiega_la_causa():
    with pytest.raises(ImagingError, match="non contiene immagini"):
        extract_gemini({"candidates": [{"content": {"parts": [{"text": "solo testo"}]}}]})


def test_openai_url_invece_dei_byte_e_un_errore_esplicito():
    with pytest.raises(ImagingError, match="URL invece dei byte"):
        extract_openai({"data": [{"url": "https://esempio/x.png"}]})


# --------------------------------------------------------------------------- #
# Scrittura e provenienza
# --------------------------------------------------------------------------- #


def test_nomi_numerati_solo_con_piu_immagini(tmp_path: Path):
    base = tmp_path / "scatto.png"
    assert destination(base, 0, 1, "image/png").name == "scatto.png"
    assert destination(base, 1, 3, "image/png").name == "scatto-2.png"


def test_estensione_dal_mime_quando_manca(tmp_path: Path):
    assert destination(tmp_path / "scatto", 0, 1, "image/webp").name == "scatto.webp"


def test_scrive_file_e_sidecar_di_provenienza(tmp_path: Path):
    out = tmp_path / "out" / "scatto.png"
    args = parse_args(["--provider", "gemini", "--model", "un-modello", "--prompt", "una borraccia", "--out", str(out)])
    written = write_outputs(args, [(PIXEL, "image/png")], [])

    assert written == [out]
    assert out.read_bytes() == PIXEL
    provenance = json.loads((tmp_path / "out" / "scatto.png.provenance.json").read_text())
    assert provenance["model"] == "un-modello"
    assert provenance["prompt"] == "una borraccia"
    assert provenance["generated_at_utc"].endswith("+00:00")


def test_non_sovrascrive_senza_flag(tmp_path: Path):
    out = png(tmp_path, "scatto.png")
    args = parse_args(["--provider", "gemini", "--model", "m", "--prompt", "x", "--out", str(out)])
    with pytest.raises(ImagingError, match="esiste già"):
        write_outputs(args, [(PIXEL, "image/png")], [])


# --------------------------------------------------------------------------- #
# Chiave e dry-run
# --------------------------------------------------------------------------- #


def test_chiave_assente_dice_quale_variabile(monkeypatch):
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(ImagingError, match="GEMINI_API_KEY"):
        read_api_key("gemini")


def test_dry_run_non_richiede_chiave_e_non_scrive(tmp_path, monkeypatch, capsys):
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    out = tmp_path / "scatto.png"

    code = main(["--provider", "gemini", "--model", "m", "--prompt", "x", "--out", str(out), "--dry-run"])

    assert code == 0
    assert not out.exists()
    assert json.loads(capsys.readouterr().out)["sent"] is False
