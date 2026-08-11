"""Le vetrine del modulo dicono tutte lo stesso numero e lo stesso elenco.

`CLAUDE.md` impone che README, manifesto, catalogo di help, marketplace, topologia e
About GitHub cambino insieme. La regola è scritta, quindi si dimentica: una figura in
più entra in `src/module.yaml` e resta fuori dalla tabella dei moduli derivati, e
nessuno se ne accorge finché un derivato non pubblica un roster diverso dalla fonte.

Questi test chiudono la regola. Ogni fallimento indica una vetrina rimasta indietro,
non un test da rilassare.
"""

from __future__ import annotations

import csv
import json
import re
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "src" / "skills"
MODULE = REPO / "src" / "module.yaml"
TOPOLOGY = REPO / "src" / "module-topology.yaml"
HELP = REPO / "src" / "module-help.csv"
MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"
README = REPO / "README.md"
CLAUDE = REPO / "CLAUDE.md"

# L'API di GitHub rifiuta con HTTP 422 una descrizione più lunga di questo.
ABOUT_MAX = 350

NUMERALI_IT = {
    1: "una", 2: "due", 3: "tre", 4: "quattro", 5: "cinque", 6: "sei", 7: "sette",
    8: "otto", 9: "nove", 10: "dieci", 11: "undici", 12: "dodici", 13: "tredici",
    14: "quattordici", 15: "quindici", 16: "sedici", 17: "diciassette",
    18: "diciotto", 19: "diciannove", 20: "venti", 21: "ventuno", 22: "ventidue",
    23: "ventitré", 24: "ventiquattro", 25: "venticinque",
}

NUMERALI_EN = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
    8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
    14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
    19: "nineteen", 20: "twenty", 21: "twenty-one", 22: "twenty-two",
    23: "twenty-three", 24: "twenty-four", 25: "twenty-five",
}

# Parole funzionali che in un README inglese non compaiono mai per caso.
SPIE_ITALIANE = (
    "della", "delle", "degli", "quando", "perché", "figure di presidio",
    "workflow di ricerca", "questo", "quello",
)


def skill_names() -> set[str]:
    return {p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()}


def module_yaml() -> dict:
    return yaml.safe_load(MODULE.read_text())


def topology() -> dict:
    return yaml.safe_load(TOPOLOGY.read_text())


def marketplace_plugin(code: str) -> dict:
    data = json.loads(MARKETPLACE.read_text())
    return next(p for p in data["plugins"] if p["name"] == code)


def vicini(numero: int, tabella: dict[int, str]) -> list[str]:
    """I numerali sbagliati più probabili: quelli attorno al numero giusto."""
    return [tabella[n] for n in range(numero - 2, numero + 3) if n in tabella and n != numero]


class CatalogCoverageTests(unittest.TestCase):
    def test_marketplace_publishes_every_skill(self) -> None:
        """Una skill fuori da `skills` non viene pubblicata dal marketplace."""
        pubblicate = {s.split("/")[-1] for s in marketplace_plugin("grl")["skills"]}
        self.assertEqual(pubblicate, skill_names())

    def test_help_catalog_lists_every_skill(self) -> None:
        """Una skill fuori dal catalogo non compare nel menu del modulo."""
        with HELP.open() as handle:
            catalogate = {row["skill"] for row in csv.DictReader(handle)}
        self.assertEqual(catalogate, skill_names())

    def test_agent_roster_matches_the_agent_skill_folders(self) -> None:
        """Ogni cartella `grl-agent-*` è una figura del manifesto, e viceversa."""
        cartelle = {s for s in skill_names() if s.startswith("grl-agent-")}
        dichiarate = {a["code"] for a in module_yaml()["agents"]}
        self.assertEqual(dichiarate, cartelle)

    def test_module_greeting_names_every_figure(self) -> None:
        """Il saluto post-install promette di convocare le figure per nome."""
        greeting = module_yaml()["module_greeting"]
        for agent in module_yaml()["agents"]:
            with self.subTest(agent=agent["code"]):
                self.assertIn(agent["name"], greeting)


class SequenceGraphTests(unittest.TestCase):
    """`preceded-by` e `followed-by` guidano il router: devono puntare a voci vere.

    `bmad-help` legge questi due campi per dire dove sei e cosa viene dopo. Un
    rimando verso una voce inesistente manda l'utente su un passo che non trova,
    e un passo senza uscita lo lascia fermo. Nessun test copriva questo grafo.
    """

    def righe(self) -> list[dict]:
        with HELP.open() as handle:
            return list(csv.DictReader(handle))

    def voci(self) -> set[str]:
        return {f"{r['skill']}:{r['action']}" for r in self.righe()}

    def test_every_link_points_at_an_existing_entry(self) -> None:
        """Un rimando verso una voce assente propone un passo che l'utente non trova."""
        voci = self.voci()
        for row in self.righe():
            for campo in ("preceded-by", "followed-by"):
                bersaglio = row[campo].strip()
                if not bersaglio:
                    continue
                with self.subTest(voce=f"{row['skill']}:{row['action']}", campo=campo):
                    self.assertIn(bersaglio, voci)

    def test_no_entry_links_to_itself(self) -> None:
        """Una voce che rimanda a sé stessa manda il router in cerchio."""
        for row in self.righe():
            voce = f"{row['skill']}:{row['action']}"
            for campo in ("preceded-by", "followed-by"):
                with self.subTest(voce=voce, campo=campo):
                    self.assertNotEqual(row[campo].strip(), voce)

    def test_every_figure_offers_a_next_step(self) -> None:
        """Dopo una consulenza il router deve saper dire cosa viene dopo.

        Le figure sono il punto d'ingresso più frequente del modulo. Se nessuna
        dichiara un seguito, ogni consulenza finisce in un vicolo cieco.
        """
        for row in self.righe():
            if not row["skill"].startswith("grl-agent-"):
                continue
            with self.subTest(figura=row["skill"], azione=row["action"]):
                self.assertTrue(row["followed-by"].strip())


