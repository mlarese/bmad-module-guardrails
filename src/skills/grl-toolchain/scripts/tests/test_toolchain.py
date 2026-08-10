#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest", "PyYAML"]
# ///
"""Test di detect_harness.py e apply_mcp.py.

I test che toccano il filesystem lavorano su `tmp_path` e riscrivono `HOME` e
`XDG_CONFIG_HOME`: nessun test legge o scrive la configurazione reale della
macchina.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import apply_mcp  # noqa: E402
import detect_harness as detect  # noqa: E402
from harness_spec import BY_ID  # noqa: E402


# --- lettura dei formati -----------------------------------------------------


def test_strip_jsonc_preserva_gli_url_dentro_le_stringhe():
    """Il caso che rompe la versione ingenua: `https://` non è un commento."""
    text = '{ "url": "https://host/mcp", // commento\n  "a": 1 }'
    assert json.loads(detect.strip_jsonc(text)) == {"url": "https://host/mcp", "a": 1}


def test_strip_jsonc_toglie_blocchi_e_virgole_finali():
    text = '{ /* nota */ "a": 1, }'
    assert json.loads(detect.strip_jsonc(text)) == {"a": 1}


@pytest.mark.parametrize(
    "entry,atteso",
    [
        ({"command": "npx", "args": []}, "stdio"),
        ({"type": "local", "command": ["npx"]}, "stdio"),
        ({"type": "remote", "url": "https://h/mcp"}, "http"),
        ({"type": "sse", "url": "https://h/sse"}, "sse"),
        ({"url": "https://h/mcp"}, "http"),
        ({"type": "streamable_http", "uri": "https://h/mcp"}, "http"),
        ({}, "sconosciuto"),
    ],
)
def test_transport_of(entry, atteso):
    spec = BY_ID["cursor"].mcp_files[0]
    assert detect.transport_of(entry, spec) == atteso


# --- segreti -----------------------------------------------------------------


def test_segreto_riconosciuto_dal_nome_del_campo():
    spec = BY_ID["cursor"].mcp_files[0]
    entry = {"headers": {"x-consumer-api-key": "ck_abc"}}
    assert detect.secrets_in(entry, spec) == ["headers.x-consumer-api-key"]


def test_percorso_lungo_non_e_un_segreto():
    """Il falso positivo da evitare: un PATH lungo in una variabile d'ambiente."""
    spec = BY_ID["cursor"].mcp_files[0]
    entry = {"env": {"NODE_PATH": "/Applications/Some.app/Contents/Resources/lib/node_modules"}}
    assert detect.secrets_in(entry, spec) == []


def test_credenziale_riconosciuta_dal_valore():
    spec = BY_ID["cursor"].mcp_files[0]
    entry = {"env": {"OPENCOSO": "sk-abcdefghijklmnopqrst"}}
    assert detect.secrets_in(entry, spec) == ["env.OPENCOSO"]


def test_riferimento_a_variabile_non_e_un_segreto():
    spec = BY_ID["cursor"].mcp_files[0]
    assert detect.secrets_in({"env": {"API_KEY": "${MIA_CHIAVE}"}}, spec) == []


def test_nessun_campo_duplicato_nel_referto():
    """`env_field` e `env` coincidono per molti harness: non vanno contati due volte."""
    spec = BY_ID["cursor"].mcp_files[0]
    entry = {"env": {"API_KEY": "abc123", "TOKEN": "def456"}}
    assert detect.secrets_in(entry, spec) == ["env.API_KEY", "env.TOKEN"]


# --- mascheramento -----------------------------------------------------------


def test_mask_non_divora_il_resto_del_comando():
    riga = "claude mcp add -e API_KEY=sk-abc123 demo -- npx -y @org/pkg"
    assert apply_mcp.mask(riga) == "claude mcp add -e API_KEY=*** demo -- npx -y @org/pkg"


def test_mask_bearer_conserva_gli_apici():
    riga = "droid mcp add s https://h/mcp --header 'Authorization: Bearer tok123456'"
    assert apply_mcp.mask(riga).endswith("'Authorization: Bearer ***'")


def test_mask_lascia_visibili_i_riferimenti_a_variabile():
    assert apply_mcp.mask('"api_key": "${MIA}"') == '"api_key": "${MIA}"'


def test_mask_copre_i_valori_con_spazi_dentro_le_virgolette():
    assert apply_mcp.mask('"token": "a b c"') == '"token": "***"'


