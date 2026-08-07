#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Confronta il sistema visivo fra le pagine di un mockup multipagina.

Nel modo mockup ogni pagina e' un file autosufficiente, quindi il CSS condiviso
e' duplicato in ciascuno. Il difetto che ne nasce — un sito che sembra fatto da
tre persone che non si parlano — e' una divergenza fra N copie: confronto puro,
stesso input stesso esito.

Lo script constata la divergenza; se sia voluta lo decide il modello. Una pagina
legale puo' legittimamente non avere il CSS dell'hero, e due tonalita' vicine
possono essere una scelta.

Uscita: JSON su stdout. Exit 0 = nessuna divergenza, 1 = divergenze, 2 = errore.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# Nome E valore: due pagine che danno valori diversi allo stesso token sono il
# difetto piu' azionabile che questo script possa nominare.
CUSTOM_PROP = re.compile(r"(--[a-zA-Z][\w-]*)\s*:\s*([^;}]+)", re.IGNORECASE)
FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;}]+)", re.IGNORECASE)
# I colori non si dichiarano solo in esadecimale: rgb(), hsl() e oklch() sono
# ordinari, e leggere solo #hex fa passare per identiche due palette opposte.
HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
COLOR_FN = re.compile(
    r"(?<![\w-])(rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|color-mix)\s*\(", re.IGNORECASE
)
# I colori si cercano nei soli valori di dichiarazione: `#feed { padding: 0 }`
# e' un selettore d'id, non un colore della palette.
DECLARATION = re.compile(r":\s*([^;{}]*)")
# Un data: URI (font o SVG in base64) non e' stile: va escluso prima di
# normalizzare. Si legge a parentesi bilanciate, non con [^)]*, se no un SVG
# che contiene «translate(1,2)» lascia i propri colori dentro il profilo.
URL_OPEN = re.compile(r"url\s*\(", re.IGNORECASE)
# I commenti non sono stile: un commento di palette su una pagina sola
# inventerebbe una divergenza fra pagine identiche, e un valore commentato
# verrebbe riportato come quello vero.
COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
WHITESPACE = re.compile(r"\s+")


class StyleCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._depth = 0
        self.css: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if tag == "style":
            self._depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self._depth = max(0, self._depth - 1)

    def handle_data(self, data: str) -> None:
        if self._depth:
            self.css.append(data)


def chiusura(text: str, start: int) -> int | None:
    """Indice subito dopo la parentesi che chiude quella aperta prima di start.
    None se non si chiude."""
    i, livello = start, 1
    while i < len(text) and livello:
        if text[i] == "(":
            livello += 1
        elif text[i] == ")":
            livello -= 1
        i += 1
    return i if not livello else None


def strip_data_uris(css: str) -> str:
    """Sostituisce ogni url(data:...) con un segnaposto. Se il contenuto e'
    quotato si va alla quota di chiusura, altrimenti a parentesi bilanciate."""
    pezzi, i = [], 0
    for m in URL_OPEN.finditer(css):
        if m.start() < i:
            continue
        j = m.end()
        while j < len(css) and css[j].isspace():
            j += 1
        if j < len(css) and css[j] in "\"'":
            fine_quota = css.find(css[j], j + 1)
            if fine_quota < 0:
                continue
            contenuto = css[j + 1:fine_quota]
            paren = css.find(")", fine_quota)
            fine = paren + 1 if paren >= 0 else None
        else:
            fine = chiusura(css, m.end())
            contenuto = css[m.end():fine - 1].strip() if fine else ""
        if fine and contenuto.lower().startswith("data:"):
            pezzi.append(css[i:m.start()])
            pezzi.append("url(data:)")
            i = fine
    pezzi.append(css[i:])
    return "".join(pezzi)


def normalize(css: str) -> str:
    """Toglie data: URI e commenti, poi collassa gli spazi: l'hash confronta lo
    stile, non i byte. L'ordine conta — un url(data:...) non codificato
    potrebbe ospitare la sequenza di apertura di un commento."""
    return WHITESPACE.sub(" ", COMMENT.sub(" ", strip_data_uris(css))).strip()


def clean(value: str) -> str:
    return WHITESPACE.sub(" ", value).strip().lower()


