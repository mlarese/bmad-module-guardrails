#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Verifica meccanica di un mockup a file singolo di grl-web.

Constata presenze, non giudica significati: dice che manca `alt`, non se l'alt
descrive bene l'immagine; trova «lorem ipsum», non se una testimonianza e'
inventata. Quel giudizio resta al modello, che e' l'unico a sapere quali
contenuti l'utente ha davvero fornito nel brief.

Due famiglie di violazioni:
  network      il file dipende dalla rete e non si apre offline
  placeholder  marcatori segnaposto letterali rimasti nella consegna

Uscita: JSON su stdout. Exit 0 = pulito, 1 = violazioni, 2 = errore d'uso.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# Uno schema remoto: http:, https:, o l'URL protocol-relative //host/path.
REMOTE = re.compile(r"""^\s*(?:https?:)?//""", re.IGNORECASE)
WHITESPACE = re.compile(r"\s+")

# Marcatori segnaposto, cercati SOLO nel testo che un visitatore legge: nodi di
# testo fuori da <style>/<script> e il pugno di attributi visibili. Mai sul
# markup, mai dentro un data: URI — «placeholder» come nome di attributo o
# pseudo-elemento CSS non significa «contenuto segnaposto», e in un font in
# base64 da 40 KB «tbd» e «todo» compaiono per puro caso.
#
# TODO/TBD si cercano nella forma che un marcatore vero ha davvero — maiuscolo,
# oppure delimitato da `:` `[]` `{}` `<>` — non come sequenza di lettere: la
# pagina segue la lingua del destinatario, e in spagnolo «todo» e' fra le parole
# piu' comuni. Si perde un «tbd» minuscolo e isolato, ed e' il verso giusto in
# cui sbagliare per un controllo che blocca la consegna.
#
# Un «VER TODO» spagnolo tutto maiuscolo resta una violazione, e va bene cosi':
# il referto porta il contesto attorno al match, quindi si liquida leggendo il
# JSON. Provare a indovinarlo con un'euristica sulle maiuscole sopprimeva
# marcatori veri («TODO scrivere la CTA finale»), ed era la stessa esenzione
# impossibile da chiudere delle ragioni sociali.
UPPER = re.compile(r"(?<![\w-])(TODO|TBD)(?![\w-])")
DELIMITED = re.compile(r"[\[{<]\s*(todo|tbd)\s*[\]}>]|(?<![\w-])(todo|tbd)\s*:", re.IGNORECASE)
# Solo token che non possono essere prosa in nessuna lingua. Le ragioni sociali
# da template («Nome azienda», «tuo prodotto») sono state tolte: erano sintagmi
# ordinari, e nessuna lista di esenzioni poteva contenerli. Quel giudizio resta
# al modello, che ha appena scritto il footer e sa cosa l'utente gli ha dato.
PLACEHOLDER_TOKENS = (UPPER, DELIMITED, re.compile(r"lorem\s+ipsum", re.IGNORECASE))

# Attributi il cui valore l'utente legge davvero. `placeholder` sta qui come
# VALORE (il testo grigio dentro un campo), non come nome.
VISIBLE_ATTRS = ("alt", "title", "aria-label", "placeholder", "value", "content")
# Un valore che e' un riferimento tecnico, non prosa: `content` di og:url ospita
# URL, dove «/todo» cadrebbe fra confini non-parola.
TECHNICAL_VALUE = re.compile(r"^\s*(https?:)?//|^\s*(data:|mailto:|tel:|#)", re.IGNORECASE)
PLACEHOLDER_HOSTS = (
    "via.placeholder.com",
    "placehold.co",
    "placehold.it",
    "picsum.photos",
    "placekitten.com",
    "dummyimage.com",
)

# Risorse remote dentro il CSS: url(...), @import, @font-face src.
CSS_URL = re.compile(r"""url\(\s*['"]?([^'")]+)['"]?\s*\)""", re.IGNORECASE)
CSS_IMPORT = re.compile(r"""@import\s+(?:url\(\s*)?['"]([^'"]+)['"]""", re.IGNORECASE)

