---
name: base-giuridica
description: Stabilisce su quale base giuridica si regge ogni funzionalità che tratta dati personali
code: BG
added: 2026-08-06
type: prompt
---

# Base giuridica per feature

L'esito è, per ogni funzionalità che tratta dati personali, **una** base giuridica e la conseguenza pratica che ne discende. Il consumatore è chi implementa: la risposta utile non è «interesse legittimo», è «non serve una spunta, ma serve un link per opporsi in questa schermata».

Una base per trattamento, non un elenco di basi possibili. Se scegli interesse legittimo, dì in una riga perché regge — finalità, necessità, aspettativa dell'utente. Se non regge, cambia base invece di difenderla.

Gli errori da intercettare, perché sono quelli che i team fanno davvero:

- **Consenso usato come default.** Quasi mai è la base giusta per far funzionare il prodotto: quella è l'esecuzione del contratto. Il consenso serve dove c'è una scelta vera.
- **Consenso impacchettato.** La spunta al signup che copre anche marketing e profilazione non vale come consenso per quelle finalità.
- **Consenso dove non c'è scelta.** Se senza spunta il servizio non funziona, non è consenso: è una base sbagliata travestita.
- **Basi mischiate nello stesso trattamento.** «Contratto, e comunque anche interesse legittimo» significa che la base non è stata scelta.
- **Categorie particolari** — salute, biometrici, opinioni, orientamento, dati di minori. La base ordinaria non basta, e l'alternativa più economica è quasi sempre non trattare quel dato.

Chiudi con cosa cambia nel prodotto: una spunta separata, un testo, un link, un'impostazione di default, o niente. Se non cambia niente, dillo e fermati.

Quando la feature comporta anche un'informativa da scrivere, indica solo cosa deve dire in più rispetto a quella che esiste — non riscriverla, e non proporne una di sei pagine.

## Traccianti: quando il consenso serve davvero

Il consenso ai cookie e agli altri traccianti non dipende dalla tecnologia — cookie, `localStorage`, pixel, fingerprint sono la stessa cosa — ma da **cosa fa** il tracciante:

| Tracciante | Consenso |
| --- | --- |
| Tiene la sessione, il carrello, la lingua, il bilanciamento del carico | no: è tecnico |
| Misura il traffico in forma aggregata, senza incrocio fra siti e con l'IP troncato | no, se il fornitore non lo riusa per sé; verificalo nel contratto |
| Profila, personalizza la pubblicità, segue l'utente fra siti, fa remarketing | sì, prima del rilascio, e revocabile con la stessa facilità |

Due errori frequenti: il banner che si mette «per sicurezza» su un sito che ha solo cookie tecnici — e allora va tolto — e il banner che c'è ma installa i traccianti prima della scelta, che vale come nessun banner.
