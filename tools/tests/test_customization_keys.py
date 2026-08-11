"""Ogni chiave di `[workflow]` deve comparire nel testo che la skill legge.

Perché esiste
-------------
Una revisione delle quarantaquattro skill ha trovato sedici difetti con la stessa
radice: una chiave dichiarata in `customize.toml`, con tanto di commento che ne
spiega l'effetto, e nessun punto della `SKILL.md` che la legga. L'utente cambia il
valore, non succede niente, e nessuno se ne accorge. Due delle chiavi inerti erano
presidi di sicurezza.

Il test è deliberatamente grezzo: cerca la stringa `{workflow.<chiave>}` nei file
`.md` e `.py` della skill. Non prova che la chiave sia usata bene — prova che
qualcuno la nomini. È il minimo che separa una leva da una decorazione.

La tabella `[agent]` resta fuori: quei campi sono il contratto di roster letto dal
manifesto del modulo, non segnaposto da risolvere dentro la prosa.
"""

from __future__ import annotations

import tomllib
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "src" / "skills"

TESTO = {".md", ".py"}


def skill_customize() -> list[tuple[str, Path]]:
    return sorted(
        (d.name, d / "customize.toml")
        for d in SKILLS.iterdir()
        if (d / "customize.toml").is_file()
    )


def leggi_testo_skill(skill: Path) -> str:
    return "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in skill.rglob("*")
        if p.suffix in TESTO
    )


class CustomizationKeysTests(unittest.TestCase):
    def test_ogni_chiave_workflow_e_usata_nella_skill(self) -> None:
        for nome, toml_path in skill_customize():
            with self.subTest(skill=nome):
                dati = tomllib.loads(toml_path.read_text(encoding="utf-8"))
                chiavi = dati.get("workflow", {})
                testo = leggi_testo_skill(toml_path.parent)
                inerti = [k for k in chiavi if f"{{workflow.{k}}}" not in testo]
                self.assertEqual(
                    inerti,
                    [],
                    f"{nome}: chiavi dichiarate e mai lette — {', '.join(inerti)}. "
                    "Usale nella SKILL.md o in una reference, oppure toglile dal customize.toml.",
                )

    def test_la_skill_con_customize_risolve_la_personalizzazione(self) -> None:
        """Chi dichiara chiavi deve anche eseguire il resolver che le popola."""
        for nome, toml_path in skill_customize():
            with self.subTest(skill=nome):
                dati = tomllib.loads(toml_path.read_text(encoding="utf-8"))
                if not dati.get("workflow"):
                    continue
                skill_md = (toml_path.parent / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(
                    "resolve_customization.py",
                    skill_md,
                    f"{nome}: dichiara [workflow] ma non esegue resolve_customization.py, "
                    "quindi ogni {workflow.*} resta un segnaposto non risolto.",
                )


if __name__ == "__main__":
    unittest.main()