# --- traduzione per harness --------------------------------------------------


def _args(**kwargs):
    base = dict(
        name="demo", url=None, transport="http", env=[], env_ref=[], header=[],
        command=["npx", "-y", "@org/pkg"], scope=None, remove=False, force=False,
        apply=False,
    )
    base.update(kwargs)
    return type("Args", (), base)()


def test_opencode_usa_un_array_unico_per_il_comando():
    harness = BY_ID["opencode"]
    entry = apply_mcp.build_entry(harness, harness.mcp_files[0], _args())
    assert entry == {"type": "local", "command": ["npx", "-y", "@org/pkg"], "enabled": True}


def test_goose_usa_cmd_e_envs_non_command_e_env():
    harness = BY_ID["goose"]
    entry = apply_mcp.build_entry(harness, harness.mcp_files[0], _args(env=["A=b"]))
    assert entry["cmd"] == "npx"
    assert entry["args"] == ["-y", "@org/pkg"]
    assert entry["envs"] == {"A": "b"}
    assert "command" not in entry and "env" not in entry


def test_crush_usa_header_al_singolare():
    harness = BY_ID["crush"]
    entry = apply_mcp.build_entry(
        harness, harness.mcp_files[0], _args(url="https://h/mcp", header=["X-Api-Key: v"])
    )
    assert entry["header"] == {"X-Api-Key": "v"}
    assert "headers" not in entry


def test_zed_usa_campi_piatti_non_annidati():
    """La forma con `source: custom` e `command: {path}` è quella vecchia."""
    harness = BY_ID["zed"]
    entry = apply_mcp.build_entry(harness, harness.mcp_files[0], _args())
    assert entry == {"command": "npx", "args": ["-y", "@org/pkg"]}
    assert "source" not in entry


def test_zed_supporta_i_server_remoti():
    harness = BY_ID["zed"]
    entry = apply_mcp.build_entry(
        harness, harness.mcp_files[0], _args(url="https://h/mcp", header=["Authorization: Bearer x"])
    )
    assert entry == {"url": "https://h/mcp", "headers": {"Authorization": "Bearer x"}}


def test_env_ref_diventa_un_riferimento_non_un_valore():
    harness = BY_ID["cursor"]
    entry = apply_mcp.build_entry(
        harness, harness.mcp_files[0], _args(env_ref=["PGPASSWORD=PG_PASS"])
    )
    assert entry["env"] == {"PGPASSWORD": "${PG_PASS}"}


def test_cli_di_claude_mette_il_separatore_prima_del_comando():
    cmd = apply_mcp.build_cli(BY_ID["claude-code"], _args(env=["A=b"], scope="user"))
    assert cmd == [
        "claude", "mcp", "add", "--scope", "user", "-e", "A=b",
        "demo", "--", "npx", "-y", "@org/pkg",
    ]


def test_cli_di_droid_mette_il_tipo_per_i_remoti():
    cmd = apply_mcp.build_cli(BY_ID["droid"], _args(url="https://h/mcp", transport="sse"))
    assert cmd == ["droid", "mcp", "add", "demo", "https://h/mcp", "--type", "sse"]


# --- scrittura ---------------------------------------------------------------


