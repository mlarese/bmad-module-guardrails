#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6.0"]
# ///
"""Genera i repository dei moduli tematici Guardrails a partire da questo repository.

Perché serve
------------
Il bundle `grl` installa dodici figure e sette workflow in un colpo solo. Chi vuole
solo la governance normativa, o solo il presidio ingegneristico, non ha motivo di
portarsi le altre dieci figure. La soluzione è un repository per area — ma scritto a
mano diventerebbe subito divergente dal bundle.

Questo script tiene una sola fonte: le skill in `src/skills/`, il manifesto in
`src/module.yaml` e la mappa in `src/module-topology.yaml`. Da lì produce in `dist/`
un albero completo per ogni modulo tematico, pronto per essere committato nel suo
repository. I repository derivati non si modificano a mano: si rigenerano.

Cosa fa, in ordine
------------------
1. Copia le skill del modulo, prendendo **solo i file tracciati da git** — così
   referti di analisi, cache ed eval run restano fuori senza doverli elencare.
2. Duplica le tre skill del core (`grl-setup`, `grl-profile`, `grl-board`)
   rinominandole con il codice del modulo (`grg-setup`, …) e riscrive ogni
   riferimento testuale a quei tre nomi. I codici delle figure (`grl-agent-*`) e la
   memoria condivisa (`grl-shared`) restano invariati: è il punto in cui due moduli
   installati insieme si incontrano.
3. Filtra il roster in `module.yaml`, le righe di `module-help.csv`, i gruppi di
   `party-groups.toml` (con i membri ridotti alle figure presenti) e la lista di
   skill in `marketplace.json`.
4. Genera `README.md`, `CLAUDE.md` e `.gitignore` del repository derivato.

Limite dichiarato: bundle e moduli tematici installano skill con lo stesso nome
(`grl-agent-privacy` sta identica in `grl` e in `grg`). Non vanno installati insieme
nello stesso progetto.

Codici di uscita: 0 = successo, 1 = errore d'uso o di validazione, 2 = errore d'ambiente.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - dipende dall'ambiente, non dalla logica
    print("Serve PyYAML: pip install PyYAML", file=sys.stderr)
    raise SystemExit(2)


# Estensioni su cui si applica la riscrittura dei nomi del core. Tutto il resto
# viene copiato byte per byte.
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".toml", ".csv", ".json", ".py", ".txt", ".html"}

# Un party group con meno di due membri non è una stanza: si omette.
MIN_PARTY_MEMBERS = 2

# Il bundle conta dodici figure e lo dice ovunque nei testi del core. In un modulo
# tematico quel numero è falso, e un numero falso in una skill è un'istruzione
# sbagliata. Con più figure si sostituisce il numerale; con una sola si toglie e
# resta il plurale generico, che è impreciso ma non falso — riscrivere l'accordo
# verbale di frasi arbitrarie non è automatizzabile.
NUMERALS = {2: "due", 3: "tre", 4: "quattro", 5: "cinque", 6: "sei", 7: "sette"}

# Nota appesa a ogni figura del modulo: le tabelle di handoff citano colleghe che
# qui non sono installate, e senza questa riga l'agente rimanda a un vuoto.
OUT_OF_MODULE_NOTE = """

## Figure fuori da questo modulo

Le tabelle qui sopra citano anche figure Guardrails che questo modulo non installa.
Qui sono installate: {installed}.

