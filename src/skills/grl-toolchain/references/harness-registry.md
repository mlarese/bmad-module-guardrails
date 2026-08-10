# Registro degli harness

Una scheda per harness. Ogni scheda dice dove si scrive, con che schema, con quale comando e come
si verifica. Le schede scadono: la colonna *stato* dice quanto ci si può fidare di questa pagina.

| Stato | Significato |
| --- | --- |
| `locale` | verificato ispezionando i file su una macchina reale alla data indicata |
| `doc` | preso dalla documentazione ufficiale, non riscontrato su file reali |
| `da-verificare` | ricostruito per analogia o incompleto: non scrivere senza una prova |

**Regola d'uso:** prima di scrivere su un harness marcato `doc` o `da-verificare`, esegui il modo
`refresh` su quella scheda. Prima di scrivere su un harness marcato `locale`, controlla comunque
che il file esista dove la scheda dice — un aggiornamento dell'harness può spostarlo.

Data di riferimento di tutte le schede: **2026-08-10**.

---

## La forma canonica da cui si traduce

Il registro ufficiale MCP (`registry.modelcontextprotocol.io`) restituisce ogni server nello
schema `server.json`. È da lì che si parte, non dal README del progetto:

```json
{
  "name": "capital.hove/read-only-local-postgres-mcp-server",
  "description": "…",
  "repository": { "url": "https://github.com/…", "source": "github" },
  "version": "0.1.0",
  "packages": [
    { "registryType": "npm", "identifier": "@org/pkg", "version": "0.1.0",
      "transport": { "type": "stdio" } }
  ],
  "remotes": [
    { "type": "streamable-http", "url": "https://example.com/mcp" }
  ]
}
```

Le due forme che ne derivano, e in cui ogni harness va tradotto:

- **stdio** — un comando locale: `command` + `args` + `env`. Da `packages[]`: `npm` →
  `npx -y <identifier>@<version>`, `pypi` → `uvx <identifier>` (oppure
  `python3 -m <module>` se il pacchetto non espone un entry point), `oci` → `docker run …`.
- **remoto** — un URL: `url` + `headers`, trasporto `http` (streamable) o `sse`. Da `remotes[]`.
  `streamable-http` nello schema del registro si chiama `http` in quasi tutti gli harness.

---

## Claude Code · `locale`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.claude/` esiste; CLI `claude` |
| MCP, scope utente | `~/.claude.json`, chiave `mcpServers` |
| MCP, scope progetto | `<progetto>/.mcp.json`, chiave `mcpServers` |
| MCP, alternativa | `~/.claude/settings.json`, chiave `mcpServers` |
| Skill, utente | `~/.claude/skills/<nome>/SKILL.md` |
| Skill, progetto | `<progetto>/.claude/skills/<nome>/SKILL.md` |
| Verifica | `claude mcp list`, `claude mcp get <nome>` |

**CLI (preferito):**

```bash
claude mcp add <nome> -- npx -y @org/pkg              # stdio
claude mcp add <nome> -e API_KEY=xxx -- npx -y @org/pkg
claude mcp add --transport http <nome> https://host/mcp
claude mcp add --transport http <nome> https://host/mcp --header "Authorization: Bearer …"
```

`--scope local|user|project` (default `local`). `local` vale solo nel progetto corrente e non è
condiviso; `user` vale ovunque; `project` scrive `.mcp.json`, che finisce in git.

**Schema del file:**

```json
{ "mcpServers": {
    "nome": { "command": "npx", "args": ["-y","@org/pkg"], "env": { "API_KEY": "…" } },
    "remoto": { "type": "http", "url": "https://host/mcp", "headers": { "…": "…" } } } }
```

Oltre alle skill, Claude Code installa plugin da un marketplace
(`~/.claude/plugins/`, `enabledPlugins` e `extraKnownMarketplaces` in `settings.json`): un plugin
può portare più skill insieme ed è la via giusta quando l'origine ne pubblica un gruppo.

---

## Codex CLI · `locale`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.codex/` esiste; CLI `codex` |
| MCP | `~/.codex/config.toml`, tabelle `[mcp_servers.<nome>]` — **TOML, non JSON** |
| Skill | `~/.codex/skills/<nome>/SKILL.md` |
| Verifica | `codex mcp list`, `codex mcp get <nome>` |

**CLI (preferito):**

```bash
codex mcp add <nome> --env KEY=val -- npx -y @org/pkg
codex mcp add <nome> --url https://host/mcp --bearer-token-env-var MY_TOKEN
```

**Schema del file:**

```toml
[mcp_servers.nome]
command = "npx"
args = ["-y", "@org/pkg"]
startup_timeout_sec = 120

[mcp_servers.nome.env]
API_KEY = "…"

[mcp_servers.remoto]
url = "https://host/mcp"

[mcp_servers.remoto.http_headers]
X-Api-Key = "…"
```

Il nome della chiave è `mcp_servers` con l'underscore: `mcpServers` in TOML non dà errore di
sintassi e viene semplicemente ignorato. È l'errore più silenzioso di tutto il registro.