class NumeralConsistencyTests(unittest.TestCase):
    """Il numero di figure e di workflow scritto a parole nelle vetrine."""

    def setUp(self) -> None:
        nomi = skill_names()
        self.figure = len([s for s in nomi if s.startswith("grl-agent-")])
        self.workflow = len(nomi) - self.figure

    def _controlla(self, path: Path, numero: int, tabella: dict[int, str], etichetta: str) -> None:
        testo = path.read_text()
        atteso = tabella[numero]
        self.assertIn(
            atteso,
            testo,
            f"{path.name} non dice «{atteso} {etichetta}»: la vetrina è rimasta indietro",
        )
        for sbagliato in vicini(numero, tabella):
            self.assertNotRegex(
                testo,
                rf"\b{re.escape(sbagliato)}\b\s+{etichetta}",
                f"{path.name} dice ancora «{sbagliato} {etichetta}»",
            )

    def test_italian_showcases_state_the_figure_count(self) -> None:
        for path in (MODULE, TOPOLOGY, MARKETPLACE, HELP, CLAUDE):
            with self.subTest(file=path.name):
                self._controlla(path, self.figure, NUMERALI_IT, "figure")

    def test_english_readme_states_the_figure_count(self) -> None:
        self._controlla(README, self.figure, NUMERALI_EN, "review agents")

    def test_italian_showcases_state_the_workflow_count(self) -> None:
        for path in (TOPOLOGY, MARKETPLACE):
            with self.subTest(file=path.name):
                self._controlla(path, self.workflow, NUMERALI_IT, "workflow")


class DerivedModuleShowcaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.topology = topology()
        self.figure = {a["code"]: a["name"] for a in module_yaml()["agents"]}

    def test_every_about_fits_the_github_limit(self) -> None:
        """Oltre 350 caratteri `gh repo edit --description` risponde HTTP 422."""
        for modulo in self.topology["modules"]:
            with self.subTest(module=modulo["code"]):
                about = modulo.get("about", "")
                self.assertTrue(about, f"{modulo['code']} non ha un About")
                self.assertLessEqual(len(about), ABOUT_MAX)

    def test_about_is_english(self) -> None:
        """L'About segue la lingua del README del derivato, che è inglese."""
        for modulo in self.topology["modules"]:
            with self.subTest(module=modulo["code"]):
                about = modulo.get("about", "").lower()
                for spia in SPIE_ITALIANE:
                    self.assertNotIn(spia, about)

    def test_figure_count_in_description_and_about_matches_the_roster(self) -> None:
        """«Otto figure» nella description deve valere otto skill agent nella topologia."""
        for modulo in self.topology["modules"]:
            attese = len([s for s in modulo["skills"] if s in self.figure])
            with self.subTest(module=modulo["code"]):
                dichiarate = re.match(r"\s*(\w+)\s+figur", modulo["description"], re.I)
                if dichiarate:
                    self.assertEqual(dichiarate.group(1).lower(), NUMERALI_IT[attese])
                inglese = re.search(r"(\d+)\s+review agents", modulo.get("about", ""))
                if inglese:
                    self.assertEqual(int(inglese.group(1)), attese)

    def test_claude_md_table_matches_the_topology(self) -> None:
        """La tabella dei nove moduli derivati elenca quello che la topologia genera."""
        righe = dict(re.findall(r"^\| `(\w{3})` \| `[^`]+` \| (.+?) \|$", CLAUDE.read_text(), re.M))
        core = set(self.topology["core"]["skills"])
        for modulo in self.topology["modules"]:
            codice = modulo["code"]
            with self.subTest(module=codice):
                riga = righe.get(codice)
                self.assertIsNotNone(riga, f"{codice} manca dalla tabella di CLAUDE.md")
                if "tutte le" in riga:
                    # `gau` riassume: porta ogni figura e ogni workflow.
                    self.assertEqual(
                        len([s for s in modulo["skills"] if s in self.figure]),
                        len(self.figure),
                    )
                    continue
                for skill in modulo["skills"]:
                    if skill in core:
                        continue
                    atteso = self.figure.get(skill, f"`{skill}`")
                    self.assertIn(atteso, riga, f"{codice} non cita {atteso}")


class ReadmeLanguageTests(unittest.TestCase):
    def test_source_readme_is_english(self) -> None:
        """`CLAUDE.md` impone il README della fonte interamente in inglese."""
        testo = README.read_text().lower()
        for spia in SPIE_ITALIANE:
            with self.subTest(parola=spia):
                self.assertNotIn(spia, testo)


if __name__ == "__main__":
    unittest.main()