Quando il tema appartiene a una figura assente, il confine resta valido: **dichiara che
il tema esce dal perimetro, nomina la competenza che servirebbe e prosegui su ciò che
resta.** Non improvvisare il parere della figura mancante e non fermare il lavoro. Il
modulo che la contiene si installa a parte; il bundle completo `grl` le contiene tutte.
"""


class BuildError(Exception):
    """Errore di validazione: la build si ferma e spiega cosa manca."""


# --------------------------------------------------------------------------- #
# Lettura della fonte
# --------------------------------------------------------------------------- #


def load_topology(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    for key in ("bundle", "core", "modules"):
        if key not in data:
            raise BuildError(f"{path}: manca la chiave `{key}`")
    return data


def load_module_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def tracked_files(source_root: Path, relative_dir: str) -> list[Path]:
    """File tracciati da git sotto `relative_dir`, come percorsi relativi alla radice."""
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", relative_dir],
        cwd=source_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise BuildError(f"git ls-files {relative_dir}: {result.stderr.strip()}")
    return [Path(p) for p in result.stdout.split("\0") if p]


# --------------------------------------------------------------------------- #
# Riscrittura dei nomi del core
# --------------------------------------------------------------------------- #


def core_renames(core_skills: list[str], code: str) -> dict[str, str]:
    """`grl-setup` → `grg-setup`, e così per profilo e collegio."""
    renames = {}
    for skill in core_skills:
        suffix = skill.split("-", 1)[1]
        renames[skill] = f"{code}-{suffix}"
    return renames


def adapt_counts(text: str, count: int) -> str:
    """Riporta al numero reale di figure i conteggi scritti per il bundle.

    Tocca solo le costruzioni in cui `dodici` è accostato alle figure o alle loro
    chiavi di config: «dodici documenti» dentro l'esempio di Enzo, o «dodici pagine»
    in una reference di grl-web, restano quello che sono.
    """
    numeral = NUMERALS.get(count)

    def replace_all_of(match: re.Match) -> str:
        return f"tutte e {numeral}" if numeral else "tutte"

    def replace_noun(match: re.Match) -> str:
        space, noun = match.group(1), match.group(2)
        if numeral:
            return f"{numeral}{space}{noun}"
        return noun

    text = re.sub(r"una\s+delle\s+dodici\s+figure", "una delle figure", text)
    text = re.sub(r"tutte\s+e\s+dodici", replace_all_of, text)
    text = re.sub(r"\bdodici(\s+)(figure|chiavi)", replace_noun, text)
    return text


def adapt_board(text: str, count: int) -> str:
    """L'unica frase del collegio che il numerale da solo non salva.

    «punta a due-quattro figure» è un consiglio sensato con dodici figure in campo e
    assurdo con due: qui la selezione non è più il problema.
    """
    if count > 4:
        return text
    return text.replace(
        "punta a **due-quattro figure**, e se le convochi tutte devi poter dire cosa "
        "ciascuna ha di decisivo da dire su *questo* artefatto.",
        "**convoca solo chi ha qualcosa di decisivo da dire su *questo* artefatto**, e se "
        "le convochi tutte devi poter dire cosa ciascuna ci aggiunge.",
    )


def filter_tables(text: str, installed_codes: set[str], installed_names: set[str]) -> str:
    """Toglie dalle tabelle markdown le righe che parlano solo di figure assenti.

    Due forme nel collegio: la tabella di selezione, che cita le skill (`grl-agent-*`),
    e la tabella dei confini, che cita i nomi propri. Una riga che nomina almeno una
    figura installata resta: descrive un confine, e il confine vale comunque.
    """
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            lines.append(line)
            continue

        codes = set(re.findall(r"grl-agent-[a-z-]+", stripped))
        if codes:
            if codes & installed_codes:
                lines.append(line)
            continue

        names = {n for n in installed_names | ALL_FIGURE_NAMES if re.search(rf"\b{n}\b", stripped)}
        if names and not (names & installed_names):
            continue
        lines.append(line)
    return "\n".join(lines)


# Popolato all'avvio della build dai nomi del roster completo: serve a distinguere
# «riga che parla di figure» da «riga di una tabella qualunque».
ALL_FIGURE_NAMES: set[str] = set()


def rewrite(text: str, renames: dict[str, str]) -> str:
    """Sostituisce i nomi del core, senza toccare identificatori che li contengono.

    Il confine è necessario: `grl-profile` non deve trasformare `grl-profile-x`, e
    `grl-board` non deve toccare `grl-boardroom` se un giorno esistesse.
    """
    for old, new in renames.items():
        text = re.sub(rf"(?<![\w-]){re.escape(old)}(?![\w-])", new, text)
    return text


# --------------------------------------------------------------------------- #
# Copia delle skill
# --------------------------------------------------------------------------- #


def copy_skill(
    source_root: Path,
    out_root: Path,
    skill: str,
    target_name: str,
    renames: dict[str, str],
    module_code: str,
    context: dict,
) -> int:
    """Copia una skill nel repository derivato. Ritorna il numero di file copiati.

    `context` porta ciò che serve per adattare i testi al perimetro del modulo:
    numero di figure, codici e nomi installati, elenco leggibile per la nota.
    """
    files = tracked_files(source_root, f"src/skills/{skill}")
    if not files:
        raise BuildError(f"skill `{skill}`: nessun file tracciato da git")

    is_board = skill == "grl-board"
    is_figure = skill.startswith("grl-agent-")
    prefix = Path("src/skills") / skill

    for rel in files:
        destination = out_root / "src" / "skills" / target_name / rel.relative_to(prefix)
        destination.parent.mkdir(parents=True, exist_ok=True)
        source_file = source_root / rel

        if rel.suffix not in TEXT_SUFFIXES:
            shutil.copy2(source_file, destination)
            continue

        text = rewrite(source_file.read_text(encoding="utf-8"), renames)
        text = adapt_counts(text, context["count"])

        if rel.name == "customize.toml":
            text = re.sub(r'^module = "grl"$', f'module = "{module_code}"', text, flags=re.M)

        if rel.name == "SKILL.md" and is_board:
            # Solo nel collegio: la tabella dice chi convocare, e una figura non
            # installata non è convocabile. Nelle figure le stesse righe dicono
            # invece «questo non è mio dominio» — un confine che vale comunque, e
            # che togliendolo lascerebbe la figura libera di invadere il tema.
            text = filter_tables(text, context["codes"], context["names"])
            text = adapt_board(text, context["count"])

        if rel.name == "SKILL.md" and (is_board or is_figure):
            text = text.rstrip("\n") + OUT_OF_MODULE_NOTE.format(installed=context["listing"])

        destination.write_text(text, encoding="utf-8")

    return len(files)


# --------------------------------------------------------------------------- #
# Manifesto del modulo
# --------------------------------------------------------------------------- #


def figures(bundle_agents: list[dict], skills: list[str]) -> list[dict]:
    """Gli agenti del bundle che appartengono a questo modulo, nell'ordine del bundle."""
    wanted = set(skills)
    return [agent for agent in bundle_agents if agent["code"] in wanted]


