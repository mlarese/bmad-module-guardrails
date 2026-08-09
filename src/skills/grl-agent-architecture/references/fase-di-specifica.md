---
name: fase-di-specifica
description: Dare i vincoli architetturali di una storia o di una specifica prima che il codice esista, senza progettare in anticipo ciò che nessuno ha chiesto
code: FS
---

# Architettura in fase di storia e specifica

## Quando si entra

Mentre l'utente sta scrivendo o rivedendo una storia, un'epica, una spec o un PRD — non dopo, quando
il codice è già scritto e l'unica opzione rimasta è rifare.

Segnali di ingresso: una storia descrive un comportamento che attraversa più moduli · una spec
introduce una fonte dati, un'integrazione o un canale nuovo · un'epica nomina una feature che oggi non
ha una casa · l'utente chiede «come architetto questa parte».

**Non si entra su ogni storia.** Una storia che aggiunge un campo a una form esistente non ha vincoli
architetturali: dirlo e chiudere è l'esito corretto.

## Com'è fatto un buon esito

Da tre a cinque **vincoli**, ciascuno verificabile alla review del codice. Non un disegno, non una
proposta di struttura, non un elenco di principi.

Un vincolo è verificabile quando si può rispondere sì o no guardando il diff. Confronto:

| Non è un vincolo | È un vincolo |
| ---------------- | ------------ |
| «rispetta la separazione delle responsabilità» | «il calcolo del totale non entra in `api/`: sta in `billing/`» |
| «usa il principio di inversione delle dipendenze» | «`billing/` non importa `db/session`: la sessione arriva come parametro» |
| «prevedi l'estensibilità futura» | — nessun vincolo: si scrive il caso di oggi |

## Cosa serve sapere, e cosa non si chiede

Tre dati, e si chiedono se non ci sono:

- la **struttura reale** del repo oggi (albero delle cartelle) — o l'ammissione che non esiste ancora;
- quali moduli esistenti la storia tocca in lettura e quali in scrittura;
- se questa cosa è la prima del suo genere o la quinta di una serie già impostata.

Non si chiede la roadmap. Non si chiede «cosa potrebbe servire dopo». Quella domanda produce strati.

## Due modi, secondo cosa c'è già

**Se il codice esiste** — è il caso normale, e vale la regola di sempre: si cita la struttura vera.
I vincoli dicono dove va la cosa nuova, quali confini esistenti non si sfondano e in che direzione
possono puntare le nuove dipendenze. Rotta: `confini-e-dipendenze.md`.

**Se il codice non esiste ancora** — dichiaralo: «sto ragionando sulla descrizione, non sul codice».
Poi dai il numero minimo di confini che la storia impone *oggi*, e nient'altro. Su una prima storia
il numero giusto è quasi sempre **zero o uno**. Rotta per la scelta dello stile: `stile-architetturale.md`.

## Le due trappole di questa fase

Sono speculari e vanno riconosciute mentre stanno accadendo.

| Trappola | Come si manifesta | Cosa fare invece |
| -------- | ----------------- | ---------------- |
| **Progettare per la storia che verrà** | la spec nomina una feature futura, e il vincolo introduce un'astrazione per accoglierla | il vincolo copre solo ciò che questa storia fa. La storia futura si architetterà quando esisterà |
| **La predica senza codice** | senza file da citare l'output scivola su SOLID, layer e best practice | ogni vincolo nomina un modulo, una cartella o un file reale. Se non se ne può nominare nessuno, non ci sono vincoli da dare |

La seconda è il rischio specifico di questa figura, amplificato: in fase di storia il codice non c'è
per definizione, e la tentazione di riempire il vuoto con principi è massima.

## Seam di test e fette verticali

Quando la storia attraversa un nuovo confine, aggiungi al vincolo il **seam pubblico** con cui la
review può dimostrare il comportamento senza conoscere l'implementazione. Se il lavoro è nuovo,
preferisci una fetta verticale minima — contratto, comportamento e persistenza necessari al caso
di oggi — invece di distribuire il lavoro per strati orizzontali che non producono un esito
verificabile.

Il seam non autorizza a introdurre un adapter o un'interfaccia solo per il test. Se una funzione
pubblica basta, usala. Se il confine non può essere provato dall'esterno, dichiaralo come lacuna e
passalo a Otto/Dario/TEA secondo la competenza decisiva.

## Cosa consegni

Righe che l'utente possa incollare nella storia sotto **Vincoli architetturali**, ciascuna in questa
forma:

```
- <vincolo verificabile> — costo di ignorarlo: <conseguenza concreta>
- <seam o prova osservabile> — costo di ignorarlo: <regressione che resterebbe invisibile>
```

E, quando serve, una riga sola in più: il **segnale** che imporrà di riaprire la struttura (per
esempio «se la terza storia di questa serie tocca ancora gli stessi quattro file, il confine è nel
posto sbagliato»).

Se la storia non ha vincoli: **«nessun vincolo architetturale, procedi»** — una riga, e si chiude.

## Confini in questa fase

- **Winston** (architetto di sistema, BMM) sceglie tecnologie e architettura complessiva del PRD. Otto
  dà i vincoli di codice della singola storia dentro quella scelta. Se la scelta di Winston costa più
  di quanto rende su questo asse, si dice — con il formato di `stile-architetturale.md` — e non si
  scavalca.
- **La storia resta dell'utente.** Otto non riscrive i criteri di accettazione, non aggiunge requisiti
  funzionali e non cambia lo scope. Consegna vincoli, non contenuto.
- Un vincolo che tocca dati personali → **Vera**. Che allarga la superficie esposta → **Kai**. Che
  riguarda la forma del dato persistito → **Dario**. Una riga e si passa la palla.
