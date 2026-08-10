#!/usr/bin/env python3
"""Registro delle run di eval del modulo Guardrails.

I report delle run restano fuori dal repository: `.gitignore` esclude
`**/eval-runs/` di proposito, perché sono voluminosi e locali. L'effetto
collaterale è che l'esito sparisce con la macchina, e ogni sessione riparte dal
dubbio su cosa sia già stato validato.

Questo registro tiene la sola riga che serve a saperlo: quale skill, quando, di
che tipo, con quale esito e dove sta l'evidenza. Non sostituisce il report, lo
indicizza.

Uso:
    python3 tools/eval_registry.py                 # copertura delle 37 skill
    python3 tools/eval_registry.py --scoperte      # solo quelle mai validate
    python3 tools/eval_registry.py --add grl-web --tipo quality --esito pass \
        --dettaglio "6/6 casi" --evidenza "skills/reports/eval-runs/<run>" --data 2026-08-10
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evals" / "run-registry.csv"
SKILLS = ROOT / "src" / "skills"

COLONNE = ["skill", "data", "tipo", "esito", "dettaglio", "runtime", "evidenza"]

# `quality` misura la risposta, `trigger` l'instradamento, `baseline` il confronto
# con il modello nudo. Una skill è validata davvero quando ha tutti e tre.
TIPI = ("quality", "trigger", "baseline")
ESITI = ("pass", "fail", "parziale")


def skill_names() -> set[str]:
    return {p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()}


def leggi() -> list[dict]:
    if not REGISTRY.is_file():
        return []
    with REGISTRY.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copertura() -> dict[str, dict[str, dict]]:
    """Per ogni skill, la run più recente di ciascun tipo."""
    mappa: dict[str, dict[str, dict]] = {s: {} for s in skill_names()}
    for riga in leggi():
        skill, tipo = riga["skill"], riga["tipo"]
        if skill not in mappa:
            continue
        corrente = mappa[skill].get(tipo)
        if corrente is None or riga["data"] > corrente["data"]:
            mappa[skill][tipo] = riga
    return mappa


def stampa(solo_scoperte: bool) -> int:
    mappa = copertura()
    validate = 0
    for skill in sorted(mappa):
        run = mappa[skill]
        if solo_scoperte and run:
            continue
        celle = []
        for tipo in TIPI:
            riga = run.get(tipo)
            celle.append(f"{tipo}={riga['esito']}@{riga['data']}" if riga else f"{tipo}=—")
        if len(run) == len(TIPI):
            validate += 1
        print(f"{skill:26} {'  '.join(celle)}")
    totale = len(mappa)
    print(f"\nvalidate su tutti e tre i tipi: {validate}/{totale}")
    print(f"senza alcuna run registrata:    {sum(1 for r in mappa.values() if not r)}/{totale}")
    return 0


def aggiungi(args: argparse.Namespace) -> int:
    if args.add not in skill_names():
        print(f"skill sconosciuta: {args.add}", file=sys.stderr)
        return 1
    riga = {
        "skill": args.add,
        "data": args.data,
        "tipo": args.tipo,
        "esito": args.esito,
        "dettaglio": args.dettaglio,
        "runtime": args.runtime,
        "evidenza": args.evidenza,
    }
    esistenti = leggi()
    with REGISTRY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLONNE, lineterminator="\n")
        writer.writeheader()
        writer.writerows([*esistenti, riga])
    print(f"registrata: {args.add} {args.tipo} {args.esito} ({args.data})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scoperte", action="store_true", help="solo le skill mai validate")
    parser.add_argument("--add", metavar="SKILL", help="registra una run")
    parser.add_argument("--data", default="", help="data ISO della run")
    parser.add_argument("--tipo", choices=TIPI, help="tipo di run")
    parser.add_argument("--esito", choices=ESITI, help="esito della run")
    parser.add_argument("--dettaglio", default="", help="il conteggio, per esempio 7/7 casi")
    parser.add_argument("--runtime", default="subagent della sessione di chat")
    parser.add_argument("--evidenza", default="", help="percorso del report o fonte")
    args = parser.parse_args()

    if args.add:
        if not (args.data and args.tipo and args.esito):
            parser.error("--add richiede --data, --tipo e --esito")
        return aggiungi(args)
    return stampa(args.scoperte)


if __name__ == "__main__":
    raise SystemExit(main())