def workflow_skills(skills: list[str], agent_codes: set[str]) -> list[str]:
    return [s for s in skills if s not in agent_codes]


def render_agents_block(agents: list[dict], module_code: str) -> str:
    blocks = []
    for agent in agents:
        entry = dict(agent)
        entry["module"] = module_code
        dumped = yaml.dump(
            [entry],
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=10**6,
        )
        blocks.append(dumped.rstrip("\n"))
    return "\n\n".join(blocks)


def render_greeting(module: dict, agents: list[dict], renames: dict[str, str]) -> str:
    names = [f"{a['name']} ({a['title'].lower()})" for a in agents]
    roster = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " e " + names[-1]
    profile_skill = renames["grl-profile"]
    single = len(agents) == 1

    entrance = (
        f"{roster} entra nel roster e si può convocare per nome."
        if single
        else f"{roster} entrano nel roster e si possono convocare per nome."
    )
    blind = (
        "la figura parte cieca e parla per luoghi comuni; con il profilo sa cosa non ti "
        "riguarda, che è il suo output più utile."
        if single
        else "le figure partono cieche e parlano per luoghi comuni; con il profilo sanno cosa "
        "non ti riguarda, che è il loro output più utile."
    )
    return (
        f"{module['name']} è installato: {entrance}\n\n"
        f"Passo successivo consigliato: esegui `{profile_skill}`. Senza il profilo di progetto "
        f"{blind}\n\n"
        f"Il profilo vive in `_bmad/memory/grl-shared/` ed è condiviso con gli altri moduli "
        f"Guardrails: si compila una volta sola."
    )


