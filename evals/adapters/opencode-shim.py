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

    opencode-shim.py --model opencode-go/deepseek-v4-flash -- "{prompt}"

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
import threading

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
        proc = subprocess.Popen(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
    except FileNotFoundError:
        print(json.dumps({"type": "error", "error": f"{args.opencode} non trovato"}),
              file=sys.stderr)
        return 127

    def inoltra_stderr() -> None:
        """Mantieni diagnostica disponibile senza bloccare stdout."""
        if proc.stderr is None:
            return
        for riga in proc.stderr:
            sys.stderr.write(riga)
            sys.stderr.flush()

    stderr_thread = threading.Thread(target=inoltra_stderr, daemon=True)
    stderr_thread.start()

    try:
        stdout = proc.stdout
        if stdout is None:
            return proc.wait()
        for riga in stdout:
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
    except (BrokenPipeError, KeyboardInterrupt):
        proc.terminate()
        proc.wait()
        return 130
    finally:
        if proc.stdout is not None:
            proc.stdout.close()

    return_code = proc.wait()
    stderr_thread.join(timeout=1)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
