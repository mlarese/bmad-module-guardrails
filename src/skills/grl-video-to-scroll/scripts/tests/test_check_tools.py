#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_tools  # noqa: E402


class TestCheckTools(unittest.TestCase):
    def test_report_passa_quando_tutto_e_disponibile(self) -> None:
        commands = [
            {"name": "uv", "installed": True, "usable": True},
            {"name": "ffmpeg", "installed": True, "usable": True},
            {"name": "ffprobe", "installed": True, "usable": True},
        ]
        runtime = [{"path": path, "installed": True} for path in check_tools.RUNTIME_FILES]
        report = check_tools.build_report(
            commands,
            runtime,
            system_name="Darwin",
            project_root=Path("/project"),
        )
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["missing"], [])
        self.assertEqual(report["install_commands"], [])

    def test_report_blocca_e_suggerisce_installazione(self) -> None:
        commands = [
            {"name": "uv", "installed": False, "usable": False},
            {"name": "ffmpeg", "installed": True, "usable": True},
            {"name": "ffprobe", "installed": False, "usable": False},
        ]
        runtime = [{"path": path, "installed": True} for path in check_tools.RUNTIME_FILES]
        report = check_tools.build_report(
            commands,
            runtime,
            system_name="Darwin",
            project_root=Path("/project"),
        )
        self.assertEqual(report["status"], "missing")
        self.assertEqual(report["missing"], ["uv", "ffprobe"])
        self.assertEqual(report["install_commands"], ["brew install uv ffmpeg"])

    def test_hint_windows_contiene_entrambi_i_tool_video(self) -> None:
        hints = check_tools.install_hints("Windows")
        self.assertTrue(any("uv" in hint for hint in hints))
        self.assertTrue(any("FFmpeg" in hint for hint in hints))


if __name__ == "__main__":
    unittest.main(verbosity=2)
