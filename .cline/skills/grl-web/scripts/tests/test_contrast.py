#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest"]
# ///
"""Test di contrast.py, su vettori noti."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from contrast import contrast_ratio, evaluate, parse_hex, relative_luminance  # noqa: E402


class TestParseHex:
    @pytest.mark.parametrize(
        "value,atteso",
        [
            ("#ffffff", (255, 255, 255)),
            ("#000000", (0, 0, 0)),
            ("ffffff", (255, 255, 255)),
            ("#fff", (255, 255, 255)),
            ("#abc", (170, 187, 204)),
            ("  #1A2B3C  ", (26, 43, 60)),
        ],
    )
    def test_forme_accettate(self, value: str, atteso: tuple[int, int, int]) -> None:
        assert parse_hex(value) == atteso

    @pytest.mark.parametrize("value", ["", "#12345", "rosso", "#gggggg", "rgb(1,2,3)"])
    def test_rifiuta_input_non_valido(self, value: str) -> None:
        with pytest.raises(ValueError):
            parse_hex(value)


class TestLuminanza:
    def test_bianco_e_uno(self) -> None:
        assert relative_luminance((255, 255, 255)) == pytest.approx(1.0)

    def test_nero_e_zero(self) -> None:
        assert relative_luminance((0, 0, 0)) == pytest.approx(0.0)


class TestRapporto:
    def test_nero_su_bianco_e_il_massimo(self) -> None:
        # Il rapporto massimo definito da WCAG e' esattamente 21:1.
        assert contrast_ratio("#000000", "#ffffff") == pytest.approx(21.0, abs=0.01)

    def test_colore_su_se_stesso_e_uno(self) -> None:
        assert contrast_ratio("#3b82f6", "#3b82f6") == pytest.approx(1.0, abs=0.001)

    def test_e_simmetrico(self) -> None:
        assert contrast_ratio("#1a1a1a", "#fafafa") == pytest.approx(
            contrast_ratio("#fafafa", "#1a1a1a")
        )

    def test_vettore_noto_grigio_medio_su_bianco(self) -> None:
        # #767676 su bianco e' il classico caso al limite di 4.5:1.
        assert contrast_ratio("#767676", "#ffffff") == pytest.approx(4.54, abs=0.02)

    def test_vettore_noto_blu_tailwind_su_bianco(self) -> None:
        # #3b82f6 su bianco non passa per il testo normale: 3.68:1.
        assert contrast_ratio("#3b82f6", "#ffffff") == pytest.approx(3.68, abs=0.02)


class TestVerdetto:
    def test_passa(self) -> None:
        r = evaluate("#000000", "#ffffff")
        assert r["verdetto"] == "passa"
        assert r["testo_normale"] and r["testo_grande"]

    def test_solo_testo_grande(self) -> None:
        r = evaluate("#3b82f6", "#ffffff")
        assert r["verdetto"] == "solo testo grande"
        assert not r["testo_normale"]
        assert r["testo_grande"]

    def test_sotto_soglia(self) -> None:
        r = evaluate("#cccccc", "#ffffff")
        assert r["verdetto"] == "sotto soglia"
        assert not r["testo_normale"] and not r["testo_grande"]

    def test_il_rapporto_e_arrotondato_a_due_decimali(self) -> None:
        assert evaluate("#767676", "#ffffff")["ratio"] == 4.54


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
