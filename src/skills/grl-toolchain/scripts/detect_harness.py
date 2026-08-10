#!/usr/bin/env python3
"""Inventario read-only degli harness presenti sulla macchina.

Risponde a quattro domande, senza scrivere niente:

1. Quali harness ci sono davvero, e dove hanno i file di configurazione.
2. Quali server MCP sono configurati, per harness, con che trasporto.
3. Quali skill sono installate, distinguendo file, collegamento valido e
   collegamento rotto.
4. Cosa è rotto: collegamenti che non puntano a niente, segreti in chiaro,
   file di configurazione illeggibili, server duplicati.

I valori dei segreti non vengono mai stampati: si riporta il file, il server e
il nome del campo.

Uso:
    python3 detect_harness.py                     # riepilogo
    python3 detect_harness.py --report            # riepilogo + difetti in dettaglio
    python3 detect_harness.py --harness codex -v  # un solo harness, verboso
    python3 detect_harness.py --json              # per un altro programma

Codici di uscita: 0 = eseguito, 1 = errore d'uso, 2 = errore d'ambiente.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness_spec import HARNESSES, BY_ID, Harness, McpFile, resolve  # noqa: E402

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None  # type: ignore[assignment]

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - dipende dall'ambiente
    yaml = None  # type: ignore[assignment]


# Nomi di campo che indicano un segreto. Il confronto è sul nome, non sulla
# lunghezza del valore: una chiave corta in un campo API_KEY resta un segreto, e
# un percorso lungo in un campo NODE_PATH non lo è. La regola "valore lungo"
# produce solo falsi positivi e non viene usata.
SECRET_NAME = re.compile(
    r"(api[-_]?key|secret|token|password|passwd|bearer|credential|private[-_]?key"
    r"|access[-_]?key|auth(oriz|entic)?)", re.IGNORECASE
)

# Valori riconoscibili come credenziale anche quando il nome del campo non dice
# niente: prefissi usati dai principali emittenti, e JWT.
CREDENTIAL_VALUE = re.compile(
    r"^(sk-[A-Za-z0-9_-]{10,}"
    r"|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
    r"|xox[baprs]-[A-Za-z0-9-]{10,}"
    r"|AKIA[0-9A-Z]{16}"
    r"|AQ\.[A-Za-z0-9_-]{16,}"
    r"|eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\."
    r"|Bearer\s+\S{16,})"
)

# Valori che sono palesemente un riferimento e non un segreto in chiaro.
PLACEHOLDER = re.compile(r"^\s*(\$\{?[A-Z0-9_]+\}?|<[^>]+>|\.\.\.|\*+|)\s*$")


def strip_jsonc(text: str) -> str:
    """Toglie commenti `//` e `/* */` da un JSON con commenti.

    Non tocca quello che sta dentro le stringhe: un URL `https://host` non è un
    commento, ed è l'errore che rende inutile la versione ingenua di questa
    funzione.
    """
    out: list[str] = []
    i, n = 0, len(text)
    in_string = False
    while i < n:
        ch = text[i]
        if in_string:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        out.append(ch)
        i += 1
    # Le virgole finali sono legali in JSONC e non in JSON.
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def load_config(path: Path, fmt: str) -> tuple[dict[str, Any] | None, str | None]:
    """Legge un file di configurazione. Ritorna (contenuto, errore)."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"illeggibile: {exc.strerror or exc}"

    try:
        if fmt == "json-map":
            return json.loads(text) if text.strip() else {}, None
        if fmt == "jsonc-map":
            return json.loads(strip_jsonc(text)) if text.strip() else {}, None
        if fmt == "toml-table":
            if tomllib is None:
                return None, "serve Python 3.11+ per leggere TOML"
            return tomllib.loads(text), None
        if fmt in ("yaml-map", "yaml-list"):
            if yaml is None:
                return None, "serve PyYAML per leggere questo file"
            return yaml.safe_load(text) or {}, None
    except (json.JSONDecodeError, ValueError) as exc:
        return None, f"sintassi non valida: {exc}"
    except Exception as exc:  # pragma: no cover - parser di terze parti
        return None, f"non interpretabile: {exc}"
    return None, f"formato sconosciuto: {fmt}"