def render_module_yaml(module: dict, agents: list[dict], renames: dict[str, str], version: str) -> str:
    code = module["code"]
    setup_skill = renames["grl-setup"]
    profile_skill = renames["grl-profile"]
    board_skill = renames["grl-board"]

    return f"""# Manifesto del modulo {module['name']} ({code}).
#
# GENERATO da tools/build_modules.py nel repository bmad-module-guardrails.
# Non modificare qui: le modifiche si fanno nella fonte e poi si rigenera.
#
# Questa è la copia che legge l'installer BMad: la cerca in src/module.yaml.
# La copia in src/skills/{setup_skill}/assets/module.yaml resta per
# l'installazione manuale via {setup_skill}: le due sono identiche.

code: {code}
name: {module['name']}
description: {json.dumps(module['description'], ensure_ascii=False)}
module_version: {version}
default_selected: false

module_greeting: >
{indent_block(render_greeting(module, agents, renames), '  ')}

# --- Contesto di esecuzione ---------------------------------------------------
# Nessuna variabile di configurazione del modulo: tutto il contesto vive nella
# memoria condivisa del progetto (_bmad/memory/grl-shared/project-profile.md).
# La severità si deriva dalla criticità dichiarata nel profilo di progetto.
#
# La cartella della memoria condivisa NON va creata dal setup: la crea
# {profile_skill} alla prima esecuzione.
#
# Questo modulo è una porzione del bundle Guardrails (`grl`). Bundle e moduli
# tematici installano skill con lo stesso nome: non vanno installati insieme
# nello stesso progetto.

post-install-notes: >
  Primo passo: esegui `{profile_skill}`. Sono otto campi, pochi minuti, quasi tutti
  pre-compilati leggendo il repository; l'unico che devi dichiarare tu è la criticità
  del progetto (hobby/prototipo · interno · produzione con clienti · regolamentato),
  perché è quella che regola quanto sarà severa ogni figura.

  Poi puoi chiamare una figura per nome, oppure usare `{board_skill}` per farle
  guardare tutte insieme lo stesso artefatto.

  Se ti servono anche le figure delle altre aree, il bundle completo `grl` le
  contiene tutte: https://github.com/mlarese/bmad-module-guardrails

# --- Roster degli agenti -----------------------------------------------------
# `code`, `name`, `title`, `icon` e `description` sono copiati verbatim dal blocco
# [agent] del customize.toml di ciascuna skill: quelli restano la fonte di verità.

agents:
{indent_block(render_agents_block(agents, code), '  ')}
"""


def indent_block(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line.strip() else line for line in text.split("\n"))


# --------------------------------------------------------------------------- #
# Catalogo di help
# --------------------------------------------------------------------------- #


def filter_help_csv(
    source: str, skills: set[str], module_name: str, renames: dict[str, str], count: int
) -> str:
    lines = source.splitlines()
    kept = [lines[0]]
    for line in lines[1:]:
        if not line.strip():
            continue
        # La seconda colonna è il nome della skill; le prime tre non contengono virgole
        # quotate, quindi lo split posizionale basta e non serve il modulo csv.
        parts = line.split(",", 2)
        if len(parts) < 3:
            continue
        if parts[1] not in skills:
            continue
        rewritten = adapt_counts(rewrite(line, renames), count)
        rewritten = rewritten.replace("Guardrails,", f"{module_name},", 1)
        rewritten = rewritten.replace("Installa Guardrails,", f"Installa {module_name},", 1)
        kept.append(rewritten)
    return "\n".join(kept) + "\n"


# --------------------------------------------------------------------------- #
# Gruppi di party mode
# --------------------------------------------------------------------------- #


def parse_party_blocks(source: str) -> tuple[str, list[tuple[str, str]]]:
    """Divide il file in intestazione e blocchi `[[workflow.party_groups]]`.

    Il parsing è testuale, non via tomllib, per conservare commenti e formattazione
    originali: dei blocchi va cambiata solo la riga `members`.
    """
    marker = "[[workflow.party_groups]]"
    chunks = source.split(marker)
    head = chunks[0]
    blocks = []
    for chunk in chunks[1:]:
        match = re.search(r'^id\s*=\s*"([^"]+)"', chunk, flags=re.M)
        if not match:
            raise BuildError("party-groups.toml: un blocco non ha `id`")
        blocks.append((match.group(1), marker + chunk))
    return head, blocks


