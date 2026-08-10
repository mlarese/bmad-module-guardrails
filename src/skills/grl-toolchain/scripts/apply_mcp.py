#!/usr/bin/env python3
"""Traduce un server MCP nella forma di un harness e lo installa.

Il default è il dry-run: senza `--apply` lo script non scrive niente e stampa il
diff, oppure il comando esatto da eseguire quando l'harness ha una CLI. Con
`--apply` scrive, dopo aver copiato il file originale in un backup con
timestamp di cui stampa il percorso.

Due strade, scelte in base all'harness:

* **CLI** — Claude Code, Codex, Droid, Gemini hanno un comando di aggiunta non
  interattivo. Lo si usa: conosce lo schema corrente meglio di questo script e
  non riscrive il resto del file. Lo script compone il comando; con `--apply` lo
  esegue.
* **File** — per gli altri si scrive la configurazione, preservando tutto quello
  che non si sta cambiando. I file JSON con commenti non si riscrivono: lo
  script si ferma e stampa il frammento da incollare.

Esempi:

    apply_mcp.py --harness cursor --name github -- npx -y @org/github-mcp
    apply_mcp.py --harness opencode --name sentry --url https://mcp.sentry.dev/mcp
    apply_mcp.py --harness goose --name db --env-ref PGPASSWORD=PG_PASS -- uvx pg-mcp
    apply_mcp.py --harness cursor --name github --remove --apply

Codici di uscita: 0 = riuscito, 1 = errore d'uso o rifiuto motivato,
2 = errore d'ambiente.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from detect_harness import load_config  # noqa: E402
from harness_spec import BY_ID, Harness, McpFile  # noqa: E402

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - dipende dall'ambiente
    yaml = None  # type: ignore[assignment]


# Harness la cui CLI accetta un'aggiunta non interattiva. Per gli altri si
# scrive il file: `opencode mcp add` e `goose configure` sono interattivi e non
# si pilotano da uno script.
CLI_BUILDERS = {"claude-code", "codex", "droid", "gemini"}


class Rifiuto(Exception):
    """Condizione in cui lo script si ferma con una spiegazione, non un errore."""


def parse_pairs(values: list[str], sep: str = "=") -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in values:
        if sep not in raw:
            raise Rifiuto(f"formato atteso NOME{sep}VALORE, ricevuto: {raw}")
        name, _, value = raw.partition(sep)
        out[name.strip()] = value.strip()
    return out


_SECRET_WORD = r"[\w.\-]*(?:key|secret|token|password|passwd|credential)[\w.\-]*"

# Tre forme distinte, perché il confine del valore cambia: dentro un file il
# valore sta fra virgolette e può contenere spazi; su una riga di comando finisce
# al primo spazio; un bearer token segue una parola fissa. Una regola sola
# divorerebbe il resto della riga.
_MASK_QUOTED = re.compile(rf'(["\']{_SECRET_WORD}["\']\s*[:=]\s*["\'])([^"\']*)(["\'])', re.I)
_MASK_BARE = re.compile(
    rf'(\b{_SECRET_WORD}\s*[:=]\s*)(\$\{{[A-Za-z0-9_]+\}}|[^\s"\',}}]+)', re.I
)
_MASK_BEARER = re.compile(r"(\bBearer\s+)([^\s'\"]+)")

# Un riferimento a variabile d'ambiente non è un segreto: è la forma corretta, e
# nasconderla toglierebbe all'utente l'informazione che serve per capire il diff.
_IS_REFERENCE = re.compile(r"^\$\{?[A-Za-z_][A-Za-z0-9_]*\}?$")


def _hide(value: str) -> str:
    return value if _IS_REFERENCE.match(value.strip()) else "***"


def mask(text: str) -> str:
    """Sostituisce i valori dei campi segreti con `***` prima di stamparli."""
    text = _MASK_QUOTED.sub(lambda m: f"{m.group(1)}{_hide(m.group(2))}{m.group(3)}", text)
    text = _MASK_BARE.sub(lambda m: f"{m.group(1)}{_hide(m.group(2))}", text)
    return _MASK_BEARER.sub(lambda m: f"{m.group(1)}{_hide(m.group(2))}", text)


# --- costruzione della voce, per formato ------------------------------------


def build_entry(harness: Harness, spec: McpFile, args: argparse.Namespace) -> dict[str, Any]:
    """Costruisce la voce di configurazione nella forma dell'harness."""
    env = parse_pairs(args.env)
    for name, var in parse_pairs(args.env_ref).items():
        env[name] = f"${{{var}}}"
    headers = parse_pairs(args.header, sep=":") if args.header else {}

    remote = bool(args.url)
    entry: dict[str, Any] = {}

    if harness.id == "opencode":
        if remote:
            entry = {"type": "remote", "url": args.url, "enabled": True}
            if headers:
                entry["headers"] = headers
        else:
            entry = {"type": "local", "command": args.command, "enabled": True}
            if env:
                entry["environment"] = env
        return entry

    if harness.id == "goose":
        if remote:
            entry = {
                "type": "sse" if args.transport == "sse" else "streamable_http",
                "name": args.name,
                "uri": args.url,
                "enabled": True,
                "timeout": 300,
            }
        else:
            entry = {
                "type": "stdio",
                "name": args.name,
                "cmd": args.command[0],
                "args": args.command[1:],
                "enabled": True,
                "timeout": 300,
            }
            if env:
                entry["envs"] = env
        return entry

    if harness.id == "continue":
        entry = {"name": args.name}
        if remote:
            entry["url"] = args.url
        else:
            entry["command"] = args.command[0]
            entry["args"] = args.command[1:]
            if env:
                entry["env"] = env
        return entry

    if harness.id == "zed":
        # Campi piatti e supporto remoto, come la documentazione ufficiale corrente.
        # La forma con `source: "custom"` e `command: {path, args, env}` è quella
        # vecchia: la scheda dell'harness spiega la discordanza.
        if remote:
            entry = {"url": args.url}
            if headers:
                entry["headers"] = headers
        else:
            entry = {"command": args.command[0], "args": args.command[1:]}
            if env:
                entry["env"] = env
        return entry

    # Forma comune: Cursor, Windsurf, Crush, VS Code, Qwen, Claude Code (file).
    if remote:
        entry = {"type": args.transport, "url": args.url}
        if headers:
            entry[spec.headers_field] = headers
    else:
        entry = {"command": args.command[0], "args": args.command[1:]}
        if env:
            entry[spec.env_field] = env
    return entry


