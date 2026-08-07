#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest"]
# ///
"""Test di check_coerenza.py."""

from __future__ import annotations

import base64
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_coerenza import compare, normalize, profile  # noqa: E402


BASE_CSS = """
:root { --spazio: 8px; --accento: #9a4a2f; }
body { font-family: Georgia, serif; color: #1a1a1a; }
"""


def pagina(tmp_path: Path, nome: str, css: str, corpo: str = "<h1>x</h1>") -> Path:
    p = tmp_path / nome
    p.write_text(f"<html><head><style>{css}</style></head><body>{corpo}</body></html>",
                 encoding="utf-8")
    return p


class TestNormalize:
    def test_collassa_gli_spazi(self) -> None:
        assert normalize("body   {\n  color:  red;\n}") == "body { color: red; }"

    def test_scarta_il_contenuto_dei_data_uri(self) -> None:
        # Due font diversi in base64 non sono una divergenza di stile.
        a = normalize("@font-face { src: url('data:font/woff2;base64,AAAA'); }")
        b = normalize("@font-face { src: url('data:font/woff2;base64,BBBB'); }")
        assert a == b


class TestProfile:
    def test_estrae_i_token_del_sistema(self, tmp_path: Path) -> None:
        p = profile(pagina(tmp_path, "a.html", BASE_CSS))
        assert p["custom_properties"] == {"--spazio": "8px", "--accento": "#9a4a2f"}
        assert p["colors"] == ["#1a1a1a", "#9a4a2f"]
        assert p["font_families"] == ["georgia, serif"]
        assert p["profilo_vuoto"] is False

    def test_pagina_senza_style(self, tmp_path: Path) -> None:
        p = tmp_path / "vuota.html"
        p.write_text("<html><body><p>x</p></body></html>", encoding="utf-8")
        r = profile(p)
        assert r["custom_properties"] == {} and r["colors"] == []
        assert r["profilo_vuoto"] is True


