#!/usr/bin/env python3
"""Test del generatore dei moduli tematici Guardrails.

Coprono le trasformazioni che possono produrre un modulo sbagliato in silenzio:
la rinomina del core, i conteggi di figure adattati al perimetro, il filtro delle
tabelle e dei gruppi di party mode, e il filtro del catalogo di help.
"""

from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_modules as bm  # noqa: E402


CORE = ["grl-setup", "grl-profile", "grl-board"]
ROOT = Path(__file__).resolve().parents[2]


class CoreRenameTests(unittest.TestCase):
    def test_prefixes_core_skills_with_module_code(self) -> None:
        self.assertEqual(
            bm.core_renames(CORE, "grg"),
            {"grl-setup": "grg-setup", "grl-profile": "grg-profile", "grl-board": "grg-board"},
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


PARTY_SOURCE = """# intestazione originale

[[workflow.party_groups]]
id = "grl-governance"
name = "Governance"
scene = "tavolo"
members = ["grl-agent-privacy", "grl-agent-legal", "grl-agent-health"]
memory = false

[[workflow.party_groups]]
id = "grl-wordpress-delivery"
name = "WordPress"
scene = "laboratorio"
members = ["grl-agent-wordpress", "grl-agent-ops", "bmad-agent-ux-designer"]
memory = false
"""


class PartyGroupTests(unittest.TestCase):
    def test_reduces_members_to_installed_figures(self) -> None:
        toml, dropped = bm.filter_party_groups(
            PARTY_SOURCE,
            ["grl-governance"],
            {"grl-agent-privacy", "grl-agent-legal"},
            "Guardrails Governance",
        )
        self.assertIn('members = ["grl-agent-privacy", "grl-agent-legal"]', toml)
        self.assertNotIn("grl-agent-health", toml)
        self.assertEqual(dropped, [])

    def test_keeps_bmm_members(self) -> None:
        toml, _ = bm.filter_party_groups(
            PARTY_SOURCE,
            ["grl-wordpress-delivery"],
            {"grl-agent-wordpress", "grl-agent-ops"},
            "Guardrails WordPress",
        )
        self.assertIn("bmad-agent-ux-designer", toml)

    def test_drops_groups_left_below_the_threshold(self) -> None:
        toml, dropped = bm.filter_party_groups(
            PARTY_SOURCE, ["grl-wordpress-delivery"], {"grl-agent-wordpress"}, "Guardrails WordPress"
        )
        self.assertEqual(dropped, ["grl-wordpress-delivery"])
        self.assertNotIn("[[workflow.party_groups]]", toml)

    def test_fails_on_an_unknown_group(self) -> None:
        with self.assertRaises(bm.BuildError):
            bm.filter_party_groups(PARTY_SOURCE, ["grl-health"], {"grl-agent-health"}, "Health")


HELP_SOURCE = """module,skill,display-name,menu-code,description,action
Guardrails,grl-setup,Installa Guardrails,GS,"Registra Guardrails e le dodici figure.",configure
Guardrails,grl-agent-privacy,Vera — privacy,GV,"Quali dati personali tocca il progetto.",consult
Guardrails,grl-agent-fiscal,Marta — fisco,GT,"Imposte e bandi.",consult
"""


class HelpCsvTests(unittest.TestCase):
    def test_keeps_only_installed_skills_and_renames_them(self) -> None:
        result = bm.filter_help_csv(
            HELP_SOURCE,
            {"grl-setup", "grl-agent-privacy"},
            "Guardrails Governance",
            bm.core_renames(CORE, "grg"),
            3,
        )
        self.assertIn("Guardrails Governance,grg-setup,Installa Guardrails Governance", result)
        self.assertIn("grl-agent-privacy", result)
        self.assertNotIn("grl-agent-fiscal", result)

    def test_adapts_the_figure_count(self) -> None:
        result = bm.filter_help_csv(
            HELP_SOURCE, {"grl-setup"}, "Guardrails Governance", bm.core_renames(CORE, "grg"), 3
        )
        self.assertIn("le tre figure", result)
        self.assertNotIn("dodici", result)


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
            "gwp-setup",
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
            [],
            self.module["party_groups"],
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
        self.assertEqual(readme.count("| `grl-wordpress-delivery` |"), 4)
        self.assertIn("| `gwp-board` | Gate di rilascio |", readme)

    def test_source_metadata_copies_and_marketplace_stay_aligned(self) -> None:
        self.assertEqual(
            (ROOT / "src" / "module.yaml").read_bytes(),
            (ROOT / "src" / "skills" / "grl-setup" / "assets" / "module.yaml").read_bytes(),
        )
        self.assertEqual(
            (ROOT / "src" / "module-help.csv").read_bytes(),
            (ROOT / "src" / "skills" / "grl-setup" / "assets" / "module-help.csv").read_bytes(),
        )
        plugin = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())["plugins"][0]
        self.assertEqual(plugin["version"], self.bundle["module_version"])
        self.assertIn("src/skills/grl-wordpress-delivery", plugin["skills"])

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
            self.assertEqual(
                (derived / "src" / "module.yaml").read_bytes(),
                (derived / "src" / "skills" / "gwp-setup" / "assets" / "module.yaml").read_bytes(),
            )
            self.assertEqual(
                (derived / "src" / "module-help.csv").read_bytes(),
                (derived / "src" / "skills" / "gwp-setup" / "assets" / "module-help.csv").read_bytes(),
            )

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
