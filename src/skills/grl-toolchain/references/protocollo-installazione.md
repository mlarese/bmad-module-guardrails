# Protocollo di installazione

Sei passi, sempre nello stesso ordine, per ogni harness. Saltarne uno non fa risparmiare tempo:
sposta il costo su quando qualcosa non funziona e non si sa cosa è cambiato.

```
read-only → dry-run → backup → applicazione → verifica → (rollback)
```

## 1. Read-only

`scripts/detect_harness.py` sull'harness bersaglio. Serve a sapere tre cose prima di toccare
niente:

- il file di configurazione esiste, ed è dove la scheda dice;
- è leggibile e sintatticamente valido — se è già rotto, va detto all'utente, non riscritto;
- il nome che si sta per aggiungere non è già occupato. Un nome occupato è una decisione
  dell'utente (aggiornare? affiancare con un altro nome? lasciare stare?), non un caso da
  risolvere in silenzio.

## 2. Dry-run

Mostra il diff prima di scrivere, con: percorso del file, chiave toccata, valore prima, valore
dopo. Non «aggiungo il server X»: il testo esatto.

`scripts/apply_mcp.py` è in dry-run per default e stampa il diff; serve `--apply` per scrivere.

I valori dei segreti nel diff si mostrano come `***`, indicando da quale variabile d'ambiente
verranno letti.

Se l'harness ha un comando CLI di aggiunta, il dry-run è il comando che verrà eseguito, scritto
per intero: l'utente deve poterlo copiare ed eseguire da sé.

## 3. Backup

Copia del file accanto all'originale, con timestamp: `mcp.json.bak-20260810-143012`. Lo script lo
fa da sé e stampa il percorso.

Il backup si fa anche quando si usa il comando CLI dell'harness, perché il comando scrive nello
stesso file e un errore di sintassi altrove nel file emerge solo dopo.

Il percorso del backup va riportato all'utente nella risposta. Un backup che non si sa dove sta
non è una via di ritorno.

## 4. Applicazione

Un file per volta. Regole che valgono per tutti:

- **preferisci il comando CLI dell'harness** quando esiste e non è interattivo: conosce lo schema
  corrente meglio della scheda e non riscrive il resto del file;
- **preserva quello che non stai cambiando**: indentazione, ordine delle chiavi, e soprattutto i
  commenti. I file JSONC (Zed, e `opencode.jsonc` quando c'è) non passano da un ciclo
  lettura-scrittura con un parser JSON standard: o si modifica il testo preservandolo, o si dà
  all'utente il frammento da incollare;
- **niente scrittura parziale**: si scrive su un file temporaneo e si rinomina, così
  un'interruzione non lascia una configurazione a metà;
- **scope corretto**: personale o di progetto è una scelta con conseguenze. Un file di progetto
  (`.mcp.json`, `.cursor/mcp.json`, `.vscode/mcp.json`) finisce in git e arriva a chiunque cloni
  il repository — insieme a qualunque chiave ci sia dentro.

## 5. Verifica

| Harness | Comando |
| --- | --- |
| Claude Code | `claude mcp list`, `claude mcp get <nome>` |
| Codex | `codex mcp list`, `codex mcp get <nome>` |
| Cursor | `cursor-agent mcp list`, poi `cursor-agent mcp enable <nome>` |
| opencode | `opencode mcp list` |
| Droid | `droid mcp list` (mostra anche lo stato di autenticazione) |
| Gemini | `gemini mcp list` |
| Goose, Windsurf, Zed, Continue, Crush, VS Code | nessun comando: rilettura del file e riavvio dell'harness |

Dove non c'è un comando, la verifica è rileggere il file e confrontarlo con quello che si voleva
scrivere. Un file scritto e non riletto non è verificato.

Molti harness leggono la configurazione MCP solo all'avvio: dopo la scrittura va detto che serve
riavviare, altrimenti l'utente prova, non vede il server, e conclude che l'installazione è
fallita.

## 6. Rollback

Si ripristina il backup e si rilegge. Va offerto — non eseguito da sé — quando:

- la verifica non trova il server;
- l'harness segnala un errore di sintassi dopo la scrittura;
- il server parte ma chiede permessi o dati che l'utente non si aspettava.

---

# Installare una skill: copia o collegamento

Il formato è lo stesso per tutti gli harness, quindi non c'è traduzione: c'è una scelta su come
la stessa cartella arriva a più harness. Le due strategie non sono equivalenti.

## Copia indipendente

Una cartella per harness, con il suo contenuto.

- Ogni harness resta indipendente: aggiornarne uno non tocca gli altri.
- Divergono nel tempo, e nessuno se ne accorge.
- Aggiornare una skill significa aggiornarla *n* volte.

Adatta quando le skill sono poche o quando si vuole modificarne una per un harness solo.

## Sorgente unica e collegamenti

Una cartella sorgente (per esempio `~/.agents/skills/<nome>/`) e un symlink dalla cartella skill
di ogni harness.

- Un aggiornamento arriva ovunque nello stesso momento.
- Nessuna divergenza possibile.
- **Fragile in un modo silenzioso**: se la sorgente viene spostata o cancellata, ogni harness si
  ritrova un collegamento rotto. Non danno errore — semplicemente non hanno più quella skill, e la
  cartella continua a sembrare piena.

È il difetto più frequente che il modo `audit` trova, e vale la pena cercarlo anche quando non è
questo il motivo per cui si sta guardando.

## Regole comuni a entrambe

- Il nome della cartella deve corrispondere al campo `name` nel frontmatter del `SKILL.md`:
  quando divergono, alcuni harness indicizzano il nome della cartella, altri il frontmatter, e la
  skill viene invocata con un nome che non esiste.
- Un `SKILL.md` con frontmatter malformato viene ignorato in silenzio da quasi tutti gli harness.
  Il campo `description` è quello che decide se la skill si attiva: se è vago, la skill è
  installata e non parte mai.
- Le skill di progetto (`<progetto>/.claude/skills/`, `<progetto>/.cursor/skills/`) finiscono in
  git. Vale la stessa distinzione di scope dei server MCP.
- Prima di installare in tutti gli harness: chiedi quali. «Tutti quelli rilevati» include
  harness che l'utente ha provato una volta e non usa più, e ogni scrittura in più è una cosa in
  più da mantenere allineata.