---

## Cursor · `locale`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.cursor/` esiste; CLI `cursor-agent` |
| MCP, scope utente | `~/.cursor/mcp.json`, chiave `mcpServers` |
| MCP, scope progetto | `<progetto>/.cursor/mcp.json`, chiave `mcpServers` |
| Skill | `~/.cursor/skills/<nome>/SKILL.md` |
| Verifica | `cursor-agent mcp list`, `cursor-agent mcp list-tools <nome>` |

**Nessun comando di aggiunta.** `cursor-agent mcp` espone solo `login`, `list`, `list-tools`,
`enable`, `disable`: il server si aggiunge scrivendo il file, poi `cursor-agent mcp enable <nome>`
lo mette nella lista approvata. Saltare `enable` lascia il server configurato ma non caricato.

Schema identico a quello di Claude Code (`command`/`args`/`env`, oppure `url`/`headers`).

---

## opencode · `locale`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.config/opencode/` esiste; CLI `opencode` |
| MCP, scope utente | `~/.config/opencode/opencode.json`, chiave `mcp` |
| MCP, scope progetto | `<progetto>/opencode.json`, chiave `mcp` |
| Skill | `~/.config/opencode/skills/<nome>/SKILL.md` |
| Verifica | `opencode mcp list` |

**CLI:** `opencode mcp add [nome]` — interattivo, quindi in automazione si scrive il file.

**Schema del file** — è quello più diverso dagli altri: `command` è un **array unico**, non
comando più argomenti separati.

```json
{ "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "locale":  { "type": "local", "command": ["npx","-y","@org/pkg"],
                 "environment": { "API_KEY": "…" }, "enabled": true },
    "remoto":  { "type": "remote", "url": "https://host/mcp",
                 "headers": { "X-Api-Key": "…" }, "enabled": true } } }
```

Attenzione: nella stessa cartella può esistere `opencode.jsonc` con commenti. Se c'è, è quello
che l'utente edita a mano: non riscriverlo con un parser JSON, che ne perderebbe i commenti.

---

## Gemini CLI · `locale` (percorsi) / `doc` (comando)

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.gemini/` esiste |
| MCP, scope utente | `~/.gemini/settings.json`, chiave `mcpServers` |
| MCP, scope progetto | `<progetto>/.gemini/settings.json`, chiave `mcpServers` |
| Skill | `~/.gemini/skills/<nome>/SKILL.md` |
| Verifica | `gemini mcp list` |

**CLI:** `gemini mcp add <nome> <comando> [args…]`, `--transport http|sse`, `-e KEY=val`.
Marcato `doc`: non riscontrato su questa macchina perché la CLI non è nel PATH.

Schema `command`/`args`/`env`, oppure `httpUrl`/`url` per i remoti — da confermare con `refresh`
prima di scrivere un server remoto.

---

## Qwen Code · `da-verificare`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.qwen/` esiste |
| MCP, scope utente | `~/.qwen/settings.json` — chiave `mcpServers` **assunta per derivazione** |
| Skill | `~/.qwen/skills/<nome>/SKILL.md` |

Qwen Code è un fork di Gemini CLI e ne eredita l'impianto di configurazione, ma su questa macchina
`settings.json` non contiene la chiave `mcpServers`, quindi lo schema non è riscontrato. Verifica
con `refresh` prima di scrivere. La cartella delle skill invece è riscontrata.

---

## Goose · `locale` (percorsi) / `doc` (schema stdio)

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.config/goose/config.yaml` esiste; CLI `goose` |
| MCP | `~/.config/goose/config.yaml`, chiave `extensions` — **YAML** |
| Skill | `~/.config/goose/skills/<nome>/SKILL.md` |
| Verifica | `goose configure` (interattivo), oppure rilettura del file |

In Goose i server MCP si chiamano *extension* e i campi non hanno gli stessi nomi degli altri
harness: il comando è `cmd`, non `command`; le variabili sono `envs`, non `env`.

```yaml
extensions:
  developer:            # builtin, non toccare
    bundled: true
    enabled: true
    name: developer
    type: builtin
    timeout: 300
  nome:
    type: stdio
    name: nome
    cmd: npx
    args: ["-y", "@org/pkg"]
    envs: { API_KEY: "…" }
    enabled: true
    timeout: 300
  remoto:
    type: streamable_http
    name: remoto
    uri: https://host/mcp
    enabled: true
```

`goose configure` è interattivo e non si automatizza: qui si scrive il file. Le voci `builtin` con
`bundled: true` non si toccano mai.

---

## Factory Droid · `locale`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.factory/` esiste; CLI `droid` |
| MCP | `~/.factory/mcp.json`, chiave `mcpServers` |
| Skill | `~/.factory/skills/<nome>/SKILL.md` |
| Verifica | `droid mcp list` |

**CLI (preferito):**

```bash
droid mcp add <nome> npx -y @org/pkg --env KEY=val
droid mcp add <nome> https://host/mcp --type http --header "Authorization: Bearer …"
droid mcp add <nome> https://host/mcp --type sse --no-oauth
```

