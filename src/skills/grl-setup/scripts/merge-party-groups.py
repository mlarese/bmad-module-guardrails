#!/usr/bin/env python3
"""Installa i gruppi tematici Guardrails nell'override di bmad-party-mode.

Il file generato vive in `_bmad/custom/`, il layer di team che l'installer BMad
non rigenera. Solo il blocco fra i marker Guardrails viene sostituito: gruppi e
impostazioni creati dall'utente restano intatti.
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path

sys.dont_write_bytecode = True

BEGIN = "# >>> grl:party-groups — generato da grl-setup, non modificare a mano >>>"
END = "# <<< grl:party-groups <<<"


def quote(value: str) -> str:
    escaped = (
        str(value)
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


def strip_block(text: str) -> str:
    begin = text.find(BEGIN)
    if begin < 0:
        return text
    end = text.find(END, begin)
    if end < 0:
        raise ValueError("marker di fine party-groups mancante")
    end += len(END)
    if end < len(text) and text[end] == "\n":
        end += 1
    return text[:begin] + text[end:]


def load_groups(source: Path) -> list[dict]:
    with source.open("rb") as stream:
        data = tomllib.load(stream)
    groups = data.get("workflow", {}).get("party_groups", [])
    if not isinstance(groups, list) or not groups:
        raise ValueError("la sorgente non contiene workflow.party_groups")
    required = ("id", "name", "scene", "members")
    seen: set[str] = set()
    for group in groups:
        if not isinstance(group, dict):
            raise ValueError("ogni party group deve essere una tabella")
        missing = [key for key in required if not group.get(key)]
        if missing:
            raise ValueError(f"party group incompleto, mancano: {', '.join(missing)}")
        if group["id"] in seen:
            raise ValueError(f"party group duplicato: {group['id']}")
        seen.add(group["id"])
        if not isinstance(group["members"], list) or not all(
            isinstance(member, str) and member for member in group["members"]
        ):
            raise ValueError(f"members non valido per {group['id']}")
        if "memory" in group and not isinstance(group["memory"], bool):
            raise ValueError(f"memory non booleano per {group['id']}")
        if "requires" in group and (
            not isinstance(group["requires"], list)
            or not all(isinstance(item, str) and item for item in group["requires"])
        ):
            raise ValueError(f"requires non valido per {group['id']}")
    return groups


def filter_groups(groups: list[dict], wanted: set[str]) -> tuple[list[dict], list[str]]:
    """Tiene solo i membri Guardrails attivi, lasciando intatti quelli di altri moduli.

    Un membro `grl-*` che non è fra gli attivi viene tolto: convocarlo aprirebbe una
    stanza con un posto vuoto. Un gruppo che resta senza alcun membro Guardrails viene
    saltato del tutto — sarebbe una stanza tematica del modulo senza il modulo dentro.
    I membri di altri moduli (es. `bmad-agent-ux-designer`) non si toccano: la loro
    presenza dipende da quel modulo, non da questa selezione.
    """
    kept: list[dict] = []
    skipped: list[str] = []
    for group in groups:
        required = group.get("requires") or []
        if required and not any(member in wanted for member in required):
            skipped.append(group["id"])
            continue
        members = [
            member
            for member in group["members"]
            if not member.startswith("grl-") or member in wanted
        ]
        if not any(member.startswith("grl-") for member in members):
            skipped.append(group["id"])
            continue
        kept.append({**group, "members": members})
    return kept, skipped


def render(groups: list[dict]) -> str:
    lines = [BEGIN, "# I gruppi vengono sostituiti in modo idempotente a ogni grl-setup.", ""]
    for group in groups:
        lines.extend(
            [
                "[[workflow.party_groups]]",
                f"id = {quote(group['id'])}",
                f"name = {quote(group['name'])}",
                f"scene = {quote(group['scene'])}",
                "members = [" + ", ".join(quote(member) for member in group["members"]) + "]",
                f"memory = {'true' if group.get('memory', False) else 'false'}",
                "",
            ]
        )
    lines.append(END)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument(
        "--only-agents",
        help=(
            "Figure Guardrails attive, separate da virgola. I membri grl-* fuori da questo "
            "elenco escono dai gruppi, e un gruppo che resta senza figure Guardrails non "
            "viene installato. Ometti per installare i gruppi come sono."
        ),
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    source = Path(args.source).resolve()
    bmad_dir = project_root / "_bmad"
    if not bmad_dir.is_dir():
        print(json.dumps({"status": "error", "error": f"_bmad non trovato in {project_root}"}, ensure_ascii=False))
        return 2
    if not source.is_file():
        print(json.dumps({"status": "error", "error": f"sorgente non trovata: {source}"}, ensure_ascii=False))
        return 2

    skipped: list[str] = []
    try:
        groups = load_groups(source)
        if args.only_agents:
            wanted = {
                name.strip()
                for name in args.only_agents.replace(";", ",").split(",")
                if name.strip()
            }
            groups, skipped = filter_groups(groups, wanted)
            if not groups:
                raise ValueError(
                    "--only-agents non lascia alcun gruppo installabile: nessuna figura "
                    "Guardrails compare nei gruppi tematici."
                )
        target = bmad_dir / "custom" / "bmad-party-mode.toml"
        existing = target.read_text(encoding="utf-8") if target.is_file() else ""
        updated = strip_block(existing)
        if updated and not updated.endswith("\n"):
            updated += "\n"
        if updated.strip():
            updated += "\n"
        updated += render(groups)
        tomllib.loads(updated)
    except (OSError, tomllib.TOMLDecodeError, ValueError) as error:
        print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False))
        return 1

    if not args.dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(updated, encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "success",
                "dry_run": args.dry_run,
                "groups": [group["id"] for group in groups],
                "groups_skipped": skipped,
                "target": str(target),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
