#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6.0"]
# ///
"""Genera i repository dei moduli tematici Guardrails a partire da questo repository.

Perché serve
------------
Il bundle `grl` installa diciannove figure e quattordici workflow in un colpo solo. Chi vuole
solo la governance normativa, o solo il presidio ingegneristico, non ha motivo di
portarsi le altre dieci figure. La soluzione è un repository per area — ma scritto a
mano diventerebbe subito divergente dal bundle.

Questo script tiene una sola fonte: le skill in `src/skills/`, il manifesto in
`src/module.yaml` e la mappa in `src/module-topology.yaml`. Da lì produce in `dist/`
un albero completo per ogni modulo tematico, pronto per essere committato nel suo
repository. I repository derivati non si modificano a mano: si rigenerano.

Cosa fa, in ordine
------------------
1. Copia le skill del modulo, prendendo **solo i file tracciati da git** e gli eventuali
   file ausiliari esplicitamente allowlisted in `SOURCE_AUXILIARY_FILES` — così referti di
   analisi, cache ed eval run restano fuori.
2. Duplica le due skill del core (`grl-profile`, `grl-board`)
   rinominandole con il codice del modulo (`grg-profile`, …) e riscrive ogni
   riferimento testuale a quei due nomi. I codici delle figure (`grl-agent-*`) e la
   memoria condivisa (`grl-shared`) restano invariati: è il punto in cui due moduli
   installati insieme si incontrano.
3. Filtra il roster in `module.yaml`, le righe di `module-help.csv` e la lista di
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

# File di skill ed eval aggiunti nello stesso turno ma non ancora presenti
# nell'indice Git gestito dal sandbox. Restano espliciti per non copiare cache o
# report di eval non destinati ai repository derivati; dopo il commit diventano
# normali risultati di `git ls-files` e l'allowlist è innocua.
SOURCE_AUXILIARY_FILES = {
    "src/skills/grl-ads/evals/fixtures/period-b-incomparable.csv",
    "src/skills/grl-agent-ads/evals/fixtures/period-a.csv",
    "src/skills/grl-agent-ads/evals/fixtures/period-b-incomparable.csv",
    "src/skills/grl-revenue-audit/SKILL.md",
    "src/skills/grl-revenue-audit/evals/README.md",
    "src/skills/grl-revenue-audit/evals/cases.json",
    "src/skills/grl-revenue-audit/evals/triggers.json",
    "src/skills/grl-revenue-plan/SKILL.md",
    "src/skills/grl-revenue-plan/evals/README.md",
    "src/skills/grl-revenue-plan/evals/cases.json",
    "src/skills/grl-revenue-plan/evals/triggers.json",
    "src/skills/grl-revenue-preflight/SKILL.md",
    "src/skills/grl-revenue-preflight/evals/README.md",
    "src/skills/grl-revenue-preflight/evals/cases.json",
    "src/skills/grl-revenue-preflight/evals/triggers.json",
    "src/skills/grl-agent-social/SKILL.md",
    "src/skills/grl-agent-social/customize.toml",
    "src/skills/grl-agent-social/evals/README.md",
    "src/skills/grl-agent-social/evals/cases.json",
    "src/skills/grl-agent-social/evals/triggers.json",
    "src/skills/grl-agent-social/evals/files/linkedin-feature-brief.md",
    "src/skills/grl-agent-creative/SKILL.md",
    "src/skills/grl-agent-creative/customize.toml",
    "src/skills/grl-agent-creative/evals/README.md",
    "src/skills/grl-agent-creative/evals/cases.json",
    "src/skills/grl-agent-creative/evals/triggers.json",
    "src/skills/grl-agent-creative/evals/files/reel-feature-brief.md",
    "src/skills/grl-agent-imaging/SKILL.md",
    "src/skills/grl-agent-imaging/customize.toml",
    "src/skills/grl-agent-imaging/scripts/generate_image.py",
    "src/skills/grl-agent-imaging/scripts/tests/test_generate_image.py",
    "src/skills/grl-agent-imaging/evals/README.md",
    "src/skills/grl-agent-imaging/evals/cases.json",
    "src/skills/grl-agent-imaging/evals/triggers.json",
    "src/skills/grl-agent-imaging/evals/files/product-shot-brief.md",
    "src/skills/grl-social/SKILL.md",
    "src/skills/grl-social/evals/README.md",
    "src/skills/grl-social/evals/cases.json",
    "src/skills/grl-social/evals/triggers.json",
    "src/skills/grl-social-creative/SKILL.md",
    "src/skills/grl-social-creative/evals/README.md",
    "src/skills/grl-social-creative/evals/cases.json",
    "src/skills/grl-social-creative/evals/triggers.json",
    "src/skills/grl-social-creative/evals/files/reel-package-brief.md",
    "src/skills/grl-agent-database/SKILL.md",
    "src/skills/grl-agent-database/customize.toml",
    "src/skills/grl-agent-database/evals/README.md",
    "src/skills/grl-agent-database/evals/cases.json",
    "src/skills/grl-agent-database/evals/triggers.json",
    "src/skills/grl-agent-database/references/ricerca-live.md",
    "src/skills/grl-agent-database/references/modello-dati-e-workload.md",
    "src/skills/grl-agent-database/references/scelta-database.md",
    "src/skills/grl-agent-database/references/relazionali-e-distribuiti.md",
    "src/skills/grl-agent-database/references/no-sql-e-specializzati.md",
    "src/skills/grl-agent-database/references/vettoriale-e-ibrido.md",
    "src/skills/grl-agent-database/references/prestazioni-affidabilita.md",
    "src/skills/grl-agent-database/references/migrazione-e-benchmark.md",
    "src/skills/grl-agent-database/references/revisione-database.md",
    "src/skills/grl-agent-database/references/fasi-bmad.md",
    "src/skills/grl-agent-database/references/prompt-quality-canon.md",
    "src/skills/grl-agent-firmware/SKILL.md",
    "src/skills/grl-agent-firmware/customize.toml",
    "src/skills/grl-agent-firmware/evals/README.md",
    "src/skills/grl-agent-firmware/evals/cases.json",
    "src/skills/grl-agent-firmware/evals/triggers.json",
    "src/skills/grl-agent-firmware/references/scrittura-e-review.md",
    "src/skills/grl-agent-firmware/references/bring-up-e-driver.md",
    "src/skills/grl-agent-firmware/references/real-time-e-rtos.md",
    "src/skills/grl-agent-firmware/references/test-e-debug.md",
    "src/skills/grl-agent-firmware/references/secure-update-e-safety.md",
    "src/skills/grl-agent-firmware/references/ricerca-live.md",
    "src/skills/grl-agent-firmware/references/prompt-quality-canon.md",
    "src/skills/grl-agent-architecture/references/deep-module-design.md",
    "src/skills/grl-automation/references/human-only-wizard.md",
    "src/skills/grl-profile/assets/domain-glossary-template.md",
}

# I file del collegio che portano il roster e i confini fra figure. Sono gli unici
# su cui si filtra per figura installata: altrove le stesse righe hanno un altro
# significato.
BOARD_ROSTER_FILES = {"SKILL.md", "selection.md"}

# Il bundle conta diciannove figure e lo dice ovunque nei testi del core. In un modulo
# tematico quel numero è falso, e un numero falso in una skill è un'istruzione
# sbagliata. Con più figure si sostituisce il numerale; con una sola si toglie e
# resta il plurale generico, che è impreciso ma non falso — riscrivere l'accordo
# verbale di frasi arbitrarie non è automatizzabile.
NUMERALS = {2: "due", 3: "tre", 4: "quattro", 5: "cinque", 6: "sei", 7: "sette", 8: "otto", 14: "quattordici", 16: "sedici", 17: "diciassette", 18: "diciotto", 19: "diciannove"}

# Nota appesa a ogni figura del modulo: le tabelle di handoff citano colleghe che
# qui non sono installate, e senza questa riga l'agente rimanda a un vuoto.
OUT_OF_MODULE_NOTE = """

