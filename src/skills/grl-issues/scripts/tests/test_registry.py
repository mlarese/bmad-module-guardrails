#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest"]
# ///
"""Test di registry.py.

Coprono le tre cose che, se sbagliano, si notano soltanto quando è tardi: la
precedenza degli stati, la conservazione dei campi che GitHub non conosce, e il
comportamento davanti a un registro illeggibile.

Nessun test chiama `gh`: il sync legge le issue da un file con `--input`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import registry  # noqa: E402


def issue(numero: int, **campi) -> dict:
    base = {
        "number": numero,
        "title": f"issue {numero}",
        "state": "OPEN",
        "labels": [],
        "milestone": None,
        "assignees": [],
        "updatedAt": "2026-08-10T10:00:00Z",
        "url": "u",
    }
    base.update(campi)
    return base


def sincronizza(tmp_path: Path, issues: list[dict], **extra) -> dict:
    sorgente = tmp_path / "gh.json"
    sorgente.write_text(json.dumps(issues), encoding="utf-8")
    argv = [
        "sync",
        "--path", str(tmp_path / "registry.json"),
        "--repo", "mlarese/x",
        "--input", str(sorgente),
        "--hold-labels", extra.get("hold", "blocked,on-hold"),
        "--rejected-labels", extra.get("rejected", "wontfix,invalid"),
    ]
    return registry.comando_sync(_costruisci_args(argv))


def _costruisci_args(argv: list[str]):
    """Gli argomenti passano dal parser vero: i default contano quanto il codice."""
    return registry.costruisci_parser().parse_args(argv)


# --- precedenza degli stati --------------------------------------------------


def test_lo_stato_chiuso_vince_su_tutto(tmp_path: Path) -> None:
    esito = sincronizza(tmp_path, [issue(1, state="CLOSED", labels=[{"name": "blocked"}])])
    assert esito["by_status"]["CHIUSA"] == 1


def test_il_rifiuto_precede_l_attesa(tmp_path: Path) -> None:
    esito = sincronizza(tmp_path, [issue(2, labels=[{"name": "wontfix"}, {"name": "blocked"}])])
    assert esito["by_status"]["NON_APPROVATA"] == 1
    assert esito["by_status"]["IN_ATTESA"] == 0


def test_l_attesa_precede_l_assegnatario(tmp_path: Path) -> None:
    esito = sincronizza(tmp_path, [issue(3, labels=[{"name": "blocked"}], assignees=[{"login": "x"}])])
    assert esito["by_status"]["IN_ATTESA"] == 1


def test_senza_verdetto_resta_da_valutare(tmp_path: Path) -> None:
    esito = sincronizza(tmp_path, [issue(4)])
    assert esito["by_status"]["DA_VALUTARE"] == 1


def test_un_attesa_da_label_non_ha_condizione_di_uscita(tmp_path: Path) -> None:
    esito = sincronizza(tmp_path, [issue(5, labels=[{"name": "on-hold"}])])
    assert esito["hold_without_exit"] == [5]


# --- campi locali e merge ----------------------------------------------------


def test_il_sync_conserva_verdetto_e_nota_dichiarata(tmp_path: Path) -> None:
    sincronizza(tmp_path, [issue(6)])
    percorso = tmp_path / "registry.json"

    registry.comando_set(
        _costruisci_args(["set", "--path", str(percorso), "--issue", "6", "--verdict", "NON_PRONTA", "--missing", "criterio_di_accettazione"])
    )
    sincronizza(tmp_path, [issue(6, updatedAt="2026-08-11T10:00:00Z")])

    voce = json.loads(percorso.read_text())["issues"][0]
    assert voce["readiness"]["verdict"] == "NON_PRONTA"
    assert voce["readiness"]["missing"] == ["criterio_di_accettazione"]
    assert voce["status"] == "DA_CHIARIRE"


def test_uno_stato_dichiarato_cede_al_fatto_letto_da_github(tmp_path: Path) -> None:
    sincronizza(tmp_path, [issue(7)])
    percorso = tmp_path / "registry.json"
    registry.comando_set(_costruisci_args(["set", "--path", str(percorso), "--issue", "7", "--status", "IN_SVILUPPO", "--note", "Mauro"]))

    esito = sincronizza(tmp_path, [issue(7, state="CLOSED")])

    assert esito["by_status"]["CHIUSA"] == 1
    assert esito["contraddizioni"] and "#7" in esito["contraddizioni"][0]


def test_uno_stato_dichiarato_regge_a_un_sync_che_non_lo_contraddice(tmp_path: Path) -> None:
    sincronizza(tmp_path, [issue(8)])
    percorso = tmp_path / "registry.json"
    registry.comando_set(_costruisci_args(["set", "--path", str(percorso), "--issue", "8", "--status", "IN_VERIFICA", "--note", "Mauro"]))

    esito = sincronizza(tmp_path, [issue(8, updatedAt="2026-08-11T12:00:00Z")])

    assert esito["by_status"]["IN_VERIFICA"] == 1


def test_uno_stato_fuori_vocabolario_viene_rifiutato(tmp_path: Path) -> None:
    """Il vocabolario è chiuso già nel parser: uno stato inventato non arriva al registro."""
    sincronizza(tmp_path, [issue(9)])
    with pytest.raises(SystemExit):
        _costruisci_args(["set", "--path", str(tmp_path / "registry.json"), "--issue", "9", "--status", "QUASI_FATTA"])


# --- robustezza --------------------------------------------------------------


def test_un_registro_illeggibile_viene_messo_da_parte_non_sovrascritto(tmp_path: Path) -> None:
    percorso = tmp_path / "registry.json"
    percorso.write_text("{ tronc", encoding="utf-8")

    registry.leggi_registro(percorso)

    assert (tmp_path / "registry.corrotto.json").is_file()
    assert not percorso.exists()


def test_uno_schema_sconosciuto_ferma_la_lettura(tmp_path: Path) -> None:
    percorso = tmp_path / "registry.json"
    percorso.write_text(json.dumps({"schema": "altro@9", "issues": []}), encoding="utf-8")

    with pytest.raises(SystemExit):
        registry.leggi_registro(percorso)


def test_il_tetto_raggiunto_marca_il_registro_parziale(tmp_path: Path) -> None:
    sorgente = tmp_path / "gh.json"
    sorgente.write_text(json.dumps([issue(n) for n in range(1, 4)]), encoding="utf-8")
    args = _costruisci_args(
        ["sync", "--path", str(tmp_path / "registry.json"), "--repo", "mlarese/x", "--input", str(sorgente), "--limit", "3"]
    )
    assert registry.comando_sync(args)["truncated"] is True
