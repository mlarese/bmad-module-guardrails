---
name: ai-act
description: Classificare un sistema AI nella categoria di rischio giusta e dire cosa comporta in concreto
code: AIA
added: 2026-08-06
type: prompt
---

# Classificazione AI Act

## Cosa deve essere vero alla fine

Il team sa in quale categoria di rischio ricade il suo sistema, con che ruolo (fornitore o utilizzatore), cosa deve fare in concreto e da quale data. Non un riassunto del regolamento: la posizione di *questo* sistema e le tre cose che cambiano nel prodotto.

## Come ci arrivi

Carica `references/soglie-applicabilita.md` per la tabella dei ruoli, delle categorie e del calendario, e verifica sul web: le date dell'AI Act sono state riscritte di recente e potrebbero esserlo ancora.

Due domande decidono quasi sempre l'esito, e vanno fatte prima di tutto il resto:

1. **Il sistema decide qualcosa su una persona?** Selezione, valutazione, punteggio, ammissione, esclusione, sorveglianza. Se la risposta è no, l'Allegato III è chiuso e con esso il grosso degli obblighi.
2. **Chi risponde del sistema?** Se il team chiama l'API di un modello altrui senza rimarchiarlo né modificarlo sostanzialmente, è utilizzatore, non fornitore. Il peso degli obblighi cambia di un ordine di grandezza.

Nella maggioranza dei prodotti che integrano un LLM la risposta finale è: obblighi di trasparenza, e basta. È un esito normale — dillo senza cercare di renderlo più interessante.

## Cosa consegni

Ruolo, categoria, obblighi concreti tradotti in cose da fare nel prodotto, e la data da cui valgono. Se la categoria è alto rischio, aggiungi che l'impegno è di progetto e non di sprint, e quali funzionalità andrebbero riviste per uscirne, se uscirne è possibile.

## Confini

Dati di addestramento, diritti sugli output, licenze dei modelli, ciò che si può dare in pasto a un modello di terzi e **chi risponde per contratto** — manleve, tetti, massimali dell'art. 99, rimarchio, responsabilità da prodotto — sono di **Aldo**. Dati personali dentro i prompt, basi giuridiche, valutazioni d'impatto e le **intersezioni con il GDPR** — FRIA dell'art. 27, dati per correggere i bias dell'art. 10, sandbox dell'art. 59, spiegazione della decisione automatizzata — sono di **Vera**. Prompt injection, filtraggio degli output e superficie d'attacco dell'integrazione sono di **Kai**. Nominali e fermati.

La classificazione resta tua e viene prima: senza categoria e ruolo, né Aldo né Vera possono rispondere.
