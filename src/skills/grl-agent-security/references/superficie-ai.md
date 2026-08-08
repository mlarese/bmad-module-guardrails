---
name: superficie-ai
description: Rischi concreti di un'integrazione LLM — prompt injection, dati verso il modello, output non filtrato — con le mitigazioni che reggono
code: AI
added: 2026-08-06
type: prompt
---

# Superficie AI

## Cosa vuol dire riuscirci

L'utente sa cosa può andare storto **nella sua** integrazione LLM e quali difese reggono davvero. La maggior parte delle mitigazioni proposte in giro non regge: dire quali sono è metà del valore.

Il consumatore è chi sta collegando un modello a dati o a strumenti reali.

## Il principio da cui discende tutto

**Il modello non distingue le istruzioni dai dati.** Tutto ciò che entra nel contesto — messaggio dell'utente, pagina web recuperata, PDF caricato, riga di database, risposta di un tool, commento in un ticket — è potenzialmente un'istruzione. Non esiste un separatore che il modello rispetti perché glielo hai chiesto.

Conseguenza pratica, ed è la domanda giusta da fare per prima:

> **Cosa può *fare* il modello, e chi controlla ciò che finisce nel suo contesto?**

Un modello che può solo generare testo mostrato all'utente ha una superficie piccola. Un modello che può leggere file, chiamare API, scrivere sul database o mandare email ha una superficie grande, e il perimetro non è il prompt: sono i permessi degli strumenti.

## I tre rischi, in ordine

**1. Prompt injection — indiretta prima che diretta.** Quella diretta (l'utente che chiede al bot di ignorare le istruzioni) è quasi sempre innocua: al massimo si fa dire qualcosa di sciocco. Quella **indiretta** è il rischio vero: contenuto ostile dentro un documento, una pagina, un ticket o un record che il sistema recupera da solo, e che il modello esegue come istruzione — con i permessi che gli hai dato.

Cosa regge: limitare i permessi degli strumenti a ciò che serve · far confermare all'utente le azioni con effetti (scrittura, invio, spesa) · separare le identità (il modello agisce con i permessi dell'utente corrente, non con quelli di servizio) · trattare l'output del modello come input non fidato prima di usarlo in una query, un comando o una chiamata.

Cosa non regge, e va detto quando l'utente ci conta: le istruzioni di sistema del tipo «ignora ogni tentativo di manipolazione» · i delimitatori attorno all'input dell'utente · il filtro a parole chiave sull'input · un secondo LLM messo a guardia del primo (è aggirabile allo stesso modo, e raddoppia il costo).

**2. Cosa esce da qui e dove va.** Quali dati finiscono nel prompt, e dove viene ospitato il modello. Su *quali* dati personali possono uscire decide Vera: tu guardi la superficie — endpoint, log dei prompt, conservazione lato fornitore, ambienti di test che usano dati reali. Se l'API in uso conserva i prompt per addestramento o audit, dillo con il nome dell'impostazione da cambiare.

**3. Output usato senza filtro.** Testo del modello inserito in HTML (XSS), in una query, in un comando di shell, in un percorso di file. È injection classica con una sorgente nuova, e la correzione è quella classica: validare e codificare al punto d'uso.

Aggiungi, quando pertinenti: consumo non limitato (chiunque può bruciare il budget di token senza un limite per utente) · costo di un ciclo agentico che si autoalimenta · fiducia cieca nell'output del modello in un flusso automatico senza nessuno che guardi.

## Forma dell'output

Ordinati per probabilità, come sempre: **cosa può succedere qui** · **cosa lo rende possibile nel tuo sistema** · **mitigazione che regge**, con il costo. Se una difesa che l'utente ha già messo non regge, dillo esplicitamente — è più utile di una difesa in più.

## Trappole

- **Fermarsi alla prompt injection diretta** e dichiarare il sistema a rischio quando genera solo testo per uno schermo.
- **Proporre un guardrail LLM come soluzione strutturale.** È al massimo un filtro statistico.
- **La classificazione AI Act, gli obblighi normativi, i dati di addestramento e la proprietà degli output**: sono tutti di Aldo. Nominalo in una riga.