@pytest.fixture
def casa(tmp_path, monkeypatch):
    """Una HOME finta: nessun test tocca la configurazione reale."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / ".config"))
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    return tmp_path


def test_scrittura_su_json_preserva_le_altre_chiavi(casa):
    target = casa / ".cursor" / "mcp.json"
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps({"mcpServers": {"esistente": {"command": "x"}}}))

    rc = apply_mcp.main(
        ["--harness", "cursor", "--name", "demo", "--apply", "--", "npx", "pkg"]
    )
    assert rc == 0
    data = json.loads(target.read_text())
    assert set(data["mcpServers"]) == {"esistente", "demo"}
    assert data["mcpServers"]["demo"]["args"] == ["pkg"]


def test_scrittura_lascia_un_backup(casa):
    target = casa / ".cursor" / "mcp.json"
    target.parent.mkdir(parents=True)
    target.write_text('{"mcpServers": {}}')

    apply_mcp.main(["--harness", "cursor", "--name", "demo", "--apply", "--", "npx", "pkg"])
    backups = list(target.parent.glob("mcp.json.bak-*"))
    assert len(backups) == 1
    assert json.loads(backups[0].read_text()) == {"mcpServers": {}}


def test_nome_gia_presente_si_ferma_senza_scrivere(casa, capsys):
    target = casa / ".cursor" / "mcp.json"
    target.parent.mkdir(parents=True)
    prima = json.dumps({"mcpServers": {"demo": {"command": "vecchio"}}})
    target.write_text(prima)

    rc = apply_mcp.main(
        ["--harness", "cursor", "--name", "demo", "--apply", "--", "npx", "pkg"]
    )
    assert rc == 1
    assert target.read_text() == prima
    assert "esiste già" in capsys.readouterr().err


def test_dry_run_non_scrive(casa):
    target = casa / ".cursor" / "mcp.json"
    target.parent.mkdir(parents=True)
    target.write_text('{"mcpServers": {}}')

    rc = apply_mcp.main(["--harness", "cursor", "--name", "demo", "--", "npx", "pkg"])
    assert rc == 0
    assert json.loads(target.read_text()) == {"mcpServers": {}}
    assert not list(target.parent.glob("*.bak-*"))


def test_file_illeggibile_non_viene_riscritto(casa, capsys):
    target = casa / ".cursor" / "mcp.json"
    target.parent.mkdir(parents=True)
    target.write_text("{ questo non è JSON ")

    rc = apply_mcp.main(
        ["--harness", "cursor", "--name", "demo", "--apply", "--", "npx", "pkg"]
    )
    assert rc == 1
    assert target.read_text() == "{ questo non è JSON "
    assert "non è leggibile" in capsys.readouterr().err


def test_yaml_lista_di_continue_sostituisce_per_nome(casa):
    target = casa / ".continue" / "config.yaml"
    target.parent.mkdir(parents=True)
    target.write_text(yaml.safe_dump({"name": "x", "mcpServers": [{"name": "demo"}]}))

    apply_mcp.main(
        ["--harness", "continue", "--name", "demo", "--apply", "--", "npx", "pkg"]
    )
    data = yaml.safe_load(target.read_text())
    assert data["name"] == "x"
    assert [e["name"] for e in data["mcpServers"]] == ["demo"]
    assert data["mcpServers"][0]["command"] == "npx"


def test_rimozione(casa):
    target = casa / ".cursor" / "mcp.json"
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps({"mcpServers": {"demo": {}, "altro": {}}}))

    rc = apply_mcp.main(["--harness", "cursor", "--name", "demo", "--remove", "--apply"])
    assert rc == 0
    assert list(json.loads(target.read_text())["mcpServers"]) == ["altro"]


def test_harness_da_verificare_si_ferma(casa, capsys):
    rc = apply_mcp.main(["--harness", "qwen", "--name", "demo", "--", "npx", "pkg"])
    assert rc == 1
    assert "da-verificare" in capsys.readouterr().err


def test_jsonc_non_si_riscrive_ma_offre_il_frammento(casa, capsys):
    target = casa / ".config" / "zed" / "settings.json"
    target.parent.mkdir(parents=True)
    target.write_text('{ // commento\n "theme": "One" }')

    rc = apply_mcp.main(["--harness", "zed", "--name", "demo", "--apply", "--", "npx", "pkg"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "context_servers" in err
    assert target.read_text() == '{ // commento\n "theme": "One" }'


# --- inventario --------------------------------------------------------------


def test_collegamento_rotto_viene_contato(casa):
    skills = casa / ".claude" / "skills"
    skills.mkdir(parents=True)
    (skills / "viva").mkdir()
    (skills / "morta").symlink_to(casa / "non-esiste")

    result = detect.read_skills("~/.claude/skills")
    assert result["ok"] == ["viva"]
    assert [b["name"] for b in result["broken"]] == ["morta"]


def test_configurazione_senza_harness_e_un_difetto(casa):
    """Un harness disinstallato che lascia i file dietro di sé va segnalato.

    Per Claude Code il file di configurazione (`~/.claude.json`) sta fuori dalla
    cartella che ne rileva la presenza (`~/.claude`), quindi il caso è reale.
    """
    (casa / ".claude.json").write_text(json.dumps({"mcpServers": {"x": {"command": "y"}}}))

    info = detect.inspect(BY_ID["claude-code"])
    assert info["present"] is False
    assert [s["name"] for s in info["servers"]] == ["x"]
    assert any("non rilevato" in p for p in info["problems"])


def test_inventario_non_scrive_niente(casa):
    prima = sorted(p.name for p in casa.iterdir())
    detect.main([])
    assert sorted(p.name for p in casa.iterdir()) == prima
