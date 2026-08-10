#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import extract_frames  # noqa: E402


class TestPianoFrame(unittest.TestCase):
    def test_timestamp_ignora_commenti_e_doppioni(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "timestamps.txt"
            path.write_text("# hero\n0\n1.5 # mezzo\n1.5\n3\n", encoding="utf-8")
            self.assertEqual(extract_frames.parse_timestamps(path, 3, 10), [0.0, 1.5, 3.0])

    def test_timestamp_fuori_range(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "timestamps.txt"
            path.write_text("4\n", encoding="utf-8")
            with self.assertRaises(extract_frames.UserError):
                extract_frames.parse_timestamps(path, 3, 10)

    def test_fps_inizia_da_zero_e_rispetta_il_tetto(self) -> None:
        self.assertEqual(extract_frames.uniform_timestamps(10, 2, 4), [0.0, 0.5, 1.0, 1.5])

    def test_progressione_normalizzata(self) -> None:
        self.assertEqual(extract_frames.make_progress(3), [0.0, 0.5, 1.0])
        self.assertEqual(extract_frames.make_progress(1), [0.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
