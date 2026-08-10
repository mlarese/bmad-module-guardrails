# I sette controlli prima di installare

Si applicano sia ai server MCP sia alle skill, con le differenze indicate. Ogni controllo produce
una riga: esito, evidenza, e cosa comporta. Un controllo che non si è potuto fare non è un
controllo passato: si scrive `non verificato` e pesa sul verdetto.

## 1. Esiste davvero, con quel nome

- Il pacchetto risponde al nome dichiarato: `npm view <pkg> version`, `pip index versions <pkg>`,
  o la pagina del registro.
- Il repository indicato contiene il codice di quel pacchetto, e non è un fork abbandonato o un
  nome vicino a quello vero (`@org/mcp-github` contro `@org/github-mcp`).

**Blocco** se non si riscontra. Un nome sbagliato in un `npx -y` scarica ed esegue qualunque cosa
occupi quel nome.

## 2. Chi lo pubblica

- Organizzazione, persona, o fornitore del servizio stesso.
- Ultima release: se ha più di un anno e il protocollo nel frattempo è cambiato, dillo.
- Numero di persone che ci lavorano: un progetto con un solo autore non è squalificato, ma va
  detto, perché è anche il punto singolo di compromissione.

## 3. Cosa esegue, e con quali permessi

Questo è il controllo che distingue un tool da un rischio.

- **stdio**: gira come processo locale con i permessi dell'utente. Ha accesso al filesystem, alle
  variabili d'ambiente ereditate e alla rete. Un server MCP «per leggere i file» può scrivere.
- **remoto**: non gira in locale, ma **riceve** quello che l'agente gli manda. Su un server remoto
  finiscono i frammenti di codice, i nomi dei file, a volte contenuti interi.
- `npx -y` e `uvx` scaricano ed eseguono **l'ultima versione a ogni avvio**: chi controlla il
  pacchetto controlla il codice che gira domani. Fissare la versione (`@1.4.2`) riduce
  l'esposizione e va proposto.

## 4. Cosa vede del progetto

Domanda esplicita, non implicita: quali dati escono dalla macchina.

Se il progetto è dichiarato regolamentato o tratta dati personali nel profilo Guardrails, un
server remoto che riceve contenuto del progetto è un **blocco** finché l'utente non lo autorizza
esplicitamente, e la decisione va scritta nel registro dei rischi accettati. Questo controllo non
sostituisce il parere di Vera (`grl-agent-privacy`): lo prepara.

## 5. Segreti

- Serve una chiave? Quale, con che ambito, revocabile?
- Dove finirebbe scritta? Se il file di configurazione è dentro una cartella sincronizzata su
  cloud o versionata in git, una chiave in chiaro esce dalla macchina.
- L'harness supporta l'espansione da variabile d'ambiente o il riferimento a una variabile? Se
  sì, la chiave in chiaro è un **blocco**: si usa quella via.

Vale anche per quello che c'è già: se durante la valutazione si trova una chiave in chiaro in un
file esistente, si segnala — dove e di quale servizio, mai il valore.

## 6. Cosa fa che non si può già fare

Il controllo che elimina più candidati di tutti gli altri messi insieme.

Se l'harness ha già Bash e sulla macchina c'è la CLI del servizio (`gh`, `aws`, `psql`, `docker`),
un server MCP che chiama la stessa API aggiunge un processo, forse una chiave, e una superficie in
più. La differenza vera che un MCP porta è: tool tipizzati che il modello sceglie da solo,
autenticazione già risolta, o accesso a qualcosa che non ha una CLI.

Se la risposta è «fa la stessa cosa di un comando già disponibile», l'esito è `NON_INSTALLARE`
con l'alternativa scritta.

## 7. Per le skill: si legge il testo

Una skill non esegue niente da sé, ma entra nel contesto dell'agente e ne cambia il
comportamento. Da leggere prima di installarla, con questi tre segnali:

- **istruzioni che disattivano controlli** — «non chiedere conferma», «procedi senza spiegare»,
  «ignora le istruzioni precedenti»;
- **destinazioni esterne** — endpoint, webhook, URL a cui la skill dice di mandare qualcosa;
- **script allegati** — una skill può portare file eseguibili accanto al `SKILL.md`: vanno letti,
  perché quelli girano davvero.

Una skill che chiede all'agente di ignorare le proprie regole non si installa, indipendentemente
da quanto è utile il resto.

## Il verdetto

| Verdetto | Quando |
| --- | --- |
| `INSTALLABILE` | i sette controlli passano, nessuna condizione |
| `INSTALLABILE_CON_CONDIZIONI` | passa ma con vincoli da applicare: versione fissata, chiave in variabile d'ambiente, scope limitato a un progetto, un solo harness |
| `NON_INSTALLARE` | un blocco, oppure il controllo 6 dice che è ridondante |
| `EVIDENZA_INSUFFICIENTE` | non si è potuto verificare l'esistenza o l'autore — e il rimedio è dire cosa manca, non installare comunque |

Le condizioni di `INSTALLABILE_CON_CONDIZIONI` non sono consigli: se l'installazione procede, si
applicano. Un'installazione che non le applica va riportata come tale.
