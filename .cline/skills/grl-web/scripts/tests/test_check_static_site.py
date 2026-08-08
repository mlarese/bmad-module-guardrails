#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest"]
# ///
"""Test di check_static_site.py."""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_static_site import check_page, check_site, image_size  # noqa: E402


COMPLETA = """<!doctype html>
<html lang="it">
<head>
  <title>Prezzi</title>
  <meta name="description" content="Quanto costa, senza sorprese.">
  <link rel="canonical" href="https://esempio.it/prezzi">
  <meta property="og:title" content="Prezzi">
  <meta property="og:description" content="Quanto costa, senza sorprese.">
  <meta property="og:image" content="/og.png">
</head>
<body>
  <main>
    <h1>Prezzi</h1>
    <img src="/grafico.png" alt="confronto piani" width="600" height="400" loading="lazy">
    <form><label for="email">Email</label><input id="email" type="email"></form>
  </main>
</body>
</html>
"""


def png(width: int, height: int) -> bytes:
    """PNG minimo valido con le dimensioni richieste nell'header IHDR."""
    ihdr = struct.pack(">II", width, height) + bytes([8, 6, 0, 0, 0])
    chunk = b"IHDR" + ihdr
    return (
        b"\x89PNG\r\n\x1a\n"
        + struct.pack(">I", len(ihdr))
        + chunk
        + struct.pack(">I", zlib.crc32(chunk))
    )


def scrivi(tmp_path: Path, nome: str, html: str) -> Path:
    p = tmp_path / nome
    p.write_text(html, encoding="utf-8")
    return p


class TestPaginaCompleta:
    def test_nessuna_mancanza(self, tmp_path: Path) -> None:
        r = check_page(scrivi(tmp_path, "prezzi.html", COMPLETA))
        assert r["ok"] is True
        assert r["missing"] == []

    def test_riporta_le_immagini_lazy_senza_giudicarle(self, tmp_path: Path) -> None:
        # Quali immagini stiano sotto la piega lo decide il modello.
        r = check_page(scrivi(tmp_path, "prezzi.html", COMPLETA))
        assert r["immagini"]["con_lazy"] == ["/grafico.png"]
        assert not any("lazy" in m for m in r["missing"])


class TestMancanze:
    @pytest.mark.parametrize(
        "rimuovi,atteso",
        [
            ('lang="it"', "attributo lang su <html>"),
            ("<title>Prezzi</title>", "<title> non vuoto"),
            ('<meta name="description" content="Quanto costa, senza sorprese.">', "meta description"),
            ('<link rel="canonical" href="https://esempio.it/prezzi">', "link rel=canonical"),
            ('<meta property="og:image" content="/og.png">', "meta og:image"),
        ],
    )
    def test_rileva_cosa_manca(self, tmp_path: Path, rimuovi: str, atteso: str) -> None:
        r = check_page(scrivi(tmp_path, "p.html", COMPLETA.replace(rimuovi, "")))
        assert atteso in r["missing"]
        assert r["ok"] is False

    def test_immagine_senza_alt(self, tmp_path: Path) -> None:
        html = COMPLETA.replace('alt="confronto piani" ', "")
        r = check_page(scrivi(tmp_path, "p.html", html))
        assert "/grafico.png" in r["immagini"]["senza_alt"]

    def test_immagine_senza_dimensioni(self, tmp_path: Path) -> None:
        html = COMPLETA.replace('width="600" height="400" ', "")
        r = check_page(scrivi(tmp_path, "p.html", html))
        assert "/grafico.png" in r["immagini"]["senza_dimensioni"]

    def test_campo_senza_etichetta(self, tmp_path: Path) -> None:
        html = COMPLETA.replace('<label for="email">Email</label>', "")
        r = check_page(scrivi(tmp_path, "p.html", html))
        assert r["campi_senza_etichetta"] == ["email"]

    def test_label_avvolgente_conta_come_etichetta(self, tmp_path: Path) -> None:
        # Regressione: <label>Email <input></label> e' valida e frequentissima.
        html = COMPLETA.replace(
            '<label for="email">Email</label><input id="email" type="email">',
            '<label>Email <input type="email" name="email"></label>',
        )
        assert check_page(scrivi(tmp_path, "p.html", html))["campi_senza_etichetta"] == []

    def test_reset_non_e_un_campo(self, tmp_path: Path) -> None:
        html = COMPLETA.replace("</form>", '<input type="reset" value="Annulla"></form>')
        assert check_page(scrivi(tmp_path, "p.html", html))["campi_senza_etichetta"] == []

    def test_campo_scoperto_e_identificabile(self, tmp_path: Path) -> None:
        # Senza id, il referto deve comunque dire di quale campo si tratta.
        html = COMPLETA.replace(
            '<label for="email">Email</label><input id="email" type="email">',
            '<input type="email" name="email_iscrizione">',
        )
        assert check_page(scrivi(tmp_path, "p.html", html))["campi_senza_etichetta"] == [
            "email_iscrizione"
        ]

    def test_aria_label_conta_come_etichetta(self, tmp_path: Path) -> None:
        html = COMPLETA.replace(
            '<label for="email">Email</label><input id="email" type="email">',
            '<input id="email" type="email" aria-label="Email">',
        )
        assert check_page(scrivi(tmp_path, "p.html", html))["campi_senza_etichetta"] == []

    def test_manca_il_main(self, tmp_path: Path) -> None:
        html = COMPLETA.replace("<main>", "<div>").replace("</main>", "</div>")
        assert "elemento <main>" in check_page(scrivi(tmp_path, "p.html", html))["missing"]


