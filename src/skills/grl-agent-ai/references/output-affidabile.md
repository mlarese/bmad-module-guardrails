---
name: output-affidabile
description: Output strutturato, validato, e un comportamento definito per quando il modello sbaglia
code: OA
added: 2026-08-07
type: prompt
---

# Output affidabile

## Cosa vuol dire riuscirci

L'utente ha un **comportamento definito per il caso in cui il modello sbaglia**, e non un sistema che funziona finché la risposta arriva nella forma sperata. Il consumatore è chi deve far consumare quell'output a del codice: un parser, un database, una chiamata a un'altra API.

## Il principio da cui discende tutto

**Il modello sbaglia sempre, prima o poi: la domanda non è se, ma cosa succede quando.** Un output che il 98% delle volte è JSON valido è un output che il 2% delle volte manda in errore la produzione, e su diecimila chiamate al giorno il 2% sono duecento errori.

La domanda che smonta il problema:

> **Cosa succede a valle se questa risposta arriva sbagliata, e chi se ne accorge?**

Se la risposta è «va in una tabella e nessuno guarda», il problema non è il prompt.

## La forma dell'output

**1. Structured output nativo, non parsing del testo.** I fornitori principali offrono la generazione vincolata a uno schema (JSON schema, function calling, structured output). Usarla è quasi sempre gratis e toglie in un colpo la classe di errori più fastidiosa. Chiedere al modello di «rispondere solo in JSON» in una istruzione di sistema **non** è la stessa cosa: è una richiesta, non un vincolo.

**2. Validazione con uno schema vero.** Pydantic, zod, o quello che il progetto già usa. Lo schema sta nel codice, versionato, ed è la stessa cosa che si passa al modello: due definizioni separate divergono.

**3. Campi enumerati invece che liberi.** Ogni volta che il valore atteso è uno di N, va dichiarato come enumerazione. `stato: "aperto" | "chiuso" | "sospeso"` non ha bisogno di normalizzazione a valle; `stato: string` ti restituirà `Aperto`, `APERTO` e `in attesa di apertura`.

**4. Struttura piatta e nomi espliciti.** Le strutture profonde e i nomi ambigui aumentano gli errori del modello. `data_scadenza_contratto` funziona meglio di `date` dentro un oggetto annidato tre livelli.

## Quando la validazione fallisce

La scala, in ordine. Ogni gradino ha un costo maggiore del precedente, e si sale solo se il precedente non ha funzionato:

1. **Retry con l'errore in pasto.** Rimanda la richiesta includendo l'errore di validazione: «il campo `importo` deve essere un numero, hai restituito `"circa 300"`». Recupera la maggior parte dei casi al primo tentativo.
2. **Un secondo tentativo con temperatura più bassa**, o con il modello più capace se stavi usando quello leggero.
3. **Fallback definito**: un valore di default dichiarato, un percorso alternativo senza modello, o la marcatura del record come «da rivedere a mano».
4. **Errore all'utente**, esplicito.

Il numero massimo di tentativi è un parametro, non una speranza: due o tre. E **mai un `except: pass`** — un fallimento silenzioso in una pipeline AI produce dati mancanti che nessuno collega alla causa per settimane.

## Il modello che inventa

Le contromisure che reggono, in ordine di efficacia:

- **Ancorare alle fonti.** Il modello risponde su ciò che gli hai dato, non su ciò che sa. Vale quanto è buono il recupero: vedi *Recupero e RAG*.
- **Chiedere le citazioni**, e verificarle nel codice: se il passaggio citato non esiste nel contesto fornito, la risposta è sospetta. È un controllo deterministico, ed è il più utile.
- **Permettere esplicitamente «non lo so».** Va scritto nelle istruzioni e va reso rappresentabile nello schema (un campo `risposta_trovata: bool`). Senza questo, il modello risponde comunque: la forma della richiesta chiede una risposta, e lui la produce.
- **Restringere il compito.** Un modello a cui si chiede di estrarre cinque campi inventa meno di uno a cui si chiede di estrarne quaranta.

Cosa **non** regge, e va detto quando l'utente ci conta: chiedere al modello di autovalutarsi come unica difesa. Un modello che dichiara la propria confidenza produce un numero plausibile, non una misura. Come segnale fra altri può stare; come cancello unico, no.

## Quando l'output produce un'azione

Se la risposta del modello scatena una scrittura, un invio o una spesa, servono due cose in più:

- **Idempotenza.** La stessa richiesta processata due volte non deve produrre due effetti. Serve una chiave dedotta dall'input, non generata dal modello.
- **Una conferma umana** dove l'azione è irreversibile. Il permesso degli strumenti e la superficie di attacco sono materia di Kai: qui basta dire che la conferma esiste anche come difesa contro l'errore ordinario, non solo contro l'abuso.

## Forma dell'output

Per ogni punto: **dove l'output entra nel codice** · **cosa succede oggi se arriva sbagliato** · **il vincolo o il fallback da aggiungere**. Se il progetto non ha nessuna validazione, quello è l'unico punto da dare: gli altri vengono dopo.

## Trappole

- **Chiedere JSON in una istruzione di sistema e chiamarla struttura.**
- **Alzare la temperatura per «risposte migliori»** su un compito di estrazione, dove serve l'opposto.
- **Aggiungere un secondo modello che controlla il primo** come rimedio strutturale: raddoppia il costo e sposta il problema.
- **Trattare l'output del modello come input fidato** in una query, un comando o dell'HTML. È injection classica con una sorgente nuova, ed è di Kai: nominalo e fermati.
