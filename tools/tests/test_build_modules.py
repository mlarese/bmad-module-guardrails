#!/usr/bin/env python3
"""Test del generatore dei moduli tematici Guardrails.

Coprono le trasformazioni che possono produrre un modulo sbagliato in silenzio:
la rinomina del core, i conteggi di figure adattati al perimetro, il filtro delle
tabelle e dei gruppi di party mode, e il filtro del catalogo di help.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_modules as bm  # noqa: E402


CORE = ["grl-setup", "grl-profile", "grl-board"]


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
