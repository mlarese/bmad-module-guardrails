#!/usr/bin/env python3
"""Il registro delle run di eval dice il vero o non serve a niente.

Un registro che nomina una skill cancellata, o che dichiara un esito fuori
vocabolario, è peggio dell'assenza di registro: si legge come una validazione e
non lo è. Questi test tengono le righe verificabili.
"""

from __future__ import annotations

import csv
import io
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import eval_registry as er  # noqa: E402

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class RegistryContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.righe = er.leggi()
        cls.skills = er.skill_names()

    def test_the_registry_file_exists(self) -> None:
        self.assertTrue(er.REGISTRY.is_file())

    def test_columns_match_the_declared_schema(self) -> None:
        with er.REGISTRY.open(encoding="utf-8") as handle:
            intestazione = next(csv.reader(handle))
        self.assertEqual(intestazione, er.COLONNE)

    def test_every_row_names_an_existing_skill(self) -> None:
        """Una riga su una skill cancellata dichiara una validazione che non copre niente."""
        for riga in self.righe:
            with self.subTest(skill=riga["skill"]):
                self.assertIn(riga["skill"], self.skills)

    def test_every_row_uses_the_declared_vocabulary(self) -> None:
        for riga in self.righe:
            with self.subTest(skill=riga["skill"], tipo=riga["tipo"]):
                self.assertIn(riga["tipo"], er.TIPI)
                self.assertIn(riga["esito"], er.ESITI)

    def test_every_row_carries_a_date_and_an_evidence(self) -> None:
        """Senza data non si sa se la run vale ancora; senza evidenza non si verifica."""
        for riga in self.righe:
            with self.subTest(skill=riga["skill"], tipo=riga["tipo"]):
                self.assertRegex(riga["data"], ISO)
                self.assertTrue(riga["evidenza"].strip())

    def test_coverage_reports_every_skill(self) -> None:
        """La copertura elenca tutte le skill, anche quelle senza alcuna run."""
        self.assertEqual(set(er.copertura()), self.skills)

    def test_a_rerun_on_the_same_day_supersedes_the_first_attempt(self) -> None:
        """Correggere una skill e rivalutarla nello stesso giorno è il caso normale.

        Il registro è append-only e cronologico: a parità di data deve vincere
        l'ultima riga, altrimenti l'esito corretto resta invisibile dietro il
        proprio primo tentativo — che è quello che si voleva superare.
        """
        skill = sorted(self.skills)[0]
        righe = [
            {"skill": skill, "data": "2026-01-01", "tipo": "quality", "esito": "parziale",
             "dettaglio": "primo tentativo", "runtime": "chat", "evidenza": "x"},
            {"skill": skill, "data": "2026-01-01", "tipo": "quality", "esito": "pass",
             "dettaglio": "dopo la correzione", "runtime": "chat", "evidenza": "x"},
        ]
        originale, er.leggi = er.leggi, lambda: righe
        try:
            vincente = er.copertura()[skill]["quality"]
        finally:
            er.leggi = originale
        self.assertEqual(vincente["esito"], "pass")
        self.assertEqual(vincente["dettaglio"], "dopo la correzione")


class RegistryWriteTests(unittest.TestCase):
    """`--add` non deve accettare una skill inventata né perdere le righe esistenti."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.registro = Path(self.tmp.name) / "run-registry.csv"
        self.registro.write_text(
            ",".join(er.COLONNE) + "\ngrl-web,2026-01-01,quality,pass,6/6,chat,report\n",
            encoding="utf-8",
        )
        self.originale, er.REGISTRY = er.REGISTRY, self.registro

    def tearDown(self) -> None:
        er.REGISTRY = self.originale
        self.tmp.cleanup()

    def argomenti(self, skill: str):
        import argparse

        return argparse.Namespace(
            add=skill, data="2026-08-10", tipo="trigger", esito="pass",
            dettaglio="20/20", runtime="chat", evidenza="report",
        )

    def test_rejects_an_unknown_skill(self) -> None:
        self.assertEqual(er.aggiungi(self.argomenti("grl-agent-inesistente")), 1)

    def test_appends_without_dropping_earlier_rows(self) -> None:
        self.assertEqual(er.aggiungi(self.argomenti("grl-web")), 0)
        righe = list(csv.DictReader(io.StringIO(self.registro.read_text(encoding="utf-8"))))
        self.assertEqual(len(righe), 2)
        self.assertEqual(righe[0]["tipo"], "quality")
        self.assertEqual(righe[1]["tipo"], "trigger")


if __name__ == "__main__":
    unittest.main()