def build_cli(harness: Harness, args: argparse.Namespace) -> list[str]:
    """Compone il comando di aggiunta della CLI dell'harness."""
    env = parse_pairs(args.env)
    for name, var in parse_pairs(args.env_ref).items():
        env[name] = f"${{{var}}}"
    headers = parse_pairs(args.header, sep=":") if args.header else {}

    if harness.id == "claude-code":
        cmd = ["claude", "mcp", "add"]
        if args.scope:
            cmd += ["--scope", args.scope]
        if args.url:
            cmd += ["--transport", args.transport, args.name, args.url]
            for name, value in headers.items():
                cmd += ["--header", f"{name}: {value}"]
        else:
            for name, value in env.items():
                cmd += ["-e", f"{name}={value}"]
            cmd += [args.name, "--"] + args.command
        return cmd

    if harness.id == "codex":
        cmd = ["codex", "mcp", "add"]
        if args.url:
            cmd += [args.name, "--url", args.url]
        else:
            for name, value in env.items():
                cmd += ["--env", f"{name}={value}"]
            cmd += [args.name, "--"] + args.command
        return cmd

    if harness.id == "droid":
        cmd = ["droid", "mcp", "add", args.name]
        if args.url:
            cmd += [args.url, "--type", args.transport]
            for name, value in headers.items():
                cmd += ["--header", f"{name}: {value}"]
        else:
            cmd += args.command
            for name, value in env.items():
                cmd += ["--env", f"{name}={value}"]
        return cmd

    if harness.id == "gemini":
        cmd = ["gemini", "mcp", "add"]
        if args.url:
            cmd += ["--transport", args.transport, args.name, args.url]
        else:
            for name, value in env.items():
                cmd += ["-e", f"{name}={value}"]
            cmd += [args.name] + args.command
        return cmd

    raise Rifiuto(f"nessun comando CLI noto per {harness.id}")


# --- scrittura ---------------------------------------------------------------


def dump(data: dict[str, Any], fmt: str) -> str:
    if fmt in ("json-map", "jsonc-map"):
        return json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if fmt in ("yaml-map", "yaml-list"):
        if yaml is None:
            raise Rifiuto("serve PyYAML per scrivere questo file: pip install PyYAML")
        return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    raise Rifiuto(f"scrittura non supportata per il formato {fmt}")


def apply_to_file(
    harness: Harness, spec: McpFile, args: argparse.Namespace
) -> tuple[str, str, Path]:
    """Ritorna (testo prima, testo dopo, percorso). Non scrive."""
    path = spec.resolved
    if not spec.writable:
        frammento = json.dumps(
            {spec.key: {args.name: build_entry(harness, spec, args)}},
            indent=2,
            ensure_ascii=False,
        )
        raise Rifiuto(
            f"{path} è un file JSON con commenti: riscriverlo li cancellerebbe.\n\n"
            f"Frammento da incollare a mano:\n{mask(frammento)}"
        )
    if spec.fmt == "toml-table":
        azione = f"codex mcp remove {args.name}" if args.remove else "codex mcp add"
        raise Rifiuto(
            f"la configurazione di {harness.label} è in TOML: usa `{azione}`. "
            "Scrivere TOML a programma perderebbe commenti e formattazione del file."
        )

    before = path.read_text(encoding="utf-8") if path.exists() else ""
    data: dict[str, Any] = {}
    if before.strip():
        data, error = load_config(path, spec.fmt)
        if error:
            raise Rifiuto(f"{path} non è leggibile ({error}): non lo riscrivo.")
        data = data or {}

    if spec.fmt == "yaml-list":
        block = data.get(spec.key) or []
        block = [e for e in block if not (isinstance(e, dict) and e.get("name") == args.name)]
        if not args.remove:
            block.append(build_entry(harness, spec, args))
        data[spec.key] = block
    else:
        block = data.get(spec.key)
        if block is None:
            block = {}
        if not isinstance(block, dict):
            raise Rifiuto(f"la chiave {spec.key} in {path} non è una mappa: non la tocco.")
        if args.remove:
            if args.name not in block:
                raise Rifiuto(f"'{args.name}' non è configurato in {path}: niente da togliere.")
            block.pop(args.name)
        else:
            if args.name in block and not args.force:
                raise Rifiuto(
                    f"'{args.name}' esiste già in {path}. Decidi tu: aggiorna con --force, "
                    "oppure scegli un altro nome."
                )
            block[args.name] = build_entry(harness, spec, args)
        data[spec.key] = block

    return before, dump(data, spec.fmt), path


