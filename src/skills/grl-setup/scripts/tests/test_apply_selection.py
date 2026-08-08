#!/usr/bin/env python3
"""Test della quarantena delle skill escluse dalla selezione dei gruppi."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "apply-selection.py"
GROUPS_MAP = ROOT / "assets" / "groups.toml"

# Un campione per gruppo, più le tre skill che non si possono disattivare.
SKILLS = (
    "grl-setup",
    "grl-profile",
    "grl-board",
    "grl-agent-privacy",
    "grl-agent-legal",
    "grl-agent-compliance",
    "grl-legal-updates",
    "grl-agent-security",
    "grl-agent-ops",
    "grl-agent-health",
    "grl-mdsw",
    "grl-agent-ui-critic",
    "grl-web",
    "grl-agent-fiscal",
    "grl-fiscal-updates",
)


class ApplySelectionTests(unittest.TestCase):
    def make_project(self, directory: str) -> Path:
        project = Path(directory)
        (project / "_bmad" / "custom").mkdir(parents=True)
        skills = project / ".claude" / "skills"
        skills.mkdir(parents=True)
        for name in SKILLS:
            (skills / name).mkdir()
            (skills / name / "SKILL.md").write_text(name, encoding="utf-8")
        return project

    def run_script(self, project: Path, groups: str, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--project-root", str(project),
                "--groups", groups,
                "--groups-map", str(GROUPS_MAP),
                *extra,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def installed(self, project: Path) -> set[str]:
        return {p.name for p in (project / ".claude" / "skills").iterdir() if p.is_dir()}

    def test_quarantines_unselected_and_keeps_always(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)

            result = self.run_script(project, "governance")

            self.assertEqual(result.returncode, 0, result.stderr)
            installed = self.installed(project)
            self.assertEqual(
                installed,
                {
                    # I sette workflow ci sono sempre, qualunque gruppo sia spuntato.
                    "grl-setup", "grl-profile", "grl-board", "grl-mdsw",
                    "grl-legal-updates", "grl-fiscal-updates", "grl-web",
                    # Le figure, invece, solo quelle di governance.
                    "grl-agent-privacy", "grl-agent-legal", "grl-agent-compliance",
                },
            )
            disabled = project / "_bmad" / "grl" / ".disabled" / "claude__skills"
            self.assertTrue((disabled / "grl-agent-health").is_dir())
            self.assertTrue((disabled / "grl-agent-ui-critic").is_dir())

    def test_restores_a_group_that_is_selected_again(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)

            self.run_script(project, "governance")
            result = self.run_script(project, "governance,health")

            self.assertEqual(result.returncode, 0, result.stderr)
            installed = self.installed(project)
            self.assertIn("grl-agent-health", installed)
            self.assertNotIn("grl-agent-ui-critic", installed)
            # Il contenuto torna com'era, non un guscio vuoto.
            self.assertEqual(
                (project / ".claude" / "skills" / "grl-agent-health" / "SKILL.md").read_text(encoding="utf-8"),
                "grl-agent-health",
            )

    def test_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)

            self.run_script(project, "web")
            result = self.run_script(project, "web")

            payload = json.loads(result.stdout)
            self.assertFalse(payload["changed"])
            self.assertEqual(payload["skills_quarantined"], [])
            self.assertEqual(payload["skills_restored"], [])

    def test_writes_selection_to_team_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)

            self.run_script(project, "governance,fiscal")

            config = project / "_bmad" / "custom" / "config.toml"
            parsed = tomllib.loads(config.read_text(encoding="utf-8"))
            self.assertEqual(
                parsed["modules"]["grl"]["enabled_groups"], ["fiscal", "governance"]
            )

    def test_all_keeps_everything(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)

            result = self.run_script(project, "all")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.installed(project), set(SKILLS))

    def test_dry_run_does_not_touch_disk(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)

            result = self.run_script(project, "governance", "--dry-run")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.installed(project), set(SKILLS))
            self.assertFalse((project / "_bmad" / "grl" / ".disabled").exists())
            self.assertFalse((project / "_bmad" / "custom" / "config.toml").exists())

    def test_unknown_skill_is_left_alone_with_a_warning(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)
            (project / ".claude" / "skills" / "grl-esperimento").mkdir()

            result = self.run_script(project, "governance")

            payload = json.loads(result.stdout)
            self.assertIn("grl-esperimento", self.installed(project))
            self.assertTrue(any("grl-esperimento" in w for w in payload["warnings"]))

    def test_unknown_group_fails_without_touching_disk(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = self.make_project(directory)

            result = self.run_script(project, "governance,inesistente")

            self.assertEqual(result.returncode, 1)
            self.assertEqual(self.installed(project), set(SKILLS))

    def test_missing_bmad_install_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / ".claude" / "skills").mkdir(parents=True)

            result = self.run_script(project, "governance")

            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
