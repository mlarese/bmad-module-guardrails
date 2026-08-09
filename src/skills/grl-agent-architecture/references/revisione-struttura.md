---
name: revisione-struttura
description: Leggere una struttura esistente o ereditata e restituire i 3-5 punti di attrito ordinati per costo futuro
code: RS
---

# Revisione di una struttura esistente

## Com'è fatto un buon esito

**Tre-cinque punti**, ordinati per **costo futuro** — non per bruttezza. Più ciò che va bene e non va toccato: è informazione utile quanto il resto, e su un progetto ereditato è la parte che rassicura chi deve lavorarci.

## Come si ordina

Costo futuro ≈ **quanto spesso si tocca × quanto fa male toccarlo × quante persone lo toccano**.

Conseguenza diretta: **il codice brutto che nessuno tocca non entra in classifica.** Se sta fermo da un anno, sta bene dov'è.

## Da dove guardare, con evidenze e non a occhio

- **File più toccati**, che è il moltiplicatore più importante:
  `git log --format= --name-only | sort | uniq -c | sort -rn | head -20`
- **File più lunghi** e cartelle catch-all (`utils/`, `common/`, `helpers/`).
- **Cicli di import** e moduli importati da tutti.
- **Punti in cui la stessa regola è scritta più volte** (prezzi, permessi, date, stati).
- Se c'è, la cronologia dei bug: dove tornano, lì la struttura sta mentendo.

L'incrocio che conta è: file molto toccato **e** difficile da toccare. Quello è il primo punto della lista.

## Cosa consegni, per ciascun punto

> **Dove** (percorso) · cosa succede quando ci si lavora · **costo se resta** · intervento minimo · cosa non toccare

L'intervento minimo è l'unica forma ammessa: spostare, rinominare, estrarre una funzione, invertire una dipendenza. Se l'unico rimedio che vedi è una riscrittura, dillo esplicitamente come tale e lascia la decisione all'utente — non presentarla come manutenzione.

## Cosa non consegni mai

- Il piano di riscrittura completo, non richiesto.
- Un elenco di dieci punti: viene ignorato per intero.
- Il giudizio su chi ha scritto il codice. La struttura ereditata è un dato, non una colpa.
- Il modernizzare per modernizzare (cambiare stile, framework o convenzioni senza un costo attuale da eliminare).

## Prima di chiudere

Se durante la revisione emerge una decisione strutturale presa insieme all'utente, scrivila in `{project-root}/_bmad/memory/grl-shared/decisions.md`. Se emerge un problema che l'utente sceglie consapevolmente di tenersi, va in `accepted-risks.md` **solo se lo conferma esplicitamente**: da quel momento non lo segnali più.

Per ogni candidato al refactoring chiediti anche:

- l'interfaccia nasconde una decisione o solo un passaggio di dati?
- il modulo è abbastanza profondo da pagare il proprio costo cognitivo?
- esiste un seam pubblico e un test comportamentale che dimostri il valore del confine?
- l'adapter è un seam reale richiesto da due implementazioni o è una previsione?

Se la risposta è negativa, la mossa minima può essere cancellare l'indirezione, non aggiungere un
altro strato.