def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = path.with_name(f"{path.name}.bak-{stamp}")
    shutil.copy2(path, target)
    return target


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


# --- programma ---------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--harness", required=True, help="id dell'harness bersaglio")
    parser.add_argument("--name", required=True, help="nome del server MCP")
    parser.add_argument("--url", help="URL di un server remoto")
    parser.add_argument(
        "--transport", default="http", choices=["http", "sse"], help="trasporto remoto"
    )
    parser.add_argument("--env", action="append", default=[], metavar="NOME=VALORE")
    parser.add_argument(
        "--env-ref",
        action="append",
        default=[],
        metavar="NOME=VARIABILE",
        help="variabile d'ambiente per riferimento, invece del valore in chiaro",
    )
    parser.add_argument("--header", action="append", default=[], metavar="NOME: VALORE")
    parser.add_argument("--scope", choices=["local", "user", "project"])
    parser.add_argument("--remove", action="store_true", help="toglie il server")
    parser.add_argument("--force", action="store_true", help="sovrascrive un nome esistente")
    parser.add_argument("--apply", action="store_true", help="scrive davvero")
    parser.add_argument(
        "command", nargs="*", help="comando del server stdio, dopo --"
    )
    args = parser.parse_args(argv)

    harness = BY_ID.get(args.harness)
    if harness is None:
        print(f"harness sconosciuto: {args.harness}", file=sys.stderr)
        print("noti: " + ", ".join(sorted(BY_ID)), file=sys.stderr)
        return 1
    if not args.remove and not args.url and not args.command:
        print("serve un comando (dopo --) oppure --url", file=sys.stderr)
        return 1

    try:
        if harness.confidence == "da-verificare" and not args.force:
            raise Rifiuto(
                f"la scheda di {harness.label} è marcata `da-verificare`: verificane il "
                "formato con il modo refresh prima di scrivere, oppure forza con --force."
            )

        if harness.id in CLI_BUILDERS and not args.remove:
            cmd = build_cli(harness, args)
            print(f"# {harness.label}: aggiunta via CLI")
            print(mask(shlex.join(cmd)))
            if args.env_ref:
                print(
                    "# nota: il valore passato è la stringa ${VAR}. Che l'harness la "
                    "espanda va verificato: se non lo fa, passa il valore risolto."
                )
            if not args.apply:
                print("\n(dry-run: nessuna esecuzione. Aggiungi --apply per eseguire.)")
                return 0
            if shutil.which(cmd[0]) is None:
                raise Rifiuto(f"{cmd[0]} non è nel PATH: non posso eseguirlo.")
            result = subprocess.run(cmd, check=False)
            if result.returncode != 0:
                print(f"il comando è uscito con codice {result.returncode}", file=sys.stderr)
                return 1
            if harness.verify:
                print(f"\nVerifica ora con: {harness.verify}")
            return 0

        if not harness.mcp_files:
            raise Rifiuto(
                f"per {harness.label} non è noto un file di configurazione MCP: "
                "esegui il modo refresh."
            )

        spec = next((f for f in harness.mcp_files if f.resolved.exists()), harness.mcp_files[0])
        before, after, path = apply_to_file(harness, spec, args)

        diff = "".join(
            difflib.unified_diff(
                before.splitlines(keepends=True),
                after.splitlines(keepends=True),
                fromfile=str(path),
                tofile=f"{path} (proposto)",
            )
        )
        print(f"# {harness.label}: {path}")
        print(mask(diff) if diff else "(nessuna differenza)")

        if not args.apply:
            print("(dry-run: nessuna scrittura. Aggiungi --apply per scrivere.)")
            return 0

        if path.exists():
            saved = backup(path)
            print(f"backup: {saved}")
        write_atomic(path, after)
        print(f"scritto: {path}")
        if harness.verify:
            print(f"Verifica ora con: {harness.verify}")
        if harness.id == "cursor" and not args.remove:
            print(f"Poi abilita: cursor-agent mcp enable {args.name}")
        return 0

    except Rifiuto as exc:
        print(f"fermato: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"errore di ambiente: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