## Figure fuori da questo modulo

Le tabelle qui sopra citano anche figure Guardrails che questo modulo non installa.
Qui sono installate: {installed}.

Quando il tema appartiene a una figura assente, il confine resta valido: **dichiara che
il tema esce dal perimetro, nomina la competenza che servirebbe e prosegui solo su ciò che
resta autorizzato.** Registra `missing_capability` e `handoff_status: pending`; non
improvvisare il parere mancante, non dichiarare completato il passaggio e non superare un
gate che dipende da quella capacità. Il lavoro indipendente può continuare, il gate dipendente
resta `blocked` o `EVIDENZA_INSUFFICIENTE`. Il modulo che la contiene si installa a parte; il
bundle completo `grl` le contiene tutte.
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
    paths = [Path(p) for p in result.stdout.split("\0") if p]
    prefix = relative_dir.rstrip("/") + "/"
    for value in sorted(SOURCE_AUXILIARY_FILES):
        if value.startswith(prefix):
            path = Path(value)
            if path.is_file() and path not in paths:
                paths.append(path)
    return paths


# --------------------------------------------------------------------------- #
# Riscrittura dei nomi del core
# --------------------------------------------------------------------------- #


def core_renames(core_skills: list[str], code: str) -> dict[str, str]:
    """Rinomina le skill core con il prefisso del modulo derivato."""
    renames = {}
    for skill in core_skills:
        suffix = skill.split("-", 1)[1]
        renames[skill] = f"{code}-{suffix}"
    return renames


