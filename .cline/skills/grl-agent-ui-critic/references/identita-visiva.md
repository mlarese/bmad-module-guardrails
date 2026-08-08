---
name: identita-visiva
description: Propone 2-3 direzioni visive concrete e diverse fra loro quando il progetto non ha ancora un carattere proprio, ciascuna con valori usabili subito.
code: identita
added: 2026-08-06
type: prompt
---

# Identità visiva

Serve quando non c'è ancora niente da criticare: il progetto parte, o riparte, e la strada di
default porta dritta al template. Qui non si diagnostica, si propone.

## Il risultato

**2-3 direzioni, ciascuna con dei valori che si possono incollare in un file di tema oggi**, e
ciascuna genuinamente diversa dalle altre. L'utente ne sceglie una, o prende un pezzo dell'una e
uno dell'altra: entrambe le cose vanno bene, purché abbia qualcosa da scegliere.

Una direzione è fatta di:

| Elemento | Cosa deve contenere |
| --- | --- |
| Nome | due o tre parole che la rendano citabile poi («editoriale severa», «terminale caldo») |
| Tesi | una riga: cosa dice questa direzione sul prodotto e perché regge per *questo* prodotto |
| Tipografia | famiglie reali con nome, pesi, scala con le dimensioni, dove reperirle e a che condizioni |
| Colore | valori esadecimali: fondo, testo, neutri con la loro tinta, l'accento e a cosa è riservato |
| Forma e densità | raggio, bordi, ombre sì/no, ritmo verticale, misura del testo |
| Immagini | il trattamento (fotografia, diagrammi, nessuna immagine, e come sono trattate) |
| La firma | **il dettaglio ricorrente che rende la pagina riconoscibile**: è la parte che manca a ogni pagina generata, e senza di essa una direzione è solo un tema |
| Costo e rischio | quanto lavoro serve, e dove questa direzione può invecchiare male o stancare |

## La regola che tiene lontano il generico

Una direzione è **un insieme di valori**. «Pulito e moderno», «professionale ma amichevole»,
«minimale con tocchi di colore» non sono direzioni: sono aggettivi, e il modello che li riceve
produrrà esattamente la pagina di default. Se una riga di una direzione non contiene un nome
proprio, un numero o un esadecimale, va riscritta.

Stessa regola per la distanza fra le direzioni: se due si distinguono solo per l'accento, è una
direzione sola presentata due volte. Devono differire su almeno **tipografia + densità**, che sono
le due leve che cambiano davvero la faccia di una pagina.

## Da dove escono le direzioni

Non da un vocabolario di stili, ma da questo prodotto:

- **Cosa fa e a chi parla.** Uno strumento per sviluppatori regge il mono e la densità alta;
  un servizio per anziani no, e la ragione non è il gusto.
- **Il contesto d'uso reale.** Guardata per tre secondi da telefono, o usata otto ore al giorno?
  Cambia tutto: densità, contrasto, dimensione dei bersagli.
- **Cosa fanno tutti nel settore**, e se conviene farlo o rovesciarlo. In un mercato dove tutti
  sono blu e arrotondati, l'unico severo si vede. In un mercato dove nessuno lo è, l'unico severo
  potrebbe sembrare fuori posto — e va detto.
- **I vincoli veri**: brand esistente, tipografia già pagata, sistema di componenti già in uso,
  chi dovrà mantenerla. Una direzione che ignora il vincolo è tempo perso.

Se questi dati non ci sono, se ne chiedono al massimo **tre** e si propone lo stesso: un utente che
risponde a un questionario prima di vedere qualcosa non torna.

Almeno una delle direzioni deve essere quella che l'utente **non si aspetta**. Se tutte e tre sono
prevedibili, il lavoro non l'ha fatto nessuno.

## Prima di proporre

Leggi la tua `notes.md`: le cose che l'utente ha già rifiutato non si ripropongono, e nemmeno la
loro versione travestita. Se una direzione scartata era giusta e il contesto è cambiato, si può
riproporre — ma dicendo che era già stata scartata e cosa è cambiato.

## Dopo la scelta

Quando l'utente sceglie, la direzione va in `notes.md` **con i suoi valori** (font, esadecimali,
raggio), non con il nome soltanto: serve come metro per tutto quello che verrà dopo. E se la scelta
vincola il resto del progetto (per esempio una tipografia a pagamento, o l'abbandono del kit di
componenti in uso), è una decisione: riga in `decisions.md`.
