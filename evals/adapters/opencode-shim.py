#!/usr/bin/env python3
"""Fa parlare `opencode run` la lingua che `bmad-eval-runner` sa leggere.

Il runner di BMad rileva il caricamento di una skill cercando, riga per riga,
eventi in forma Anthropic:

    {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {...}}]}}

`opencode run --format json` emette invece eventi propri, con il tool annidato
sotto `part` e i parametri sotto `state.input`:

    {"type": "tool_use", "part": {"type": "tool", "tool": "skill",
        "state": {"input": {"name": "..."}}}}

Questo shim esegue opencode, traduce ogni chiamata a tool nella forma attesa e
la riemette su stdout. Non tocca la skill installata `bmad-eval-runner`, che
l'installer BMad riscrive a ogni aggiornamento: la traduzione vive qui.

Uso (è il campo `invocation` di un adapter):

    opencode-shim.py --model opencode/deepseek-v4-flash-free -- "{prompt}"

Il nome del tool di lettura cambia anch'esso: opencode usa `read` con
`filePath`, la forma attesa è `Read` con `file_path`. La traduzione normalizza
entrambi, così `load_signal` resta `{"skill_tool": "Skill", "read_tool": "Read"}`
e l'adapter non deve conoscere i nomi interni di opencode.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

# nome opencode -> nome nella forma attesa dal runner
TOOL_ALIAS = {"skill": "Skill", "read": "Read"}
# chiave del parametro di percorso: opencode -> forma attesa
INPUT_ALIAS = {"filePath": "file_path"}


def traduci(evento: dict) -> dict | None:
    """Una chiamata a tool di opencode nella forma Anthropic, o None."""
    if evento.get("type") != "tool_use":
        return None
    part = evento.get("part") or {}
    if part.get("type") != "tool":
        return None

    nome = part.get("tool", "")
    stato = part.get("state") or {}
    parametri = stato.get("input")
    if not isinstance(parametri, dict):
        parametri = {}

    return {
        "type": "assistant",
        "message": {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": part.get("callID", ""),
                    "name": TOOL_ALIAS.get(nome, nome),
                    "input": {INPUT_ALIAS.get(k, k): v for k, v in parametri.items()},
                }
            ],
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True, help="provider/modello per opencode run")
    ap.add_argument("--opencode", default="opencode", help="eseguibile di opencode")
    ap.add_argument("--variant", default=None,
                    help="variante del modello (sforzo di ragionamento: high, max, minimal)")
    ap.add_argument("--passthrough", action="store_true",
                    help="riemetti anche gli eventi non tradotti, per ispezione")
    ap.add_argument("prompt", nargs="+", help="il messaggio da mandare")
    args = ap.parse_args()

    # `--pure` tiene fuori i plugin esterni: la misura riguarda la description
    # della skill, non l'ambiente personale di chi lancia il runner.
    argv = [args.opencode, "run", "--format", "json", "--pure", "--auto",
            "-m", args.model]
    if args.variant:
        argv += ["--variant", args.variant]
    argv.append(" ".join(args.prompt))

    try:
        proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print(json.dumps({"type": "error", "error": f"{args.opencode} non trovato"}),
              file=sys.stderr)
        return 127

    for riga in (proc.stdout or b"").decode("utf-8", errors="replace").splitlines():
        riga = riga.strip()
        if not riga:
            continue
        try:
            evento = json.loads(riga)
        except json.JSONDecodeError:
            continue
        if not isinstance(evento, dict):
            continue
        tradotto = traduci(evento)
        if tradotto is not None:
            print(json.dumps(tradotto, ensure_ascii=False), flush=True)
        elif args.passthrough:
            print(riga, flush=True)

    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
