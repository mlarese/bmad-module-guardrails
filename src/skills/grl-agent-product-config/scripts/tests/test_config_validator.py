import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config_validator import (  # noqa: E402
    DocumentError,
    load_document,
    resolve_catalog_path,
    validate_catalog,
    validate_config,
)

CATALOG = {
    "version": 1,
    "line": {
        "code": "infissi-pvc",
        "name": "Serramenti in PVC",
        "source": "listino 2026 rev.3",
        "reviewed_by": "Ufficio tecnico",
        "reviewed_on": "2026-08-10",
    },
    "options": [
        {
            "code": "serie",
            "type": "enum",
            "required": True,
            "impact": "blocking",
            "values": [{"code": "s70"}, {"code": "s82"}],
        },
        {
            "code": "larghezza",
            "type": "number",
            "unit": "mm",
            "required": True,
            "impact": "blocking",
            "min": 400,
            "max": 2400,
        },
        {"code": "rinforzo", "type": "boolean", "impact": "blocking"},
        {
            "code": "colore_interno",
            "type": "enum",
            "impact": "pricing",
            "values": [{"code": "bianco"}, {"code": "ral"}],
        },
        {"code": "codice_ral", "type": "text", "impact": "cosmetic"},
    ],
    "rules": [
        {
            "kind": "requires",
            "when": {"option": "serie", "value": "s82"},
            "then": {"option": "rinforzo", "value": True},
            "because": "peso anta oltre 90 kg",
        },
        {
            "kind": "excludes",
            "when": {"option": "colore_interno", "value": "ral"},
            "then": {"option": "serie", "value": "s70"},
            "because": "la verniciatura RAL non è disponibile sul profilo 70",
        },
        {
            "kind": "required_if",
            "when": {"option": "colore_interno", "value": "ral"},
            "then": {"option": "codice_ral"},
            "because": "senza codice non è ordinabile",
        },
    ],
}

CONFIG = {
    "version": 1,
    "line": "infissi-pvc",
    "selections": {"serie": "s82", "larghezza": 1800, "rinforzo": True},
    "evidence": {
        "serie": {"origin": "written", "quote": "p. 2 r. 14"},
        "larghezza": {"origin": "written", "quote": "allegato A"},
        "rinforzo": {"origin": "imposed", "rule": "requires: serie=s82"},
    },
}


def codes(entries):
    return [entry["code"] for entry in entries]


