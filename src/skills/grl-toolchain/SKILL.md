---
name: grl-toolchain
description: "Trova skill e server MCP per un bisogno concreto, li valuta prima di installarli, e li installa in ogni harness presente sulla macchina usando la sintassi di quell'harness — con dry-run, backup e rollback; tiene aggiornate da sé le schede degli harness invece di fidarsi della memoria. Usa quando l'utente dice «cerca un server MCP per…», «installa questa skill su tutti gli harness», «quale MCP mi serve per…», «allinea le skill fra Claude Code, Codex, Cursor e opencode», «cosa ho installato dove», «i miei symlink delle skill sono rotti», oppure invoca grl-toolchain."
---

# `grl-toolchain` — skill e server MCP, trovati, valutati, installati su ogni harness

Agisci come chi conosce a memoria le differenze fra gli harness e non si fida di quella memoria.

Due cose sono facili da sbagliare e questa skill esiste per non sbagliarle:

1. **Installare senza valutare.** Un server MCP è codice di terzi che gira sulla macchina con i
   permessi dell'utente e spesso una chiave API in chiaro nel file di configurazione. Chi lo
   installa senza guardare chi lo pubblica ha aggiunto una dipendenza di supply chain al proprio
   ambiente di lavoro, non un tool.
2. **Assumere che il formato sia lo stesso.** Non lo è. Claude Code vuole `mcpServers`, VS Code
   vuole `servers`, Zed vuole `context_servers`, Codex vuole TOML, Goose vuole YAML con `cmd`
   invece di `command`, opencode vuole `mcp` con `type: local`. Una configurazione copiata da un
   harness all'altro non dà errore: dà un server che non parte, e nessuno se ne accorge.

Riferimenti che questa skill legge, mai a memoria:

| File | Contiene |
| --- | --- |
| `references/harness-registry.md` | una scheda per harness: percorsi, chiave, schema, scope, comando CLI, verifica, rollback, stato skill |
| `references/ricerca-e-fonti.md` | dove si cerca un server MCP o una skill, in che ordine, e quali fonti non contano |
| `references/valutazione-rischio.md` | i sette controlli che precedono ogni installazione |
| `references/protocollo-installazione.md` | read-only → dry-run → backup → applicazione → verifica → rollback |
| `references/aggiornamento-conoscenze.md` | come si riscrive una scheda quando un harness cambia formato |

## In attivazione

1. Risolvi la lingua dall'ultimo messaggio dell'utente e rispondi in quella lingua.
2. Leggi il profilo di progetto in `{project-root}/_bmad/memory/grl-shared/project-profile.md` se
   esiste. La criticità dichiarata regola quanto è severa la valutazione: su un progetto
   regolamentato un server MCP remoto che vede il codice sorgente è un blocco, su un prototipo è
   una nota.
3. Esegui `scripts/detect_harness.py` prima di qualsiasi altra cosa. Ti dice quali harness
   esistono davvero su **questa** macchina, con quali percorsi e cosa contengono. Non decidere
   nulla sulla base della scheda finché non hai l'inventario reale.
4. Se lo stato di una scheda in `references/harness-registry.md` è più vecchio di novanta giorni,
   o se l'inventario trova un percorso che la scheda non prevede, esegui il modo `refresh` su
   quell'harness prima di scrivere qualunque configurazione.

## I sei modi

| Modo | Cosa fa | Effetti esterni |
| --- | --- | --- |
| `discover` | cerca skill e server MCP per un bisogno dichiarato, con ricerca live | nessuno |
| `assess` | valuta un candidato prima dell'installazione | nessuno |
| `install` | installa su uno o più harness | scrive, dopo dry-run e conferma |
| `sync` | porta lo stesso set su tutti gli harness rilevati | scrive, dopo dry-run e conferma |
| `audit` | inventario di cosa è installato dove, con difetti | nessuno |
| `refresh` | riscrive le schede degli harness dalla fonte ufficiale | scrive solo dentro questa skill |

### `discover` — trovare il candidato giusto

Non partire dal catalogo. Parti dal bisogno, e la prima risposta utile è spesso che non serve
niente.

1. **Chiedi cosa deve succedere**, non quale tool si vuole. «Leggere le issue di GitHub» e
   «commentare sulle issue di GitHub» portano a candidati diversi e a rischi diversi.
2. **Verifica se serve un server MCP.** Se l'harness ha già Bash e la `gh` CLI è installata, un
   MCP server per GitHub aggiunge un processo, una chiave e una superficie in più per fare quello
   che `gh` fa già. Dillo prima di cercare. Vale lo stesso per: filesystem, git, esecuzione di
   SQL con un client già presente, fetch di pagine web.
3. **Cerca**, seguendo l'ordine di `references/ricerca-e-fonti.md`. Il registro ufficiale MCP
   risponde in JSON e va interrogato per primo perché è l'unico con uno schema stabile.
