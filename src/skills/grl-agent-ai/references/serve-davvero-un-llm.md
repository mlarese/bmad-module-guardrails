---
name: serve-davvero-un-llm
description: Quali parti del problema si risolvono senza modello, e dove un LLM paga davvero il proprio costo
code: SD
added: 2026-08-07
type: prompt
---

# Serve davvero un LLM

## Cosa vuol dire riuscirci

L'utente sa **quali pezzi della funzione richiesta non hanno bisogno di un modello** e con cosa si risolvono, e quali invece lo richiedono davvero. Il valore sta soprattutto nel primo elenco: una funzione tolta dalla pipeline è codice che non si scrive, costo che non si paga e un modo in meno di sbagliare.

Il consumatore è chi sta per iniziare a costruire, o chi ha un prototipo che funziona in demo e deve decidere cosa portare avanti.

## Il principio da cui discende tutto

**Un LLM è la risposta giusta quando l'input è linguaggio naturale aperto *e* l'output tollera variabilità.** Servono entrambe le condizioni. Se l'input ha una struttura nota, esiste un parser. Se l'output deve essere sempre identico a parità di input, un modello è lo strumento sbagliato per definizione: il non-determinismo è la sua natura, non un difetto da correggere con la temperatura a zero.

La domanda che smonta il problema:

> **Se questa funzione dovesse dare sempre la stessa risposta allo stesso input, il modello sarebbe ancora la scelta giusta?**

## Repertorio: cosa si risolve senza modello

| La funzione richiesta | Cosa la risolve senza LLM | Quando invece il modello serve |
| --------------------- | ------------------------- | ------------------------------ |
| Classificazione in poche classi stabili | un classificatore addestrato una volta, o una tabella di regole sulle parole chiave | le classi sono molte, si sovrappongono, o cambiano spesso; il testo è lungo e ambiguo |
| Estrazione da documenti a struttura fissa | un parser: template posizionale, espressioni regolari, libreria di estrazione tabellare | i documenti hanno layout e diciture diverse da fornitore a fornitore |
| Ricerca fra documenti | indice full-text (Postgres, Elasticsearch, SQLite FTS) o ricerca vettoriale **senza generazione**: mostra i passaggi, non li riassume | la domanda richiede di combinare informazioni sparse in più passaggi |
| Instradamento di una richiesta | una tabella o un albero di condizioni sui campi che hai già | l'unico segnale è testo libero scritto da una persona |
| Validazione di un dato | uno schema, un vincolo di database, una regola | la validazione è un giudizio sul contenuto («questa descrizione è pertinente al prodotto?») |
| Traduzione di formati fra due sistemi | una mappatura scritta a mano | i due lati non sono strutturati e cambiano |
| Sommario di un campo che già hai | mostrare i campi | il testo di partenza è lungo, non strutturato e va condensato per una persona |

Regola pratica: se la funzione si può descrivere per intero come una tabella di corrispondenze, scrivi la tabella.

## Dove il modello serve davvero

- **Testo libero scritto da persone in ingresso**, senza forma prevedibile: ticket, email, note, trascrizioni.
- **Compiti generativi**: scrivere, riformulare, tradurre, adattare il tono.
- **Domande in linguaggio naturale su un corpus**, quando la risposta va composta da più fonti (vedi *Recupero e RAG*).
- **Compiti a coda lunga**: mille varianti rare, ciascuna troppo poco frequente per meritare una regola.
- **Prototipazione**: un modello può coprire in un giorno una funzione che vale la pena studiare prima di costruirla per bene. Questo è un uso legittimo, purché sia dichiarato come temporaneo e non finisca in produzione per inerzia.

## Fine-tuning contro prompting

Quando il modello serve, resta la domanda su **come** adattarlo. L'ordine è sempre lo stesso, dal
più economico al più costoso: prompt migliore → esempi nel prompt → recupero dei dati giusti (RAG)
→ fine-tuning.

| Segnale | Cosa dice |
| ------- | --------- |
| Il modello sbaglia perché non conosce i tuoi dati | serve recupero, non fine-tuning: i dati cambiano, i pesi no |
| Il modello sbaglia perché non capisce l'istruzione | serve un prompt migliore, o esempi |
| Il modello capisce e conosce, ma non tiene la forma o il tono su migliaia di casi | qui il fine-tuning paga |
| Il compito è raro o il volume è basso | il fine-tuning non rientra: costa dati etichettati, una pipeline di training e una nuova versione da mantenere |

Il fine-tuning insegna un **comportamento**, non dei **fatti**. Chi lo usa per iniettare
conoscenza aggiornabile compra un modello che sarà vecchio alla prossima modifica dei dati, e non
saprà dire cosa sa. Prima di proporlo servono: un set di casi che misura il difetto, la prova che
prompting e recupero non lo chiudono, e chi manterrà il modello addestrato.

## Il costo nascosto, che va detto prima

Un LLM non è una funzione più costosa: è un tipo diverso di componente.

| Costo | Cosa comporta in pratica |
| ----- | ------------------------ |
| Non-determinismo | lo stesso input può dare risposte diverse. I test a confronto esatto non funzionano; serve un set di casi con criteri (vedi *Eval e osservabilità*) |
| Latenza | da centinaia di millisecondi a decine di secondi. Una funzione che prima era istantanea diventa qualcosa che va atteso, mostrato, o messo in coda |
| Prezzo per chiamata | ogni esecuzione costa. Moltiplicato per il volume vero, non per quello della demo (vedi *Costi e latenza*) |
| Impossibilità di fare debug come su una funzione | non c'è uno stack trace. Non si mette un breakpoint dentro il modello. Si cambia il prompt e si riprova, e senza un set di casi non si sa nemmeno se è migliorato |
| Dipendenza da un fornitore esterno | disponibilità, limiti di frequenza, e un modello che può cambiare comportamento senza che tu abbia cambiato niente |

Questi cinque punti si dicono **prima** di progettare l'impianto, non dopo.

## Forma dell'output

Due elenchi. Primo: **cosa non serve** — la funzione, con cosa si risolve, cosa si risparmia. Secondo: **cosa serve davvero** — la funzione, perché il modello è la scelta giusta, e quale dei cinque costi qui pesa di più. Se l'intero problema si risolve senza modello, dillo in una riga e fermati: è il risultato migliore.

## Trappole

- **Usare l'LLM come scorciatoia per non definire il problema.** «Ci pensa il modello» spesso significa che nessuno ha deciso quali sono i casi.
- **Togliere il modello dove è l'unica cosa che regge la coda lunga.** Una tabella di regole che copre l'80% dei casi e sbaglia in silenzio sul resto non è sempre un miglioramento: dipende da cosa succede sul 20% — se il caso non coperto è visibile e gestito, la tabella vince; se sparisce, no.
- **Confondere «non serve un LLM» con «non serve l'AI».** Un classificatore, un modello di embedding per la ricerca, un OCR sono componenti diversi con costi diversi.
- **Trattare i rischi di sicurezza dell'integrazione.** Sono di Kai. Qui si decide solo se il componente esiste.