class TestDimensioniImmagine:
    def test_legge_l_header_png(self, tmp_path: Path) -> None:
        p = tmp_path / "og.png"
        p.write_bytes(png(1200, 630))
        assert image_size(p) == (1200, 630)

    def test_file_illeggibile(self, tmp_path: Path) -> None:
        p = tmp_path / "rotto.png"
        p.write_bytes(b"non sono un png")
        assert image_size(p) is None


class TestSito:
    def _sito(self, tmp_path: Path, og: tuple[int, int] | None = (1200, 630)) -> Path:
        scrivi(tmp_path, "index.html", COMPLETA)
        (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        if og:
            (tmp_path / "og.png").write_bytes(png(*og))
        return tmp_path

    def test_sito_completo(self, tmp_path: Path) -> None:
        r = check_site(self._sito(tmp_path))
        assert r["ok"] is True
        assert r["pagine_scansionate"] == 1

    @pytest.mark.parametrize(
        "nomi",
        [
            ["sitemap.xml"],
            ["sitemap-index.xml", "sitemap-0.xml"],   # quello che emette Astro
            ["sitemap_index.xml"],
        ],
    )
    def test_la_sitemap_si_riconosce_in_tutte_le_sue_forme(
        self, tmp_path: Path, nomi: list[str]
    ) -> None:
        # Regressione: il nome letterale dichiarava mancante una sitemap
        # completa su ogni build Astro fatta bene.
        scrivi(tmp_path, "index.html", COMPLETA)
        (tmp_path / "og.png").write_bytes(png(1200, 630))
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        for n in nomi:
            (tmp_path / n).write_text("<urlset/>", encoding="utf-8")
        assert check_site(tmp_path)["mancanti_a_livello_di_sito"] == []

    def test_sitemap_e_robots_mancanti(self, tmp_path: Path) -> None:
        scrivi(tmp_path, "index.html", COMPLETA)
        (tmp_path / "og.png").write_bytes(png(1200, 630))
        r = check_site(tmp_path)
        assert set(r["mancanti_a_livello_di_sito"]) == {"sitemap*.xml", "robots.txt"}

    def test_og_image_di_rapporto_sbagliato(self, tmp_path: Path) -> None:
        r = check_site(self._sito(tmp_path, og=(800, 600)))
        assert "rapporto" in r["og_image"][0]["problema"]
        assert r["og_image"][0]["dimensioni"] == [800, 600]
        assert r["ok"] is False

    def test_og_image_2x_e_accettata(self, tmp_path: Path) -> None:
        # Stesso rapporto 1.91:1, taglio per schermi ad alta densita'.
        assert check_site(self._sito(tmp_path, og=(2400, 1260)))["og_image"] == []

    def test_og_image_troppo_stretta(self, tmp_path: Path) -> None:
        # Rapporto giusto, larghezza sotto il minimo.
        r = check_site(self._sito(tmp_path, og=(600, 315)))
        assert "larghezza" in r["og_image"][0]["problema"]

    def test_og_image_assente_dal_disco(self, tmp_path: Path) -> None:
        r = check_site(self._sito(tmp_path, og=None))
        assert r["og_image"][0]["problema"] == "non trovata"

    def test_og_image_remota_non_viene_verificata(self, tmp_path: Path) -> None:
        html = COMPLETA.replace('content="/og.png"', 'content="https://cdn.esempio.it/og.png"')
        scrivi(tmp_path, "index.html", html)
        (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        assert check_site(tmp_path)["og_image"] == []

    def test_pagine_in_sottocartelle_sono_distinguibili(self, tmp_path: Path) -> None:
        # Regressione: due index.html in cartelle diverse sono il layout
        # standard degli URL puliti.
        for nome in ("prezzi", "contatti"):
            (tmp_path / nome).mkdir()
            (tmp_path / nome / "index.html").write_text(COMPLETA, encoding="utf-8")
        (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        (tmp_path / "og.png").write_bytes(png(1200, 630))
        identita = [p["file"] for p in check_site(tmp_path)["pagine"]]
        assert identita == ["contatti/index.html", "prezzi/index.html"]

    def test_og_image_relativa_risolta_dalla_pagina(self, tmp_path: Path) -> None:
        # Regressione: `../assets/og.png` e' relativo alla pagina, non alla radice.
        (tmp_path / "assets").mkdir()
        (tmp_path / "assets/og.png").write_bytes(png(2400, 1260))
        (tmp_path / "prezzi").mkdir()
        (tmp_path / "prezzi/index.html").write_text(
            COMPLETA.replace('content="/og.png"', 'content="../assets/og.png"'), encoding="utf-8"
        )
        (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        r = check_site(tmp_path)
        assert r["og_image"] == []
        assert r["ok"] is True

    def test_og_image_assoluta_risolta_dalla_radice(self, tmp_path: Path) -> None:
        (tmp_path / "prezzi").mkdir()
        (tmp_path / "prezzi/index.html").write_text(COMPLETA, encoding="utf-8")
        (tmp_path / "og.png").write_bytes(png(1200, 630))
        (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        assert check_site(tmp_path)["og_image"] == []

    @pytest.mark.parametrize(
        "ref,nome_file",
        [
            ("og.png?v=2", "og.png"),
            ("/og.png#x", "og.png"),
            ("/og%20hero.png", "og hero.png"),
        ],
    )
    def test_query_frammento_e_percent_encoding(self, tmp_path: Path, ref: str, nome_file: str) -> None:
        # Regressione: il riferimento andava sul disco come URL, non come percorso.
        (tmp_path / nome_file).write_bytes(png(1200, 630))
        (tmp_path / "index.html").write_text(
            COMPLETA.replace('content="/og.png"', f'content="{ref}"'), encoding="utf-8"
        )
        (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        assert check_site(tmp_path)["og_image"] == []

    @pytest.mark.parametrize("ref", ["HTTPS://cdn.example.com/og.png", "//cdn.example.com/og.png"])
    def test_og_image_remota_riconosciuta_anche_in_maiuscolo(self, tmp_path: Path, ref: str) -> None:
        # Regressione: lo startswith letterale non riconosceva HTTPS://.
        (tmp_path / "index.html").write_text(
            COMPLETA.replace('content="/og.png"', f'content="{ref}"'), encoding="utf-8"
        )
        (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        assert check_site(tmp_path)["og_image"] == []

    @pytest.mark.parametrize("ref", ["?v=2", "#hero"])
    def test_og_image_senza_percorso_viene_riportata(self, tmp_path: Path, ref: str) -> None:
        # Il tag c'e' e non punta a niente: constatarlo e' nel mandato.
        (tmp_path / "index.html").write_text(
            COMPLETA.replace('content="/og.png"', f'content="{ref}"'), encoding="utf-8"
        )
        (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        assert check_site(tmp_path)["og_image"][0]["problema"] == "og:image senza percorso"

    def test_og_image_webp_viene_letta(self, tmp_path: Path) -> None:
        # Regressione: webp e' il formato che emette la pipeline di Astro, e
        # veniva dichiarato «non trovata».
        vp8x = b"VP8X" + struct.pack("<I", 10) + bytes(4) \
            + (1199).to_bytes(3, "little") + (629).to_bytes(3, "little")
        body = b"WEBP" + vp8x
        (tmp_path / "og.webp").write_bytes(b"RIFF" + struct.pack("<I", len(body)) + body)
        (tmp_path / "index.html").write_text(
            COMPLETA.replace('content="/og.png"', 'content="/og.webp"'), encoding="utf-8"
        )
        (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        r = check_site(tmp_path)
        assert r["og_image"] == [] and r["og_image_non_letta"] == []
        assert r["ok"] is True

    def test_formato_non_riconosciuto_non_e_una_mancanza(self, tmp_path: Path) -> None:
        (tmp_path / "og.avif").write_bytes(b"\x00\x00\x00\x20ftypavif")
        (tmp_path / "index.html").write_text(
            COMPLETA.replace('content="/og.png"', 'content="/og.avif"'), encoding="utf-8"
        )
        (tmp_path / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        r = check_site(tmp_path)
        assert r["og_image"] == []
        assert "formato non riconosciuto" in r["og_image_non_letta"][0]["nota"]
        assert r["ok"] is True

    def test_il_referto_nomina_i_file_che_hanno_soddisfatto_il_controllo(
        self, tmp_path: Path
    ) -> None:
        scrivi(tmp_path, "index.html", COMPLETA)
        (tmp_path / "og.png").write_bytes(png(1200, 630))
        (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        for n in ("sitemap-index.xml", "sitemap-0.xml"):
            (tmp_path / n).write_text("<urlset/>", encoding="utf-8")
        r = check_site(tmp_path)
        assert r["sitemap"] == ["sitemap-0.xml", "sitemap-index.xml"]
        assert r["robots"] == ["robots.txt"]

    def test_riferimento_che_esce_dall_albero_non_si_legge(self, tmp_path: Path) -> None:
        sito = tmp_path / "sito"
        sito.mkdir()
        (tmp_path / "fuori.png").write_bytes(png(1200, 630))
        (sito / "index.html").write_text(
            COMPLETA.replace('content="/og.png"', 'content="../fuori.png"'), encoding="utf-8"
        )
        (sito / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
        (sito / "robots.txt").write_text("User-agent: *", encoding="utf-8")
        assert check_site(sito)["og_image"][0]["problema"] == "non trovata"

    def test_cartella_senza_pagine(self, tmp_path: Path) -> None:
        r = check_site(tmp_path)
        assert r["ok"] is False
        assert "nessun file .html" in r["errore"]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
