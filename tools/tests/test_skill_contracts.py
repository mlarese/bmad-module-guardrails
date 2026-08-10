"""Invarianti che ogni skill di `src/skills/` deve rispettare.

Sono i contratti che una review ha già trovato rotti almeno una volta: frontmatter
non parsabile, figure non convocabili per nome, roster del collegio incompleto,
percorsi personali finiti in un repository pubblico. Un test li tiene chiusi.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "src" / "skills"
TOPOLOGY = REPO / "src" / "module-topology.yaml"
MODULE = REPO / "src" / "module.yaml"

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)


def skill_dirs() -> list[Path]:
    return sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())


def frontmatter(path: Path) -> dict:
    match = FRONTMATTER.match(path.read_text())
    assert match, f"{path} non ha un frontmatter"
    return yaml.safe_load(match.group(1))


class SkillFrontmatterTests(unittest.TestCase):
    def test_frontmatter_is_valid_yaml_with_name_and_description(self) -> None:
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                data = frontmatter(skill / "SKILL.md")
                self.assertEqual(data["name"], skill.name)
                self.assertIsInstance(data["description"], str)
                self.assertGreaterEqual(len(data["description"]), 120)

    def test_h1_follows_the_frontmatter(self) -> None:
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                body = FRONTMATTER.sub("", (skill / "SKILL.md").read_text(), count=1)
                self.assertTrue(
                    body.lstrip("\n").startswith("# "),
                    "il corpo deve aprirsi con l'H1, non con una direttiva di consegna",
                )

    def test_prose_review_block_closes_every_skill(self) -> None:
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                sections = re.findall(r"^## (.+)$", (skill / "SKILL.md").read_text(), re.M)
                self.assertEqual(sections[-1], "Revisione editoriale finale")


class AgentRosterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agents = yaml.safe_load(MODULE.read_text())["agents"]

    def test_every_figure_is_summoned_by_name(self) -> None:
        """`module.yaml` promette che le figure si convocano per nome: la description deve permetterlo."""
        for agent in self.agents:
            with self.subTest(agent=agent["code"]):
                description = frontmatter(SKILLS / agent["code"] / "SKILL.md")["description"]
                self.assertIn(agent["name"], description)

    def test_metadata_match_the_customize_surface(self) -> None:
        import tomllib

        for agent in self.agents:
            with self.subTest(agent=agent["code"]):
                path = SKILLS / agent["code"] / "customize.toml"
                block = tomllib.loads(path.read_text())["agent"]
                for key in ("name", "title", "icon", "description", "module", "team"):
                    self.assertEqual(block.get(key), agent.get(key), f"{agent['code']}.{key}")

    def test_board_roster_covers_every_figure(self) -> None:
        roster = (SKILLS / "grl-board" / "references" / "selection.md").read_text()
        for agent in self.agents:
            with self.subTest(agent=agent["code"]):
                self.assertIn(agent["code"], roster)


class DistributionHygieneTests(unittest.TestCase):
    def test_no_absolute_or_personal_paths_in_distributed_files(self) -> None:
        vietati = ("/Users/", "/home/", "development_obsidian", "C:\\")
        for skill in skill_dirs():
            for path in sorted(skill.rglob("*.md")):
                if ".analysis" in path.parts or path.name == ".memlog.md":
                    continue
                with self.subTest(file=str(path.relative_to(SKILLS))):
                    testo = path.read_text()
                    for frammento in vietati:
                        self.assertNotIn(frammento, testo)

    def test_no_skill_escapes_the_project_root(self) -> None:
        for skill in skill_dirs():
            for path in sorted(skill.rglob("*.md")):
                if ".analysis" in path.parts:
                    continue
                with self.subTest(file=str(path.relative_to(SKILLS))):
                    self.assertNotIn("{project-root}/../", path.read_text())


class GitTrackingTests(unittest.TestCase):
    """`build_modules.py` copia nei derivati solo i file che `git ls-files` restituisce.

    Un file non tracciato non arriva al derivato, e nessun test lo segnala: la skill
    parte monca. Il caso è già successo con `grl-bug-finder` e con la fixture di
    `grl-profile`, esclusa da una regola `.gitignore` troppo larga. La scorciatoia
    applicata allora — una allowlist di percorsi dentro `build_modules.py` — ha nascosto
    il problema per 75 file: il secondo test vieta di rimetterla.
    """

    ESCLUSI = ("__pycache__", ".analysis")

    def _distribuibili(self) -> set[str]:
        risultato = set()
        for path in SKILLS.rglob("*"):
            if not path.is_file():
                continue
            parti = path.relative_to(REPO).parts
            if any(p in self.ESCLUSI or p.startswith(".") for p in parti):
                continue
            risultato.add(str(path.relative_to(REPO)))
        return risultato

    def _tracciati(self) -> set[str]:
        import subprocess

        result = subprocess.run(
            ["git", "ls-files", "--", "src/skills"],
            cwd=REPO, capture_output=True, text=True, check=True,
        )
        return set(result.stdout.split())

    def test_every_distributed_file_is_tracked_by_git(self) -> None:
        mancanti = sorted(self._distribuibili() - self._tracciati())
        self.assertEqual(mancanti, [], "file non tracciati: non arrivano nei derivati")

    def test_the_build_copies_only_what_git_tracks(self) -> None:
        """Nessuna allowlist di percorsi rientra in `build_modules.py`."""
        import sys

        sys.path.insert(0, str(REPO / "tools"))
        import build_modules

        self.assertFalse(
            hasattr(build_modules, "SOURCE_AUXILIARY_FILES"),
            "un file che serve al derivato si committa, non si elenca nel builder",
        )


class InternalLinkTests(unittest.TestCase):
    """Ogni rimando a `references/` o `assets/` punta a un file che esiste.

    Una skill carica le sue reference su richiesta: il rimando è l'unico indirizzo che
    l'agente ha. Un file rinominato o spostato lascia il rimando in piedi, e l'agente
    prosegue senza la parte di istruzioni che quel file conteneva.
    """

    # Il rimando sta sempre dentro backtick, e vale sia dentro la skill
    # (`references/x.md`) sia verso un'altra skill (`grl-agent-ads/references/x.md`).
    RIMANDO = re.compile(r"`([A-Za-z0-9_.<>{}-]*/?(?:references|assets)/[A-Za-z0-9_./-]+\.[a-z]{2,4})`")

    def test_every_reference_link_resolves(self) -> None:
        nomi = {skill.name for skill in skill_dirs()}
        for skill in skill_dirs():
            for documento in sorted(skill.rglob("*.md")):
                if ".analysis" in documento.parts or documento.name == ".memlog.md":
                    continue
                testo = documento.read_text()
                for numero, riga in enumerate(testo.splitlines(), 1):
                    for match in self.RIMANDO.finditer(riga):
                        bersaglio = match.group(1)
                        # I rimandi con segnaposto (`{project-root}`, `<skill>`) non
                        # sono indirizzi: li risolve chi legge, a runtime.
                        if "{" in bersaglio or "<" in bersaglio:
                            continue
                        testa, _, coda = bersaglio.partition("/")
                        base = SKILLS / testa if testa in nomi else skill
                        percorso = coda if testa in nomi else bersaglio
                        with self.subTest(file=f"{documento.relative_to(SKILLS)}:{numero}"):
                            self.assertTrue(
                                (base / percorso).is_file(),
                                f"rimando morto: {bersaglio}",
                            )


class TopologyCoverageTests(unittest.TestCase):
    def test_every_skill_reaches_at_least_one_derived_module(self) -> None:
        topology = yaml.safe_load(TOPOLOGY.read_text())
        core = set(topology["core"]["skills"])
        coperte = {s for module in topology["modules"] for s in module["skills"]} | core
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                self.assertIn(skill.name, coperte)

    def test_automation_module_carries_every_workflow(self) -> None:
        topology = yaml.safe_load(TOPOLOGY.read_text())
        gau = next(m for m in topology["modules"] if m["code"] == "gau")
        core = set(topology["core"]["skills"])
        attese = {skill.name for skill in skill_dirs()} - core
        self.assertEqual(set(gau["skills"]), attese)


if __name__ == "__main__":
    unittest.main()
