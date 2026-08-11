"""La versione del modulo descrive davvero quello che si installa.

`module_version` non lo calcola nessuno: resta fermo finché una persona non lo
tocca. Così il modulo è cresciuto da ventidue a ventitré figure restando a
`1.34.1` per sette commit, e chi aveva installato non ha visto niente cambiare.

Il lucchetto `src/module-version.lock` registra, accanto alla versione, il set di
skill e di moduli derivati che quella versione descrive. Questi test rendono la
regola vincolante: se il set cambia e la versione no, la build si ferma.

Un fallimento qui non si aggira aggiornando il lucchetto a mano: si alza la
versione con `python3 tools/bump_version.py --minor` (o `--patch`), che riscrive
entrambe le sedi e il lucchetto insieme.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))

import bump_version as bump  # noqa: E402

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


class VersionLockTests(unittest.TestCase):
    def setUp(self) -> None:
        self.lucchetto = json.loads((REPO / "src" / "module-version.lock").read_text(encoding="utf-8"))
        self.attuale = bump.stato_attuale()

    def test_le_due_sedi_dicono_la_stessa_versione(self) -> None:
        """`src/module.yaml` e il marketplace si leggono in momenti diversi: se divergono, uno dei due mente."""
        self.assertEqual(bump.versione_manifesto(), bump.versione_marketplace())

    def test_la_versione_ha_la_forma_di_una_versione(self) -> None:
        self.assertRegex(bump.versione_manifesto(), SEMVER)

    def test_il_lucchetto_e_alla_versione_corrente(self) -> None:
        self.assertEqual(
            self.lucchetto["module_version"],
            self.attuale["module_version"],
            "manifesto e lucchetto divergono: alza la versione con tools/bump_version.py",
        )

    def test_la_versione_descrive_le_skill_installate(self) -> None:
        """Una skill in più o in meno cambia cosa si installa: la versione deve dirlo."""
        cambiamenti = bump.differenze(self.lucchetto, self.attuale)
        self.assertEqual(
            cambiamenti,
            [],
            "il pacchetto è cambiato senza bump — esegui `python3 tools/bump_version.py --minor`",
        )

    def test_i_derivati_ereditano_la_versione_della_fonte(self) -> None:
        """I dieci moduli derivati non hanno una versione propria: la ricevono dalla build."""
        attesa = bump.versione_manifesto()
        for marketplace in sorted((REPO / "dist").glob("*/.claude-plugin/marketplace.json")):
            with self.subTest(modulo=marketplace.parents[1].name):
                dati = json.loads(marketplace.read_text(encoding="utf-8"))
                self.assertEqual(dati["plugins"][0]["version"], attesa)


class BumpArithmeticTests(unittest.TestCase):
    def test_i_tre_salti(self) -> None:
        self.assertEqual(bump.alza("1.35.1", "patch"), "1.35.2")
        self.assertEqual(bump.alza("1.35.1", "minor"), "1.36.0")
        self.assertEqual(bump.alza("1.35.1", "major"), "2.0.0")

    def test_il_minor_azzera_la_patch_e_il_major_azzera_tutto(self) -> None:
        """Un salto che non azzera lascia numeri come `2.3.7`, che non dicono niente."""
        self.assertEqual(bump.alza("1.9.9", "minor"), "1.10.0")
        self.assertEqual(bump.alza("1.9.9", "major"), "2.0.0")


if __name__ == "__main__":
    unittest.main()
