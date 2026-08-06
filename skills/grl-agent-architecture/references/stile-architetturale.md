---
name: stile-architetturale
description: Scegliere fra struttura piatta, strati, vertical slice, esagonale o monolite modulare — con il costo di adottare e il costo di non adottare
code: SA
---

# Scelta dello stile architetturale

## Com'è fatto un buon esito

Una raccomandazione sola, motivata, con **il costo di adottarla**, **il costo di non adottarla** e **il segnale** che dirà quando cambiare idea.

**«Nessuno stile particolare: tieni la struttura piatta» è un esito legittimo e frequente.** Va detto con la stessa sicurezza di una raccomandazione forte, non come ripiego.

## Cosa devi sapere prima di rispondere

Cinque dati, e si chiedono se non ci sono:

- quanto codice c'è oggi (ordine di grandezza dei file, non il numero esatto);
- quante persone ci lavorano, ora e fra un anno;
- quanti domini davvero distinti ci sono (non quante entità: quante aree che cambiano per motivi diversi);
- quanto spesso l'infrastruttura è realmente sostituita o simulata;
- quanto deve durare il progetto.

Senza questi, qualunque stile raccomandato è una preferenza personale travestita da consiglio.

## Le opzioni, con il loro conto

| Stile | Conviene quando | Costo di adottarlo | Come degrada |
| ----- | --------------- | ------------------ | ------------ |
| **Struttura piatta** (file per funzione, nessuna gerarchia) | poche decine di file, una o due persone, un dominio solo, durata incerta | nessuno | quando due domini iniziano a pestarsi nello stesso file, o entra la terza persona |
| **Strati** (controller / service / repository) | gli strati hanno regole davvero diverse e team diversi li toccano | ogni feature attraversa tutti gli strati | degenera in pass-through: strati che inoltrano e basta, e una modifica costa cinque file |
| **Vertical slice** (una cartella per feature) | le feature sono indipendenti e più persone lavorano in parallelo | duplicazione voluta fra slice — va accettata esplicitamente, altrimenti qualcuno la «rifattorizza» e ricrea l'accoppiamento | quando le slice iniziano a importarsi a vicenda |
| **Esagonale** (porte e adattatori) | l'infrastruttura è **davvero** sostituita o simulata: più adattatori reali, test pesanti, dominio con regole complesse | due traduzioni per ogni chiamata, più tipi da mantenere | con un solo adattatore per porta e nessuna intenzione di sostituirlo: **qui non serve** |
| **Monolite modulare** | i domini sono realmente separati ma il rilascio resta uno | disciplina sui confini, che nessuno strumento impone al posto tuo | quando i moduli condividono le tabelle: allora i confini non esistono |

## Due regole che valgono più della tabella

- **Non raccomandare due stili insieme «in transizione»** senza una data e un punto di arrivo. Metà codice in un modo e metà nell'altro è il caso peggiore di entrambi.
- **Lo stile non si sceglie per il progetto che immagini fra due anni**, ma per quello che hai davanti oggi, più il segnale che dirà quando cambiare. Se il progetto cresce, si cambia — e il cambio costa meno della struttura sbagliata tenuta per due anni.

## Formato della risposta

Quattro righe, non una relazione:

1. **Raccomandazione** — in una riga, con il perché legato a uno dei cinque dati.
2. **Costo di adottarla.**
3. **Costo di non adottarla.**
4. **Segnale di revisione** — l'evento concreto che imporrà di riaprire la scelta.

Se Winston (architetto di sistema, BMM) ha già scelto uno stile, non lo scavalchi: dici su quale asse quella scelta costa più di quanto rende, con lo stesso formato.
