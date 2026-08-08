---
name: orchestrazione
description: LangChain, LangGraph, LlamaIndex, framework ad agenti o SDK nudo — quando ciascuno paga il proprio costo
code: OR
added: 2026-08-07
type: prompt
---

# Orchestrazione

## Cosa vuol dire riuscirci

L'utente sa **con cosa scrivere la propria pipeline** e perché, e sa quanto gli costerà cambiare idea. Nella maggior parte dei casi la risposta è meno framework di quanto si aspettasse.

Il consumatore è chi sta per iniziare a scrivere, o chi ha una pipeline che è diventata difficile da capire.

## Il principio da cui discende tutto

**Un framework di orchestrazione si paga in opacità.** Ogni strato fra il tuo codice e la chiamata al modello è uno strato in cui, quando la risposta non torna, devi capire cosa è stato davvero mandato. Il framework guadagna il proprio posto solo se ti dà qualcosa che dovresti scrivere tu e che scriveresti peggio.

La domanda che smonta il problema:

> **Cosa mi dà questo framework che dovrei scrivere io, e quanto mi costa uscirne fra sei mesi?**

Se la prima risposta è «una funzione che concatena due prompt» e la seconda è «riscrivo tutto», la scelta è già fatta.

## La mappa

| Strumento | Quando è la risposta giusta | Quando è overhead |
| --------- | --------------------------- | ----------------- |
| **SDK del fornitore, nudo** | catene lineari di uno-tre passi, tool calling semplice, estrazione, classificazione. È il default | quasi mai, se non quando ti ritrovi a riscrivere gestione dello stato, ripresa e checkpoint |
| **LangChain** | ti serve un insieme ampio di connettori già pronti (loader di documenti, integrazioni con store e fornitori) e vuoi partire in fretta | una catena di due passi fissi: aggiunge astrazioni e rende meno visibile il prompt effettivo |
| **LangGraph** | il flusso ha **cicli**, ramificazioni condizionali, stato che persiste fra i passi, checkpoint e ripresa dopo un errore o dopo un'attesa umana | flusso lineare senza cicli: il grafo è un modo complicato di scrivere tre chiamate in fila |
| **LlamaIndex** | il centro del lavoro è l'**ingestione documentale**: caricare, spezzare, indicizzare, interrogare un corpus | il corpus è piccolo, o hai già il tuo pipeline di ingestione |
| **Framework ad agenti** (multi-agente, ruoli, deleghe) | contesti davvero separati con strumenti diversi e un coordinamento non banale — raro | quasi sempre. Vedi *Agenti e tool*: la maggior parte dei problemi «da agenti multipli» è una catena fissa |

## I criteri, in ordine

**1. Quanti passi, e sono sempre gli stessi?** Numero fisso e sequenza nota → nessun framework serve. Numero di passi deciso a runtime, con cicli → un grafo di stato paga.

**2. Serve riprendere da dove si era fermato?** Un flusso lungo che può fallire a metà, o che aspetta l'approvazione di una persona, ha bisogno di checkpoint. Scriverli a mano è possibile ma noioso: è il caso in cui LangGraph guadagna il proprio posto.

**3. Riesci a vedere cosa è stato mandato al modello?** Prima di scegliere, verifica che il framework ti lasci stampare il prompt finale, i parametri e la risposta grezza. Se non è banale, sarà il tuo problema principale il primo giorno che qualcosa non funziona.

**4. Streaming e gestione degli errori attraversano tutto lo stack.** Se l'interfaccia deve mostrare il testo mentre arriva, lo streaming deve passare attraverso ogni strato del framework. Stesso discorso per i retry, i timeout e la propagazione degli errori. **Verificalo prima di scegliere**, non dopo aver scritto la pipeline: sono le due funzioni che più spesso si scoprono mancanti o scomode.

**5. Chi lo manterrà.** Un framework aggiunge una dipendenza che va aggiornata e una documentazione da leggere. Su un team di una persona che non conosce lo strumento, il costo è tutto in salita.

## Il costo di uscita

Si valuta subito, non alla fine:

- Le astrazioni del framework compaiono nella firma delle tue funzioni? Se il tipo del framework attraversa tutto il codice, uscirne è una riscrittura.
- Il prompt è scritto da te o composto dal framework? Prompt costruiti internamente sono la parte più difficile da replicare altrove.
- Lo stato è persistito in un formato tuo o in uno del framework?

Modo economico di limitare il danno: **tenere le chiamate al modello dietro una funzione tua**, e lasciare che il framework stia sopra, non dentro. È l'unico strato di indirezione che qui paga il proprio costo.

## Versioni

Le librerie di orchestrazione cambiano API più in fretta di qualunque altra dipendenza del progetto, e le rotture di compatibilità fra versioni minori sono normali. **Prima di raccomandare una libreria o un modulo, verifica sul web la versione corrente e se il pezzo che stai nominando esiste ancora con quel nome.** Se non puoi verificare, dichiaralo e indica la data del tuo riferimento. Pinna le versioni nel progetto: qui l'aggiornamento automatico rompe.

## Forma dell'output

Una riga di verdetto («per questo flusso, SDK nudo»), poi il perché in tre punti: numero e stabilità dei passi, bisogno di stato e ripresa, chi lo manterrà. Poi cosa costa cambiare idea dopo. Se raccomandi un framework, di' quale singola cosa ti sta facendo scegliere quello.

## Trappole

- **Scegliere il framework prima di sapere quanti passi ha il flusso.**
- **Adottare un framework per i connettori, e restarci per tutto il resto.** I loader si possono usare in fase di ingestione e basta.
- **Il grafo di stato per un flusso lineare.** Aggiunge vocabolario, non capacità.
- **Non verificare lo streaming.** Si scopre a interfaccia già fatta.
- **Andare a memoria su nomi di moduli e firme.** Cambiano; verifica.
