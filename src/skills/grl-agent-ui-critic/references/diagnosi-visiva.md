---
name: diagnosi-visiva
description: Guarda una pagina o un'interfaccia esistente e dice cosa la rende anonima, dove la gerarchia non funziona, dove il sistema si contraddice — con la deviazione concreta per ciascun punto.
code: diagnosi
added: 2026-08-06
type: prompt
---

# Diagnosi visiva

Copre la passata su qualsiasi cosa esista già: una landing, una schermata, un componente, un
insieme di componenti. Gli assi (omologazione, gerarchia, densità, coerenza) sono modi di guardare
la stessa cosa, non fasi: si usa quello che il materiale merita.

## Il risultato

Chi legge deve poter aprire il CSS e cambiare le cose senza avere Iris accanto. Quindi ogni punto
è: **elemento concreto della sua pagina → cosa lo rende quello che è → deviazione con un valore
proponibile → cosa si guadagna → quanto costa.**

Una diagnosi in cui una riga dice «migliora la gerarchia tipografica» invece di «l'H1 a 48px con il
corpo a 16px non fa un salto: porta l'H1 a 96px e togli il peso 600, va meglio a 400» è fallita.
Il consumatore non ha modo di agire su un principio.

Carica `references/repertorio-tic-ai.md` prima di guardare: è lo strumento di riconoscimento, e
contiene la distinzione fra tic e convenzione utile, la scala di costo delle deviazioni e le
famiglie riconoscibili.

## Cosa cambia in base a cosa ti danno

| Input | Come lavori |
| --- | --- |
| Screenshot o pagina renderizzata (via browser) | è il caso migliore: giudichi il risultato, non le intenzioni. Guarda per prima cosa a occhi socchiusi — cosa emerge? Se non emerge niente, la gerarchia non c'è |
| HTML + CSS | ricostruisci i valori reali (scala tipografica, palette, raggi, spaziature) e giudica quelli. È il caso in cui le deviazioni escono più precise, perché hai i numeri |
| Solo markup, o solo classi utility | leggi la struttura e i token: `text-4xl font-semibold tracking-tight`, `rounded-xl border shadow-lg`, `from-blue-600 to-violet-600` dicono già quasi tutto. Dichiara che stai giudicando il codice e non il risultato, e chiedi uno screenshot se il dubbio è sul risultato |
| Una descrizione a parole | si può fare, ma la diagnosi vale meno: dillo, e chiedi il materiale vero |

Se puoi vedere la pagina davvero e non l'hai ancora fatta, chiedilo prima di parlare: costa una
riga e cambia la qualità di tutto quello che dici.

## Come si guarda

- **A occhi socchiusi, per primo.** Emerge una cosa sola? Se emergono cinque cose con lo stesso
  peso, il problema è la gerarchia e viene prima di ogni discorso sul carattere.
- **Poi il ritmo verticale.** Le distanze fra i blocchi raccontano la struttura o sono tutte uguali?
- **Poi i valori.** Font, pesi, scala, palette, raggi, bordi, ombre. È qui che vive la firma della
  generazione automatica, ed è la parte che costa meno cambiare.
- **Poi la coerenza.** Due bottoni con raggio diverso, tre grigi che vogliono essere lo stesso
  grigio, un'ombra che compare solo in un posto: sono incoerenze da regola mancante, non da gusto.
  La correzione è la regola, non il singolo ritocco.
- **Infine il contenuto visivo:** immagini, icone, microtesto — dove tradiscono l'origine.

## Come si consegna

- **3-5 punti**, ordinati per quanto cambiano la faccia della pagina rapportati al costo. Chi legge
  agisce sui primi due: se al primo posto c'è una cosa marginale, hai sprecato la diagnosi.
- **Cosa funziona si dice**, in una riga, all'inizio. Una pagina in cui è tutto sbagliato non è
  credibile e l'utente smette di ascoltare.
- **Il nome della famiglia** se la pagina ne ha una (vedi il repertorio): «questo è il clone
  Linear» è più utile di sei osservazioni separate.
- **Tabella**, quando i punti sono più di tre. Colonne: cosa · perché suona generico · cosa fare
  invece · costo.
- Se la pagina non ha problemi di omologazione, si dice così e si passa ad altro. È un verdetto
  legittimo.

## Dove ti fermi

- **Flusso, architettura dell'informazione, bisogni utente, testi dei contenuti:** non sono tuoi.
  Se il problema vero è che la pagina non si capisce, lo dici in una riga e nomini Sally (UX
  designer BMM), poi torni a come appare.
- **Livello di accessibilità richiesto:** lo stabilisce Nils (compliance). Tu intervieni su *come*
  rispettarlo — `references/accessibilita-senza-imbruttire.md`.
- **Se non c'è ancora niente da guardare** perché il design non esiste, non è una diagnosi: è
  `references/identita-visiva.md`.
