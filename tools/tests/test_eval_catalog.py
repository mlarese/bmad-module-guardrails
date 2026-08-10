"""Regression contracts for the Guardrails eval catalog.

These checks protect the high-risk routing and capability contracts that are
easy to regress while editing long natural-language skills.  They do not
replace runtime evals; they make the catalogue and its safety boundaries
machine-checkable before those evals run.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _trigger_entries(path: Path) -> list[dict]:
    data = _json(path)
    return data if isinstance(data, list) else data.get("triggers", data.get("queries", []))


def _resolve_ref(case_file: Path, value: str) -> list[Path]:
    skill_dir = case_file.parent.parent
    eval_dir = case_file.parent
    return [ROOT / value, skill_dir / value, eval_dir / value]


def test_all_eval_suites_and_fixture_references_are_structurally_valid() -> None:
    case_files = sorted((ROOT / "src" / "skills").glob("*/evals/cases.json"))
    trigger_files = sorted((ROOT / "src" / "skills").glob("*/evals/triggers.json"))

    assert len(case_files) == 32
    assert len(trigger_files) == len(case_files)

    case_count = 0
    trigger_count = 0
    missing: list[str] = []
    for case_file in case_files:
        data = _json(case_file)
        for case in data.get("cases", []):
            case_count += 1
            for value in case.get("files", []):
                if not any(path.is_file() for path in _resolve_ref(case_file, value)):
                    missing.append(f"{case_file}: {value}")
            fixture = case.get("fixture")
            if fixture and not any(path.exists() for path in _resolve_ref(case_file, fixture)):
                missing.append(f"{case_file}: {fixture}")
    for trigger_file in trigger_files:
        trigger_count += len(_trigger_entries(trigger_file))

    assert case_count >= 162
    assert trigger_count >= 413
    assert not missing, "fixture non risolti: " + "; ".join(missing)


def test_mdsw_owns_medical_device_and_dose_classification_queries() -> None:
    query = "il nostro software calcola la dose consigliata: dobbiamo marcarlo CE come dispositivo medico?"
    mdsw_entries = _trigger_entries(ROOT / "src/skills/grl-mdsw/evals/triggers.json")
    health_entries = _trigger_entries(ROOT / "src/skills/grl-agent-health/evals/triggers.json")

    assert any(item["query"] == query and item["should_trigger"] for item in mdsw_entries)
    assert any(item["query"] == query and not item["should_trigger"] for item in health_entries)
    description = (ROOT / "src/skills/grl-mdsw/SKILL.md").read_text(encoding="utf-8").lower()
    assert "marcatura ce" in description
    assert "dose" in description


def test_privacy_ai_act_ownership_matches_the_skill_contract() -> None:
    skill = (ROOT / "src/skills/grl-agent-privacy/SKILL.md").read_text(encoding="utf-8")
    cases = _json(ROOT / "src/skills/grl-agent-privacy/evals/cases.json")
    by_id = {case["id"]: " ".join(case.get("rubric", [])) for case in cases["cases"]}

    assert "FRIA" in skill and "Vera" in skill
    assert "Tutto il resto dell'AI Act è di **Aldo**" in skill
    assert "Aldo" in by_id["bias-e-dati-sensibili"]
    assert "Aldo" in by_id["fria-oltre-alla-dpia"]


def test_module_uses_root_metadata_without_a_setup_skill() -> None:
    assert not (ROOT / "src/skills/grl-setup").exists()
    help_csv = (ROOT / "src/module-help.csv").read_text(encoding="utf-8")
    assert "grl-setup" not in help_csv
    assert "grl-profile" in help_csv


def test_live_update_workflows_have_explicit_capability_fallbacks() -> None:
    for name in ("grl-fiscal-updates", "grl-legal-updates"):
        skill = (ROOT / "src/skills" / name / "SKILL.md").read_text(encoding="utf-8").lower()
        assert "missing_capability" in skill
        assert "fallback_review" in skill
        assert "bmad-deep-recon" in skill
        assert "bmad-review" in skill


def test_install_manifest_and_roster_metadata_preserve_routing_boundaries() -> None:
    manifest = (ROOT / "src/module.yaml").read_bytes()
    assert manifest
    assert (ROOT / "src/module-help.csv").is_file()
    manifest_text = manifest.decode("utf-8")

    for name, tokens in {
        "grl-agent-ai": ("Prompt injection", "AI Act-GDPR", "FRIA", "bias", "hosting", "GPU"),
        "grl-agent-ops": ("Prompt injection", "retention/privacy", "licenz", "Nils"),
        "grl-agent-database": ("ricerca live", "PostgreSQL", "Oracle", "MongoDB", "Redis", "vector"),
    }.items():
        skill = (ROOT / "src/skills" / name / "SKILL.md").read_text(encoding="utf-8")
        customize = (ROOT / "src/skills" / name / "customize.toml").read_text(encoding="utf-8")
        assert all(token.lower() in skill.lower() for token in tokens)
        assert all(token.lower() in customize.lower() for token in tokens)
        assert all(token.lower() in manifest_text.lower() for token in tokens)


def test_automation_contract_and_paid_media_evals_cover_safe_paths() -> None:
    route_matrix = (ROOT / "src/skills/grl-automation/references/route-matrix.md").read_text(
        encoding="utf-8"
    )
    execution_contract = (
        ROOT / "src/skills/grl-automation/references/execution-contract.md"
    ).read_text(encoding="utf-8")
    assert "TEA" in route_matrix
    assert all(token in execution_contract for token in ("owner:", "idempotency_key:", "stop_condition:"))
    automation = (ROOT / "src/skills/grl-automation/SKILL.md").read_text(encoding="utf-8")
    assert "handoff_status: pending" in automation
    assert "gate che dipende dalla capability resta `blocked`" in automation

    ads = (ROOT / "src/skills/grl-ads/SKILL.md").read_text(encoding="utf-8")
    assert "reachability: non verificata" in ads
    assert "prova osservata" in ads

    for name in ("grl-ads", "grl-agent-ads"):
        cases = _json(ROOT / "src/skills" / name / "evals/cases.json")["cases"]
        ids = {case["id"] for case in cases}
        assert any("comparable-change-set" in case_id for case_id in ids)
        incomparable = next(case for case in cases if "incomparable-stop" in case["id"])
        assert len(incomparable.get("files", [])) == 2
        assert "period-b-incomparable.csv" in " ".join(incomparable["files"] + [incomparable["input"]])
