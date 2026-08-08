#!/usr/bin/env python3
"""Regression tests for the streaming OpenCode adapter shim."""
from __future__ import annotations

import json
import stat
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SHIM = ROOT / "evals" / "adapters" / "opencode-shim.py"


def test_translates_events_before_opencode_exits_and_forwards_stderr(tmp_path: Path) -> None:
    fake = tmp_path / "fake-opencode.py"
    fake.write_text(
        "#!/usr/bin/env python3\n"
        "import json, sys, time\n"
        "event = {'type': 'tool_use', 'part': {'type': 'tool', 'tool': 'skill', "
        "'callID': 'call-1', 'state': {'input': {'name': 'demo'}}}}\n"
        "print(json.dumps(event), flush=True)\n"
        "print('diagnostic from fake opencode', file=sys.stderr, flush=True)\n"
        "time.sleep(1.0)\n",
        encoding="utf-8",
    )
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)

    started = time.monotonic()
    proc = subprocess.Popen(
        [sys.executable, str(SHIM), "--opencode", str(fake), "--model", "fake", "prompt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert proc.stdout is not None
    first_line = proc.stdout.readline()
    first_event_elapsed = time.monotonic() - started
    stdout_tail, stderr = proc.communicate(timeout=3)

    assert proc.returncode == 0, stderr
    assert first_event_elapsed < 0.7, "the shim must not buffer stdout until process exit"
    translated = json.loads(first_line)
    assert translated["message"]["content"][0]["name"] == "Skill"
    assert "diagnostic from fake opencode" in stderr
    assert stdout_tail == ""