def find_colors(css: str) -> list[str]:
    """Esadecimali piu' forme funzionali, cercati nei soli valori di
    dichiarazione e letti a parentesi bilanciate: `[^)]*` troncherebbe
    `color-mix(in oklch, var(--a), var(--b))` dove i due colori si distinguono."""
    out = []
    for d in DECLARATION.finditer(css):
        valore = d.group(1)
        out.extend(m.group(0) for m in HEX_COLOR.finditer(valore))
        for m in COLOR_FN.finditer(valore):
            fine = chiusura(valore, m.end())
            if fine:  # parentesi chiuse: la dichiarazione e' completa
                out.append(valore[m.start():fine])
    return out


def profile(path: Path, root: Path | None = None) -> dict:
    parser = StyleCollector()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    parser.close()
    css = normalize("\n".join(parser.css))
    props = {name: clean(value) for name, value in CUSTOM_PROP.findall(css)}
    colors = sorted({clean(c) for c in find_colors(css)})
    fonts = sorted({clean(f) for f in FONT_FAMILY.findall(css)})
    # Identita' = percorso relativo alla radice comune: due `index.html` in
    # cartelle diverse sono il layout standard degli URL puliti, e col solo nome
    # del file i due profili collassano su una chiave sola — la divergenza di
    # valore, che e' il dato piu' utile di questo script, non scatterebbe mai.
    try:
        nome = str(path.relative_to(root)).replace("\\", "/") if root else path.name
    except ValueError:
        nome = path.name

    return {
        "file": nome,
        "style_hash": hashlib.sha256(css.encode("utf-8")).hexdigest()[:12],
        "custom_properties": props,
        "font_families": fonts,
        "colors": colors,
        # Senza questo, un profilo che non ha visto niente e un profilo
        # concorde producono lo stesso «nessuna divergenza».
        "profilo_vuoto": not (props or colors or fonts),
    }


def compare(paths: list[Path], root: Path | None = None) -> dict:
    profiles = [profile(p, root) for p in paths]

    divergenze = []

    # Conflitto di valore: lo stesso token vale due cose diverse. E' il fatto
    # piu' utile che lo script possa produrre.
    nomi: set[str] = set()
    for p in profiles:
        nomi |= set(p["custom_properties"])
    for nome in sorted(nomi):
        valori = {p["file"]: p["custom_properties"][nome]
                  for p in profiles if nome in p["custom_properties"]}
        if len(set(valori.values())) > 1:
            divergenze.append({"campo": "valore_custom_property", "token": nome, "valori": valori})

    # Presenza: chi non ha un token che gli altri hanno.
    for campo in ("custom_properties", "font_families", "colors"):
        unione: set[str] = set()
        for p in profiles:
            unione |= set(p[campo])
        for p in profiles:
            mancanti = sorted(unione - set(p[campo]))
            if mancanti:
                divergenze.append({"campo": campo, "file": p["file"], "non_ha": mancanti})

    vuoti = [p["file"] for p in profiles if p["profilo_vuoto"]]
    hashes = {p["style_hash"] for p in profiles}
    return {
        "pagine": len(profiles),
        # Un profilo vuoto non e' accordo: e' un'estrazione che non ha visto
        # niente, e non deve passare per «coerente».
        "ok": not divergenze and not vuoti,
        "stile_identico": len(hashes) == 1,
        "profili_vuoti": vuoti,
        "profili": profiles,
        "divergenze": divergenze,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Confronta il sistema visivo fra le pagine di un mockup multipagina."
    )
    ap.add_argument("paths", nargs="+", type=Path, metavar="FILE_O_CARTELLA")
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args(argv)

    files: list[Path] = []
    cartelle: list[Path] = []
    for p in args.paths:
        if p.is_dir():
            cartelle.append(p.resolve())
            files.extend(sorted(p.rglob("*.html")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"percorso non trovato: {p}", file=sys.stderr)
            return 2

    if len(files) < 2:
        print("servono almeno due pagine da confrontare", file=sys.stderr)
        return 2

    # La radice su cui si calcola l'identita' delle pagine: la cartella passata
    # se ce n'e' una sola, altrimenti l'antenato comune dei file raccolti.
    risolti = [f.resolve() for f in files]
    if len(cartelle) == 1 and not any(f.is_file() for f in args.paths):
        radice = cartelle[0]
    else:
        radice = Path(os.path.commonpath([str(f.parent) for f in risolti]))

    report = compare(risolti, radice)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
