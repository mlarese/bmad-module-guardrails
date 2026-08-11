#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML"]
# ///
"""Alza la versione del modulo e riallinea il lucchetto che la tiene onesta.

La versione vive in due punti — `src/module.yaml` e `.claude-plugin/marketplace.json` —
e nessuno dei due la calcola: resta ferma finché qualcuno non la tocca. È così che
il modulo è cresciuto da ventidue a ventitré figure restando a `1.34.1` per sette
commit di fila, e chi aveva installato non ha visto niente.

Il lucchetto `src/module-version.lock` registra, accanto alla versione, il set di
skill e di moduli derivati che quella versione descrive. Se il set cambia e la
versione no, `tools/tests/test_version_lock.py` fallisce e dice quale salto serve.

Uso:

    bump_version.py --check              # cosa è cambiato rispetto al lucchetto
    bump_version.py --patch              # istruzioni riscritte, correzioni, vetrine
    bump_version.py --minor              # una figura o una skill in più o in meno
    bump_version.py --major              # un contratto che rompe le installazioni

`--check` non scrive niente ed esce 1 se il lucchetto non corrisponde: è il
comando da guardare prima della build.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
MANIFESTO = RADICE / "src" / "module.yaml"
MARKETPLACE = RADICE / ".claude-plugin" / "marketplace.json"
LUCCHETTO = RADICE / "src" / "module-version.lock"
SKILLS = RADICE / "src" / "skills"
TOPOLOGIA = RADICE / "src" / "module-topology.yaml"


def versione_manifesto() -> str:
    match = re.search(r"^module_version:\s*(\S+)", MANIFESTO.read_text(encoding="utf-8"), re.M)
    if not match:
        raise SystemExit("src/module.yaml non dichiara module_version")
    return match.group(1)


def versione_marketplace() -> str:
    return json.loads(MARKETPLACE.read_text(encoding="utf-8"))["plugins"][0]["version"]


def stato_attuale() -> dict:
    import yaml

    skill = sorted(p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())
    topologia = yaml.safe_load(TOPOLOGIA.read_text(encoding="utf-8"))
    return {
        "module_version": versione_manifesto(),
        "skills": skill,
        "modules": sorted(m["code"] for m in topologia["modules"]),
    }


def lucchetto() -> dict:
    if not LUCCHETTO.is_file():
        raise SystemExit("src/module-version.lock non esiste: crealo con --patch")
    return json.loads(LUCCHETTO.read_text(encoding="utf-8"))


def differenze(atteso: dict, attuale: dict) -> list[str]:
    """Cosa è cambiato rispetto alla versione dichiarata nel lucchetto."""
    righe = []
    for chiave, etichetta in (("skills", "skill"), ("modules", "modulo derivato")):
        aggiunte = sorted(set(attuale[chiave]) - set(atteso.get(chiave, [])))
        rimosse = sorted(set(atteso.get(chiave, [])) - set(attuale[chiave]))
        righe += [f"{etichetta} aggiunto: {v}" for v in aggiunte]
        righe += [f"{etichetta} rimosso: {v}" for v in rimosse]
    return righe


def alza(versione: str, salto: str) -> str:
    maggiore, minore, patch = (int(p) for p in versione.split("."))
    if salto == "major":
        return f"{maggiore + 1}.0.0"
    if salto == "minor":
        return f"{maggiore}.{minore + 1}.0"
    return f"{maggiore}.{minore}.{patch + 1}"


def scrivi(nuova: str, attuale: dict) -> None:
    MANIFESTO.write_text(
        re.sub(r"^module_version:\s*\S+", f"module_version: {nuova}", MANIFESTO.read_text(encoding="utf-8"), count=1, flags=re.M),
        encoding="utf-8",
    )
    dati = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    dati["plugins"][0]["version"] = nuova
    MARKETPLACE.write_text(json.dumps(dati, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LUCCHETTO.write_text(
        json.dumps({**attuale, "module_version": nuova}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    gruppo = parser.add_mutually_exclusive_group(required=True)
    gruppo.add_argument("--check", action="store_true", help="verifica senza scrivere")
    gruppo.add_argument("--patch", action="store_true")
    gruppo.add_argument("--minor", action="store_true")
    gruppo.add_argument("--major", action="store_true")
    args = parser.parse_args()

    attuale = stato_attuale()
    if args.check:
        atteso = lucchetto()
        cambiamenti = differenze(atteso, attuale)
        if versione_manifesto() != versione_marketplace():
            print(f"disallineate: module.yaml {versione_manifesto()}, marketplace {versione_marketplace()}")
            return 1
        if not cambiamenti and atteso["module_version"] == attuale["module_version"]:
            print(f"allineato: {attuale['module_version']}")
            return 0
        if cambiamenti:
            print(f"la versione {atteso['module_version']} non descrive più il pacchetto:")
            for riga in cambiamenti:
                print(f"  {riga}")
            print("alza la versione con --minor (o --patch se il cambiamento non tocca cosa si installa)")
        else:
            print(f"lucchetto a {atteso['module_version']}, manifesto a {attuale['module_version']}: riallinea con un bump")
        return 1

    salto = "major" if args.major else "minor" if args.minor else "patch"
    precedente = versione_manifesto()
    nuova = alza(precedente, salto)
    scrivi(nuova, attuale)
    print(f"{salto}: {precedente} → {nuova}")
    print("ora rigenera i derivati con tools/build_modules.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