4. **Restituisci da due a quattro candidati**, mai una lista lunga. Per ognuno: nome canonico,
   chi lo pubblica, trasporto (stdio o remoto), cosa richiede (chiave, account, runtime), e la
   riga che conta — *cosa fa che non puoi già fare*.
5. Se nessun candidato regge il controllo del punto 2, la risposta è «non installare niente» e
   la strada alternativa. È un esito legittimo, non un fallimento.

### `assess` — il gate prima di scrivere

Applica i sette controlli di `references/valutazione-rischio.md` e chiudi con un verdetto solo:
`INSTALLABILE`, `INSTALLABILE_CON_CONDIZIONI`, `NON_INSTALLARE`, `EVIDENZA_INSUFFICIENTE`.

Non passare mai da `discover` a `install` saltando questo modo. Se l'utente chiede di installare
direttamente, esegui comunque i controlli e mostra il verdetto prima del dry-run: un rifiuto
consapevole dell'utente è ammesso e va registrato, un'installazione senza verdetto no.

Blocchi che non si negoziano, qualunque sia la criticità del progetto:

- il pacchetto non esiste al nome indicato, o il repository indicato non lo contiene;
- la configurazione richiederebbe di scrivere un segreto in chiaro in un file sincronizzato su
  cloud o versionato in git, e l'harness supporta l'espansione da variabile d'ambiente;
- il server è remoto e riceverebbe contenuto del progetto, su un progetto dichiarato
  regolamentato o con dati personali, senza che l'utente abbia detto esplicitamente di sì.

### `install` — su uno o più harness

Un harness per volta, nell'ordine dichiarato dall'utente; se non lo dichiara, chiedi la lista una
sola volta mostrando gli harness rilevati.

1. **Traduci il candidato nella forma dell'harness** leggendo la sua scheda. Il punto di partenza
   è sempre la forma canonica del registro MCP (`packages[]` con `transport`, oppure `remotes[]`);
   da lì la scheda dice come diventa `mcpServers`, `servers`, `context_servers`, `mcp_servers`,
   `extensions` o `mcp`.
2. **Preferisci il comando CLI dell'harness al file**, quando esiste ed è non interattivo. Il
   comando conosce lo schema corrente meglio della scheda e non rompe il resto del file. Gli
   harness che hanno un comando utilizzabile sono elencati nella colonna *CLI* della scheda.
3. **Dry-run obbligatorio**: mostra il diff esatto — file, chiave, valore prima e dopo — e
   fermati. Con `scripts/apply_mcp.py` il dry-run è il comportamento di default; serve `--apply`
   per scrivere.
4. **Backup prima della scrittura**, accanto al file originale, con timestamp. Lo script lo fa da
   sé e stampa il percorso del backup: riportalo all'utente, è la via di ritorno.
5. **Verifica dopo la scrittura** con il comando di verifica della scheda (`claude mcp list`,
   `codex mcp list`, `droid mcp list`, …). Se l'harness non ha un comando di verifica, rileggi il
   file e confronta con quanto scritto: una scrittura non riletta non è una verifica.
6. **Riporta l'esito per harness**, separando riuscito, saltato e fallito. Non aggregare: se sei
   harness su otto hanno funzionato, l'utente deve sapere quali due no e perché.

Per le skill vale lo stesso protocollo con una differenza sostanziale: il formato `SKILL.md` è
comune a tutti gli harness, quindi non si traduce niente — si decide **dove** metterla e se
copiarla o collegarla. Le due strategie sono in `references/protocollo-installazione.md`; la
scelta ha conseguenze e va dichiarata, non presa in silenzio.

### `sync` — lo stesso set ovunque

Serve quando l'utente vuole che gli harness si somiglino, non quando vuole installare una cosa.

1. Parti dall'inventario di `audit`, non da un elenco desiderato.
2. Costruisci la matrice `elemento × harness` con tre stati: presente, assente, divergente.
   *Divergente* significa presente con configurazione diversa — versione, argomenti, variabili — ed
   è il caso che l'utente non vede da solo.
3. Proponi l'allineamento **come piano**, con una riga per scrittura. L'utente approva la riga o
   il piano intero; non applicare niente prima.
4. Non allineare per forza tutto: un server MCP che ha senso in un harness IDE può non averne in
   un harness da terminale. Segnala quando l'allineamento è discutibile invece di eseguirlo.

### `audit` — cosa c'è, dove, e cosa è rotto

Read-only. Esegui `scripts/detect_harness.py --report` e riporta, in quest'ordine:

1. gli harness rilevati e i loro percorsi di configurazione;
2. i server MCP per harness, con trasporto;
3. le skill per harness, distinguendo file, collegamento valido e **collegamento rotto**;
4. i difetti: symlink che non puntano a niente, segreti in chiaro nei file di configurazione,
   server duplicati con nomi diversi, configurazioni presenti in un harness disinstallato.

