#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Applica la selezione dei gruppi Guardrails alle skill installate su disco.

Perché serve
------------
L'installer BMad copia **tutte** le skill del modulo: il formato `module.yaml`
non ha modo di escluderne alcune dalla copia (`post-install-notes` è un messaggio,
non un hook eseguibile). Le spunte raccolte durante l'installazione sarebbero
quindi solo una dichiarazione di intenti: le figure non volute resterebbero sul
disco, si attiverebbero da sole alla prima frase che assomiglia alla loro
`description`, e comparirebbero nell'elenco delle skill.

Questo script chiude quella distanza subito dopo la copia: sposta le skill dei
gruppi non spuntati in `_bmad/grl/.disabled/`, dove Claude Code non le carica.
Per l'utente il risultato è indistinguibile dal non averle mai installate.

Reversibile, non distruttivo
----------------------------
Niente viene cancellato: le cartelle vengono spostate. Rispuntare un gruppo e
rieseguire il setup le riporta esattamente da dove erano venute — lo script
ripristina prima e disattiva dopo, nella stessa passata.

Idempotente
-----------
Se lo stato su disco coincide già con la selezione, non tocca nulla ed esce con
`changed: false`. Rieseguirlo non ha effetti collaterali.

Skill sconosciute
-----------------
Una cartella `grl-*` che non compare né in `always` né in un gruppo di
`groups.toml` non viene toccata: è segnalata fra i `warnings` e lasciata attiva.
Non si disattiva ciò che non si sa cosa sia.

Codici di uscita: 0 = successo, 1 = errore d'uso o di validazione, 2 = errore d'ambiente.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tomllib
from pathlib import Path

sys.dont_write_bytecode = True

MODULE_CODE = "grl"
DISABLED_DIRNAME = ".disabled"

# Cartelle in cui gli installer depositano le skill, relative alla radice del progetto.
# Sono tutte facoltative: si considerano solo quelle che esistono davvero.
DEFAULT_SKILL_ROOTS = (
    ".claude/skills",
    ".agents/skills",
    ".cline/skills",
    ".opencode/skill",
    f"_bmad/{MODULE_CODE}",
)


def fail(message: str, code: int = 1) -> int:
    print(json.dumps({"status": "error", "error": message}, indent=2, ensure_ascii=False))
    return code


def load_groups_map(path: Path) -> tuple[list[str], dict[str, list[str]], dict[str, str]]:
    """Legge groups.toml → (always, {group_id: [skill]}, {group_id: label})."""
    with path.open("rb") as stream:
        data = tomllib.load(stream)

    always = data.get("always", [])
    if not isinstance(always, list) or not all(isinstance(s, str) and s for s in always):
        raise ValueError("`always` deve essere una lista di nomi di skill")

    groups: dict[str, list[str]] = {}
    labels: dict[str, str] = {}
    entries = data.get("groups", [])
    if not isinstance(entries, list) or not entries:
        raise ValueError("groups.toml non contiene alcun gruppo")

    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("ogni gruppo deve essere una tabella")
        group_id = entry.get("id")
        skills = entry.get("skills")
        if not isinstance(group_id, str) or not group_id:
            raise ValueError("gruppo senza `id`")
        if group_id in groups:
            raise ValueError(f"gruppo duplicato: {group_id}")
        if not isinstance(skills, list) or not all(isinstance(s, str) and s for s in skills):
            raise ValueError(f"`skills` non valido per il gruppo {group_id}")
        groups[group_id] = skills
        labels[group_id] = entry.get("label", group_id)

    # Ogni skill deve comparire una volta sola: un doppione qui produrrebbe una
    # disattivazione che dipende dall'ordine dei gruppi, cioè un comportamento a caso.
    seen: dict[str, str] = {s: "always" for s in always}
    for group_id, skills in groups.items():
        for skill in skills:
            if skill in seen:
                raise ValueError(
                    f"la skill {skill} compare sia in {seen[skill]} sia in {group_id}"
                )
            seen[skill] = group_id

    return always, groups, labels


