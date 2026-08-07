# Il brief di conversione

Il lavoro vero di `grl-web`, e l'unica cosa che nessun modello può inventare al posto dell'utente. Precede l'HTML sempre.

Si riempie **con le parole dell'utente**: un brief che non riconosce come suo è un brief inventato.

## Apri il campo prima di qualsiasi domanda

Invitalo a versare tutto quello che ha — prodotto, chi compra, cosa gli dicono i clienti, le obiezioni che si sente ripetere, pagine e materiali che esistono già, link, percorsi di file. Adatta l'invito a come è arrivato: a una richiesta vaga «raccontami tutto», a un URL o a un percorso «cosa vuoi che guardi qui dentro».

Quel versamento sostituisce quasi tutte le domande che verrebbero dopo. Poi chiedi solo i campi rimasti scoperti, pochi alla volta — mai un questionario campo per campo su cose che l'utente aveva già in mano.

## I cinque campi

| Campo | La domanda | Senza, esce |
| --- | --- | --- |
| Destinatario | Chi arriva su questa pagina, da dove, e cosa sa già del problema | copy che parla a tutti e non convince nessuno |
| Promessa | Cosa cambia per lui, in una riga, senza aggettivi | «la piattaforma all-in-one per il tuo business» |
| Obiezione | Il motivo per cui **non** compra, detto con parole sue | un elenco di funzionalità che nessuno ha chiesto |
| Prova | Cosa smonta quell'obiezione: numeri, nomi, una demo, una garanzia | una promessa che resta un'affermazione |
| Azione | L'unica cosa da fare, e dove arriva concretamente il contatto | tre call-to-action che si annullano a vicenda |

Il tuo valore è l'attrito: la promessa che è un aggettivo travestito, l'obiezione vera che l'utente sta evitando, la prova che non esiste ancora, la seconda CTA che ha appena aggiunto. Una pagina che trascrive la prima idea è un fallimento anche se è bella.

Quando l'attrito produce qualcosa — un campo riformulato, una CTA tolta, una prova che si è rivelata inesistente — la versione scartata va nella sezione **Scartato** del brief con il suo perché. È ciò che impedisce che fra sei mesi la stessa idea torni e venga riargomentata da capo.

## Dove vive

In `{workflow.output_path}/{workflow.run_folder_pattern}/brief.md`, seguendo la struttura di `{workflow.brief_template}`; in un sito, `brief-sito.md` alla radice della cartella di lavoro e `brief.md` dentro la cartella di ciascuna pagina. Si scrive appena i primi campi reggono, non alla fine.

Da lì in poi **è lui lo stato del lavoro**: tiene i campi, il percorso della pagina, lo stato del gate dei revisori e ciò che è stato scartato. Rientrando in una sessione qualsiasi si riparte leggendolo, ed è il motivo per cui va aggiornato insieme alla pagina a ogni modifica: un brief che non descrive più la pagina rende inutile il rientro.

Il brief è scritto in `{document_output_language}`. La **pagina** invece segue la lingua del destinatario dichiarato nel brief, che spesso non è quella della conversazione — un utente italiano che vende a un mercato internazionale scrive la landing in inglese.

## Prima di passare alla pagina

Prima dell'HTML chiedi se manca altro: tornare sul destinatario o sull'obiezione a pagina già scritta costa una riscrittura. Poi `references/mockup-html.md`, che apre con la direzione visiva.
