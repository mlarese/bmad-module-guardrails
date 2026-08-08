#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest"]
# ///
"""Test di check_mockup.py. Esegui: uv run pytest scripts/tests/"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_mockup import check, is_remote  # noqa: E402


PULITO = """<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <title>Esporta 10.000 righe in 4 secondi</title>
  <style>
    body { font-family: ui-sans-serif, system-ui, sans-serif; }
    .hero { background: url('data:image/svg+xml;base64,PHN2Zz48L3N2Zz4='); }
  </style>
</head>
<body>
  <h1>Esporta 10.000 righe in 4 secondi</h1>
  <img src="data:image/png;base64,iVBORw0KGgo=" alt="grafico dei tempi">
  <a href="#form">Provalo</a>
</body>
</html>
"""


def kinds(report: dict) -> set[str]:
    return {v["kind"] for v in report["violations"]}


def scrivi(tmp_path: Path, html: str) -> Path:
    p = tmp_path / "pagina.html"
    p.write_text(html, encoding="utf-8")
    return p


class TestIsRemote:
    @pytest.mark.parametrize(
        "value",
        ["http://a.b/c", "https://a.b/c", "//a.b/c", "  https://a.b/c", "HTTPS://A.B"],
    )
    def test_riconosce_i_riferimenti_remoti(self, value: str) -> None:
        assert is_remote(value)

    @pytest.mark.parametrize(
        "value",
        ["", "data:image/png;base64,AAAA", "#ancora", "pagina.html", "blob:xyz", "mailto:a@b.c"],
    )
    def test_lascia_passare_quelli_locali(self, value: str) -> None:
        assert not is_remote(value)


class TestFilePulito:
    def test_nessuna_violazione(self, tmp_path: Path) -> None:
        report = check(scrivi(tmp_path, PULITO))
        assert report["ok"] is True
        assert report["violations"] == []
        assert report["has_inline_style"] is True

    def test_data_uri_non_e_una_violazione(self, tmp_path: Path) -> None:
        # Il vincolo e' "niente rete", non "niente asset": base64 e' ammesso.
        report = check(scrivi(tmp_path, PULITO))
        assert "media-remoto" not in kinds(report)
        assert "css-remoto" not in kinds(report)


class TestDipendenzeDiRete:
    def test_foglio_di_stile_remoto(self, tmp_path: Path) -> None:
        html = '<link rel="stylesheet" href="https://cdn.example.com/a.css">'
        assert "link-remoto" in kinds(check(scrivi(tmp_path, html)))

    def test_script_remoto(self, tmp_path: Path) -> None:
        html = '<script src="https://example.com/a.js"></script>'
        assert "script-remoto" in kinds(check(scrivi(tmp_path, html)))

    def test_immagine_remota(self, tmp_path: Path) -> None:
        html = '<img src="https://example.com/foto.jpg" alt="x">'
        assert "media-remoto" in kinds(check(scrivi(tmp_path, html)))

    def test_srcset_remoto(self, tmp_path: Path) -> None:
        html = '<img srcset="https://example.com/a.jpg 1x, b.jpg 2x" alt="x">'
        assert "media-remoto" in kinds(check(scrivi(tmp_path, html)))

    def test_iframe_remoto(self, tmp_path: Path) -> None:
        html = '<iframe src="https://www.youtube.com/embed/x"></iframe>'
        assert "iframe-remoto" in kinds(check(scrivi(tmp_path, html)))

    def test_url_protocol_relative(self, tmp_path: Path) -> None:
        html = '<script src="//example.com/a.js"></script>'
        assert "script-remoto" in kinds(check(scrivi(tmp_path, html)))

    def test_font_remoto_nel_css(self, tmp_path: Path) -> None:
        html = """<style>
        @font-face { font-family: X; src: url('https://fonts.gstatic.com/x.woff2'); }
        </style>"""
        assert "css-remoto" in kinds(check(scrivi(tmp_path, html)))

    def test_import_remoto_nel_css(self, tmp_path: Path) -> None:
        html = "<style>@import url('https://fonts.googleapis.com/css2?family=Inter');</style>"
        assert "css-import-remoto" in kinds(check(scrivi(tmp_path, html)))

    def test_style_inline_con_url_remoto(self, tmp_path: Path) -> None:
        html = '<div style="background: url(https://example.com/bg.png)"></div>'
        assert "css-remoto" in kinds(check(scrivi(tmp_path, html)))

    @pytest.mark.parametrize(
        "js",
        ["fetch('/api')", "new XMLHttpRequest()", "navigator.sendBeacon('/x')",
         "new WebSocket('wss://x')", "new EventSource('/s')"],
    )
    def test_chiamate_di_rete_nel_javascript(self, tmp_path: Path, js: str) -> None:
        html = f"<script>{js}</script>"
        assert "chiamata-di-rete" in kinds(check(scrivi(tmp_path, html)))

    def test_tailwind_da_cdn(self, tmp_path: Path) -> None:
        html = '<script src="https://cdn.tailwindcss.com"></script>'
        k = kinds(check(scrivi(tmp_path, html)))
        assert "tailwind-cdn" in k
        assert "script-remoto" in k


class TestSegnaposto:
    @pytest.mark.parametrize(
        "testo", ["Lorem ipsum dolor sit amet", "TODO: scrivere", "TBD"]
    )
    def test_marcatori_letterali(self, tmp_path: Path, testo: str) -> None:
        html = f"<body><p>{testo}</p></body>"
        assert "marcatore-segnaposto" in kinds(check(scrivi(tmp_path, html)))

    @pytest.mark.parametrize(
        "host", ["via.placeholder.com", "placehold.co", "picsum.photos", "dummyimage.com"]
    )
    def test_servizi_di_immagini_segnaposto(self, tmp_path: Path, host: str) -> None:
        html = f'<img src="https://{host}/600x400" alt="x">'
        assert "immagine-segnaposto" in kinds(check(scrivi(tmp_path, html)))

    def test_placeholder_come_attributo_non_e_un_segnaposto(self, tmp_path: Path) -> None:
        # Regressione: «placeholder» e' un nome di attributo standard.
        html = '<form><input type="email" placeholder="nome@azienda.it"></form>'
        assert check(scrivi(tmp_path, html))["ok"] is True

    def test_pseudo_elemento_css_placeholder_non_e_un_segnaposto(self, tmp_path: Path) -> None:
        # Regressione: input::placeholder e' CSS legittimo, non contenuto finto.
        html = "<style>input::placeholder { color: #999; }</style>"
        assert check(scrivi(tmp_path, html))["ok"] is True

    def test_font_in_base64_non_produce_falsi_positivi(self, tmp_path: Path) -> None:
        # Regressione: in un blob base64 di dimensione reale «tbd» e «todo»
        # compaiono per caso. Il font incorporato e' prescritto dalla rotta.
        import base64
        import os

        blob = base64.b64encode(os.urandom(30000)).decode()
        html = (
            f"<style>@font-face {{ font-family: X; "
            f"src: url('data:font/woff2;base64,{blob}'); }}</style>"
            "<body><p>Esporta 10.000 righe in 4 secondi</p></body>"
        )
        assert check(scrivi(tmp_path, html))["ok"] is True

    def test_todo_dentro_una_parola_non_conta(self, tmp_path: Path) -> None:
        # Regressione: ancoraggio al confine di parola.
        html = "<body><p>Il metodo Kirkpatrick, non il me-TODO improvvisato.</p></body>"
        assert check(scrivi(tmp_path, html))["ok"] is True

    def test_todo_come_marcatore_vero_conta(self, tmp_path: Path) -> None:
        html = "<body><p>TODO: scrivere la sezione prezzi</p></body>"
        assert "marcatore-segnaposto" in kinds(check(scrivi(tmp_path, html)))

    @pytest.mark.parametrize(
        # `<tbd>` non compare: in HTML e' un tag, non testo. La forma con le
        # parentesi angolari si vede solo escapata, e li' il parser la
        # restituisce come testo.
        "testo", ["TODO scrivere", "[todo] prezzi", "{TBD}", "&lt;tbd&gt;", "tbd: numeri veri"]
    )
    def test_forme_delimitate_o_maiuscole_contano(self, tmp_path: Path, testo: str) -> None:
        assert "marcatore-segnaposto" in kinds(check(scrivi(tmp_path, f"<body><p>{testo}</p></body>")))

    @pytest.mark.parametrize(
        "frase",
        [
            "Todo lo que necesitas para vender mas",
            "Gestiona todo tu inventario desde un panel",
            "Tudo o que voce precisa",
        ],
    )
    def test_prosa_spagnola_o_portoghese_non_e_un_marcatore(self, tmp_path: Path, frase: str) -> None:
        # Regressione: la pagina segue la lingua del destinatario, e «todo» e'
        # fra le parole piu' comuni in spagnolo.
        html = f'<html lang="es"><body><main><h1>{frase}</h1></main></body></html>'
        assert check(scrivi(tmp_path, html))["ok"] is True

    def test_url_in_un_attributo_visibile_non_e_un_marcatore(self, tmp_path: Path) -> None:
        # Regressione: `content` di og:url ospita URL, dove «/todo» cade fra
        # confini non-parola.
        html = '<meta property="og:url" content="https://esempio.it/todo">'
        assert check(scrivi(tmp_path, html))["ok"] is True

    @pytest.mark.parametrize(
        "html",
        [
            '<form><label for="a">Nome azienda</label><input id="a" placeholder="Nome azienda"></form>',
            '<form><input aria-label="Nome azienda"></form>',
            "<main><h1>Il tuo prodotto in produzione in 4 minuti</h1></main>",
            "<footer><p>© 2026 Nome Azienda</p></footer>",
        ],
    )
    def test_le_ragioni_sociali_non_sono_piu_marcatori(self, tmp_path: Path, html: str) -> None:
        # Erano sintagmi ordinari: nessuna lista di esenzioni poteva contenerli,
        # e bloccavano titoli che superano i test del copy della skill stessa.
        # Il giudizio su una ragione sociale da template resta al modello.
        assert check(scrivi(tmp_path, html))["ok"] is True

    @pytest.mark.parametrize(
        "frase",
        [
            "TODO scrivere la CTA finale",
            "Serve una FAQ TODO",
            "TODO rifare l HTML",
            "TODO",
        ],
    )
    def test_un_marcatore_non_si_lascia_sopprimere_da_una_sigla(
        self, tmp_path: Path, frase: str
    ) -> None:
        # Regressione: un'euristica sulle maiuscole azzerava la segnalazione
        # appena accanto al token compariva una sigla — CTA, FAQ, HTML — cioe'
        # il vocabolario proprio di questa skill.
        html = f"<body><p>{frase}</p></body>"
        assert "marcatore-segnaposto" in kinds(check(scrivi(tmp_path, html)))

    def test_due_marcatori_non_si_annullano_a_vicenda(self, tmp_path: Path) -> None:
        segnaposto = [v for v in check(scrivi(tmp_path, "<p>TODO e poi TBD</p>"))["violations"]
                      if v["family"] == "placeholder"]
        assert len(segnaposto) == 2

    def test_il_referto_porta_il_contesto(self, tmp_path: Path) -> None:
        # Un falso positivo si deve poter liquidare leggendo il JSON.
        html = "<body><p>TODO: scrivere la sezione dei prezzi</p></body>"
        detail = check(scrivi(tmp_path, html))["violations"][0]["detail"]
        assert "scrivere la sezione" in detail

    def test_un_marcatore_produce_una_violazione_sola(self, tmp_path: Path) -> None:
        # «TODO:» e' coperto sia da UPPER sia da DELIMITED: una violazione, non due.
        html = "<body><p>TODO: aggiungere le testimonianze</p></body>"
        segnaposto = [v for v in check(scrivi(tmp_path, html))["violations"]
                      if v["family"] == "placeholder"]
        assert len(segnaposto) == 1

    def test_due_marcatori_distinti_restano_due(self, tmp_path: Path) -> None:
        html = "<body><p>TODO: scrivere</p><p>Lorem ipsum dolor</p></body>"
        segnaposto = [v for v in check(scrivi(tmp_path, html))["violations"]
                      if v["family"] == "placeholder"]
        assert len(segnaposto) == 2

    def test_lorem_ipsum_conta_ovunque(self, tmp_path: Path) -> None:
        html = "<form><label>Lorem ipsum</label><input></form>"
        assert "marcatore-segnaposto" in kinds(check(scrivi(tmp_path, html)))

    def test_segnaposto_dentro_un_attributo_visibile(self, tmp_path: Path) -> None:
        html = '<img src="data:image/png;base64,AA==" alt="Lorem ipsum">'
        assert "marcatore-segnaposto" in kinds(check(scrivi(tmp_path, html)))

    def test_una_testimonianza_plausibile_non_viene_giudicata(self, tmp_path: Path) -> None:
        # Confine da non superare: se un contenuto sia inventato lo decide il
        # modello leggendo il brief, mai una regex.
        html = '<blockquote>«Ci ha fatto risparmiare 12 ore a settimana.» — Marco Rossi, Acme</blockquote>'
        assert check(scrivi(tmp_path, html))["ok"] is True


class TestReferto:
    def test_conteggi_per_famiglia(self, tmp_path: Path) -> None:
        html = """<link rel="stylesheet" href="https://a.b/c.css">
        <p>Lorem ipsum</p>"""
        report = check(scrivi(tmp_path, html))
        assert report["counts"]["network"] == 1
        assert report["counts"]["placeholder"] == 1
        assert report["ok"] is False

    def test_violazioni_ordinate_per_riga(self, tmp_path: Path) -> None:
        html = "<p>x</p>\n<p>Lorem ipsum</p>\n<script src='https://a.b/c.js'></script>"
        righe = [v["line"] for v in check(scrivi(tmp_path, html))["violations"]]
        assert righe == sorted(righe)

    def test_nessun_duplicato(self, tmp_path: Path) -> None:
        html = '<script src="https://cdn.tailwindcss.com"></script>'
        violations = check(scrivi(tmp_path, html))["violations"]
        chiavi = [(v["kind"], v["line"], v["detail"]) for v in violations]
        assert len(chiavi) == len(set(chiavi))


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
