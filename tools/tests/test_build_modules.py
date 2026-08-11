#!/usr/bin/env python3
"""Test del generatore dei moduli tematici Guardrails.

Coprono le trasformazioni che possono produrre un modulo sbagliato in silenzio:
la rinomina del core, i conteggi di figure adattati al perimetro, il filtro delle
tabelle e il filtro del catalogo di help.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_modules as bm  # noqa: E402


CORE = ["grl-profile", "grl-board"]
ROOT = Path(__file__).resolve().parents[2]


class CoreRenameTests(unittest.TestCase):
    def test_prefixes_core_skills_with_module_code(self) -> None:
        self.assertEqual(
            bm.core_renames(CORE, "grg"),
            {"grl-profile": "grg-profile", "grl-board": "grg-board"},
        )

    def test_rewrites_only_whole_names(self) -> None:
        renames = bm.core_renames(CORE, "grw")
        text = "esegui `grl-profile`, non grl-profiler, e la memoria resta in grl-shared/"
        result = bm.rewrite(text, renames)
        self.assertIn("`grw-profile`", result)
        self.assertIn("grl-profiler", result)
        self.assertIn("grl-shared/", result)

    def test_leaves_agent_codes_untouched(self) -> None:
        renames = bm.core_renames(CORE, "gre")
        self.assertEqual(bm.rewrite("grl-agent-security", renames), "grl-agent-security")


class CountTests(unittest.TestCase):
    def test_replaces_numeral_when_more_than_one_figure(self) -> None:
        self.assertEqual(
            bm.adapt_counts("le dodici figure del modulo", 3), "le tre figure del modulo"
        )
        self.assertEqual(
            bm.adapt_counts("le tredici figure del modulo", 3), "le tre figure del modulo"
        )
        self.assertEqual(bm.adapt_counts("tutte e dodici le chiavi", 4), "tutte e quattro le chiavi")
        self.assertEqual(bm.adapt_counts("le sedici figure", 3), "le tre figure")
        self.assertEqual(bm.adapt_counts("le diciannove figure", 6), "le sei figure")

    def test_drops_numeral_for_a_single_figure(self) -> None:
        self.assertEqual(bm.adapt_counts("le dodici figure", 1), "le figure")
        self.assertEqual(bm.adapt_counts("tutte e dodici", 1), "tutte")

    def test_crosses_line_breaks(self) -> None:
        self.assertEqual(bm.adapt_counts("delle dodici\nfigure", 2), "delle due\nfigure")

    def test_does_not_touch_unrelated_dozens(self) -> None:
        text = "un RAG costruito sopra dodici documenti che starebbero nel contesto"
        self.assertEqual(bm.adapt_counts(text, 3), text)

    def test_generalizes_the_collegial_sentence(self) -> None:
        self.assertEqual(
            bm.adapt_counts("Sei una delle dodici figure del collegio", 2),
            "Sei una delle figure del collegio",
        )


class TableFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        bm.ALL_FIGURE_NAMES.clear()
        bm.ALL_FIGURE_NAMES.update({"Vera", "Kai", "Aldo", "Marta", "Livia"})

    def test_drops_rows_whose_skills_are_all_absent(self) -> None:
        text = (
            "| Vera | `grl-agent-privacy` | dati personali |\n"
            "| Marta | `grl-agent-fiscal` | imposte |\n"
        )
        result = bm.filter_tables(text, {"grl-agent-privacy"}, {"Vera"})
        self.assertIn("grl-agent-privacy", result)
        self.assertNotIn("grl-agent-fiscal", result)

    def test_keeps_boundary_rows_that_name_an_installed_figure(self) -> None:
        text = "| Cifratura a riposo | Kai | Vera dice solo che serve |\n"
        self.assertIn("Kai", bm.filter_tables(text, set(), {"Vera"}))

    def test_drops_boundary_rows_about_absent_figures_only(self) -> None:
        text = "| Bandi e incentivi | Marta | Livia |\n"
        self.assertEqual(bm.filter_tables(text, set(), {"Vera"}), "")

    def test_leaves_non_figure_rows_alone(self) -> None:
        text = "| Campo | Valore |\n| ----- | ------ |\n"
        self.assertEqual(bm.filter_tables(text, set(), {"Vera"}), text)


class BoardSelectionSentenceTests(unittest.TestCase):
    SENTENCE = (
        "Punta a **due-quattro figure**; se le convochi tutte, indica cosa ciascuna "
        "ha di decisivo da dire su *questo* artefatto."
    )

    def test_keeps_the_range_when_the_module_has_more_than_four_figures(self) -> None:
        self.assertEqual(bm.adapt_board(self.SENTENCE, 5), self.SENTENCE)

    def test_drops_the_range_in_a_small_module(self) -> None:
        result = bm.adapt_board(self.SENTENCE, 2)
        self.assertNotIn("due-quattro", result)
        self.assertIn("Convoca solo chi ha qualcosa di decisivo", result)

    def test_the_sentence_still_exists_in_the_source_skill(self) -> None:
        # La sostituzione è testuale: se SKILL.md cambia frase e questo file no,
        # il derivato piccolo continua a consigliare quattro figure su due.
        skill = (ROOT / "src" / "skills" / "grl-board" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(self.SENTENCE, skill)

    def test_the_roster_lives_where_the_build_filters_it(self) -> None:
        self.assertIn("selection.md", bm.BOARD_ROSTER_FILES)
        roster = ROOT / "src" / "skills" / "grl-board" / "references" / "selection.md"
        self.assertIn("`grl-agent-seo`", roster.read_text(encoding="utf-8"))
        self.assertIn("`grl-agent-ads`", roster.read_text(encoding="utf-8"))


HELP_SOURCE = """module,skill,display-name,menu-code,description,action
Guardrails,grl-profile,Profila Guardrails,GP,"Profila le dodici figure.",profile
Guardrails,grl-agent-privacy,Vera — privacy,GV,"Quali dati personali tocca il progetto.",consult
Guardrails,grl-agent-fiscal,Marta — fisco,GT,"Imposte e bandi.",consult
"""


class HelpCsvTests(unittest.TestCase):
    def test_keeps_only_installed_skills_and_renames_them(self) -> None:
        result = bm.filter_help_csv(
            HELP_SOURCE,
            {"grl-profile", "grl-agent-privacy"},
            "Guardrails Governance",
            bm.core_renames(CORE, "grg"),
            3,
        )
        self.assertIn("Guardrails Governance,grg-profile,Profila Guardrails", result)
        self.assertIn("grl-agent-privacy", result)
        self.assertNotIn("grl-agent-fiscal", result)

    def test_adapts_the_figure_count(self) -> None:
        result = bm.filter_help_csv(
            HELP_SOURCE, {"grl-profile"}, "Guardrails Governance", bm.core_renames(CORE, "grg"), 3
        )
        self.assertIn("le tre figure", result)
        self.assertNotIn("dodici", result)


# Catalogo minimo con le colonne dei rimandi: `grl-agent-health` punta a una voce
# che un modulo ristretto non riceve.
HELP_LINKS_SOURCE = """module,skill,display-name,menu-code,description,action,args,phase,preceded-by,followed-by,required,output-location,outputs
Guardrails,grl-profile,Profila Guardrails,GP,"Profila le figure.",profile,,1-analysis,,grl-board:review,true,,profilo
Guardrails,grl-board,Convoca il collegio,GB,"Fa leggere l'artefatto.",review,[path],anytime,grl-profile:profile,grl-board:release-gate,false,,riepilogo
Guardrails,grl-agent-health,Livia — dominio clinico,GH,"Dato clinico e reparto.",consult,,anytime,grl-profile:profile,grl-mdsw:qualify,false,,clinico
Guardrails,grl-mdsw,È un dispositivo medico?,GQ,"Qualifica il software.",qualify,,anytime,grl-profile:profile,,false,,verdetto
"""


class HelpLinkPruningTests(unittest.TestCase):
    """Un modulo tematico riceve solo alcune righe: i rimandi fuori perimetro vanno tolti.

    Prima di questa potatura, `grh` pubblicava `grl-mdsw:qualify -> grl-agent-compliance:consult`
    verso una figura che quel modulo non installa, e `grw` faceva lo stesso con Bruno.
    """

    def filtra(self, skills: set[str]) -> str:
        return bm.filter_help_csv(HELP_LINKS_SOURCE, skills, "Guardrails Health", {}, 3)

    def test_drops_links_to_entries_left_out_of_the_module(self) -> None:
        result = self.filtra({"grl-profile", "grl-agent-health"})
        self.assertNotIn("grl-mdsw:qualify", result)
        self.assertNotIn("grl-board:review", result)

    def test_a_figure_falls_back_to_the_module_board(self) -> None:
        """Persa l'uscita verticale, la figura rimanda comunque al collegio."""
        result = self.filtra({"grl-profile", "grl-board", "grl-agent-health"})
        livia = next(
            r for r in csv.DictReader(io.StringIO(result)) if r["skill"] == "grl-agent-health"
        )
        self.assertEqual(livia["followed-by"], "grl-board:review")

    def test_a_missing_prerequisite_is_not_invented(self) -> None:
        """`preceded-by` è un vincolo: fuori perimetro si azzera, non si sostituisce."""
        result = self.filtra({"grl-board", "grl-agent-health"})
        livia = next(
            r for r in csv.DictReader(io.StringIO(result)) if r["skill"] == "grl-agent-health"
        )
        self.assertEqual(livia["preceded-by"], "")

    def test_the_board_does_not_fall_back_to_itself(self) -> None:
        """Il collegio non può essere il proprio passo successivo."""
        result = self.filtra({"grl-board", "grl-agent-health"})
        board = next(r for r in csv.DictReader(io.StringIO(result)) if r["skill"] == "grl-board")
        self.assertEqual(board["followed-by"], "")

    def test_keeps_links_whose_target_is_installed(self) -> None:
        result = self.filtra({"grl-profile", "grl-agent-health", "grl-mdsw", "grl-board"})
        self.assertIn("grl-mdsw:qualify", result)
        self.assertIn("grl-board:review", result)

    def test_pruning_only_empties_the_link_columns(self) -> None:
        """La potatura non deve spostare o riscrivere le altre colonne."""
        result = self.filtra({"grl-profile", "grl-agent-health"})
        righe = list(csv.DictReader(io.StringIO(result)))
        livia = next(r for r in righe if r["skill"] == "grl-agent-health")
        self.assertEqual(livia["display-name"], "Livia — dominio clinico")
        self.assertEqual(livia["description"], "Dato clinico e reparto.")
        self.assertEqual(livia["outputs"], "clinico")
        self.assertEqual(livia["followed-by"], "")

    def test_pruning_follows_the_core_rename(self) -> None:
        """Un rimando al core rinominato resta valido sotto il nuovo nome."""
        result = bm.filter_help_csv(
            HELP_LINKS_SOURCE,
            {"grl-profile", "grl-board", "grl-agent-health", "grl-mdsw"},
            "Guardrails Health",
            bm.core_renames(CORE, "grh"),
            3,
        )
        self.assertIn("grh-board:review", result)
        self.assertIn("grh-profile:profile", result)
        self.assertNotIn("grl-board:review", result)


