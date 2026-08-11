# Dove si cerca, in che ordine

I cataloghi da cui si parte sono quelli di `{workflow.discovery_sources}`; questa scheda dice in
che ordine si consultano e quanto vale ciascuno. Una fonte fuori da quell'elenco si può usare, ma
si dichiara.

L'ordine conta: le prime fonti hanno uno schema stabile e dicono chi pubblica, le ultime dicono
solo che qualcosa esiste. Fermarsi appena si trova un candidato buono è corretto; scendere fino
in fondo alla lista per completezza non lo è.

## Server MCP

### 1. Registro ufficiale — l'unico interrogabile in modo deterministico

`https://registry.modelcontextprotocol.io` risponde in JSON con lo schema `server.json`, che è la
forma canonica da cui si traduce per ogni harness.

```bash
curl -s "https://registry.modelcontextprotocol.io/v0/servers?search=<termine>&limit=10"
curl -s "https://registry.modelcontextprotocol.io/v0/servers?search=<nome.esatto>"
```

Campi che servono e vanno letti tutti: `name` (namespace invertito, `io.github.org/nome`),
`repository.url`, `version`, `packages[].registryType` e `identifier`, `remotes[].url`, e
`_meta."io.modelcontextprotocol.registry/official".status` — uno stato diverso da `active` è un
server ritirato o deprecato, e non si installa.

Il registro **non ospita il codice**: dice dove sta. Un'entrata nel registro non è una revisione
di sicurezza e non va presentata come tale.

### 2. Il repository di riferimento del protocollo

`github.com/modelcontextprotocol/servers` raccoglie i server di riferimento e quelli mantenuti
dai fornitori. Quando esiste qui una versione ufficiale di quello che serve, è quella: gli
equivalenti di terzi aggiungono rischio senza aggiungere funzioni.

### 3. Il fornitore stesso

Molti servizi pubblicano il proprio server MCP nella loro documentazione, spesso remoto e con
OAuth invece che con una chiave in chiaro. È quasi sempre l'opzione migliore quando esiste.
Cercala prima di prendere un wrapper di terzi che chiama la stessa API.

### 4. Le directory della comunità

PulseMCP, Glama, Smithery, `mcpservers.org` (`punkpeye/awesome-mcp-servers`). Servono a **trovare
il nome**, non a decidere. Numeri di installazioni e badge non sono garanzie: quasi tutte queste
directory indicizzano automaticamente e la verifica di proprietà, dove c'è, dice solo chi ha
rivendicato la voce.

Quando un candidato arriva da qui, torna al punto 1 e cerca il suo nome canonico nel registro
ufficiale: se non c'è, la valutazione parte già con un'evidenza in meno.

## Skill

Il formato `SKILL.md` — una cartella con un file, frontmatter YAML e istruzioni in Markdown — è
comune a tutti gli harness che compaiono nel registro. Una skill trovata per un harness funziona
sugli altri: cambia solo la cartella in cui va messa.

### 1. La fonte ufficiale del formato

`github.com/anthropics/skills` contiene le skill di riferimento e mostra le convenzioni del
formato — frontmatter minimo, riferimenti a file esterni, script accanto alla skill.

### 2. Chi pubblica il tool a cui la skill si riferisce

Una skill che descrive come usare un prodotto è utile quanto è aggiornata. Quella pubblicata da
chi fa il prodotto invecchia più lentamente di una scritta da terzi sei mesi fa.

### 3. Marketplace e raccolte

Esistono raccolte grandi (nell'ordine delle centinaia di migliaia di voci) e alcune installano
tramite un proprio gestore che collega le skill agli harness invece di copiarle. Conseguenze da
conoscere prima di usarle, in `protocollo-installazione.md`.

Su una raccolta di quelle dimensioni, il numero di stelle e la posizione in classifica non
selezionano niente. Il criterio è: si legge il `SKILL.md` prima di installarlo. Una skill è un
testo che entrerà nel contesto di un agente e ne cambierà il comportamento — leggerla richiede
due minuti e sostituisce ogni altro segnale.

### 4. Quello che c'è già

Prima di cercare fuori, `scripts/detect_harness.py` dice cosa è già installato sugli altri
harness della macchina. Molto spesso la skill che serve è già lì, su un harness solo.

## Ricerca live: cosa chiedere

Le query che funzionano nominano il bisogno e il formato, non il nome del prodotto:

- `MCP server <servizio> official documentation` — per trovare il fornitore prima dei wrapper
- `site:github.com <servizio> mcp server stars` — per distinguere il progetto principale dai fork
- `<harness> MCP configuration file path <anno>` — quando serve aggiornare una scheda

Da non fare: chiedere «il migliore server MCP per X» e riportare la risposta. Le pagine che
rispondono a quella domanda sono quasi tutte generate e citano progetti che a volte non esistono.
Ogni candidato va riscontrato sul registro o sul repository prima di essere nominato all'utente.