# Chiamate di rete da JavaScript.
NET_CALLS = (
    ("fetch(", "chiamata fetch()"),
    ("XMLHttpRequest", "uso di XMLHttpRequest"),
    ("navigator.sendBeacon", "chiamata navigator.sendBeacon()"),
    ("EventSource(", "apertura di EventSource"),
    ("new WebSocket", "apertura di WebSocket"),
)

TAILWIND_CDN = "cdn.tailwindcss.com"


def is_remote(value: str) -> bool:
    """True se il riferimento esce dal file (esclude data:, blob: e le ancore)."""
    if not value:
        return False
    return bool(REMOTE.match(value))


class MockupParser(HTMLParser):
    """Raccoglie gli attributi che possono puntare fuori dal file."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.violations: list[dict] = []
        self._style_depth = 0
        self._script_depth = 0
        self.style_blocks: list[tuple[int, str]] = []
        self.script_blocks: list[tuple[int, str]] = []
        self.has_inline_style = False
        # Solo cio' che un visitatore legge: nodi di testo e attributi visibili.
        self.visible: list[tuple[int, str]] = []
        # Ogni riferimento che punta a una risorsa, per la caccia agli host.
        self.urls: list[tuple[int, str]] = []

    def _add(self, kind: str, detail: str) -> None:
        self.violations.append(
            {"family": "network", "kind": kind, "line": self.getpos()[0], "detail": detail}
        )

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        line = self.getpos()[0]

        for name in VISIBLE_ATTRS:
            value = a.get(name)
            if value and not TECHNICAL_VALUE.match(value):
                self.visible.append((line, value))
        for name in ("href", "src", "poster", "srcset", "data", "action"):
            if a.get(name):
                self.urls.append((line, a[name]))

        if tag == "style":
            self._style_depth += 1
            self.has_inline_style = True
        elif tag == "script":
            self._script_depth += 1

        if tag == "link":
            href = a.get("href", "")
            rel = a.get("rel", "").lower()
            if is_remote(href):
                self._add("link-remoto", f"<link rel=\"{rel}\"> punta a {href}")
        elif tag == "script" and is_remote(a.get("src", "")):
            self._add("script-remoto", f"<script src> punta a {a['src']}")
        elif tag == "iframe" and is_remote(a.get("src", "")):
            self._add("iframe-remoto", f"<iframe src> punta a {a['src']}")
        elif tag in ("img", "source", "video", "audio", "embed", "track"):
            for attr in ("src", "poster"):
                if is_remote(a.get(attr, "")):
                    self._add("media-remoto", f"<{tag} {attr}> punta a {a[attr]}")
            for candidate in a.get("srcset", "").split(","):
                url = candidate.strip().split(" ")[0]
                if is_remote(url):
                    self._add("media-remoto", f"<{tag} srcset> contiene {url}")

        inline_style = a.get("style", "")
        if inline_style:
            for url in CSS_URL.findall(inline_style):
                if is_remote(url):
                    self._add("css-remoto", f"style inline su <{tag}> carica {url}")

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self._style_depth = max(0, self._style_depth - 1)
        elif tag == "script":
            self._script_depth = max(0, self._script_depth - 1)

    def handle_data(self, data: str) -> None:
        if self._style_depth:
            self.style_blocks.append((self.getpos()[0], data))
        elif self._script_depth:
            self.script_blocks.append((self.getpos()[0], data))
        elif data.strip():
            self.visible.append((self.getpos()[0], data))


def scan_css(blocks: list[tuple[int, str]]) -> list[dict]:
    out = []
    for line, block in blocks:
        for url in CSS_URL.findall(block):
            if is_remote(url):
                out.append(
                    {"family": "network", "kind": "css-remoto", "line": line,
                     "detail": f"url() nel CSS carica {url}"}
                )
        for url in CSS_IMPORT.findall(block):
            if is_remote(url):
                out.append(
                    {"family": "network", "kind": "css-import-remoto", "line": line,
                     "detail": f"@import nel CSS carica {url}"}
                )
    return out


def scan_scripts(blocks: list[tuple[int, str]]) -> list[dict]:
    out = []
    for line, block in blocks:
        for needle, label in NET_CALLS:
            if needle in block:
                out.append(
                    {"family": "network", "kind": "chiamata-di-rete", "line": line,
                     "detail": f"{label} nel JavaScript inline"}
                )
    return out


def contesto(chunk: str, inizio: int, fine: int, ampiezza: int = 30) -> str:
    """Il tratto di testo attorno al match, cosi' un falso positivo si liquida
    leggendo il JSON invece di riaprire il file."""
    a, b = max(0, inizio - ampiezza), min(len(chunk), fine + ampiezza)
    frammento = WHITESPACE.sub(" ", chunk[a:b]).strip()
    return ("…" if a > 0 else "") + frammento + ("…" if b < len(chunk) else "")


def scan_visible(chunks: list[tuple[int, str]]) -> list[dict]:
    """Marcatori segnaposto nel solo testo che il visitatore legge."""
    out = []
    for line, chunk in chunks:
        # Piu' pattern possono coprire lo stesso marcatore (`TODO` e `TODO:`):
        # si tiene una violazione sola per tratto di testo.
        visti: list[tuple[int, int]] = []
        for pattern in PLACEHOLDER_TOKENS:
            for m in pattern.finditer(chunk):
                if any(m.start() < fine and inizio < m.end() for inizio, fine in visti):
                    continue
                visti.append((m.start(), m.end()))
                out.append(
                    {"family": "placeholder", "kind": "marcatore-segnaposto", "line": line,
                     "detail": f"marcatore «{m.group(0).strip()}» in: {contesto(chunk, m.start(), m.end())}"}
                )
    return out


def scan_urls(urls: list[tuple[int, str]]) -> list[dict]:
    """Servizi di immagini segnaposto e Tailwind da CDN, dai soli riferimenti."""
    out = []
    for line, url in urls:
        low = url.lower()
        for host in PLACEHOLDER_HOSTS:
            if host in low:
                out.append(
                    {"family": "placeholder", "kind": "immagine-segnaposto", "line": line,
                     "detail": f"servizio di immagini segnaposto {host}"}
                )
        if TAILWIND_CDN in low:
            out.append(
                {"family": "network", "kind": "tailwind-cdn", "line": line,
                 "detail": "Tailwind caricato da CDN: escluso dai mockup e dalla produzione"}
            )
    return out


def check(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    parser = MockupParser()
    parser.feed(text)
    parser.close()

    violations = (
        parser.violations
        + scan_css(parser.style_blocks)
        + scan_scripts(parser.script_blocks)
        + scan_visible(parser.visible)
        + scan_urls(parser.urls)
    )

    # Deduplica: la stessa violazione puo' emergere dal parser e dalla scansione testuale.
    seen, unique = set(), []
    for v in violations:
        key = (v["kind"], v["line"], v["detail"])
        if key not in seen:
            seen.add(key)
            unique.append(v)
    unique.sort(key=lambda v: (v["line"], v["kind"]))

    counts: dict[str, int] = {}
    for v in unique:
        counts[v["family"]] = counts.get(v["family"], 0) + 1

    return {
        "file": str(path),
        "ok": not unique,
        "has_inline_style": parser.has_inline_style,
        "counts": counts,
        "violations": unique,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Verifica il vincolo del file singolo di un mockup grl-web."
    )
    ap.add_argument("file", type=Path, help="il file .html da verificare")
    ap.add_argument("-o", "--output", type=Path, help="scrive il JSON su file invece che su stdout")
    args = ap.parse_args(argv)

    if not args.file.is_file():
        print(f"file non trovato: {args.file}", file=sys.stderr)
        return 2

    report = check(args.file)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
