---
name: over-engineering
description: Trovare gli strati che non pagano il proprio costo, dire cosa si guadagna a toglierli, e riconoscere il caso opposto
code: OE
---

# Caccia all'over-engineering

## Com'è fatto un buon esito

L'utente ha un elenco corto di **astrazioni da rimuovere**, ciascuna con **cosa si guadagna** a toglierla. Non «il codice è più pulito»: file in meno da aprire, salti in meno per capire dove succede una cosa, un posto solo da cambiare.

Uno strato si paga sempre. La domanda non è «è elegante?» ma **«quale problema vero ti obbliga ad averlo?»**.

## Repertorio delle astrazioni sospette

Ognuna è sospetta, non colpevole: la colonna di destra è la domanda che la smonta o la salva.

| Astrazione | La domanda che la smonta |
| ---------- | ------------------------ |
| Interfaccia con una sola implementazione | chi è la seconda implementazione? Se la risposta è «i test», serve davvero un test che la sostituisca, o basta un test un livello più in alto? |
| Repository sopra un ORM | l'ORM è già un repository. Cosa aggiunge il tuo strato che lui non fa? |
| Service layer che inoltra e basta | quale metodo di questo servizio fa qualcosa oltre a chiamare il livello sotto? |
| Factory che chiama solo il costruttore | quale scelta fa la factory che il chiamante non può fare? |
| DTO che ricopiano l'entity campo per campo | quale campo è diverso? Se sono identici, la traduzione è solo lavoro |
| Wrapper del framework «per poterlo cambiare» | quante volte hai cambiato framework? E il wrapper nasconde davvero il framework, o ne fa trapelare i tipi? |
| Evento o coda per una chiamata sincrona nello stesso processo | chi altro ascolta l'evento? Se nessuno, è una chiamata di funzione con due file in più e uno stack trace in meno |
| Configurazione per valori mai cambiati | quante volte quel valore è cambiato? Chi lo cambierebbe senza toccare il codice? |
| Generico o parametro di tipo con un solo tipo istanziato | qual è il secondo tipo? |
| Sistema a plugin senza plugin | chi scriverà il primo plugin, e quando? |
| Servizi separati con un solo team, un solo deploy e un solo database | cosa si distribuisce separatamente? Se niente, sono moduli con la latenza di rete in regalo |
| Classe base per condividere quattro righe | le quattro righe cambiano insieme, o si somigliano soltanto? |
| Astrazione introdotta «per i test» | il test che la richiede esiste? Se no, sta pagando un costo per un test immaginario |

## Prima di dire «togli»

Chiedi se c'è una ragione che non vedi: un test che la sfrutta, un vincolo di team, una storia («l'abbiamo messa perché il cliente cambiò database due anni fa»). Se la ragione c'è ed è buona, la partita è chiusa: registra l'eccezione in `{project-root}/_bmad/memory/grl-agent-architecture/notes.md` come **eccezione concordata**, così non la ridiscuti alla prossima sessione.

Si toglie **uno strato alla volta**. Un piano che elimina quattro astrazioni insieme non viene eseguito da nessuno.

## Il caso opposto vale allo stesso modo

Manca un confine dove servirebbe. Segnali:

- una funzione lunghissima che tutti toccano e nessuno legge per intero;
- regole di business dentro un controller, un handler HTTP o un componente di UI;
- query SQL o chiamate al database sparse nei punti di presentazione;
- lo stesso calcolo (prezzi, permessi, date) rifatto in tre posti con tre risultati leggermente diversi.

Il metro è identico: chi paga, quando, quanto — e il rimedio minimo, non la riscrittura.

## Cosa non consegni

- Il piano di riscrittura completo.
- Il giudizio sul lavoro di chi c'era prima.
- L'osservazione su codice che nessuno tocca da mesi: brutto e fermo non costa niente.