def filter_party_groups(
    source: str,
    wanted_ids: list[str],
    installed_agents: set[str],
    module_name: str,
) -> tuple[str, list[str]]:
    """Tiene i gruppi del modulo e riduce i membri alle figure installate.

    I membri `bmad-agent-*` restano: appartengono a BMM e sono facoltativi.
    Un gruppo che resta con meno di due membri viene scartato.
    """
    head, blocks = parse_party_blocks(source)
    kept: list[str] = []
    dropped: list[str] = []

    by_id = {group_id: block for group_id, block in blocks}
    for group_id in wanted_ids:
        block = by_id.get(group_id)
        if block is None:
            raise BuildError(f"party-groups.toml: gruppo `{group_id}` non trovato")

        match = re.search(r"^members\s*=\s*\[(.*?)\]", block, flags=re.M | re.S)
        if not match:
            raise BuildError(f"gruppo `{group_id}`: manca `members`")
        members = re.findall(r'"([^"]+)"', match.group(1))
        filtered = [m for m in members if m in installed_agents or m.startswith("bmad-agent-")]
        own = [m for m in filtered if not m.startswith("bmad-agent-")]

        if len(own) < MIN_PARTY_MEMBERS:
            dropped.append(group_id)
            continue

        rendered = "[" + ", ".join(f'"{m}"' for m in filtered) + "]"
        kept.append(block[: match.start()] + f"members = {rendered}" + block[match.end() :])

    header = (
        f"# Gruppi tematici di bmad-party-mode installati dal setup di {module_name}.\n"
        "#\n"
        "# GENERATO da tools/build_modules.py: i membri sono ridotti alle figure che\n"
        "# questo modulo installa. Le figure delle altre aree Guardrails restano fuori.\n"
        "#\n"
        "# Sono override di team in {project-root}/_bmad/custom/bmad-party-mode.toml:\n"
        "# nessun default_party viene imposto, ogni gruppo si convoca con `--party <id>`.\n\n"
    )
    if not kept:
        return header + "# Nessun gruppo: il modulo installa troppe poche figure per una stanza.\n", dropped
    return header + "\n".join(block.rstrip() + "\n" for block in kept), dropped


# --------------------------------------------------------------------------- #
# Vetrine del repository derivato
# --------------------------------------------------------------------------- #