def parse_selection(raw: str, groups: dict[str, list[str]]) -> list[str]:
    """Normalizza il valore di --groups. `all` (o vuoto) significa tutti i gruppi."""
    tokens = [t.strip() for t in raw.replace(";", ",").split(",")]
    tokens = [t for t in tokens if t]
    if not tokens or "all" in tokens or "tutti" in tokens:
        return sorted(groups)
    unknown = [t for t in tokens if t not in groups]
    if unknown:
        raise ValueError(
            f"gruppi sconosciuti: {', '.join(sorted(unknown))}. "
            f"Ammessi: {', '.join(sorted(groups))}, oppure `all`."
        )
    return sorted(set(tokens))


def strip_tables(text: str, matches) -> str:
    """Rimuove le tabelle TOML il cui header soddisfa `matches(header)`.

    Stessa forma di register-agents.py: in TOML una tabella dichiarata due volte è
    un errore di parsing, quindi la vecchia va via prima di riscrivere.
    """
    out: list[str] = []
    skipping = False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("[") and "]" in stripped:
            header = stripped[1 : stripped.index("]")].strip()
            skipping = matches(header)
        if not skipping:
            out.append(line)
    return "".join(out)


def persist_selection(bmad_dir: Path, selected: list[str], dry_run: bool) -> Path:
    """Scrive la selezione in `[modules.grl] enabled_groups` di custom/config.toml.

    Il layer `custom/` è quello che l'installer non rigenera, ed è di team: la scelta
    dei gruppi vale per il progetto, non per la singola persona (a differenza di
    `strictness_override`, che vive nel layer utente). Serve a due cose: rieseguire
    il setup partendo dalla scelta già fatta, e permettere alle skill di sapere cosa
    è attivo senza guardare il disco.
    """
    config = bmad_dir / "custom" / "config.toml"
    text = config.read_text(encoding="utf-8") if config.is_file() else ""
    text = strip_tables(text, lambda header: header == f"modules.{MODULE_CODE}")
    if text and not text.endswith("\n"):
        text += "\n"
    if text.strip():
        text += "\n"
    values = ", ".join(f'"{group}"' for group in selected)
    text += (
        "# Gruppi Guardrails attivi in questo progetto, scelti durante l'installazione.\n"
        "# Le skill dei gruppi esclusi stanno in _bmad/grl/.disabled/: per riattivarle\n"
        "# riesegui grl-setup e rispuntale, non spostarle a mano.\n"
        f"[modules.{MODULE_CODE}]\n"
        f"enabled_groups = [{values}]\n"
    )
    try:
        tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise ValueError(f"il risultato per {config} non è TOML valido: {error}")
    if not dry_run:
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(text, encoding="utf-8")
    return config


def root_slug(project_root: Path, root: Path) -> str:
    """Etichetta stabile della root, usata come sottocartella della quarantena."""
    relative = root.relative_to(project_root)
    return str(relative).replace("/", "__").lstrip(".") or "root"