class CatalogTests(unittest.TestCase):
    def test_reference_catalog_is_valid(self):
        report = validate_catalog(copy.deepcopy(CATALOG))
        self.assertEqual(report["status"], "valid")
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["options"], 5)

    def test_catalog_without_human_review_is_rejected(self):
        catalog = copy.deepcopy(CATALOG)
        del catalog["line"]["reviewed_by"]
        report = validate_catalog(catalog)
        self.assertEqual(report["status"], "invalid")
        self.assertIn("catalog-not-reviewed", codes(report["errors"]))

    def test_rule_without_reason_is_an_error(self):
        catalog = copy.deepcopy(CATALOG)
        del catalog["rules"][0]["because"]
        report = validate_catalog(catalog)
        self.assertIn("rule-without-reason", codes(report["errors"]))

    def test_requires_and_excludes_on_the_same_pair_contradict(self):
        catalog = copy.deepcopy(CATALOG)
        catalog["rules"].append(
            {
                "kind": "excludes",
                "when": {"option": "serie", "value": "s82"},
                "then": {"option": "rinforzo", "value": True},
                "because": "regola inserita per errore",
            }
        )
        report = validate_catalog(catalog)
        self.assertIn("rule-contradiction", codes(report["errors"]))

    def test_required_option_made_impossible_by_an_excludes(self):
        """Un obbligo con un solo valore, vietato da un excludes: catalogo insolubile."""
        catalog = copy.deepcopy(CATALOG)
        catalog["options"].append(
            {
                "code": "vetro",
                "type": "enum",
                "required": True,
                "impact": "blocking",
                "values": [{"code": "triplo"}],
            }
        )
        catalog["rules"].append(
            {
                "kind": "excludes",
                "when": {"option": "serie", "value": "s70"},
                "then": {"option": "vetro", "value": "triplo"},
                "because": "la serie 70 non porta il triplo vetro",
            }
        )
        report = validate_catalog(catalog)
        self.assertIn("required-impossible", codes(report["errors"]))
        self.assertEqual(report["status"], "invalid")

    def test_required_option_with_alternatives_is_not_impossible(self):
        """Se l'obbligo ha un'alternativa, l'excludes non lo rende insolubile."""
        catalog = copy.deepcopy(CATALOG)
        catalog["rules"].append(
            {
                "kind": "excludes",
                "when": {"option": "rinforzo", "value": True},
                "then": {"option": "serie", "value": "s70"},
                "because": "il rinforzo non entra nella serie 70",
            }
        )
        report = validate_catalog(catalog)
        self.assertNotIn("required-impossible", codes(report["errors"]))

    def test_rule_pointing_at_an_unknown_option(self):
        catalog = copy.deepcopy(CATALOG)
        catalog["rules"][0]["then"] = {"option": "maniglia", "value": "cromo"}
        report = validate_catalog(catalog)
        self.assertIn("rule-unknown-option", codes(report["errors"]))

    def test_rule_using_a_value_the_option_does_not_allow(self):
        catalog = copy.deepcopy(CATALOG)
        catalog["rules"][0]["when"] = {"option": "serie", "value": "s90"}
        report = validate_catalog(catalog)
        self.assertIn("value-not-allowed", codes(report["errors"]))

    def test_duplicated_option_code(self):
        catalog = copy.deepcopy(CATALOG)
        catalog["options"].append({"code": "serie", "type": "text"})
        report = validate_catalog(catalog)
        self.assertIn("option-duplicated", codes(report["errors"]))

    def test_inverted_numeric_range(self):
        catalog = copy.deepcopy(CATALOG)
        catalog["options"][1]["min"] = 3000
        report = validate_catalog(catalog)
        self.assertIn("range-inverted", codes(report["errors"]))

    def test_requires_cycle_is_only_a_warning(self):
        catalog = copy.deepcopy(CATALOG)
        catalog["rules"].append(
            {
                "kind": "requires",
                "when": {"option": "rinforzo", "value": True},
                "then": {"option": "serie", "value": "s82"},
                "because": "il rinforzo esiste solo sulla serie 82",
            }
        )
        report = validate_catalog(catalog)
        self.assertEqual(report["status"], "valid")
        self.assertIn("rule-cycle", codes(report["warnings"]))


