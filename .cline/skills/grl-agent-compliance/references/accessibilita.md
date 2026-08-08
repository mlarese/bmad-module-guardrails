---
name: accessibilita
description: Dire quale livello di accessibilità è richiesto (o che non lo è) e quali punti incidono sul design prima che venga disegnato
code: ACC
added: 2026-08-06
type: prompt
---

# Accessibilità

## Cosa deve essere vero alla fine

Chi disegna sa, **prima di disegnare**, se c'è un obbligo, quale standard e quale livello, e i pochi punti che vincolano davvero le scelte visive. Arrivare dopo costa un rifacimento: è l'unica capacità del tuo repertorio che ha una finestra utile.

Se l'obbligo non c'è, dillo per primo. Poi, in una riga, che l'accessibilità resta una buona idea — senza trasformarla in un obbligo che non esiste.

## Come ci arrivi

Carica `references/soglie-applicabilita.md`. Tre cose decidono l'esito: **a chi** è rivolto il servizio (consumatori o imprese), **cosa** è il servizio (rientra nell'elenco dell'EAA?), e **quanto è grande** l'azienda (esenzione microimprese per i servizi; in Italia la soglia dei 500 milioni della L. 4/2004; committente pubblico che obbliga a prescindere).

Un gestionale B2B e uno strumento interno di norma sono fuori. Un e-commerce verso consumatori è dentro, ovunque abbia sede.

## Cosa consegni

Il livello richiesto — di norma EN 301 549, che significa WCAG 2.1 AA — e i punti che toccano il design, non l'elenco dei criteri:

- contrasto minimo su testo e componenti interattivi
- dimensione e spaziatura dei bersagli toccabili
- focus visibile e ordine di tabulazione coerente
- niente informazione affidata al solo colore
- testi alternativi, etichette dei campi, messaggi d'errore associati al campo
- video e audio: sottotitoli e alternative
- il percorso completo di acquisto o di iscrizione, non la sola home

Se il servizio è un e-commerce, ricorda che l'obbligo copre l'intero flusso: informazioni precontrattuali, checkout, pagamento, assistenza.

## Confine con Iris

Tu dichiari il **livello richiesto** e i vincoli. **Iris** decide come rispettarli senza appiattire il design. Se l'utente chiede «e allora come lo faccio bello lo stesso?», passa a lei e fermati.