def discover_roots(project_root: Path, extra: list[str]) -> list[Path]:
    candidates = list(DEFAULT_SKILL_ROOTS) + list(extra or [])
    roots: list[Path] = []
    for candidate in candidates:
        path = (project_root / candidate).resolve()
        if path.is_dir() and path not in roots and project_root in path.parents:
            roots.append(path)
    return roots


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Disattiva e riattiva le skill Guardrails secondo i gruppi scelti in installazione."
    )
    parser.add_argument(
        "--project-root", required=True,
        help="Radice del progetto che contiene _bmad/ (percorso reale, non {project-root}).",
    )
    parser.add_argument(
        "--groups", required=True,
        help='Gruppi attivi, separati da virgola (es. "governance,web"). `all` li tiene tutti.',
    )
    parser.add_argument(
        "--groups-map",
        help="groups.toml da cui leggere la mappa gruppo→skill. Default: ./assets/groups.toml accanto allo script.",
    )
    parser.add_argument(
        "--skills-root", action="append", default=[],
        help="Cartella aggiuntiva di skill installate, relativa alla radice del progetto. Ripetibile.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Mostra cosa verrebbe spostato senza toccare il disco.",
    )
    args = parser.parse_args()

    if "{project-root}" in args.project_root:
        return fail(
            "token '{project-root}' non risolto in --project-root: passa il percorso reale del progetto."
        )

    project_root = Path(args.project_root).resolve()
    bmad_dir = project_root / "_bmad"
    if not bmad_dir.is_dir():
        return fail(f"_bmad/ non trovato in {project_root}: il progetto non ha un'installazione BMad.", 2)

    groups_map = (
        Path(args.groups_map).resolve()
        if args.groups_map
        else (Path(__file__).resolve().parent.parent / "assets" / "groups.toml")
    )
    if not groups_map.is_file():
        return fail(f"mappa dei gruppi non trovata: {groups_map}", 2)

    try:
        always, groups, labels = load_groups_map(groups_map)
        selected = parse_selection(args.groups, groups)
    except (OSError, ValueError, tomllib.TOMLDecodeError) as error:
        return fail(str(error))

    keep = set(always)
    for group_id in selected:
        keep.update(groups[group_id])
    known = set(always) | {skill for skills in groups.values() for skill in skills}

    disabled_root = bmad_dir / MODULE_CODE / DISABLED_DIRNAME
    roots = discover_roots(project_root, args.skills_root)
    if not roots:
        return fail(
            "nessuna cartella di skill trovata: il modulo non risulta installato in questo progetto.", 2
        )

    warnings: list[str] = []
    restored: list[str] = []
    quarantined: list[str] = []

    # 1. Ripristino: ciò che è in quarantena e torna a essere richiesto rientra
    #    nella root da cui era stato tolto. Prima del passo 2, così un gruppo
    #    riacceso è già al suo posto quando il roster viene riscritto.
    if disabled_root.is_dir():
        for slot in sorted(p for p in disabled_root.iterdir() if p.is_dir()):
            for skill_dir in sorted(p for p in slot.iterdir() if p.is_dir()):
                if skill_dir.name not in keep:
                    continue
                target_root = next(
                    (r for r in roots if root_slug(project_root, r) == slot.name), None
                )
                if target_root is None:
                    warnings.append(
                        f"{skill_dir.name}: la cartella di origine `{slot.name}` non esiste più, resta in quarantena"
                    )
                    continue
                destination = target_root / skill_dir.name
                if destination.exists():
                    warnings.append(
                        f"{skill_dir.name}: già presente in {target_root}, la copia in quarantena è stata lasciata lì"
                    )
                    continue
                if not args.dry_run:
                    shutil.move(str(skill_dir), str(destination))
                restored.append(f"{skill_dir.name} → {destination}")

    # 2. Quarantena: ciò che è installato ma non è più richiesto esce dalle
    #    cartelle che gli agenti leggono.
    for root in roots:
        slot = disabled_root / root_slug(project_root, root)
        for skill_dir in sorted(root.glob(f"{MODULE_CODE}-*")):
            if not skill_dir.is_dir() or skill_dir.name == DISABLED_DIRNAME:
                continue
            if skill_dir.name in keep:
                continue
            if skill_dir.name not in known:
                warnings.append(
                    f"{skill_dir.name}: non compare in {groups_map.name}, lasciata attiva"
                )
                continue
            destination = slot / skill_dir.name
            if not args.dry_run:
                if destination.exists():
                    # Copia rimasta da una disattivazione precedente: quella su disco
                    # è la più recente e vince.
                    shutil.rmtree(destination)
                slot.mkdir(parents=True, exist_ok=True)
                shutil.move(str(skill_dir), str(destination))
            quarantined.append(f"{skill_dir.name} ({root_slug(project_root, root)})")

    active = sorted(
        {
            skill_dir.name
            for root in roots
            for skill_dir in root.glob(f"{MODULE_CODE}-*")
            if skill_dir.is_dir() and skill_dir.name in known
        }
        if not args.dry_run
        else keep & known
    )

    try:
        config_file = persist_selection(bmad_dir, selected, args.dry_run)
    except (OSError, ValueError) as error:
        return fail(str(error))

    print(json.dumps({
        "status": "success",
        "dry_run": args.dry_run,
        "changed": bool(restored or quarantined),
        "config_file": str(config_file),
        "groups_selected": selected,
        "groups_labels": [labels[g] for g in selected],
        "skills_active": active,
        "skills_quarantined": quarantined,
        "skills_restored": restored,
        "disabled_dir": str(disabled_root),
        "roots": [str(r) for r in roots],
        "warnings": warnings,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
