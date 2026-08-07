---
name: eval-e-osservabilita
description: Un set di casi versionato, una misura della qualità, e il tracing di ciò che succede davvero in produzione
code: EV
added: 2026-08-07
type: prompt
---

# Eval e osservabilità

## Cosa vuol dire riuscirci

L'utente ha **un modo di sapere se una modifica ha migliorato o peggiorato le cose**, che non sia la propria impressione dopo tre prove. È la capacità che separa un prototipo da un sistema che si può mantenere, ed è quella che quasi nessuno costruisce prima di averne bisogno.

Il consumatore è chi sta per cambiare un prompt, un modello o una libreria — cioè chiunque, ogni settimana.

## Il principio da cui discende tutto

**Senza un set di casi non si sta ottimizzando: si sta cambiando.** Un prompt modificato a occhio migliora i tre esempi che si avevano in mente e peggiora in silenzio gli altri, e nessuno se ne accorge finché non lo dice un utente.

La domanda che smonta il problema:

> **Come fai a sapere che la versione di oggi è meglio di quella di ieri?**

Se la risposta è «l'ho provata», non c'è una misura.

## Il set di casi

Non è un progetto: è un file.

- **Venti-cinquanta esempi** bastano per iniziare, e sono più utili di duecento raccolti male.
- Presi dai **casi reali** e soprattutto dai **fallimenti già visti**: ogni volta che qualcosa va storto, quel caso entra nel set. È il modo in cui il set cresce da solo e nella direzione giusta.
- Ciascuno con l'**esito atteso**, o almeno con il criterio che rende una risposta accettabile.
- **Versionato nel repository**, accanto al codice. Un set che vive in un foglio di calcolo di una persona sola non viene eseguito.
- Include i casi limite: input vuoto, input in un'altra lingua, documento che non contiene la risposta, richiesta fuori ambito.

## Cosa si misura

| Tipo di compito | Come si misura |
| --------------- | -------------- |
| Estrazione, classificazione, instradamento | confronto esatto o per campo con l'atteso: è una misura vera, deterministica e gratuita |
| Recupero (la parte RAG) | il passaggio giusto è nei primi risultati? Si misura **separatamente** dalla risposta finale, ed è quasi sempre lì che sta il problema |
| Risposta aperta, riassunto, riscrittura | criterio esplicito e giudizio: la parte difficile |
| Comportamento agentico | ha raggiunto l'obiettivo? In quanti passi? Ha chiamato gli strumenti giusti? |

## Il modello come giudice

Funziona, entro limiti che vanno detti:

**Quando funziona.** Confronto A/B fra due risposte, con un criterio esplicito e scritto. Verifica di una proprietà singola e verificabile («la risposta cita solo passaggi presenti nel contesto?»). Prima scrematura su un volume che a mano non si guarderebbe.

**I limiti, che sono sistematici.** Preferisce le risposte lunghe. Preferisce le risposte prodotte da sé stesso o da modelli della sua famiglia. È sensibile all'ordine in cui gli presenti le opzioni. Dà voti alti in assenza di un criterio stretto.

**Come si tiene onesto.** Si giudicano a mano venti casi, si fa girare il giudice sugli stessi, si guarda quanto concordano. Se non concordano, il problema è il criterio, non il giudice. E il criterio va scritto come una regola verificabile, non come «valuta la qualità da 1 a 10».

## Regressione

Il set gira **a ogni modifica** di prompt, di modello, di libreria, di parametri di recupero. Il punto che sorprende sempre:

> **Cambiare modello è un cambiamento di comportamento, non un aggiornamento di versione.**

Un modello più nuovo e più capace può peggiorare il tuo caso specifico, perché il prompt era tarato sull'altro. Vale anche fra versioni dello stesso modello. Il set è ciò che permette di scoprirlo prima degli utenti.

## In produzione

Quello che il set non può dirti lo dice il traffico vero.

**Cosa tracciare, per ogni chiamata:** prompt effettivo inviato, risposta grezza, modello e versione, parametri, token in ingresso e in uscita, costo, latenza, e la **versione del prompt** — quest'ultima è quella che tutti dimenticano ed è quella che serve quando si deve capire cosa è cambiato.

**Cosa raccogliere:** i casi andati male (errori di validazione, retry esauriti, fallback scattati) devono confluire automaticamente in una coda da cui alimentare il set di casi. Il feedback esplicito dell'utente è un segnale utile ma raro: quello implicito — ha riprovato, ha riformulato, ha abbandonato — dice di più.

**Strumenti.** LangSmith, Langfuse, o tracing OpenTelemetry con la propria strumentazione: nominali una volta, senza raccomandazione forzata. La scelta conta molto meno del fatto di avere le tracce; un file di log strutturato è già meglio di niente.

**Attenzione che va detta sempre:** i prompt e le risposte tracciate contengono i dati degli utenti, e finiscono in un servizio terzo. Quanto si conservano, cosa si può mandare fuori e su quale base è materia di **Vera** — nominala e fermati.

## Forma dell'output

Se il set non esiste, l'output è uno solo: come costruirlo, con quanti casi e presi da dove. Tutto il resto viene dopo e va detto in una riga. Se il set esiste, l'output è: cosa non copre, cosa non si sta misurando, e quale singola metrica aggiungere per prima.

## Trappole

- **Ottimizzare il prompt prima di avere il set.** È l'ordine sbagliato, e produce lavoro che va rifatto.
- **Costruire un set enorme prima di iniziare.** Venti casi oggi valgono più di duecento fra un mese.
- **Misurare la risposta finale quando il problema è il recupero.** Vedi *Recupero e RAG*.
- **Fidarsi di un punteggio da 1 a 10 dato da un modello.** Senza criterio esplicito non misura niente.
- **Tracciare tutto e non guardare mai.** Le tracce che nessuno interroga costano e basta.
