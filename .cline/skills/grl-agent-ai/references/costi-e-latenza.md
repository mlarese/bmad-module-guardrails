---
name: costi-e-latenza
description: Il conto per chiamata prima del lancio, e le leve per abbassarlo in ordine di resa
code: CL
added: 2026-08-07
type: prompt
---

# Costi e latenza

## Cosa vuol dire riuscirci

L'utente sa **quanto gli costerà al mese** e **quanto aspetterà l'utente finale**, prima di lanciare invece che dopo la prima bolletta. E sa quale leva tirare per prima, perché non sono equivalenti.

## Il principio da cui discende tutto

**Il costo è quasi sempre nei token in ingresso, non in quelli in uscita.** Il contesto lungo — istruzioni cresciute per accumulo, dieci documenti recuperati per sicurezza, l'intera cronologia della conversazione a ogni turno — è la voce che fa il conto, e viene pagata a ogni singola chiamata.

La domanda che smonta il problema:

> **Quanti token entrano, per quante chiamate al giorno?**

Le due cifre si moltiplicano e il resto è aritmetica.

## Il conto, prima del lancio

Si fa in tre righe, con i numeri veri:

```
costo per chiamata = (token_ingresso × prezzo_ingresso) + (token_uscita × prezzo_uscita)
costo al giorno    = costo per chiamata × chiamate al giorno
```

I due errori tipici: contare una chiamata per interazione quando una catena ne fa quattro, e usare il volume della demo invece di quello vero.

**I prezzi, i nomi dei modelli e le finestre di contesto cambiano di continuo. Verifica sul web prima di dare un numero.** Se non puoi verificare, dillo esplicitamente e dichiara la data del tuo riferimento: un preventivo basato su listini a memoria è peggio di nessun preventivo.

## Le leve, in ordine di resa

**1. Ridurre il contesto.** È quasi sempre la voce più grande e la più facile da tagliare.
- Meno documenti recuperati, ma migliori: cinque passaggi pertinenti battono venti a caso, e costano un quarto. Se i cinque non bastano, il problema è il recupero.
- Cronologia della conversazione: finestra scorrevole o riassunto periodico invece dell'intero storico a ogni turno.
- Istruzioni cresciute per accumulo: le istruzioni di sistema si accorciano più spesso di quanto si allunghino.

**2. Caching del prompt.** La parte stabile del contesto — istruzioni, esempi, documenti fissi — può essere memorizzata dal fornitore e ripagata a frazione. Vincolo pratico: la parte stabile deve stare **all'inizio** e non cambiare, quindi il prompt va costruito con la parte fissa davanti e quella variabile in fondo. È una modifica piccola con una resa alta, e va fatta prima di ottimizzare qualsiasi altra cosa.

**3. Il modello giusto per il passo giusto.** Non serve il modello più capace per classificare un'email in tre categorie. Instradare i passi semplici a un modello leggero e tenere quello capace dove serve davvero è spesso una riduzione di parecchie volte a qualità invariata. Il modo di verificarlo è il set di casi: vedi *Eval e osservabilità*.

**4. Risposte più corte.** Un limite ai token in uscita e un formato strutturato invece di prosa. Vale meno delle prime tre, ma è gratis.

**5. Batch.** Dove la latenza non conta (elaborazioni notturne, arricchimento di archivi), le API in modalità batch costano meno. Vale solo per il lavoro asincrono: vedi *Automazioni e code*.

## La latenza

È un problema diverso e si risolve con leve diverse.

- **Percepita contro reale.** Con lo streaming conta il tempo al primo token, non quello totale: una risposta che inizia dopo mezzo secondo e finisce in otto è vissuta meglio di una che arriva tutta insieme dopo quattro. Se l'interfaccia lo permette, lo streaming è la prima cosa da fare.
- **Le catene sommano.** Quattro chiamate in sequenza da due secondi fanno otto secondi. **Parallelizzare ciò che è indipendente** è la leva più semplice e la meno usata: recupero e classificazione, per esempio, spesso non dipendono l'uno dall'altra.
- **Cosa mostrare mentre si aspetta.** Un indicatore generico su otto secondi fa abbandonare; mostrare i passi che stanno accadendo no. Come si disegna è di Iris, che ci sia è una scelta di impianto.
- **Il modello leggero è anche più veloce**, ed è spesso la risposta giusta a un problema di latenza prima che a uno di costo.

## Quando il fornitore non risponde

Va progettato prima, non dopo il primo disservizio:

- **Limiti di frequenza**: si superano prima di quanto si pensi, e la reazione corretta è una coda, non un ciclo di retry stretto.
- **Retry con attesa crescente** e un tetto ai tentativi. Un retry immediato su un limite di frequenza lo peggiora.
- **Timeout espliciti.** Il default della libreria è quasi sempre troppo alto per una richiesta interattiva.
- **Fallback su un secondo fornitore o su un modello più piccolo**, se il servizio è critico. Ha un costo di manutenzione: due prompt tarati su due modelli. Va deciso, non ereditato.

## Il tetto di spesa

Due meccanismi distinti, entrambi necessari se il sistema è pubblico:

- **Limite per utente**, altrimenti un singolo utilizzatore consuma il budget di tutti.
- **Limite per esecuzione agentica**, perché un ciclo che si autoalimenta spende finché qualcuno non lo ferma: vedi *Agenti e tool*.

Che questo sia anche una superficie di abuso — qualcuno che brucia il budget di proposito — è materia di **Kai**: nominalo e fermati.

## Forma dell'output

Il conto in tre righe con i numeri del progetto, poi le leve applicabili **a questo caso** in ordine di resa, ciascuna con la stima di quanto toglie e cosa costa applicarla. Se il volume è basso e il conto è di poche decine al mese, dillo e fermati: ottimizzare lì è tempo sprecato.

## Trappole

- **Dare prezzi a memoria.** Cambiano; verifica.
- **Ottimizzare prima di misurare.** Senza le tracce non si sa dove vanno i token.
- **Scegliere il modello più capace per default** e scoprire il conto in produzione.
- **Confondere costo e latenza.** Il caching abbassa il costo, non sempre l'attesa; il modello leggero abbassa entrambi; lo streaming non abbassa niente ma cambia l'esperienza.
- **Ignorare il costo del recupero.** Embedding, reranking e store hanno un prezzo proprio, che nel conto non compare quasi mai.