def transport_of(entry: dict[str, Any], spec: McpFile) -> str:
    """Deduce il trasporto di un server dalla sua voce di configurazione."""
    declared = entry.get("type") or entry.get("transport")
    if isinstance(declared, str):
        low = declared.lower()
        if low in ("local", "stdio"):
            return "stdio"
        if low in ("remote", "http", "streamable_http", "streamable-http", "sse"):
            return "sse" if low == "sse" else "http"
    if entry.get("url") or entry.get("uri") or entry.get("httpUrl"):
        return "http"
    if entry.get(spec.command_field) or entry.get("command") or entry.get("cmd"):
        return "stdio"
    return "sconosciuto"


def secrets_in(entry: dict[str, Any], spec: McpFile) -> list[str]:
    """Nomi dei campi che contengono un segreto in chiaro. Mai i valori.

    Un campo è un segreto se il suo nome lo dichiara, oppure se il valore ha la
    forma di una credenziale nota. Non basta che il valore sia lungo: percorsi e
    URL sono lunghi e non sono segreti.
    """
    containers = list(
        dict.fromkeys(
            [spec.env_field, "env", "envs", "environment",
             spec.headers_field, "headers", "header", "http_headers"]
        )
    )
    found: list[str] = []
    for container in containers:
        block = entry.get(container)
        if not isinstance(block, dict):
            continue
        for name, value in block.items():
            if not isinstance(value, str) or PLACEHOLDER.match(value):
                continue
            if SECRET_NAME.search(name) or CREDENTIAL_VALUE.match(value.strip()):
                found.append(f"{container}.{name}")
    return list(dict.fromkeys(found))


def read_servers(spec: McpFile) -> tuple[list[dict[str, Any]], str | None]:
    """Legge i server MCP da un file. Ritorna (server, errore)."""
    path = spec.resolved
    if not path.exists():
        return [], None
    data, error = load_config(path, spec.fmt)
    if error:
        return [], error
    block = (data or {}).get(spec.key)
    servers: list[dict[str, Any]] = []

    if spec.fmt == "yaml-list":
        for entry in block or []:
            if isinstance(entry, dict):
                name = entry.get("name") or "(senza nome)"
                servers.append(_describe(name, entry, spec))
        return servers, None

    if isinstance(block, dict):
        for name, entry in block.items():
            if isinstance(entry, dict):
                servers.append(_describe(name, entry, spec))
    elif block is not None:
        return [], f"la chiave {spec.key} non è una mappa"
    return servers, None


def _describe(name: str, entry: dict[str, Any], spec: McpFile) -> dict[str, Any]:
    enabled = entry.get("enabled")
    return {
        "name": name,
        "transport": transport_of(entry, spec),
        "enabled": True if enabled is None else bool(enabled),
        "builtin": entry.get("type") == "builtin" or bool(entry.get("bundled")),
        "secrets": secrets_in(entry, spec),
    }


def read_skills(raw_dir: str) -> dict[str, Any]:
    """Elenca le skill in una cartella, distinguendo i collegamenti rotti."""
    path = resolve(raw_dir)
    result: dict[str, Any] = {
        "path": str(path),
        "exists": path.is_dir(),
        "ok": [],
        "broken": [],
    }
    if not path.is_dir():
        return result
    try:
        entries = sorted(path.iterdir())
    except OSError:
        return result
    for entry in entries:
        if entry.name.startswith("."):
            continue
        if entry.is_symlink() and not entry.exists():
            result["broken"].append({"name": entry.name, "target": os.readlink(entry)})
        elif entry.is_dir() or entry.suffix == ".md":
            result["ok"].append(entry.name)
    return result


