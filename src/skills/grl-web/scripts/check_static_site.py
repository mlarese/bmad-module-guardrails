#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Referto di presenza sulle pagine di un sito statico grl-web.

Constata presenze, mai significati. Dice che manca `alt`, non se l'alt descrive
la funzione dell'immagine; dice che manca `<title>`, non se il titolo dice cosa
c'e' in quella pagina; riporta quali immagini hanno `loading=lazy`, non quali
avrebbero dovuto averlo — dove stia la piega lo decide il modello.

Pensato come pre-pass: il modello ragiona sul referto compatto invece di
rileggersi tutte le pagine.

Uscita: JSON su stdout. Exit 0 = nessuna mancanza, 1 = mancanze, 2 = errore d'uso.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

OG_ATTESA = (1200, 630)          # larghezza minima e rapporto di riferimento
OG_TOLLERANZA = 0.05             # scarto ammesso sul rapporto d'aspetto


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title_present = False
        self._in_title = False
        self.title_text = ""
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.images: list[dict] = []
        self.inputs: list[dict] = []
        self.labels_for: set[str] = set()
        self.landmarks: set[str] = set()
        self._label_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self.title_present = True
            self._in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and "canonical" in a.get("rel", "").lower():
            self.canonical = a.get("href", "")
        elif tag == "img":
            self.images.append({
                "src": a.get("src", ""),
                "has_alt": "alt" in a,
                "has_dimensions": "width" in a and "height" in a,
                "lazy": a.get("loading", "").lower() == "lazy",
            })
        elif tag in ("input", "textarea", "select"):
            if a.get("type", "").lower() not in ("hidden", "submit", "button", "reset", "image"):
                self.inputs.append({
                    "id": a.get("id", ""),
                    "name": a.get("name", ""),
                    "tag": tag,
                    "has_aria_label": bool(a.get("aria-label") or a.get("aria-labelledby")),
                    # <label>Email <input></label> etichetta senza bisogno di for/id.
                    "wrapped": self._label_depth > 0,
                })
        elif tag == "label":
            self._label_depth += 1
            if a.get("for"):
                self.labels_for.add(a["for"])
        elif tag in ("main", "nav", "header", "footer"):
            self.landmarks.add(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "label":
            self._label_depth = max(0, self._label_depth - 1)

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_text += data


def image_size(path: Path) -> tuple[int, int] | None:
    """Dimensioni di un PNG o JPEG leggendone l'header. None se illeggibile."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        w, h = struct.unpack(">II", data[16:24])
        return int(w), int(h)
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return int(w), int(h)
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            (seg,) = struct.unpack(">H", data[i + 2:i + 4])
            i += 2 + seg
    return None


def check_page(path: Path, root: Path | None = None) -> dict:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    parser.close()

    missing: list[str] = []
    if not parser.lang:
        missing.append("attributo lang su <html>")
    if not parser.title_present or not parser.title_text.strip():
        missing.append("<title> non vuoto")
    if not parser.meta.get("description", "").strip():
        missing.append("meta description")
    if not parser.canonical:
        missing.append("link rel=canonical")
    for prop in ("og:title", "og:description", "og:image"):
        if not parser.meta.get(prop, "").strip():
            missing.append(f"meta {prop}")

    senza_alt = [i["src"] or "(senza src)" for i in parser.images if not i["has_alt"]]
    senza_dim = [i["src"] or "(senza src)" for i in parser.images if not i["has_dimensions"]]
    if senza_alt:
        missing.append(f"attributo alt su {len(senza_alt)} immagini")
    if senza_dim:
        missing.append(f"width/height su {len(senza_dim)} immagini")

    campi_scoperti = [
        c["id"] or c["name"] or f"<{c['tag']}> #{n}"
        for n, c in enumerate(parser.inputs, start=1)
        if not c["has_aria_label"]
        and not c["wrapped"]
        and (not c["id"] or c["id"] not in parser.labels_for)
    ]
    if campi_scoperti:
        missing.append(f"label o aria-label su {len(campi_scoperti)} campi")

    if "main" not in parser.landmarks:
        missing.append("elemento <main>")

    # Identita' = percorso relativo alla radice: due `index.html` in cartelle
    # diverse sono il layout standard degli URL puliti, e col solo nome del file
    # il referto non direbbe di quale pagina sta parlando.
    if root is not None:
        identita = str(path.relative_to(root)).replace("\\", "/")
    else:
        identita = path.name

    return {
        "file": identita,
        "ok": not missing,
        "missing": missing,
        "og_image": parser.meta.get("og:image", ""),
        "immagini": {
            "totali": len(parser.images),
            "senza_alt": senza_alt,
            "senza_dimensioni": senza_dim,
            # Quali stiano sotto la piega lo decide il modello, non lo script.
            "con_lazy": [i["src"] for i in parser.images if i["lazy"]],
        },
        "campi_senza_etichetta": campi_scoperti,
        "landmark": sorted(parser.landmarks),
    }


def check_site(root: Path) -> dict:
    # Risolvere PRIMA di raccogliere: relative_to() confronta percorsi risolti.
    root = root.resolve()
    pages = sorted(p for p in root.rglob("*.html") if p.is_file())
    if not pages:
        return {"root": str(root), "ok": False, "errore": "nessun file .html trovato", "pagine": []}

    reports = [check_page(p, root) for p in pages]

    site_missing = []
    for name in ("sitemap.xml", "robots.txt"):
        if not any(root.rglob(name)):
            site_missing.append(name)

    # L'immagine Open Graph ha un rapporto d'aspetto atteso: verificabile.
    og_problemi = []
    for page, r in zip(pages, reports):
        ref = r["og_image"]
        if not ref:
            continue
        parti = urlsplit(ref)
        # Remoto: stesso concetto e stessa insensibilita' alle maiuscole del
        # gemello check_mockup.py, invece di uno startswith letterale.
        if parti.scheme.lower() in ("http", "https", "data") or parti.netloc:
            continue
        # Un URL non e' un percorso: la query di cache-busting, il frammento e
        # le sequenze percent vanno tolti prima di toccare il disco.
        percorso = unquote(parti.path)
        if not percorso:
            og_problemi.append({"file": r["file"], "og_image": ref,
                                "problema": "og:image senza percorso"})
            continue
        # Un riferimento che inizia con `/` e' assoluto rispetto alla radice del
        # sito; ogni altro e' relativo alla PAGINA, non alla radice.
        if percorso.startswith("/"):
            candidate = (root / percorso.lstrip("/")).resolve()
        else:
            candidate = (page.parent / percorso).resolve()
        # Un `../` di troppo puo' uscire dall'albero: fuori non si legge.
        dentro = candidate == root or root in candidate.parents
        size = image_size(candidate) if dentro and candidate.is_file() else None
        if size is None:
            og_problemi.append({"file": r["file"], "og_image": ref, "problema": "non trovata o illeggibile"})
            continue
        # Il fatto verificabile e' il rapporto d'aspetto e la larghezza minima,
        # non l'uguaglianza esatta: 2400×1260 e' il taglio 2x della stessa
        # immagine e va benissimo. Le dimensioni lette restano nel referto, cosi'
        # un caso limite lo decide il modello.
        w, h = size
        ratio = w / h if h else 0
        atteso = OG_ATTESA[0] / OG_ATTESA[1]
        if abs(ratio - atteso) > OG_TOLLERANZA:
            og_problemi.append({
                "file": r["file"], "og_image": ref, "dimensioni": [w, h],
                "problema": f"rapporto {ratio:.2f}:1, atteso {atteso:.2f}:1",
            })
        elif w < OG_ATTESA[0]:
            og_problemi.append({
                "file": r["file"], "og_image": ref, "dimensioni": [w, h],
                "problema": f"larghezza {w}px, minimo {OG_ATTESA[0]}px",
            })

    ok = all(r["ok"] for r in reports) and not site_missing and not og_problemi
    return {
        "root": str(root),
        "ok": ok,
        "pagine_scansionate": len(reports),
        "mancanti_a_livello_di_sito": site_missing,
        "og_image": og_problemi,
        "pagine": reports,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Referto di presenza sulle pagine di un sito statico grl-web."
    )
    ap.add_argument("root", type=Path, help="la cartella che contiene le pagine .html")
    ap.add_argument("-o", "--output", type=Path, help="scrive il JSON su file invece che su stdout")
    args = ap.parse_args(argv)

    if not args.root.is_dir():
        print(f"cartella non trovata: {args.root}", file=sys.stderr)
        return 2

    report = check_site(args.root)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