def adapt_counts(text: str, count: int) -> str:
    """Riporta al numero reale di figure i conteggi scritti per il bundle.

    Tocca solo le costruzioni in cui `diciannove` o `diciotto` (o i vecchi `diciassette`, `sedici`, `quattordici`, `tredici` e `dodici`) è accostato alle
    figure o alle loro chiavi di config: «tredici documenti» dentro un esempio, o
    «tredici pagine» in una reference, restano quello che sono.
    """
    numeral = NUMERALS.get(count)

    def replace_all_of(match: re.Match) -> str:
        return f"tutte e {numeral}" if numeral else "tutte"

    def replace_noun(match: re.Match) -> str:
        space, noun = match.group(1), match.group(2)
        if numeral:
            return f"{numeral}{space}{noun}"
        return noun

    numerals = r"(?:dodici|tredici|quattordici|sedici|diciassette|diciotto|diciannove)"
    text = re.sub(rf"una\s+delle\s+{numerals}\s+figure", "una delle figure", text)
    text = re.sub(rf"tutte\s+e\s+{numerals}", replace_all_of, text)
    text = re.sub(rf"\b{numerals}(\s+)(figure|chiavi)", replace_noun, text)
    return text


def adapt_board(text: str, count: int) -> str:
    """L'unica frase del collegio che il numerale da solo non salva.

    «punta a due-quattro figure» è un consiglio sensato con dodici figure in campo e
    assurdo con due: qui la selezione non è più il problema.
    """
    if count > 4:
        return text
    return text.replace(
        "Punta a **due-quattro figure**; se le convochi tutte, indica cosa ciascuna "
        "ha di decisivo da dire su *questo* artefatto.",
        "**Convoca solo chi ha qualcosa di decisivo da dire su *questo* artefatto**; "
        "se le convochi tutte, indica cosa ciascuna ci aggiunge.",
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

        if is_board and rel.name in BOARD_ROSTER_FILES:
            # Solo nel collegio: la tabella dice chi convocare, e una figura non
            # installata non è convocabile. Nelle figure le stesse righe dicono
            # invece «questo non è mio dominio» — un confine che vale comunque, e
            # che togliendolo lascerebbe la figura libera di invadere il tema.
            # Il roster vive in references/selection.md: filtrare il solo SKILL.md
            # lascerebbe convocabili figure che il modulo non installa.
            text = filter_tables(text, context["codes"], context["names"])
            text = adapt_board(text, context["count"])

        # La nota va dove stanno le tabelle: nelle figure è SKILL.md, nel collegio
        # è references/selection.md, che dopo il carve porta roster e confini.
        if (is_figure and rel.name == "SKILL.md") or (is_board and rel.name == "selection.md"):
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
    profile_skill = renames["grl-profile"]
    board_skill = renames["grl-board"]

    return f"""# Manifesto del modulo {module['name']} ({code}).
#
# GENERATO da tools/build_modules.py nel repository bmad-module-guardrails.
# Non modificare qui: le modifiche si fanno nella fonte e poi si rigenera.
#
# Questa è la copia che legge l'installer BMad: la cerca in src/module.yaml.

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
# La cartella della memoria condivisa NON va creata dall'installer: la crea
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
# Vetrine del repository derivato
# --------------------------------------------------------------------------- #

# Il catalogo operativo del modulo resta in italiano perché è la fonte usata
# dall'installer BMad. I README dei repository pubblici derivati sono invece
# vetrine in inglese: queste copie editoriali impediscono che la lingua della
# vetrina dipenda dalla lingua del catalogo interno.
README_MODULE_COPY = {
    "grg": "A focused BMad module for privacy, legal and licensing, regulatory compliance, and live legal updates. It separates actual obligations from common practice and identifies rules that do not apply.",
    "gre": "A focused BMad module for code architecture, database architecture and design, embedded firmware, application security, infrastructure and operations, and AI application design. Every recommendation includes the cost of ignoring it.",
    "grf": "A focused BMad module for tax, accounting operations, grants, incentives, and live fiscal updates. It checks requirements, deadlines, eligible expenses, and reporting against primary sources.",
    "grh": "A focused BMad module for clinical data, healthcare interoperability, patient safety, and medical-device qualification. It keeps real clinical workflows and MDR scope in view.",
    "grw": "A focused BMad module for visual quality, search, web delivery, paid media, organic social content, creative video, and AI image generation. It guards against generic pages, unsupported ranking promises, unplanned posts, and unmeasured spend.",
    "gpm": "A focused BMad module for paid media, Google Ads, tracking, consent, social content, creative production, and AI image generation. It keeps campaigns and assets behind evidence, approval, and rollback gates.",
    "grv": "A focused BMad module for hotel revenue management, pricing, forecasting, profit, and PMS/Channel Manager integrations. It keeps external publication behind explicit gates, dry-runs, approval, and rollback.",
    "gau": "A focused BMad module for routing repeatable processes across software, databases, legal, tax, design, architecture, healthcare, web, paid media, social content, creative video, AI image generation, and revenue management.",
    "gwp": "A focused BMad module for component-based WordPress architecture and controlled delivery through the release gate. It covers Gutenberg, Elementor, ACF, templates, the Media Library, and migration work.",
}

README_AGENT_TITLES = {
    "grl-agent-fiscal": "Tax and Incentives Specialist",
}

README_AGENT_FOCUS = {
    "grl-agent-privacy": "Personal data, GDPR, DPIAs, retention, analytics, logs, and data in prompts.",
    "grl-agent-security": "APIs, authentication, authorization, secrets, dependencies, CVEs, and LLM attack surfaces.",
    "grl-agent-legal": "Licenses, contracts, DPAs, ownership, AI outputs, and AI Act obligations.",
    "grl-agent-compliance": "NIS2, DORA, EAA/WCAG, eIDAS, CRA, MDR, and sector-specific obligations.",
    "grl-agent-fiscal": "Taxes, VAT, grants, incentives, tax credits, and reporting.",
    "grl-agent-ui-critic": "UI, landing pages, markup, CSS, typography, palettes, density, and layout.",
    "grl-agent-architecture": "Boundaries, folders, dependencies, interfaces, factories, architectural layers, and the architectural constraints of a story or spec.",
    "grl-agent-database": "Data models, PostgreSQL, Oracle, MongoDB, Redis/Valkey, distributed SQL, NoSQL, search, analytics, time-series, graph, vector, and hybrid search.",
    "grl-agent-firmware": "MCU and SoC firmware, startup, drivers, registers, interrupts/DMA, RTOS, timing, memory, bring-up, testing, debugging, bootloaders, and secure updates.",
    "grl-agent-ops": "Servers, VPS, Docker, CI/CD, deployment, TLS, backups, logs, and incidents.",
    "grl-agent-health": "Clinical data, codes, HL7/FHIR/DICOM, clinical workflows, and patient safety.",
    "grl-agent-ai": "LLMs, prompts, RAG, embeddings, tool calling, evaluations, costs, and latency.",
    "grl-agent-wordpress": "Gutenberg, Elementor, ACF, post types, template parts, and the Media Library.",
    "grl-agent-seo": "Search intent, crawling, indexing, content, structured data, and Search Console.",
    "grl-agent-ads": "Google Ads, paid advertising, audiences, creative, tracking, consent, budgets, and policies.",
    "grl-agent-social": "Organic strategy, content pillars, calendars, posts, captions, community, and metrics.",
    "grl-agent-creative": "Advertising concepts, design, scripts, storyboards, shot lists, Reels, TikToks, and Shorts.",
    "grl-agent-imaging": "Nano Banana, Imagen, GPT Image, Photoshop, prompts, masks, subject consistency, provenance, and export.",
    "grl-agent-revenue": "Occupancy, ADR, RevPAR, TRevPAR, NRevPAR, GOPPAR, MUP, MOL, pickup, forecasting, pricing, PMS, and Channel Manager.",
}

README_WORKFLOW_COPY = {
    "grl-legal-updates": (
        "Live legal updates",
        "Searches primary sources for laws, decrees, rulings, and amendments in a defined period, with coverage and freshness checks.",
    ),
    "grl-fiscal-updates": (
        "Live fiscal updates",
        "Searches primary sources for tax rules, circulars, grants, incentives, amendments, and deadlines in a defined period.",
    ),
    "grl-mdsw": (
        "Medical-device qualification",
        "Assesses whether a software feature has a medical purpose and identifies the relevant MDR scope and planning impact.",
    ),
    "grl-web": (
        "Web experience delivery",
        "Moves landing pages and websites from a conversion brief through visual review, accessibility, SEO, and delivery.",
    ),
    "grl-wordpress-delivery": (
        "Controlled WordPress delivery",
        "Coordinates WordPress creation, migration, resumption, and verification through a release gate.",
    ),
    "grl-ads": (
        "Paid media operations",
        "Audits, plans, tracks, optimizes, preflights, and applies paid-media change sets behind approval and rollback gates.",
    ),
    "grl-social": (
        "Organic social strategy",
        "Builds social strategies, calendars, content, audits, and measurement plans without scheduling or publishing.",
    ),
    "grl-social-creative": (
        "Social creative production",
        "Turns a brief into producible concepts, scripts, storyboards, shot lists, specifications, and channel variants.",
    ),
    "grl-revenue-audit": (
        "Revenue data and pricing audit",
        "Produces a read-only audit of exports, data quality, KPIs, demand, and the economic floor.",
    ),
    "grl-revenue-plan": (
        "Revenue planning",
        "Builds pricing, demand, and profit scenarios while separating the economic floor, market, and forecast.",
    ),
    "grl-revenue-preflight": (
        "PMS and Channel Manager preflight",
        "Checks contract, mapping, dry-run, response, reconciliation, idempotency, and rollback before transmission.",
    ),
    "grl-automation": (
        "Controlled automation",
        "Routes work from read-only checks through dry-run to observable execution, with explicit approvals and rollback.",
    ),
    "grl-toolchain": (
        "Skills and MCP servers across harnesses",
        "Finds and assesses skills and MCP servers, then installs them in each harness's own syntax behind a dry-run, a backup, and a verification step.",
    ),
}


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
    _help_rows: dict[str, list[tuple[str, str]]],
    renames: dict[str, str],
) -> str:
    code = module["code"]
    profile_skill = renames["grl-profile"]
    board_skill = renames["grl-board"]

    try:
        module_copy = README_MODULE_COPY[code]
    except KeyError as error:
        raise BuildError(f"Manca la copia inglese del README per il modulo `{code}`") from error

    figure_rows = "\n".join(
        f"| {a['icon']} {a['name']} | {README_AGENT_TITLES.get(a['code'], a['title'])} | `{a['code']}` | {README_AGENT_FOCUS[a['code']]} |"
        for a in agents
    )

    workflow_copy = {
        profile_skill: (
            "Project profile",
            "Collects the project context shared by every installed figure.",
        ),
        board_skill: (
            "Multidisciplinary review",
            "Convenes the relevant figures on one artifact and returns a review summary or release verdict.",
        ),
        **README_WORKFLOW_COPY,
    }
    workflow_lines = []
    for skill in [profile_skill, board_skill] + list(workflows):
        try:
            display, description = workflow_copy[skill]
        except KeyError as error:
            raise BuildError(f"Manca la copia inglese del workflow `{skill}`") from error
        workflow_lines.append(f"| `{skill}` | {display} | {description} |")
    workflow_rows = "\n".join(workflow_lines)

    return f"""# {module['name']} (`{code}`)

{module_copy}

This is a focused BMad module in the [Guardrails](https://github.com/mlarese/bmad-module-guardrails)
bundle. It keeps the same behavior and shared memory while installing only the figures and
workflows for the {module['name'].replace('Guardrails ', '').lower()} area.

> **Generated.** This repository is produced by `tools/build_modules.py` in the
> [bmad-module-guardrails](https://github.com/mlarese/bmad-module-guardrails) repository.
> Make changes there and regenerate; local changes here will be overwritten.

## Agents

| Agent | Role | Skill | Focus |
| ----- | ---- | ----- | ----- |
{figure_rows}

## Skills and workflows

| Skill | Purpose |
| ----- | ------- |
{workflow_rows}

## Installation

```
bmad install {code}
```

As a first step, run `{profile_skill}`. It collects the project profile — sector, data,
market, stack, and criticality — so each figure can calibrate its review. Without a profile,
the default remains `normal` and the figures start without context.

## Shared memory

The profile lives in `{{project-root}}/_bmad/memory/grl-shared/project-profile.md`, together
with `decisions.md` and `accepted-risks.md`. All Guardrails modules use the same path, so two
installed modules still share one profile.

## Using it with the bundle

This module installs skills with **the same names** as the `grl` bundle — `{agents[0]['code']}`
is identical in both. Do not install the full bundle and thematic modules in the same project:
choose the complete bundle, or only the thematic modules you need.

## License

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
- le due skill del core sono rinominate: `{renames['grl-profile']}`, `{renames['grl-board']}`
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

    # Manifesto: in src/ per l'installer.
    manifest = render_module_yaml(module, module_agents, renames, version)
    (module_out / "src" / "module.yaml").write_text(manifest, encoding="utf-8")

    # Catalogo di help.
    help_source = (source_root / "src" / "module-help.csv").read_text(encoding="utf-8")
    installed = set(module["skills"]) | set(core_skills)
    help_csv = filter_help_csv(help_source, installed, module["name"], renames, context["count"])
    (module_out / "src" / "module-help.csv").write_text(help_csv, encoding="utf-8")

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
    print(f"\n{len(results)} moduli in {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