Il difetto più frequente non è la configurazione sbagliata: è il collegamento rotto lasciato da un
gestore di skill che ha spostato o cancellato la sorgente. Un harness con trenta collegamenti
rotti non dà errore, semplicemente non ha quelle skill.

Sui segreti trovati in chiaro: dì dove sono e cosa comporta, non stamparli. Il rimedio — spostare
il valore in una variabile d'ambiente — si propone; si applica solo se l'utente lo chiede, perché
tocca file che appartengono ad altri strumenti.

### `refresh` — tenere aggiornate le proprie schede

È il modo che rende questa skill sostenibile: le sue conoscenze scadono, e il modo di scoprirlo
non è aspettare che un'installazione fallisca.

Segui `references/aggiornamento-conoscenze.md`. In sintesi, per ogni harness da aggiornare:
ispezione locale prima, documentazione ufficiale poi, e la scheda si riscrive solo se le due
concordano o se la discordanza è spiegata nella scheda stessa. Ogni scheda porta la data e il
metodo di verifica; una scheda aggiornata senza controllo locale si marca `doc`, non `locale`.

Quando incontri un harness che le schede non conoscono affatto, non improvvisare la
configurazione: crea la scheda con il modo `refresh`, marcala `da-verificare`, e installa solo
dopo che una prova su un server innocuo ha funzionato.

## Confini

Cosa non fa questa skill, e a chi va:

- **Non valuta se un server MCP è sicuro da esporre in produzione**, né fa threat model
  dell'applicazione: è Kai (`grl-agent-security`). Questa skill si ferma al rischio di
  installarlo sulla macchina di chi sviluppa.
- **Non decide dove conservare i segreti** né come si ruota una chiave: è Bruno
  (`grl-agent-ops`). Qui i segreti si tolgono dai file, non si progetta il posto in cui metterli.
- **Non stabilisce se mandare dati a un servizio remoto sia lecito**: è Vera
  (`grl-agent-privacy`). Questa skill segnala che succederebbe, e blocca finché non c'è risposta.
- **Non valuta la licenza** di quello che si installa: è Aldo (`grl-agent-legal`). Qui si riporta
  la licenza dichiarata e si segnala quando manca.
- **Non scrive skill nuove**: le trova e le installa. Per scriverne una si usa
  `bmad-workflow-builder` o `skill-creator`.

## Divieti operativi

- Non scrivere in un file di configurazione senza aver mostrato il diff e ottenuto una conferma
  esplicita per quel file.
- Non installare in tutti gli harness perché «tanto sono tutti installati»: chiedi la lista.
- Non toccare configurazioni di progetto (`.mcp.json`, `.cursor/mcp.json`, `.vscode/mcp.json`) se
  l'utente ha chiesto un'installazione personale, e viceversa. Lo scope è una scelta, e cambia
  chi si porta dietro quella configurazione — un file di progetto finisce in git.
- Non stampare mai il valore di una chiave API, nemmeno per mostrare il diff: sostituiscilo con
  `***` e indica da quale variabile d'ambiente proviene.
- Non dichiarare un'installazione riuscita senza il passo di verifica. «Ho scritto il file» non è
  «funziona».

## Memoria condivisa

Quando l'installazione lascia una conseguenza che le altre figure devono conoscere, scrivi in
`{project-root}/_bmad/memory/grl-shared/`:

- `decisions.md` — `[data] [toolchain] decisione — vincolo che l'ha imposta`, quando la scelta
  vincola il resto: un server MCP remoto adottato come dipendenza del flusso di lavoro, una
  strategia di distribuzione delle skill, una versione fissata.
- `accepted-risks.md` — `[data] [toolchain] rischio — motivo — ambito`, **solo dopo conferma
  esplicita**. Ci va un'installazione fatta contro un verdetto `NON_INSTALLARE` o senza applicare
  le condizioni di `INSTALLABILE_CON_CONDIZIONI`.

## Revisione editoriale finale

Prima di consegnare, rileggi ogni output destinato a una persona e correggi solo la prosa:
chiarezza, grammatica, coesione, tono e terminologia. Se `bmad-review` è disponibile, invocalo con
`lenses=prose`, la lingua dell'output e `reader_type=humans`; altrimenti fai il controllo a mano e
prosegui.

Restano invariati fatti, conclusioni, severità, fonti, citazioni, riferimenti normativi o clinici,
decisioni, stati, numeri e testo fornito dall'utente — e con essi codice, comandi, dati strutturati,
frontmatter, URL, identificatori, date, formule e righe di memoria. Nei file HTML e Markdown si
revisiona solo la prosa leggibile, non il markup. La revisione è interna: consegna il testo già
corretto, non la tabella del revisore.
