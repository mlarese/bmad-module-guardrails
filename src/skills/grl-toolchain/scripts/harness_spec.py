#!/usr/bin/env python3
"""Specifica degli harness: dove stanno i file, con che formato, con che chiave.

È l'unica fonte condivisa fra `detect_harness.py` (che legge) e `apply_mcp.py`
(che scrive). Tenerla separata evita che i due script divergano sul percorso o
sulla chiave di un harness — cioè esattamente il difetto che questi script
esistono per non produrre.

I percorsi usano `~` e `$XDG_CONFIG_HOME`, risolti a runtime: Crush e altri
rispettano XDG, quindi il percorso non si può fissare.

Formati:
    json-map    {"<chiave>": {"<nome>": {...}}}
    jsonc-map   come sopra, ma il file ammette commenti: si legge, non si riscrive
    toml-table  [<chiave>.<nome>] in TOML
    yaml-map    <chiave>: {<nome>: {...}} in YAML
    yaml-list   <chiave>: [ {name: <nome>, ...} ] in YAML
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def config_home() -> Path:
    """`$XDG_CONFIG_HOME` se impostata, altrimenti `~/.config`."""
    raw = os.environ.get("XDG_CONFIG_HOME")
    if raw:
        return Path(raw).expanduser()
    return Path.home() / ".config"


def resolve(raw: str) -> Path:
    """Espande `~` e il segnaposto `{config}` in un percorso della specifica."""
    return Path(raw.replace("{config}", str(config_home()))).expanduser()


@dataclass(frozen=True)
class McpFile:
    """Un file che contiene configurazione MCP per un harness."""

    path: str
    fmt: str
    key: str
    scope: str = "user"
    #: campo che contiene il comando locale, quando non è `command`
    command_field: str = "command"
    #: campo che contiene le variabili d'ambiente, quando non è `env`
    env_field: str = "env"
    #: campo che contiene gli header dei server remoti, quando non è `headers`
    headers_field: str = "headers"
    writable: bool = True

    @property
    def resolved(self) -> Path:
        return resolve(self.path)


@dataclass(frozen=True)
class Harness:
    id: str
    label: str
    #: se uno di questi percorsi esiste, l'harness è considerato presente
    detect: tuple[str, ...]
    #: comando in PATH che conferma l'installazione (facoltativo)
    cli: str | None = None
    mcp_files: tuple[McpFile, ...] = ()
    skills_dirs: tuple[str, ...] = ()
    #: comando che verifica la configurazione dopo una scrittura
    verify: str | None = None
    #: stato della scheda in references/harness-registry.md
    confidence: str = "doc"
    notes: str = ""
    aliases: tuple[str, ...] = field(default_factory=tuple)

    def present(self) -> bool:
        return any(resolve(p).exists() for p in self.detect)


HARNESSES: tuple[Harness, ...] = (
    Harness(
        id="claude-code",
        label="Claude Code",
        detect=("~/.claude",),
        cli="claude",
        mcp_files=(
            McpFile("~/.claude.json", "json-map", "mcpServers", scope="user"),
            McpFile("~/.claude/settings.json", "json-map", "mcpServers", scope="user"),
        ),
        skills_dirs=("~/.claude/skills",),
        verify="claude mcp list",
        confidence="locale",
        notes="CLI preferita: claude mcp add [--transport http] [--scope user] …",
    ),
    Harness(
        id="codex",
        label="Codex CLI",
        detect=("~/.codex",),
        cli="codex",
        mcp_files=(
            McpFile(
                "~/.codex/config.toml",
                "toml-table",
                "mcp_servers",
                headers_field="http_headers",
            ),
        ),
        skills_dirs=("~/.codex/skills",),
        verify="codex mcp list",
        confidence="locale",
        notes="TOML: la chiave è mcp_servers con underscore, non mcpServers.",
    ),
    Harness(
        id="cursor",
        label="Cursor",
        detect=("~/.cursor",),
        cli="cursor-agent",
        mcp_files=(McpFile("~/.cursor/mcp.json", "json-map", "mcpServers"),),
        skills_dirs=("~/.cursor/skills", "~/.cursor/skills-cursor"),
        verify="cursor-agent mcp list",
        confidence="locale",
        notes="Nessun comando di aggiunta: dopo la scrittura serve cursor-agent mcp enable <nome>.",
    ),
    Harness(
        id="opencode",
        label="opencode",
        detect=("{config}/opencode",),
        cli="opencode",
        mcp_files=(McpFile("{config}/opencode/opencode.json", "json-map", "mcp"),),
        skills_dirs=("{config}/opencode/skills",),
        verify="opencode mcp list",
        confidence="locale",
        notes="command è un array unico; type vale local o remote.",
    ),
    Harness(
        id="gemini",
        label="Gemini CLI",
        detect=("~/.gemini",),
        cli="gemini",
        mcp_files=(McpFile("~/.gemini/settings.json", "json-map", "mcpServers"),),
        skills_dirs=("~/.gemini/skills",),
        verify="gemini mcp list",
        confidence="locale",
    ),
    Harness(
        id="qwen",
        label="Qwen Code",
        detect=("~/.qwen",),
        cli="qwen",
        mcp_files=(McpFile("~/.qwen/settings.json", "json-map", "mcpServers"),),
        skills_dirs=("~/.qwen/skills",),
        confidence="da-verificare",
        notes="Schema assunto per derivazione da Gemini CLI: verificare prima di scrivere.",
    ),
    Harness(
        id="goose",
        label="Goose",
        detect=("{config}/goose",),
        cli="goose",
        mcp_files=(
            McpFile(
                "{config}/goose/config.yaml",
                "yaml-map",
                "extensions",
                command_field="cmd",
                env_field="envs",
            ),
        ),
        skills_dirs=("{config}/goose/skills",),
        confidence="locale",
        notes="I server si chiamano extension; il comando è cmd, le variabili sono envs.",
    ),
    Harness(
        id="droid",
        label="Factory Droid",
        detect=("~/.factory",),
        cli="droid",
        mcp_files=(McpFile("~/.factory/mcp.json", "json-map", "mcpServers"),),
        skills_dirs=("~/.factory/skills",),
        verify="droid mcp list",
        confidence="locale",
        notes="CLI preferita: droid mcp add <nome> <url|comando> --type http|sse|stdio",
    ),
    Harness(
        id="windsurf",
        label="Windsurf",
        detect=("~/.codeium/windsurf",),
        mcp_files=(McpFile("~/.codeium/windsurf/mcp_config.json", "json-map", "mcpServers"),),
        skills_dirs=("~/.codeium/windsurf/skills",),
        confidence="locale",
        notes="Il percorso è ~/.codeium/windsurf, non ~/.windsurf.",
    ),
    Harness(
        id="zed",
        label="Zed",
        detect=("{config}/zed",),
        mcp_files=(
            McpFile(
                "{config}/zed/settings.json",
                "jsonc-map",
                "context_servers",
                writable=False,
            ),
        ),
        confidence="doc",
        notes="JSON con commenti: si legge, non si riscrive con un parser JSON.",
    ),
    Harness(
        id="continue",
        label="Continue",
        detect=("~/.continue",),
        mcp_files=(McpFile("~/.continue/config.yaml", "yaml-list", "mcpServers"),),
        skills_dirs=("~/.continue/skills",),
        confidence="doc",
        notes="mcpServers è una lista: il nome è un campo, non una chiave.",
    ),
    Harness(
        id="crush",
        label="Crush",
        detect=("{config}/crush",),
        cli="crush",
        mcp_files=(
            McpFile("{config}/crush/crush.json", "json-map", "mcp", headers_field="header"),
        ),
        skills_dirs=("{config}/crush/skills",),
        confidence="doc",
        notes="Rispetta XDG; gli header remoti stanno in header al singolare.",
    ),
    Harness(
        id="cline",
        label="Cline",
        detect=("~/.cline",),
        skills_dirs=("~/.cline/skills",),
        confidence="da-verificare",
        notes="Percorso MCP dentro lo storage dell'estensione VS Code: non riscontrato.",
    ),
    Harness(
        id="vscode",
        label="VS Code + Copilot",
        detect=(
            "~/Library/Application Support/Code/User",
            "{config}/Code/User",
        ),
        mcp_files=(
            McpFile(
                "~/Library/Application Support/Code/User/mcp.json",
                "json-map",
                "servers",
            ),
            McpFile("{config}/Code/User/mcp.json", "json-map", "servers"),
        ),
        confidence="doc",
        notes="La chiave è servers, non mcpServers. CLI: code --add-mcp '{...}'.",
    ),
)


BY_ID = {h.id: h for h in HARNESSES}