def inspect(harness: Harness) -> dict[str, Any]:
    info: dict[str, Any] = {
        "id": harness.id,
        "label": harness.label,
        "present": harness.present(),
        "confidence": harness.confidence,
        "cli": harness.cli,
        "cli_path": shutil.which(harness.cli) if harness.cli else None,
        "verify": harness.verify,
        "notes": harness.notes,
        "config_files": [],
        "servers": [],
        "skills": [],
        "problems": [],
    }

    seen: dict[str, str] = {}
    for spec in harness.mcp_files:
        path = spec.resolved
        entry = {
            "path": str(path),
            "format": spec.fmt,
            "key": spec.key,
            "scope": spec.scope,
            "exists": path.exists(),
            "writable": spec.writable,
        }
        info["config_files"].append(entry)
        servers, error = read_servers(spec)
        if error:
            info["problems"].append(f"{path}: {error}")
            entry["error"] = error
            continue
        for server in servers:
            server["file"] = str(path)
            info["servers"].append(server)
            if server["secrets"]:
                info["problems"].append(
                    f"segreto in chiaro in {path} → {server['name']}: "
                    + ", ".join(server["secrets"])
                )
            previous = seen.get(server["name"])
            if previous and previous != str(path):
                info["problems"].append(
                    f"server '{server['name']}' definito in due file: {previous} e {path}"
                )
            seen[server["name"]] = str(path)

    for raw_dir in harness.skills_dirs:
        skills = read_skills(raw_dir)
        info["skills"].append(skills)
        if skills["broken"]:
            n = len(skills["broken"])
            voce = "collegamento rotto" if n == 1 else "collegamenti rotti"
            info["problems"].append(f"{n} {voce} in {skills['path']}")

    if not info["present"] and (info["servers"] or any(s["ok"] for s in info["skills"])):
        info["problems"].append(
            "configurazione presente ma harness non rilevato: forse disinstallato"
        )
    return info


def render(results: list[dict[str, Any]], report: bool, verbose: bool) -> str:
    lines: list[str] = []
    present = [r for r in results if r["present"]]
    absent = [r for r in results if not r["present"]]

    lines.append(f"# Harness rilevati: {len(present)} su {len(results)} noti")
    lines.append("")
    lines.append("| Harness | Scheda | CLI | Server MCP | Skill | Rotti |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for r in present:
        n_skills = sum(len(s["ok"]) for s in r["skills"])
        n_broken = sum(len(s["broken"]) for s in r["skills"])
        cli = "sì" if r["cli_path"] else ("assente" if r["cli"] else "—")
        lines.append(
            f"| {r['label']} | `{r['confidence']}` | {cli} | "
            f"{len(r['servers'])} | {n_skills} | {n_broken or '—'} |"
        )
    lines.append("")

    if absent:
        lines.append("Non rilevati: " + ", ".join(r["label"] for r in absent))
        lines.append("")

    problems = [(r["label"], p) for r in results for p in r["problems"]]
    if problems:
        lines.append(f"## Difetti: {len(problems)}")
        lines.append("")
        for label, problem in problems:
            lines.append(f"- **{label}** — {problem}")
        lines.append("")
    else:
        lines.append("Nessun difetto rilevato.")
        lines.append("")

    if report or verbose:
        for r in present:
            lines.append(f"## {r['label']} (`{r['id']}`)")
            lines.append("")
            for f in r["config_files"]:
                state = "presente" if f["exists"] else "assente"
                extra = "" if f["writable"] else ", non riscrivibile a programma"
                lines.append(
                    f"- config: `{f['path']}` — {state}, {f['format']}, "
                    f"chiave `{f['key']}`{extra}"
                )
            for s in r["servers"]:
                flag = "" if s["enabled"] else " (disabilitato)"
                kind = " [builtin]" if s["builtin"] else ""
                lines.append(f"- server: `{s['name']}` — {s['transport']}{flag}{kind}")
            for s in r["skills"]:
                if not s["exists"]:
                    continue
                lines.append(
                    f"- skill: `{s['path']}` — {len(s['ok'])} valide, "
                    f"{len(s['broken'])} rotte"
                )
                if verbose:
                    for broken in s["broken"]:
                        lines.append(f"  - rotto: `{broken['name']}` → `{broken['target']}`")
            if r["verify"]:
                lines.append(f"- verifica: `{r['verify']}`")
            if r["notes"]:
                lines.append(f"- nota: {r['notes']}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--harness", help="limita a un harness (id della specifica)")
    parser.add_argument("--report", action="store_true", help="dettaglio per harness")
    parser.add_argument("-v", "--verbose", action="store_true", help="elenca ogni difetto")
    parser.add_argument("--json", action="store_true", help="output JSON")
    args = parser.parse_args(argv)

    targets = list(HARNESSES)
    if args.harness:
        harness = BY_ID.get(args.harness)
        if harness is None:
            print(
                f"harness sconosciuto: {args.harness}\nnoti: "
                + ", ".join(sorted(BY_ID)),
                file=sys.stderr,
            )
            return 1
        targets = [harness]

    results = [inspect(h) for h in targets]
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(render(results, args.report, args.verbose), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
