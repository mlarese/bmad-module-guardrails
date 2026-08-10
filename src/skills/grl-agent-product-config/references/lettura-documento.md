# Leggere un documento e ricavarne una configurazione

Il documento è una richiesta d'offerta, un capitolato, una email, una specifica tecnica, a volte tutte insieme in allegato. È scritto da chi compra, non da chi produce: usa parole che non stanno nel catalogo, salta ciò che dà per scontato e a volte descrive il problema invece del prodotto.

## Ordine di lavoro

### 1. Identifica la linea di prodotto

Prima di leggere i requisiti, stabilisci quale catalogo si applica. Se il documento copre due linee, sono due configurazioni, non una con opzioni miste. Se non si capisce quale linea sia, è la prima domanda da fare, non un'ipotesi da tenere in piedi per tutto il lavoro.

Se il catalogo di quella linea non esiste, dillo subito e passa a `references/bootstrap-catalogo.md`.

### 2. Estrai i requisiti espliciti

Ogni requisito porta la citazione: pagina e riga, o il testo esatto se il documento non è paginato. La citazione serve al venditore quando il cliente contesta, e a te quando il documento viene sostituito da una revisione.

Fai attenzione a dove i requisiti si nascondono:

- tabelle e allegati, spesso più precisi del corpo del testo;
- disegni e quote, che possono contraddire il testo — se lo fanno, è un conflitto da segnalare, non da risolvere scegliendo;
- riferimenti a ordini precedenti («come la fornitura di marzo»), che sono requisiti a tutti gli effetti ma vanno recuperati;
- norme e certificazioni citate, che spesso impongono opzioni.

### 3. Traduci in scelte sul catalogo

Il linguaggio del cliente non coincide con i codici del catalogo. «Rinforzato», «versione pesante», «tipo quello di prima» vanno tradotti, e la traduzione è una decisione da mostrare, non un passaggio invisibile:

> `serie: s82` — il documento dice «profilo maggiorato» (p. 2 r. 14); nel catalogo la sola serie maggiorata è la 82.

Quando una parola del cliente ammette due traduzioni, non sceglierne una: diventa una domanda.

### 4. Marca i requisiti impliciti come tali

Norme citate, tolleranze di settore, prassi consolidate: possono essere vincolanti quanto il testo, ma nessuna di esse è scritta. Trattale come assunzioni dichiarate (`origin: assumed`), mai come requisiti espliciti. La differenza conta il giorno in cui il cliente dice che non l'aveva chiesto.

### 5. Applica il catalogo e lascia parlare le regole

Le opzioni imposte da un `requires` entrano in configurazione con `origin: imposed` e la regola citata. Non chiederle al cliente: il catalogo le ha già decise, e chiederle fa sembrare aperto ciò che non lo è.

Un `excludes` violato dal documento è la scoperta più importante di tutta la lettura: il cliente ha chiesto una combinazione che non esiste. Non riscriverla per farla stare in piedi. Presenta il conflitto, la ragione dal `because`, e le alternative che il catalogo permette.

### 6. Separa ciò che blocca da ciò che resta aperto

Le opzioni obbligatorie e quelle imposte da una regola, se non risolte, diventano `missing` e rendono la configurazione `incomplete`. Le facoltative non decise diventano `open_choices`: restano visibili, con il loro `impact`, ma non bloccano l'ordine e non cambiano l'esito. Le due liste non si mescolano — un colore ancora da scegliere non è un ostacolo, e presentarlo come tale fa sembrare ferma una richiesta che si può già evadere.

Entrambe le liste si ordinano per `impact`: prima ciò che blocca, poi ciò che cambia il prezzo, per ultimo l'estetico.

Ogni voce di entrambe porta la domanda già formulata, pronta da inoltrare al cliente senza riscritture. Non una richiesta di dati: una domanda a cui si risponde in una riga.

> Colore interno: bianco, noce, o RAL a campione? Con RAL serve anche il codice.

### 7. Valida

Esegui `uv run scripts/config_validator.py config <path>` prima di presentare qualsiasi esito. L'output dello script è la fonte del verdetto: `valid`, `incomplete` o `invalid`.

Se lo script non è eseguibile, applica le stesse verifiche a mano nello stesso ordine — dominio, obbligatorietà, `required_if`, `requires`, `excludes`, copertura di `evidence` — e dichiara che la validazione è manuale.

L'esito si scrive con la stessa parola in entrambi i casi, e ogni violazione porta il suo codice: `serie=s82` con `rinforzo=false` è `invalid` per `requires-violated`, non «c'è un conflitto». Se hai potuto controllare solo una parte, dillo — ma il verdetto resta `valid`, `incomplete` o `invalid`, perché è quello che finisce nei due output di consegna.

## Le tre cose da non fare

- **Non riempire i vuoti.** Un'opzione non citata resta `missing`. Se serve un valore per procedere, diventa un'assunzione dichiarata, visibile anche nell'output al cliente.
- **Non inventare compatibilità.** Se il catalogo tace su una combinazione, la risposta è «il catalogo non copre questo caso», e diventa un lavoro per `references/bootstrap-catalogo.md`.
- **Non risolvere le contraddizioni del documento.** Testo contro disegno, allegato contro corpo, revisione contro originale: si segnalano entrambi, con le due citazioni.

## Documento sostituito o revisionato

Quando arriva una revisione del documento, non ripartire da zero: confronta e mostra cosa cambia in configurazione. Le tre righe che servono sono quali selezioni cambiano, quali assunzioni decadono e quali domande aperte trovano risposta.
