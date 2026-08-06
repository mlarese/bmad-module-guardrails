---
name: dipendenze
description: Quali vulnerabilità delle dipendenze contano davvero in questo progetto, e cosa aggiornare per prime
code: DEP
added: 2026-08-06
type: prompt
---

# Dipendenze e CVE

## Cosa vuol dire riuscirci

L'utente sa **quali** delle vulnerabilità segnalate lo riguardano davvero e in che ordine aggiornare. Un output che ricopia l'elenco dello scanner non serve a niente: quello lo produce già lo scanner.

Il consumatore è chi deve decidere se fermare il rilascio o no.

## Come si guarda

Usa lo strumento se c'è, in base al gestore di pacchetti del progetto:

| Ecosistema | Comando |
| ---------- | ------- |
| npm / pnpm / yarn | `npm audit --json` · `pnpm audit --json` · `yarn npm audit` |
| qualsiasi (se installato) | `osv-scanner scan source -r .` |
| Python | `pip-audit` · `uv pip audit` |
| Rust | `cargo audit` |
| Go | `govulncheck ./...` |

Se nessuno è disponibile, **non chiederne l'installazione**: leggi il file di lock, individua le librerie note per aver avuto problemi seri nella fascia di versione presente, e dichiara che stai lavorando sulle versioni dichiarate senza scanner. Verifica sul web le CVE recenti e la versione in cui sono state corrette — la memoria del modello su questo invecchia in mesi.

## Il filtro che fa il lavoro

Tre domande, applicate a ogni segnalazione:

1. **È raggiungibile dal codice del progetto?** Una dipendenza che gira solo in build o solo nei test non ha lo stesso peso di una nel percorso di una richiesta HTTP. Cerca dove la libreria è effettivamente importata.
2. **Il vettore esiste qui?** Una vulnerabilità che si attiva solo processando input non fidato conta se l'input arriva dall'esterno, non se il file lo genera il progetto stesso.
3. **È transitiva e la correzione dipende da altri?** Se il fix richiede un aggiornamento maggiore del pacchetto padre, il costo cambia e va detto.

Il punteggio CVSS **non** è l'ordine. Una CVE 9.8 in un pacchetto non raggiungibile viene dopo una 6.5 nel parser degli upload.

## Forma dell'output

Poche righe, ordinate:

- **Da aggiornare adesso** — pacchetto, versione attuale → versione corretta, perché conta *qui*.
- **Può aspettare** — con il motivo in mezza riga (non raggiungibile, vettore assente, dev-only).
- Se l'aggiornamento è rischioso (breaking change, pacchetto padre bloccato), dillo e proponi l'alternativa: pin, patch, sostituzione, o accettazione consapevole del rischio.

Se non c'è niente di urgente, la risposta è una riga: «niente di raggiungibile, il resto lo prendi al prossimo giro di aggiornamenti».

## Trappole

- **Elencare tutto.** È il modo più veloce per far ignorare il prossimo avviso.
- **Le licenze.** Anche se stanno nello stesso `package.json`, sono di Aldo. Se ne vedi una problematica, nominalo in una riga e vai avanti.
- **Suggerire `npm audit fix --force`** senza dire che aggiorna a versioni maggiori e può rompere il build.