`--type` vale `stdio` (default), `http`, `sse`. `droid mcp list` mostra anche lo stato di
autenticazione, quindi è una verifica vera e non solo una rilettura.

---

## Windsurf · `locale`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.codeium/windsurf/` esiste |
| MCP | `~/.codeium/windsurf/mcp_config.json`, chiave `mcpServers` |
| Skill | `~/.codeium/windsurf/skills/` |
| Altro | `~/.codeium/windsurf/workflows/` per i workflow propri di Windsurf |

Il percorso **non** è `~/.windsurf/`, che pure esiste e contiene estensioni e configurazione
dell'editor: scriverci il file MCP non produce nessun effetto e nessun errore.

Schema `command`/`args`/`env`, come Claude Code. Nessun comando CLI: si scrive il file e si
riavvia l'editor.

---

## VS Code + GitHub Copilot · `doc`

| Voce | Valore |
| --- | --- |
| MCP, scope utente | `mcp.json` nella cartella del profilo utente (comando *MCP: Open User Configuration*) |
| MCP, scope progetto | `<progetto>/.vscode/mcp.json` |
| Chiave | `servers` — **non** `mcpServers` |
| CLI | `code --add-mcp '{"name":"…","command":"npx","args":["-y","@org/pkg"]}'` |

```json
{ "servers": {
    "nome":   { "command": "npx", "args": ["-y","@org/pkg"] },
    "remoto": { "type": "http", "url": "https://host/mcp" } } }
```

`code --add-mcp` scrive nel profilo utente ed è il modo più affidabile perché il percorso del
profilo cambia con il profilo attivo e non si indovina.

---

## Zed · `doc`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.config/zed/settings.json` esiste |
| MCP | `~/.config/zed/settings.json`, chiave `context_servers` |

```json
{ "context_servers": {
    "nome": { "source": "custom",
              "command": { "path": "npx", "args": ["-y","@org/pkg"], "env": {} } } } }
```

Due trappole: la chiave si chiama `context_servers`, e comando e argomenti stanno **dentro** un
oggetto `command`. In più `settings.json` di Zed è JSON **con commenti**: un ciclo
lettura-scrittura con un parser JSON standard fallisce o cancella i commenti dell'utente. Va
modificato preservando il testo, o lasciato all'utente con il frammento pronto da incollare.

---

## Continue · `doc`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.continue/config.yaml` esiste |
| MCP | `~/.continue/config.yaml`, chiave `mcpServers` (schema `v1`) |
| Skill | `~/.continue/skills/<nome>/SKILL.md` |

```yaml
mcpServers:
  - name: nome
    command: npx
    args: ["-y", "@org/pkg"]
    env: { API_KEY: "…" }
```

È una **lista**, non una mappa: il nome è un campo, non una chiave. Su questa macchina il file
esiste ma non contiene la sezione, quindi lo schema non è riscontrato.

---

## Cline · `da-verificare`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.cline/` esiste (CLI), oppure l'estensione VS Code |
| MCP | `cline_mcp_settings.json` nello storage globale dell'estensione VS Code |
| Skill | `~/.cline/skills/` |

Il percorso del file dipende dall'installazione di VS Code e dal sistema operativo, e non è stato
riscontrato qui. Non scrivere a mano: usa l'interfaccia di Cline, oppure esegui `refresh` e trova
il percorso reale prima di toccare qualcosa.

---

## Crush · `doc`

| Voce | Valore |
| --- | --- |
| Rilevamento | `~/.config/crush/` esiste |
| MCP | `~/.config/crush/crush.json` (o `crushrc`), chiave `mcp` |
| Skill | `~/.config/crush/skills/` |

```json
{ "mcp": {
    "nome":   { "type": "stdio", "command": "npx", "args": ["-y","@org/pkg"],
                "env": { "API_KEY": "…" }, "timeout": 10 },
    "remoto": { "type": "http", "url": "https://host/mcp",
                "header": { "Authorization": "Bearer …" } } } }
```

Il campo degli header remoti è `header` al singolare. Crush rispetta XDG: con `XDG_CONFIG_HOME`
impostato il percorso cambia, quindi va risolto e non assunto.

---

## Riepilogo delle differenze che rompono un copia-incolla

| Harness | Chiave | Formato | Nome del comando | Header remoti |
| --- | --- | --- | --- | --- |
| Claude Code, Cursor, Windsurf, Droid | `mcpServers` | JSON | `command` + `args` | `headers` |
| Codex | `mcp_servers` | TOML | `command` + `args` | `http_headers` |
| VS Code | `servers` | JSON | `command` + `args` | — |
| Zed | `context_servers` | JSONC | `command: { path, args }` | — |
| opencode | `mcp` | JSON | `command: [ … ]` (array unico) | `headers` |
| Goose | `extensions` | YAML | `cmd` + `args` | — (`uri`) |
| Continue | `mcpServers` | YAML, **lista** | `command` + `args` | — |
| Crush | `mcp` | JSON | `command` + `args` | `header` |
