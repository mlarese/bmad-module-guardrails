---
name: agenti-e-tool
description: Tool calling prima degli agenti — come si progettano i tool e quali controlli impediscono a un ciclo di scappare
code: AG
added: 2026-08-07
type: prompt
---

# Agenti e tool

## Cosa vuol dire riuscirci

L'utente ha **tool progettati per essere usati da un modello**, sa se gli serve davvero un agente o gli basta una catena fissa, e ha i controlli che impediscono a un ciclo di girare a vuoto bruciando tempo e denaro.

Il consumatore è chi sta collegando un modello a strumenti che fanno qualcosa.

## Il principio da cui discende tutto

**Tool calling non è un agente.** Un modello che sceglie fra tre funzioni e ne chiama una è tool calling: il flusso resta tuo, il numero di passi lo decidi tu. Un agente è un modello che decide *quanti* passi fare e *in che ordine*, e quel controllo lo perdi.

La domanda che smonta il problema:

> **Sai già in anticipo quanti passi servono? Se sì, non ti serve un agente.**

Quasi sempre lo sai. «Recupera, poi rispondi» è una catena. «Estrai i campi, valida, salva» è una catena. Un agente serve quando il numero di passi dipende da cosa il modello trova strada facendo, e non lo si può sapere prima.

## Catena fissa contro agente

| | Catena fissa | Agente |
| --- | --- | --- |
| Passi | noti, in sequenza | decisi a runtime |
| Costo | prevedibile | variabile, e senza controlli può esplodere |
| Debug | si sa dove ha sbagliato | va ricostruito dalla traccia |
| Latenza | somma nota | sconosciuta finché non finisce |
| Quando | quasi sempre | ricerca in più passi, compiti esplorativi, correzione iterativa con verifica |

Se stai esitando, parti dalla catena. Passare da catena a agente è facile; il contrario no.

## Progettare i tool

I tool non si scrivono per il programmatore: si scrivono **per il modello che deve leggerli e sceglierli**.

- **Pochi.** Oltre una decina, la scelta peggiora visibilmente. Se ne servono venti, quasi sempre due o tre tool con un parametro in più fanno lo stesso lavoro.
- **Nomi e descrizioni espliciti.** La descrizione è un prompt: dice *quando* usare il tool e quando non usarlo, non solo cosa fa. `cerca_ordini` con «cerca gli ordini di un cliente per data; non usare per i resi» è meglio di `search` con «esegue una ricerca».
- **Parametri stretti.** Enumerazioni invece di stringhe libere, tipi precisi, campi obbligatori dichiarati. Ogni grado di libertà in più è un modo in cui il modello sbaglia.
- **Nessun parametro che il modello non può conoscere.** Se serve l'ID interno dell'utente, lo passa il tuo codice, non il modello.
- **Errori restituiti in modo che il modello possa correggersi.** Non `Error 400`, ma «la data va nel formato AAAA-MM-GG, hai passato "ieri"». Un errore leggibile trasforma un fallimento in un secondo tentativo riuscito.
- **Risposte corte.** Un tool che restituisce trecento righe di JSON riempie il contesto e costa a ogni passo successivo. Restituisci i campi che servono.

## I controlli non negoziabili

Se c'è un ciclo, servono tutti e cinque. Non sono opzionali e non dipendono dalla severità:

| Controllo | Cosa impedisce |
| --------- | -------------- |
| **Budget massimo di passi** | il ciclo che non converge e continua a provare |
| **Budget di spesa** per esecuzione | la singola richiesta che costa cento volte la media |
| **Condizione di terminazione esplicita** | l'agente che non sa quando ha finito |
| **Timeout complessivo** | l'esecuzione che resta appesa e tiene occupata una risorsa |
| **Conferma umana sulle azioni con effetti** | scrittura, invio, pagamento, cancellazione eseguiti per errore |

L'ultimo punto è anche un punto di **Kai**: il modello può essere indotto a chiamare un tool da contenuto ostile arrivato nel contesto, e i permessi dei tool sono il perimetro vero. Qui lo si progetta, la valutazione del rischio è sua.

Cosa succede quando un budget si esaurisce va deciso: errore all'utente, risposta parziale dichiarata come tale, o passaggio a una persona. Mai un fallimento silenzioso.

## Multi-agente

Giustificato quando: due o più compiti hanno **contesti davvero separati** (istruzioni lunghe e incompatibili, insiemi di tool disgiunti), e tenerli in un solo contesto peggiora le scelte del modello.

Non giustificato quando: si vuole «dividere le responsabilità» per pulizia di progetto. In quel caso è una catena di chiamate con in più il costo di passare il contesto fra un agente e l'altro — che è il punto in cui l'informazione si perde. Il coordinamento fra agenti costa chiamate, latenza e una nuova classe di errori difficili da riprodurre.

Regola: **prima di dividere in agenti, prova a ridurre i tool.** Il problema quasi sempre è quello.

## Memoria conversazionale

Va deciso cosa si conserva davvero, perché la conversazione intera nel contesto è la voce di costo che cresce da sola.

| Strategia | Quando | Cosa perdi |
| --------- | ------ | ---------- |
| Finestra scorrevole (ultimi N turni) | conversazioni brevi, contesto locale | ciò che è stato detto all'inizio |
| Riassunto progressivo | conversazioni lunghe | dettagli precisi; il riassunto è generato, quindi può sbagliare |
| Fatti estratti e salvati in modo strutturato | quando servono poche informazioni stabili (nome, preferenze, contesto del cliente) | niente, ma va progettato |

L'approccio che regge quasi sempre: finestra scorrevole **più** pochi fatti strutturati. Il riassunto progressivo si aggiunge solo se le conversazioni superano davvero il contesto. Se i fatti conservati riguardano persone, quanto tenerli è materia di **Vera**.

## Forma dell'output

Verdetto per primo: catena o agente, con il motivo in una riga. Poi l'elenco dei tool con nome, quando usarli, parametri. Poi i cinque controlli, con i valori concreti proposti (quanti passi, quanto budget, quale timeout). Se serve conferma umana, di' esattamente su quali azioni.

## Trappole

- **L'agente montato per un problema che è una chiamata sola.**
- **Venti tool con nomi generici.** Il modello sbaglia a scegliere e nessuno capisce perché.
- **Nessun budget di passi.** Si scopre con la fattura.
- **Errori dei tool restituiti in forma illeggibile**: il modello non può correggersi e riprova identico.
- **Dare all'agente i permessi di servizio invece di quelli dell'utente corrente.** È un punto di Kai, ma se lo vedi lo nomini.
