#!/usr/bin/env python3
"""Coerenza fra i gruppi installabili, il manifesto e le skill che esistono davvero.

Sono i disallineamenti che si creano da soli aggiungendo una skill al modulo e
dimenticando di assegnarla a un gruppo: la skill verrebbe installata sempre, fuori
da ogni spunta, e nessuno se ne accorgerebbe.
"""

from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path


SETUP_SKILL = Path(__file__).resolve().parents[2]
SKILLS_DIR = SETUP_SKILL.parent
GROUPS_MAP = SETUP_SKILL / "assets" / "groups.toml"
MODULE_YAML = SETUP_SKILL / "assets" / "module.yaml"
PARTY_GROUPS = SETUP_SKILL / "assets" / "party-groups.toml"


def load(path: Path) -> dict:
    with path.open("rb") as stream:
        return tomllib.load(stream)


class GroupsCoherenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.groups = load(GROUPS_MAP)
        self.assigned = {
            skill for group in self.groups["groups"] for skill in group["skills"]
        }
        self.always = set(self.groups["always"])

    def test_every_installed_skill_belongs_somewhere(self) -> None:
        on_disk = {
            path.name
            for path in SKILLS_DIR.glob("grl-*")
            if path.is_dir() and (path / "SKILL.md").is_file()
        }
        self.assertEqual(
            on_disk - (self.assigned | self.always),
            set(),
            "skill del modulo non assegnate né a `always` né a un gruppo di groups.toml",
        )
        self.assertEqual(
            (self.assigned | self.always) - on_disk,
            set(),
            "groups.toml cita skill che non esistono su disco",
        )

    def test_group_ids_match_the_module_yaml_multiselect(self) -> None:
        text = MODULE_YAML.read_text(encoding="utf-8")
        block = text.split("enabled_groups:", 1)[1].split("strictness_override:", 1)[0]
        declared = set(re.findall(r'-\s+value:\s+"([^"]+)"', block))
        self.assertEqual(
            declared,
            {group["id"] for group in self.groups["groups"]},
            "i `value` della multi-select non coincidono con gli `id` di groups.toml",
        )

    def test_party_group_requirements_name_real_skills(self) -> None:
        known = self.assigned | self.always
        for group in load(PARTY_GROUPS)["workflow"]["party_groups"]:
            for skill in group.get("requires", []):
                self.assertIn(
                    skill, known, f"{group['id']}: `requires` cita {skill}, che non esiste"
                )


if __name__ == "__main__":
    unittest.main()