class ConfigTests(unittest.TestCase):
    def test_complete_configuration_is_valid(self):
        report = validate_config(copy.deepcopy(CONFIG), copy.deepcopy(CATALOG))
        self.assertEqual(report["status"], "valid")
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["missing"], [])

    def test_missing_required_option_is_incomplete_not_invalid(self):
        config = copy.deepcopy(CONFIG)
        del config["selections"]["larghezza"]
        del config["evidence"]["larghezza"]
        report = validate_config(config, copy.deepcopy(CATALOG))
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual([item["option"] for item in report["missing"]], ["larghezza"])

    def test_requires_with_a_different_value_is_a_conflict(self):
        config = copy.deepcopy(CONFIG)
        config["selections"]["rinforzo"] = False
        report = validate_config(config, copy.deepcopy(CATALOG))
        self.assertEqual(report["status"], "invalid")
        self.assertIn("requires-violated", codes(report["errors"]))

    def test_requires_with_the_option_absent_is_incomplete(self):
        config = copy.deepcopy(CONFIG)
        del config["selections"]["rinforzo"]
        del config["evidence"]["rinforzo"]
        report = validate_config(config, copy.deepcopy(CATALOG))
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual(report["missing"][0]["expected"], True)

    def test_excludes_violation_is_invalid(self):
        config = copy.deepcopy(CONFIG)
        config["selections"] = {"serie": "s70", "larghezza": 1200, "colore_interno": "ral"}
        config["evidence"] = {
            "serie": {"origin": "written", "quote": "p. 1"},
            "larghezza": {"origin": "written", "quote": "p. 1"},
            "colore_interno": {"origin": "written", "quote": "p. 3"},
        }
        report = validate_config(config, copy.deepcopy(CATALOG))
        self.assertEqual(report["status"], "invalid")
        self.assertIn("excludes-violated", codes(report["errors"]))

    def test_required_if_opens_a_missing_entry(self):
        config = copy.deepcopy(CONFIG)
        config["selections"]["colore_interno"] = "ral"
        config["evidence"]["colore_interno"] = {"origin": "written", "quote": "p. 3"}
        report = validate_config(config, copy.deepcopy(CATALOG))
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual([item["option"] for item in report["missing"]], ["codice_ral"])

    def test_selection_without_declared_origin_is_invalid(self):
        config = copy.deepcopy(CONFIG)
        del config["evidence"]["serie"]
        report = validate_config(config, copy.deepcopy(CATALOG))
        self.assertEqual(report["status"], "invalid")
        self.assertIn("evidence-missing", codes(report["errors"]))

    def test_value_outside_the_declared_range(self):
        config = copy.deepcopy(CONFIG)
        config["selections"]["larghezza"] = 3000
        report = validate_config(config, copy.deepcopy(CATALOG))
        self.assertIn("value-above-max", codes(report["errors"]))

    def test_unknown_option_is_not_silently_accepted(self):
        config = copy.deepcopy(CONFIG)
        config["selections"]["maniglia"] = "cromo"
        config["evidence"]["maniglia"] = {"origin": "written", "quote": "p. 4"}
        report = validate_config(config, copy.deepcopy(CATALOG))
        self.assertIn("unknown-option", codes(report["errors"]))

    def test_configuration_on_an_unreviewed_catalog_is_invalid(self):
        catalog = copy.deepcopy(CATALOG)
        del catalog["line"]["reviewed_by"]
        report = validate_config(copy.deepcopy(CONFIG), catalog)
        self.assertEqual(report["status"], "invalid")
        self.assertIn("catalog-not-reviewed", codes(report["errors"]))

    def test_line_mismatch_between_config_and_catalog(self):
        config = copy.deepcopy(CONFIG)
        config["line"] = "portoni"
        report = validate_config(config, copy.deepcopy(CATALOG))
        self.assertIn("line-mismatch", codes(report["errors"]))

    def test_optional_option_left_open_does_not_break_validity(self):
        report = validate_config(copy.deepcopy(CONFIG), copy.deepcopy(CATALOG))
        self.assertEqual(report["status"], "valid")
        self.assertEqual([item["option"] for item in report["open_choices"]], ["colore_interno"])
        self.assertEqual(report["open_choices"][0]["impact"], "pricing")

    def test_a_conditional_option_is_not_an_open_choice_until_its_rule_fires(self):
        report = validate_config(copy.deepcopy(CONFIG), copy.deepcopy(CATALOG))
        self.assertNotIn("codice_ral", [item["option"] for item in report["open_choices"]])

    def test_an_option_the_rules_demand_is_missing_not_an_open_choice(self):
        config = copy.deepcopy(CONFIG)
        config["selections"]["colore_interno"] = "ral"
        config["evidence"]["colore_interno"] = {"origin": "written", "quote": "p. 3"}
        report = validate_config(config, copy.deepcopy(CATALOG))
        self.assertEqual(report["status"], "incomplete")
        self.assertEqual([item["option"] for item in report["missing"]], ["codice_ral"])
        self.assertEqual(report["open_choices"], [])

    def test_missing_entries_are_ordered_by_impact(self):
        config = copy.deepcopy(CONFIG)
        config["selections"] = {"colore_interno": "ral"}
        config["evidence"] = {"colore_interno": {"origin": "written", "quote": "p. 3"}}
        report = validate_config(config, copy.deepcopy(CATALOG))
        impacts = [item["impact"] for item in report["missing"]]
        self.assertEqual(impacts, sorted(impacts, key=["blocking", "pricing", "cosmetic"].index))


class DocumentTests(unittest.TestCase):
    def test_json_is_readable_without_pyyaml(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "catalog.json"
            path.write_text(json.dumps(CATALOG), encoding="utf-8")
            self.assertEqual(load_document(path)["line"]["code"], "infissi-pvc")

    def test_unknown_extension_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "catalog.txt"
            path.write_text("serie: s70", encoding="utf-8")
            with self.assertRaises(DocumentError):
                load_document(path)

    def test_catalog_path_is_resolved_next_to_the_configuration(self):
        resolved = resolve_catalog_path(
            {"catalog": "cataloghi/infissi.yaml"}, Path("/progetto/config.yaml"), None
        )
        self.assertEqual(resolved, Path("/progetto/cataloghi/infissi.yaml"))

    def test_configuration_without_catalog_reference_is_refused(self):
        with self.assertRaises(DocumentError):
            resolve_catalog_path({}, Path("/progetto/config.yaml"), None)


if __name__ == "__main__":
    unittest.main()
