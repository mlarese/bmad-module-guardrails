#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validate_manifest  # noqa: E402


class TestManifest(unittest.TestCase):
    def setUp(self) -> None:
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        frames = self.root / "frames"
        frames.mkdir()
        payload = b"frame"
        (frames / "frame-00000.webp").write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        self.document = {
            "schema": validate_manifest.SCHEMA,
            "frame_count": 1,
            "total_bytes": len(payload),
            "frames": [
                {
                    "index": 0,
                    "file": "frames/frame-00000.webp",
                    "timestamp_seconds": 0.0,
                    "scroll_progress": 0.0,
                    "bytes": len(payload),
                    "sha256": digest,
                }
            ],
        }
        self.path = self.root / "frame-manifest.json"
        self.path.write_text(json.dumps(self.document), encoding="utf-8")

    def tearDown(self) -> None:
        self.folder.cleanup()

    def test_manifest_valido(self) -> None:
        report = validate_manifest.validate_manifest(self.path, root=self.root)
        self.assertEqual(report["status"], "pass")

    def test_hash_modificato_fallisce(self) -> None:
        (self.root / "frames" / "frame-00000.webp").write_bytes(b"changed")
        report = validate_manifest.validate_manifest(self.path, root=self.root)
        self.assertEqual(report["status"], "fail")
        self.assertTrue(any("sha256" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