class DerivedModuleLinkTests(unittest.TestCase):
    """Nessuno dei nove moduli generati pubblica un rimando verso una voce che non ha."""

    def test_no_derived_module_publishes_a_dead_link(self) -> None:
        topology = bm.load_topology(ROOT / "src" / "module-topology.yaml")
        source = (ROOT / "src" / "module-help.csv").read_text(encoding="utf-8")
        core = topology["core"]["skills"]
        for module in topology["modules"]:
            code = module["code"]
            installed = set(module["skills"]) | set(core)
            csv_text = bm.filter_help_csv(
                source, installed, module["name"], bm.core_renames(core, code), len(installed)
            )
            righe = list(csv.DictReader(io.StringIO(csv_text)))
            voci = {f"{r['skill']}:{r['action']}" for r in righe}
            for row in righe:
                for campo in ("preceded-by", "followed-by"):
                    bersaglio = row[campo].strip()
                    if not bersaglio:
                        continue
                    with self.subTest(modulo=code, voce=row["skill"], campo=campo):
                        self.assertIn(bersaglio, voci)


class WordPressModuleMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.topology = bm.load_topology(ROOT / "src" / "module-topology.yaml")
        cls.bundle = bm.load_module_yaml(ROOT / "src" / "module.yaml")
        cls.module = next(module for module in cls.topology["modules"] if module["code"] == "gwp")
        cls.renames = bm.core_renames(cls.topology["core"]["skills"], "gwp")
        cls.agents = bm.figures(cls.bundle["agents"], cls.module["skills"])
        cls.workflows = bm.workflow_skills(
            cls.module["skills"], {agent["code"] for agent in cls.bundle["agents"]}
        )
        help_source = (ROOT / "src" / "module-help.csv").read_text(encoding="utf-8")
        installed = set(cls.topology["core"]["skills"]) | set(cls.module["skills"])
        cls.help_csv = bm.filter_help_csv(
            help_source,
            installed,
            cls.module["name"],
            cls.renames,
            len(cls.agents),
        )

    def test_gwp_includes_wordpress_delivery(self) -> None:
        self.assertEqual(
            self.module["skills"],
            ["grl-agent-wordpress", "grl-wordpress-delivery", "grl-automation"],
        )
        self.assertEqual(self.workflows, ["grl-wordpress-delivery", "grl-automation"])

    def test_generated_metadata_stays_coherent(self) -> None:
        expected_skills = [
            "gwp-profile",
            "gwp-board",
            "grl-agent-wordpress",
            "grl-wordpress-delivery",
            "grl-automation",
        ]
        marketplace = json.loads(
            bm.render_marketplace(self.module, expected_skills, self.bundle["module_version"])
        )["plugins"][0]
        manifest = bm.yaml.safe_load(
            bm.render_module_yaml(
                self.module,
                self.agents,
                self.renames,
                self.bundle["module_version"],
            )
        )
        help_rows = list(csv.DictReader(io.StringIO(self.help_csv)))
        readme = bm.render_readme(
            self.module,
            self.agents,
            self.workflows,
            bm.parse_help_rows(self.help_csv),
            self.renames,
        )

        self.assertEqual(
            marketplace["skills"],
            [f"src/skills/{skill}" for skill in expected_skills],
        )
        self.assertEqual(marketplace["version"], manifest["module_version"])
        self.assertEqual(manifest["code"], "gwp")
        self.assertEqual([agent["code"] for agent in manifest["agents"]], ["grl-agent-wordpress"])

        delivery_rows = [row for row in help_rows if row["skill"] == "grl-wordpress-delivery"]
        self.assertEqual(
            {row["action"] for row in delivery_rows},
            {"create", "resume", "migrate", "verify"},
        )
        self.assertEqual(
            {row["action"]: row["preceded-by"] for row in delivery_rows},
            {
                "create": "gwp-profile:profile",
                "resume": "",
                "migrate": "gwp-profile:profile",
                "verify": "gwp-profile:profile",
            },
        )
        self.assertTrue(all(row["followed-by"] == "gwp-board:release-gate" for row in delivery_rows))
        self.assertTrue(
            all(
                row["output-location"] == "{output_folder}/wordpress/{slug}"
                for row in delivery_rows
            )
        )
        release_gate = next(
            row
            for row in help_rows
            if row["skill"] == "gwp-board" and row["action"] == "release-gate"
        )
        self.assertEqual(release_gate["output-location"], "{output_folder}/release-gates")
        self.assertEqual(release_gate["outputs"], "{release_slug}-{gate_started_at_utc}.md")
        self.assertEqual(readme.count("| `grl-wordpress-delivery` |"), 1)
        self.assertIn("| `gwp-board` | Multidisciplinary review |", readme)
        self.assertIn("## Skills and workflows", readme)
        self.assertNotIn("## Figure", readme)
        self.assertNotIn("## Skill e workflow", readme)

    def test_source_metadata_and_marketplace_stay_aligned(self) -> None:
        self.assertTrue((ROOT / "src" / "module.yaml").is_file())
        self.assertTrue((ROOT / "src" / "module-help.csv").is_file())
        self.assertFalse((ROOT / "src" / "skills" / "grl-setup").exists())
        plugin = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())["plugins"][0]
        self.assertEqual(plugin["version"], self.bundle["module_version"])
        self.assertIn("src/skills/grl-wordpress-delivery", plugin["skills"])
        self.assertNotIn("src/skills/grl-setup", plugin["skills"])

    def test_build_module_contains_delivery_and_board_references(self) -> None:
        def filesystem_files(source_root: Path, relative_dir: str) -> list[Path]:
            base = source_root / relative_dir
            return [
                path.relative_to(source_root)
                for path in base.rglob("*")
                if path.is_file() and path.name != ".memlog.md" and "__pycache__" not in path.parts
            ]

        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
            bm, "tracked_files", side_effect=filesystem_files
        ):
            result = bm.build_module(
                ROOT,
                Path(tmp),
                self.topology,
                self.module,
                self.bundle,
            )
            derived = Path(result["path"])
            self.assertTrue(
                (derived / "src" / "skills" / "grl-wordpress-delivery" / "SKILL.md").is_file()
            )
            self.assertTrue(
                (derived / "src" / "skills" / "gwp-board" / "references" / "release-gate.md").is_file()
            )
            self.assertTrue((derived / "src" / "module.yaml").is_file())
            self.assertTrue((derived / "src" / "module-help.csv").is_file())
            self.assertFalse((derived / "src" / "skills" / "gwp-setup").exists())

            board = derived / "src" / "skills" / "gwp-board"
            roster = (board / "references" / "selection.md").read_text(encoding="utf-8")
            # gwp installa il solo Milo: il roster non può restare quello del bundle,
            # o il collegio convoca figure che il modulo non ha.
            self.assertIn("`grl-agent-wordpress`", roster)
            self.assertNotIn("`grl-agent-privacy`", roster)
            self.assertIn("## Figure fuori da questo modulo", roster)
            skill = (board / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("## Figure fuori da questo modulo", skill)
            self.assertIn("Convoca solo chi ha qualcosa di decisivo", skill)


class DedicatedGroupModuleTopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.topology = bm.load_topology(ROOT / "src" / "module-topology.yaml")
        cls.bundle = bm.load_module_yaml(ROOT / "src" / "module.yaml")
        cls.by_code = {module["code"]: module for module in cls.topology["modules"]}

    def test_paid_media_has_its_own_repository_and_workflows(self) -> None:
        module = self.by_code["gpm"]
        self.assertEqual(module["repo"], "bmad-module-guardrails-paid-media")
        self.assertEqual(
            module["skills"],
            [
                "grl-agent-privacy",
                "grl-agent-legal",
                "grl-agent-ui-critic",
                "grl-agent-seo",
                "grl-agent-ads",
                "grl-agent-social",
                "grl-agent-creative",
                "grl-agent-imaging",
                "grl-ads",
                "grl-social",
                "grl-social-creative",
                "grl-automation",
            ],
        )
        self.assertEqual(
            bm.workflow_skills(module["skills"], {agent["code"] for agent in self.bundle["agents"]}),
            ["grl-ads", "grl-social", "grl-social-creative", "grl-automation"],
        )

    def test_automation_has_all_domain_agents_and_domain_workflows(self) -> None:
        module = self.by_code["gau"]
        self.assertEqual(module["repo"], "bmad-module-guardrails-automation")
        agent_codes = {agent["code"] for agent in self.bundle["agents"]}
        self.assertEqual(
            {skill for skill in module["skills"] if skill in agent_codes},
            agent_codes,
        )
        self.assertEqual(
            bm.workflow_skills(module["skills"], agent_codes),
            [
                "grl-legal-updates",
                "grl-fiscal-updates",
                "grl-mdsw",
                "grl-web",
                "grl-video-to-scroll",
                "grl-ads",
                "grl-social",
                "grl-social-creative",
                "grl-revenue-audit",
                "grl-revenue-plan",
                "grl-revenue-preflight",
                "grl-wordpress-delivery",
                "grl-bug-finder",
                "grl-issues",
                "grl-issue-readiness",
                "grl-issue-verify",
                "grl-automation",
                "grl-toolchain",
            ],
        )

    def test_revenue_has_its_own_repository_and_workflows(self) -> None:
        module = self.by_code["grv"]
        self.assertEqual(module["repo"], "bmad-module-guardrails-revenue")
        self.assertEqual(
            module["skills"],
            [
                "grl-agent-revenue",
                "grl-revenue-audit",
                "grl-revenue-plan",
                "grl-revenue-preflight",
                "grl-automation",
            ],
        )
        agent_codes = {agent["code"] for agent in self.bundle["agents"]}
        self.assertEqual(
            bm.workflow_skills(module["skills"], agent_codes),
            ["grl-revenue-audit", "grl-revenue-plan", "grl-revenue-preflight", "grl-automation"],
        )

    def test_topology_has_ten_unique_derived_repositories(self) -> None:
        modules = self.topology["modules"]
        self.assertEqual(self.topology["core"]["skills"], ["grl-profile", "grl-board"])
        self.assertEqual(len(modules), 10)
        self.assertEqual(len({module["code"] for module in modules}), 10)
        self.assertEqual(len({module["repo"] for module in modules}), 10)

    def test_every_derived_module_has_an_english_about_copy(self) -> None:
        for module in self.topology["modules"]:
            about = module["about"]
            self.assertLessEqual(len(about), 350)
            self.assertIn("review agent", about)
            self.assertIn("controlled BMad workflows", about)


class GreetingTests(unittest.TestCase):
    module = {"name": "Guardrails Fiscal", "code": "grf"}

    def test_singular_agreement(self) -> None:
        agents = [{"name": "Marta", "title": "Fiscalista"}]
        greeting = bm.render_greeting(self.module, agents, bm.core_renames(CORE, "grf"))
        self.assertIn("Marta (fiscalista) entra nel roster", greeting)
        self.assertIn("la figura parte cieca", greeting)

    def test_plural_agreement(self) -> None:
        agents = [{"name": "Vera", "title": "DPO"}, {"name": "Aldo", "title": "Tech Lawyer"}]
        greeting = bm.render_greeting(self.module, agents, bm.core_renames(CORE, "grg"))
        self.assertIn("Vera (dpo) e Aldo (tech lawyer) entrano nel roster", greeting)
        self.assertIn("le figure partono cieche", greeting)


class GeneratedGitignoreTests(unittest.TestCase):
    """Il `.gitignore` del derivato non deve escludere le fixture degli eval.

    Una regola `_bmad/` senza barra iniziale vale a ogni livello, quindi copre anche
    `src/skills/*/evals/_bmad/`. Nel derivato la fixture arriva ma non entra in git, e
    l'eval che la dichiara parte senza il file.
    """

    def test_local_install_rules_are_anchored_to_the_root(self) -> None:
        for regola in ("_bmad/", "_bmad-output/"):
            with self.subTest(regola=regola):
                self.assertIn(f"/{regola}", bm.GITIGNORE)
                self.assertNotRegex(bm.GITIGNORE, rf"(?m)^{re.escape(regola)}$")


class ShortDescriptionTests(unittest.TestCase):
    def test_keeps_the_first_sentence(self) -> None:
        self.assertEqual(bm.short("Prima frase. Seconda frase."), "Prima frase.")

    def test_truncates_without_double_punctuation(self) -> None:
        result = bm.short("parola " * 60)
        self.assertTrue(result.endswith("…"))
        self.assertNotIn(".…", result)

    def test_escapes_table_pipes(self) -> None:
        self.assertEqual(bm.short("a | b"), "a \\| b.")


if __name__ == "__main__":
    unittest.main()
