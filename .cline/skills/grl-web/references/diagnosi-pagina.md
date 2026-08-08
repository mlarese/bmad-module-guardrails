# Diagnosi di una pagina esistente

La rotta di `grl-web` quando c'è già una pagina — dell'utente o di un concorrente — e la domanda è perché non converte. L'esito è **un verdetto in conversazione**, non un documento e non una riscrittura: l'utente deve sapere cosa cambiare per primo e quanto gli costa.

Serve vedere la pagina davvero: un URL con un browser a disposizione, il file, o uno screenshot. Con il solo markup si lavora comunque, dichiarandolo: stai giudicando il codice, non il risultato.

## Ricostruire il brief all'indietro

La diagnosi utile non è un elenco di difetti: è il confronto fra quello che la pagina *sta* facendo e quello che dovrebbe fare. Quindi si ricostruisce dalla pagina, leggendola come farebbe uno che ci arriva freddo, quello che il brief avrebbe dovuto contenere.

| Campo | Cosa cerchi nella pagina | Il guasto tipico |
| --- | --- | --- |
| Destinatario | a chi è rivolta, deducibile dalle prime due righe | parla a tutti: ogni frase regge anche su un altro sito |
| Promessa | cosa cambia per chi legge, entro la prima schermata | c'è una categoria («la piattaforma per…»), non un cambiamento |
| Obiezione | il dubbio che la pagina affronta per nome | nessuna: la pagina non ammette che qualcuno possa dire di no |
| Prova | numeri, nomi, demo, garanzie — e dove stanno | in fondo, dopo che chi dubitava se n'è già andato |
| Azione | cosa vuole far fare, e quante volte lo chiede | tre azioni pari che si annullano, o nessuna sotto la prima schermata |

I campi che non riesci a ricavare sono già il referto: se dopo aver letto la pagina non sai dire a chi parla, non lo sa nemmeno chi ci arriva.

Poi verifica la sequenza. La promessa deve precedere la prova, la prova precedere l'obiezione, l'obiezione precedere la richiesta. Chiedere l'azione prima di aver smontato l'obiezione è il modo più comune in cui una pagina perde, ed è anche il più facile da correggere: spesso i blocchi ci sono tutti e sono solo nell'ordine sbagliato.

## Il verdetto

Da tre a cinque punti, ordinati per **quanto cambiano il risultato rispetto a quanto costano** — si parte da ciò che si sposta o si riscrive in un pomeriggio, non da ciò che richiede una ridefinizione del prodotto. Ogni punto dice: cosa non funziona, perché conta su *questa* pagina, e la mossa concreta.

Concreto significa la frase riscritta, il blocco spostato, il campo tolto dal form. «Rafforzare la proposta di valore» non è una mossa: è la stessa diagnosi detta due volte.

Apri con ciò che funziona, in una riga. Una pagina in cui è tutto sbagliato non è credibile, e chi la legge smette di ascoltare al secondo punto.

**«Questa pagina va bene» è un esito legittimo**, e si dà con la stessa sicurezza di una stroncatura.

## Confini

Il pezzo visivo — tipografia, palette, densità, omologazione — è di `grl-agent-ui-critic`. Se il problema principale è che la pagina sembra generata, la diagnosi lo nomina in una riga e passa a lei: qui si giudica cosa la pagina *dice* e in che ordine, non come appare.

Se la pagina è di un concorrente, il referto vale come materiale per il brief dell'utente, non come modello da copiare: quello che funziona per il loro destinatario contro la loro obiezione non funziona automaticamente per i suoi.

Se dalla diagnosi l'utente decide di rifare la pagina, si riparte da `references/brief-di-conversione.md` — i campi ricostruiti qui sono una bozza da fargli correggere, mai un brief già valido: sono dedotti da te, non detti da lui.

Questa rotta non scrive niente su disco e non tocca la memoria condivisa.