def render_marketplace(module: dict, skills: list[str], version: str) -> str:
    data = {
        "name": module["repo"].replace("bmad-module-", ""),
        "owner": "mlarese",
        "description": f"{module['name']}: {module['purpose'][0].lower()}{module['purpose'][1:]}",
        "plugins": [
            {
                "name": module["code"],
                "source": "./src",
                "description": module["description"],
                "version": version,
                "author": "mlarese",
                "homepage": f"https://github.com/mlarese/{module['repo']}",
                "repository": f"https://github.com/mlarese/{module['repo']}",
                "license": "MIT",
                "skills": [f"src/skills/{s}" for s in skills],
            }
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def render_readme(
    module: dict,
    agents: list[dict],
    workflows: list[str],
    help_rows: dict[str, list[tuple[str, str]]],
    renames: dict[str, str],
    dropped_groups: list[str],
    party_ids: list[str],
) -> str:
    code = module["code"]
    setup_skill = renames["grl-setup"]
    profile_skill = renames["grl-profile"]
    board_skill = renames["grl-board"]

    figure_rows = "\n".join(
        f"| {a['icon']} {a['name']} | {a['title']} | `{a['code']}` | {short(a['description'])} |"
        for a in agents
    )

    workflow_lines = []
    for skill in [setup_skill, profile_skill, board_skill] + list(workflows):
        for display, description in help_rows.get(skill, []):
            workflow_lines.append(f"| `{skill}` | {display} | {description} |")
    workflow_rows = "\n".join(workflow_lines)

    party_section = ""
    live_groups = [g for g in party_ids if g not in dropped_groups]
    if live_groups:
        listed = "\n".join(f"- `bmad-party-mode --party {g}`" for g in live_groups)
        party_section = (
            "\n## Stanze di party mode\n\n"
            f"{setup_skill} installa le stanze del modulo in "
            "`_bmad/custom/bmad-party-mode.toml`, senza cambiare la stanza di default:\n\n"
            f"{listed}\n"
        )

    return f"""# {module['name']} (`{code}`)

{module['description']}

Modulo BMad. È una porzione del bundle [Guardrails](https://github.com/mlarese/bmad-module-guardrails):
stesse figure, stesso comportamento, solo l'area {module['name'].replace('Guardrails ', '').lower()}.

> **Generato.** Questo repository è prodotto da `tools/build_modules.py` nel
> repository [bmad-module-guardrails](https://github.com/mlarese/bmad-module-guardrails).
> Le modifiche si fanno lì e poi si rigenera: qui vengono sovrascritte.

## Figure

| Figura | Ruolo | Skill | Cosa presidia |
| ------ | ----- | ----- | ------------- |
{figure_rows}

## Skill e workflow

| Skill | Comando | Cosa fa |
| ----- | ------- | ------- |
{workflow_rows}

## Installazione

```
bmad install {code}
```

Poi, come primo passo, `{profile_skill}`: raccoglie il profilo di progetto — settore,
dati trattati, mercato, stack, criticità — e da lì ogni figura deriva quanto essere
severa. Senza profilo il default resta `normal` e le figure partono senza contesto.

## Memoria condivisa

Il profilo vive in `{{project-root}}/_bmad/memory/grl-shared/project-profile.md`, insieme
a `decisions.md` e `accepted-risks.md`. Il percorso è lo stesso per tutti i moduli
Guardrails: installandone due, il profilo resta uno solo e si compila una volta.

## Convivenza con il bundle

Questo modulo installa skill con **lo stesso nome** del bundle `grl` — `{agents[0]['code']}`
sta identica in entrambi. Bundle e moduli tematici non vanno installati insieme nello
stesso progetto: si sceglie il bundle completo, oppure i moduli delle aree che servono.
{party_section}
## Licenza

MIT.
"""


def short(description: str, limit: int = 180) -> str:
    """Prima frase della descrizione, per la tabella del README."""
    text = description.split(". ")[0].strip().replace("|", "\\|")
    if len(text) > limit:
        return text[: limit - 1].rsplit(" ", 1)[0] + "…"
    return text.rstrip(".") + "."


def render_claude_md(module: dict, renames: dict[str, str]) -> str:
    return f"""# {module['name']} (`{module['code']}`) — istruzioni di progetto

## Questo repository è generato

Il contenuto è prodotto da `tools/build_modules.py` nel repository
[bmad-module-guardrails](https://github.com/mlarese/bmad-module-guardrails), che resta
la fonte unica delle skill.

**Non modificare le skill qui.** Una modifica fatta in questo repository viene persa
alla prima rigenerazione. Il percorso corretto è: modifica in `src/skills/` della
fonte, poi `python3 tools/build_modules.py --module {module['code']}`, poi commit qui.

## Cosa cambia rispetto al bundle

- il roster contiene solo le figure di quest'area
- le tre skill del core sono rinominate: `{renames['grl-setup']}`, `{renames['grl-profile']}`,
  `{renames['grl-board']}`
- i gruppi di party mode contengono solo i membri installati
- la memoria condivisa resta `_bmad/memory/grl-shared/`, uguale per tutti i moduli

## Niente pull request

Il lavoro finisce con i commit e, se richiesto, con il push del branch.
"""


GITIGNORE = """# Installazione BMad locale e skill di terze parti
_bmad/
_bmad-output/
.claude/
.agents/
.opencode/
.cline/

# Log di build e referti di analisi del builder
**/.memlog.md
**/.analysis/

# Report e cache locali degli eval runner: mai versionare
**/eval-runs/

# Python
__pycache__/
*.py[cod]
.pytest_cache/

# macOS
.DS_Store
"""


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #


def parse_help_rows(source: str) -> dict[str, list[tuple[str, str]]]:
    """Da module-help.csv: per ogni skill, le coppie (display-name, descrizione)."""
    rows: dict[str, list[tuple[str, str]]] = {}
    for line in source.splitlines()[1:]:
        if not line.strip():
            continue
        parts = line.split(",", 4)
        if len(parts) < 5:
            continue
        skill, display = parts[1], parts[2]
        rest = parts[4]
        match = re.match(r'^"(.*?)",', rest) or re.match(r"^([^,]*),", rest)
        description = match.group(1) if match else ""
        rows.setdefault(skill, []).append((display, description.replace("|", "\\|")))
    return rows


def clean_output(module_out: Path) -> None:
    """Svuota la cartella del modulo conservando `.git`.

    La cartella in `dist/` è anche il clone del repository derivato: cancellarla
    intera a ogni build significherebbe perdere la storia e i remote, e rifare
    `git init` prima di ogni push.
    """
    if not module_out.exists():
        module_out.mkdir(parents=True)
        return
    for entry in module_out.iterdir():
        if entry.name == ".git":
            continue
        shutil.rmtree(entry) if entry.is_dir() else entry.unlink()


def build_module(source_root: Path, out_root: Path, topology: dict, module: dict, bundle: dict) -> dict:
    code = module["code"]
    core_skills = topology["core"]["skills"]
    renames = core_renames(core_skills, code)
    version = bundle["module_version"]

    module_out = out_root / module["repo"]
    clean_output(module_out)

    agent_codes = {a["code"] for a in bundle["agents"]}
    module_agents = figures(bundle["agents"], module["skills"])
    if not module_agents:
        raise BuildError(f"modulo `{code}`: nessuna figura fra le skill dichiarate")
    module_workflows = workflow_skills(module["skills"], agent_codes)

    context = {
        "count": len(module_agents),
        "codes": {a["code"] for a in module_agents},
        "names": {a["name"] for a in module_agents},
        "listing": ", ".join(f"{a['name']} ({a['code']})" for a in module_agents),
    }

    copied = 0
    for skill in core_skills:
        copied += copy_skill(source_root, module_out, skill, renames[skill], renames, code, context)
    for skill in module["skills"]:
        copied += copy_skill(source_root, module_out, skill, skill, renames, code, context)

    # Manifesto: in src/ per l'installer, e identico negli assets del setup.
    manifest = render_module_yaml(module, module_agents, renames, version)
    (module_out / "src" / "module.yaml").write_text(manifest, encoding="utf-8")
    setup_assets = module_out / "src" / "skills" / renames["grl-setup"] / "assets"
    (setup_assets / "module.yaml").write_text(manifest, encoding="utf-8")

    # Catalogo di help.
    help_source = (source_root / "src" / "module-help.csv").read_text(encoding="utf-8")
    installed = set(module["skills"]) | set(core_skills)
    help_csv = filter_help_csv(help_source, installed, module["name"], renames, context["count"])
    (module_out / "src" / "module-help.csv").write_text(help_csv, encoding="utf-8")
    (setup_assets / "module-help.csv").write_text(help_csv, encoding="utf-8")

    # Stanze di party mode.
    party_source = (
        source_root / "src" / "skills" / "grl-setup" / "assets" / "party-groups.toml"
    ).read_text(encoding="utf-8")
    party_toml, dropped = filter_party_groups(
        party_source,
        module.get("party_groups", []),
        {a["code"] for a in module_agents},
        module["name"],
    )
    (setup_assets / "party-groups.toml").write_text(party_toml, encoding="utf-8")

    # Vetrine.
    skill_order = [renames[s] for s in core_skills] + list(module["skills"])
    (module_out / ".claude-plugin").mkdir()
    (module_out / ".claude-plugin" / "marketplace.json").write_text(
        render_marketplace(module, skill_order, version), encoding="utf-8"
    )
    (module_out / "README.md").write_text(
        render_readme(
            module,
            module_agents,
            module_workflows,
            parse_help_rows(help_csv),
            renames,
            dropped,
            module.get("party_groups", []),
        ),
        encoding="utf-8",
    )
    (module_out / "CLAUDE.md").write_text(render_claude_md(module, renames), encoding="utf-8")
    (module_out / ".gitignore").write_text(GITIGNORE, encoding="utf-8")

    return {
        "code": code,
        "repo": module["repo"],
        "path": module_out,
        "files": copied,
        "agents": [a["name"] for a in module_agents],
        "workflows": module_workflows,
        "dropped_groups": dropped,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source-root", default=".", help="radice del repository fonte")
    parser.add_argument("--out", default="dist", help="cartella di output (default: dist/)")
    parser.add_argument("--module", action="append", help="genera solo questo codice (ripetibile)")
    args = parser.parse_args(argv)

    source_root = Path(args.source_root).resolve()
    out_root = Path(args.out)
    if not out_root.is_absolute():
        out_root = source_root / out_root

    try:
        topology = load_topology(source_root / "src" / "module-topology.yaml")
        bundle = load_module_yaml(source_root / "src" / "module.yaml")
        ALL_FIGURE_NAMES.update(a["name"] for a in bundle["agents"])
        wanted = set(args.module) if args.module else None
        modules = [m for m in topology["modules"] if wanted is None or m["code"] in wanted]
        if wanted:
            missing = wanted - {m["code"] for m in modules}
            if missing:
                raise BuildError(f"codici non presenti in module-topology.yaml: {', '.join(sorted(missing))}")

        results = [build_module(source_root, out_root, topology, m, bundle) for m in modules]
    except BuildError as error:
        print(f"errore: {error}", file=sys.stderr)
        return 1

    for result in results:
        figures_list = ", ".join(result["agents"])
        print(f"{result['code']:>4}  {result['repo']}")
        print(f"      {result['files']} file · figure: {figures_list}")
        if result["workflows"]:
            print(f"      workflow: {', '.join(result['workflows'])}")
        if result["dropped_groups"]:
            print(f"      stanze omesse (meno di {MIN_PARTY_MEMBERS} membri installati): "
                  f"{', '.join(result['dropped_groups'])}")
    print(f"\n{len(results)} moduli in {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
