#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Rapporti di contrasto WCAG per la palette dichiarata.

Il rapporto di contrasto e' una funzione chiusa della luminanza relativa di due
colori: stesso input, stesso numero, sempre. Il modello lo stima male, e qui lo
stimerebbe su valori che ha scelto lui.

Si applica alla palette che Iris consegna come direzione visiva, non al CSS
arbitrario: estrarre le coppie testo/sfondo effettive dipende dalla cascata e
non e' deterministico in modo affidabile.

Le soglie sono un dato di fatto (4.5:1 per il testo normale, 3:1 per il testo
grande e i componenti). QUALE livello sia obbligatorio lo dice
grl-agent-compliance; cosa fare di una coppia al limite resta giudizio.

Uscita: JSON su stdout. Exit 0 = tutte le coppie passano, 1 = almeno una sotto
soglia, 2 = errore d'uso.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

HEX = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

SOGLIA_TESTO = 4.5
SOGLIA_GRANDE = 3.0


def parse_hex(value: str) -> tuple[int, int, int]:
    """'#1a2b3c' o '#abc' -> (r, g, b). Solleva ValueError su input non valido."""
    m = HEX.match(value.strip())
    if not m:
        raise ValueError(f"colore non valido: {value!r} (atteso #rgb o #rrggbb)")
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Luminanza relativa secondo la definizione WCAG 2."""
    channels = []
    for c in rgb:
        s = c / 255
        channels.append(s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str) -> float:
    """Rapporto di contrasto fra due colori esadecimali, da 1.0 a 21.0."""
    l1 = relative_luminance(parse_hex(fg))
    l2 = relative_luminance(parse_hex(bg))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def evaluate(fg: str, bg: str) -> dict:
    ratio = contrast_ratio(fg, bg)
    return {
        "fg": fg,
        "bg": bg,
        "ratio": round(ratio, 2),
        "testo_normale": ratio >= SOGLIA_TESTO,
        "testo_grande": ratio >= SOGLIA_GRANDE,
        "verdetto": (
            "passa" if ratio >= SOGLIA_TESTO
            else "solo testo grande" if ratio >= SOGLIA_GRANDE
            else "sotto soglia"
        ),
    }


def split_pair(raw: str) -> tuple[str, str]:
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) != 2:
        raise ValueError(f"coppia non valida: {raw!r} (atteso '#fg,#bg')")
    return parts[0], parts[1]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Rapporti di contrasto WCAG per le coppie della palette dichiarata."
    )
    ap.add_argument(
        "pair", nargs="+", metavar="FG,BG",
        help="una o piu' coppie colore-testo/colore-sfondo, es. '#1a1a1a,#ffffff'",
    )
    args = ap.parse_args(argv)

    results = []
    try:
        for raw in args.pair:
            fg, bg = split_pair(raw)
            results.append(evaluate(fg, bg))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    sotto = [r for r in results if not r["testo_normale"]]
    print(json.dumps(
        {"ok": not sotto, "soglie": {"testo_normale": SOGLIA_TESTO, "testo_grande": SOGLIA_GRANDE},
         "coppie": results},
        ensure_ascii=False, indent=2,
    ))
    return 0 if not sotto else 1


if __name__ == "__main__":
    sys.exit(main())