class TestCompare:
    def test_pagine_identiche_non_divergono(self, tmp_path: Path) -> None:
        files = [pagina(tmp_path, "a.html", BASE_CSS), pagina(tmp_path, "b.html", BASE_CSS)]
        r = compare(files)
        assert r["ok"] is True
        assert r["stile_identico"] is True
        assert r["divergenze"] == []

    def test_font_diverso_e_una_divergenza(self, tmp_path: Path) -> None:
        alt = BASE_CSS.replace("Georgia, serif", "Inter, sans-serif")
        r = compare([pagina(tmp_path, "a.html", BASE_CSS), pagina(tmp_path, "b.html", alt)])
        assert r["ok"] is False
        campi = {d["campo"] for d in r["divergenze"]}
        assert "font_families" in campi

    def test_token_mancante_in_una_pagina(self, tmp_path: Path) -> None:
        ridotto = ":root { --spazio: 8px; } body { color: #1a1a1a; }"
        r = compare([pagina(tmp_path, "a.html", BASE_CSS), pagina(tmp_path, "b.html", ridotto)])
        mancanti = [d for d in r["divergenze"] if d["file"] == "b.html"]
        assert any("--accento" in d["non_ha"] for d in mancanti)
        assert any("#9a4a2f" in d["non_ha"] for d in mancanti)

    def test_il_referto_dice_quale_pagina_e_su_cosa(self, tmp_path: Path) -> None:
        # Il dato deve essere azionabile: file piu' token, non un booleano.
        ridotto = ":root { --spazio: 8px; } body { font-family: Georgia, serif; color: #1a1a1a; }"
        r = compare([pagina(tmp_path, "home.html", BASE_CSS), pagina(tmp_path, "prezzi.html", ridotto)])
        d = next(x for x in r["divergenze"] if x["campo"] == "custom_properties")
        assert d["file"] == "prezzi.html"
        assert d["non_ha"] == ["--accento"]

    def test_font_in_base64_non_produce_divergenza(self, tmp_path: Path) -> None:
        # Regressione: due blob diversi dello stesso font non sono deriva.
        css_a = BASE_CSS + f"@font-face {{ src: url('data:font/woff2;base64,{base64.b64encode(os.urandom(300)).decode()}'); }}"
        css_b = BASE_CSS + f"@font-face {{ src: url('data:font/woff2;base64,{base64.b64encode(os.urandom(300)).decode()}'); }}"
        r = compare([pagina(tmp_path, "a.html", css_a), pagina(tmp_path, "b.html", css_b)])
        assert r["stile_identico"] is True
        assert r["ok"] is True

    def test_colori_funzionali_sono_visti(self, tmp_path: Path) -> None:
        # Regressione: due palette opposte in rgb()/oklch() passavano per identiche.
        a = ":root{--brand: oklch(55% 0.2 250);} body{color: rgb(0 85 255);}"
        b = ":root{--brand: oklch(70% 0.05 30);} body{color: rgb(200 20 20);}"
        r = compare([pagina(tmp_path, "a.html", a), pagina(tmp_path, "b.html", b)])
        assert r["ok"] is False
        assert all(p["colors"] for p in r["profili"])

    def test_esadecimale_con_alpha_e_visto(self, tmp_path: Path) -> None:
        r = compare([
            pagina(tmp_path, "a.html", "body{color:#0055ff88}"),
            pagina(tmp_path, "b.html", "body{color:#0055ff88}"),
        ])
        assert r["profili"][0]["colors"] == ["#0055ff88"]

    def test_stesso_token_con_valore_diverso_e_una_divergenza(self, tmp_path: Path) -> None:
        # Regressione: prima si confrontavano solo i NOMI.
        r = compare([
            pagina(tmp_path, "home.html", ":root{--brand:#0055ff}"),
            pagina(tmp_path, "prezzi.html", ":root{--brand:#0044ee}"),
        ])
        conflitto = next(d for d in r["divergenze"] if d["campo"] == "valore_custom_property")
        assert conflitto["token"] == "--brand"
        assert conflitto["valori"] == {"home.html": "#0055ff", "prezzi.html": "#0044ee"}

    def test_profilo_vuoto_non_passa_per_coerente(self, tmp_path: Path) -> None:
        # Regressione: due pagine senza <style> profilavano insiemi vuoti e
        # uscivano «ok».
        for n in ("a.html", "b.html"):
            (tmp_path / n).write_text("<html><body><p>x</p></body></html>", encoding="utf-8")
        r = compare([tmp_path / "a.html", tmp_path / "b.html"])
        assert r["ok"] is False
        assert r["profili_vuoti"] == ["a.html", "b.html"]

    def test_un_commento_non_inventa_una_divergenza(self, tmp_path: Path) -> None:
        # Regressione: un commento di palette su una pagina sola faceva
        # divergere due pagine con lo stesso identico stile.
        con_commento = BASE_CSS + "/* Palette: #0055ff primario, #ff9900 accento */"
        r = compare([
            pagina(tmp_path, "a.html", con_commento),
            pagina(tmp_path, "b.html", BASE_CSS),
        ])
        assert r["ok"] is True
        assert r["divergenze"] == []

    def test_un_valore_commentato_non_diventa_il_valore_vero(self, tmp_path: Path) -> None:
        # Regressione: il referto riportava «#003399 */» come valore di --brand.
        r = compare([
            pagina(tmp_path, "home.html", ":root{--brand:#0055ff; /* prima era --brand:#003399 */}"),
            pagina(tmp_path, "prezzi.html", ":root{--brand:#0055ff;}"),
        ])
        assert r["ok"] is True
        assert r["profili"][0]["custom_properties"]["--brand"] == "#0055ff"

    @pytest.mark.parametrize(
        "css,atteso",
        [
            ("body{color: color-mix(in oklch, var(--a), var(--b))}",
             "color-mix(in oklch, var(--a), var(--b))"),
            ("body{color: rgb(calc(1 * 255) 0 0)}", "rgb(calc(1 * 255) 0 0)"),
            ("body{color: oklch(from var(--brand) calc(l + .1) c h)}",
             "oklch(from var(--brand) calc(l + .1) c h)"),
        ],
    )
    def test_forme_annidate_lette_per_intero(self, tmp_path: Path, css: str, atteso: str) -> None:
        # Regressione: [^)]* troncava proprio dove due colori si distinguono.
        assert profile(pagina(tmp_path, "a.html", css))["colors"] == [atteso]

    def test_un_selettore_esadecimale_non_e_un_colore(self, tmp_path: Path) -> None:
        # Regressione: `#feed { }` finiva nell'inventario della palette.
        r = compare([
            pagina(tmp_path, "a.html", BASE_CSS + "#feed { padding: 0 }"),
            pagina(tmp_path, "b.html", BASE_CSS),
        ])
        assert "#feed" not in r["profili"][0]["colors"]
        assert r["divergenze"] == []

    def test_un_svg_in_data_uri_non_presta_i_suoi_colori(self, tmp_path: Path) -> None:
        # Regressione: [^)]* si fermava a «translate(1,2)» e lasciava il resto
        # dell'SVG — colori compresi — dentro il CSS normalizzato.
        svg = ("url(\"data:image/svg+xml,<svg><g transform='translate(1,2)'>"
               "<circle fill='rgb(255,0,0)'/></g></svg>\")")
        css = BASE_CSS + f"body {{ background: {svg}; }}"
        assert "rgb(255,0,0)" not in profile(pagina(tmp_path, "a.html", css))["colors"]

    def test_ordine_delle_dichiarazioni_non_conta_sui_token(self, tmp_path: Path) -> None:
        invertito = ":root { --accento: #9a4a2f; --spazio: 8px; }\nbody { color: #1a1a1a; font-family: Georgia, serif; }"
        r = compare([pagina(tmp_path, "a.html", BASE_CSS), pagina(tmp_path, "b.html", invertito)])
        assert r["divergenze"] == []


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
