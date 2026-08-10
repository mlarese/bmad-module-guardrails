# Aggiornare le proprie conoscenze

Le schede in `harness-registry.md` scadono. Gli harness cambiano percorso, rinominano una chiave,
aggiungono un comando CLI che prima non c'era. Una skill che si fida della propria memoria scrive
configurazioni che non danno errore e non funzionano.

Questo file dice come si riscrive una scheda. Il modo `refresh` della skill esegue questa
procedura.

## Quando parte un refresh

- La scheda ha più di **novanta giorni**, e si sta per scrivere su quell'harness.
- L'inventario locale trova un percorso, una chiave o un file che la scheda non prevede.
- Una scrittura è andata a buon fine ma la verifica non trova il server.
- L'harness non è nel registro.
- L'utente lo chiede.

Non serve un refresh globale per installare una cosa su un harness: si aggiorna la scheda che
serve. Il refresh di tutte le schede è un'operazione a sé, che si fa quando la si chiede.

## La procedura, per un harness

### 1. Ispezione locale, prima di tutto

L'evidenza più forte è il filesystem della macchina, non la documentazione. La documentazione
descrive l'ultima versione; l'utente ha quella che ha.

```bash
python3 scripts/detect_harness.py --harness <id> --verbose
<cli> --version
<cli> mcp --help          # se esiste un comando mcp
<cli> --help              # per scoprire se è comparso
```

Da qui si ricavano: percorsi reali, chiavi realmente presenti, sotto-comandi realmente
disponibili. Le opzioni di un `--help` sono più affidabili di qualunque pagina.

### 2. Documentazione ufficiale, poi

Nell'ordine: documentazione del prodotto, `README` del repository, note di rilascio. Le pagine di
terzi — blog, guide, aggregatori — non si usano per scrivere una scheda: al massimo indicano dove
guardare.

Query che funzionano:

- `<harness> MCP server configuration file path`
- `<harness> settings.json mcpServers schema`
- `site:github.com/<org>/<repo> mcp configuration`

### 3. Riconciliazione

| Situazione | Cosa scrivere |
| --- | --- |
| Locale e doc concordano | scheda aggiornata, stato `locale` |
| Locale non ha il file, doc chiara | stato `doc`, con il percorso atteso |
| Locale e doc discordano | vince il locale, e la discordanza si scrive nella scheda — è l'informazione più utile della pagina |
| Nessuna delle due è chiara | stato `da-verificare`, e non si scrive su quell'harness finché una prova non riesce |

Una scheda non si aggiorna «per pulizia»: se non c'è evidenza nuova, si lascia com'è con la sua
data. Una data spostata senza controllo è peggio di una data vecchia, perché toglie il segnale che
serviva a far scattare il prossimo refresh.

### 4. Prova su un caso innocuo

Per un harness `da-verificare`, prima di dichiarare la scheda buona: si installa un server MCP
banale e senza segreti — uno che risponde a un `ping`, o il server di riferimento del filesystem
limitato a una cartella temporanea — e si verifica che l'harness lo veda. Poi si rimuove.

È l'unico modo per distinguere «la scheda descrive il formato giusto» da «la scheda descrive un
formato plausibile».

### 5. Riscrittura

Nella scheda si aggiornano: percorsi, chiave, schema, comando CLI, comando di verifica, cartella
delle skill, stato e data. Se una trappola è emersa durante la prova — una chiave con l'underscore
invece del camelCase, un array dove ci si aspettava una stringa, un file JSONC che non si può
riscrivere con un parser JSON — va nella scheda, perché è esattamente quello che la prossima
esecuzione sbaglierebbe di nuovo.

## Un harness nuovo

Quando compare un harness che il registro non conosce:

1. Individua la sua cartella di configurazione (`~/.<nome>`, `~/.config/<nome>`,
   `~/Library/Application Support/<nome>`).
2. Cerca in quei file le chiavi note: `mcpServers`, `mcp_servers`, `servers`, `context_servers`,
   `mcp`, `extensions`.
3. Cerca una cartella `skills/`: se c'è, l'harness legge il formato `SKILL.md` e le skill si
   installano lì senza altro lavoro.
4. Scrivi la scheda con stato `da-verificare` e fai la prova del punto 4.

L'ordine è quello: prima si guarda cosa c'è sulla macchina, poi si cerca la documentazione. Un
harness che non ha nessuna di quelle chiavi probabilmente non supporta MCP, e va scritto nella
scheda invece di essere cercato di nuovo la volta dopo.

## Cosa non è un refresh

- Cambiare la data senza aver riletto niente.
- Copiare in una scheda uno schema trovato su una guida di terzi.
- Aggiungere un harness al registro perché esiste: il registro contiene harness di cui si sa come
  si configurano, non un elenco di prodotti.
