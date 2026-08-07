---
name: automazioni
description: Quando basta un workflow visuale, quando serve codice, e le regole che tengono in piedi una coda di lavori AI
code: AU
added: 2026-08-07
type: prompt
---

# Automazioni e code

## Cosa vuol dire riuscirci

L'utente sa **con cosa costruire l'automazione** e — più importante — **cosa succede quando fallisce**, che è la parte che non viene mai progettata e che decide se l'automazione resta in piedi dopo tre mesi.

Il consumatore è chi vuole che qualcosa accada da solo: un documento che arriva e viene classificato, una mail che genera una bozza di risposta, un archivio che viene arricchito ogni notte.

## Il principio da cui discende tutto

**Il lavoro con un modello è lento e fallisce.** Non è una chiamata a un database: sono secondi, a volte decine, con una probabilità di errore che non è trascurabile. Metterlo dentro una richiesta HTTP sincrona è la causa più comune di automazioni che «ogni tanto non funzionano».

La domanda che smonta il problema:

> **Se questa cosa sbaglia in silenzio per due settimane, chi se ne accorge e come?**

Se non c'è risposta, l'automazione non è finita, qualunque sia lo strumento.

## Workflow visuale o codice

| Criterio | Workflow visuale (n8n, Make, Zapier) | Codice |
| -------- | ------------------------------------ | ------ |
| Numero di passi | fino a una manciata, lineari | oltre, o con ramificazioni vere |
| Logica condizionale | poca, semplice | condizioni annidate, cicli, casi limite |
| Testabilità | si prova eseguendo; nessun test automatico serio | test veri, eseguibili in continuo |
| Chi lo manterrà | anche chi non programma — è il vantaggio principale | chi programma |
| Versionamento | esiste ma è scomodo; le differenze fra versioni non si leggono | naturale |
| Credenziali | dentro la piattaforma, e vanno guardate: è un terzo che tiene le tue chiavi | dove le tieni già |
| Costo di uscita | alto: la logica è nella piattaforma, non è portabile | nessuno |

Il criterio pratico: **un workflow visuale è la risposta giusta finché resta leggibile in una schermata e finché a manutenerlo è chi lo ha fatto.** Superata quella soglia, il costo di non poterlo testare supera il vantaggio di non doverlo scrivere. n8n autogestito è la via di mezzo che regge meglio, perché almeno le credenziali e i dati restano in casa.

Dove stanno le chiavi API e chi le vede è materia di **Bruno** e di **Kai**: nominali una riga e vai avanti.

## Come si mette in piedi una coda

Il minimo che regge, per qualunque lavoro AI non interattivo:

**1. Il lavoro va in coda, non nella richiesta.** L'utente riceve subito un identificativo e uno stato; il risultato arriva dopo. Vale anche quando il lavoro dura otto secondi: otto secondi diventano trenta il giorno in cui il fornitore rallenta.

**2. Stato visibile.** In attesa, in corso, riuscito, fallito. Se l'utente non può vedere a che punto è, riproverà — e riprovare senza idempotenza raddoppia gli effetti.

**3. Idempotenza.** Lo stesso evento processato due volte non deve produrre due effetti. Serve una chiave dedotta dall'input (identificativo del documento, dell'evento, del messaggio), **non** generata dal modello e non casuale. Senza questa, ogni retry è un rischio.

**4. Retry con un tetto.** Attesa crescente, tre tentativi, poi si smette. Un retry infinito su un errore permanente consuma budget finché non lo si nota.

**5. Dead letter.** Ciò che fallisce sempre finisce in una coda a parte, non sparisce e non blocca il resto. E quella coda deve avere qualcuno che la guarda.

**6. Una notifica a una persona quando la coda si blocca o la dead letter cresce.** È l'unica parte che trasforma un'automazione in qualcosa di cui ci si può fidare. Un log non è una notifica.

## I trigger

| Modo | Quando | Cosa va previsto comunque |
| ---- | ------ | ------------------------- |
| Webhook | l'evento arriva da un sistema che sa chiamarti | il webhook perso: serve una riconciliazione periodica, perché prima o poi uno si perde |
| Polling | il sistema di origine non chiama | ogni quanto, e come si ricorda dove era arrivato (il segnaposto va persistito, non tenuto in memoria) |
| Schedulazione | lavoro periodico, arricchimento, riepiloghi | cosa succede se l'esecuzione precedente non è ancora finita: sovrapposizione o salto, va scelto |

## La trappola specifica

**L'automazione che scrive da sola su sistemi esterni** — manda email, aggiorna un CRM, pubblica, risponde a un cliente — e che nessuno rilegge. Funziona benissimo per settimane, poi cambia qualcosa a monte e continua a funzionare producendo risultati sbagliati, senza errori e senza avvisi.

Le difese, in ordine: una revisione umana sui primi N casi prima di aprire il rubinetto · un campione rivisto periodicamente anche a regime · una soglia di anomalia (se il volume o la distribuzione degli esiti cambia, ci si ferma) · e la conferma umana obbligatoria dove l'effetto è irreversibile o va verso l'esterno.

Che gli strumenti dell'automazione abbiano permessi stretti e che i contenuti recuperati possano contenere istruzioni ostili è materia di **Kai**: nominalo e fermati.

## Forma dell'output

Verdetto in una riga (workflow visuale o codice, e perché), poi l'impianto minimo della coda applicato a questo caso, poi il punto sul «chi se ne accorge». Se l'automazione tocca solo dati interni e a bassa frequenza, molti di questi pezzi non servono: dillo, invece di prescriverli tutti.

## Trappole

- **Chiamare il modello dentro una richiesta HTTP sincrona.**
- **Costruire l'impianto completo per un lavoro che gira una volta al giorno su venti record.**
- **Retry senza idempotenza.** È il modo più efficace per mandare la stessa email tre volte.
- **Affidarsi al log come sistema di allerta.**
- **Dimenticare il costo.** Un'automazione che gira ogni cinque minuti su un modello capace fa un conto che nessuno ha preventivato: vedi *Costi e latenza*.
