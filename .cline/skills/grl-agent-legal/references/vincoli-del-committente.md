---
name: vincoli-del-committente
description: I vincoli tecnici nascosti nel contratto o nel capitolato del cliente
code: COM
added: 2026-08-06
type: prompt
---

# Vincoli del committente

## Il risultato

L'utente conosce, **prima di progettare**, i vincoli del contratto che condizionano scelte
tecniche. Solo quelli: ciò che non tocca lo sviluppo non si commenta.

## Da dove parti

Se c'è un contratto o un capitolato, lo leggi. Se non c'è, si ricostruisce dall'offerta, dalle
email di conferma e dall'ordine — che nella pratica valgono quanto un contratto e nessuno
rilegge mai.

## Dove si nascondono i vincoli tecnici

I contratti tecnici li mettono in punti che sembrano burocratici. Cerca lì:

| Clausola | Cosa vincola davvero |
| -------- | -------------------- |
| Titolarità del codice e diritto di riuso | se puoi riportare in casa il framework che stai scrivendo, o riusarlo per un altro cliente. Cambia se conviene generalizzare o no |
| Esclusiva / non concorrenza | per quanto tempo e in quale settore non puoi lavorare con altri |
| Componenti di terzi | alcuni contratti vietano il software con licenza copyleft, o impongono l'elenco delle componenti open source usate |
| Hosting e localizzazione | «solo UE», «solo Italia», «solo sulla nostra infrastruttura»: decide il cloud prima che tu lo scelga |
| Subappalto | un freelance può essere subappalto. In alcuni contratti pubblici, anche un servizio cloud lo è |
| Collaudo e accettazione | cosa fa scattare il pagamento, chi firma, entro quanto. Determina cosa deve esistere e quando |
| Garanzia e manutenzione | per quanti mesi correggi gratis, e cosa conta come difetto invece che come nuova richiesta |
| Penali di ritardo | quanto costa una settimana. Determina se conviene tagliare scope o slittare |
| Audit e ispezione | il cliente può chiedere di vedere codice, log o processi: cambia cosa devi essere in grado di mostrare |
| Dati e uscita | di chi sono i dati, in che formato te li fai restituire, cosa cancelli a fine rapporto |
| Riservatezza | spesso impedisce anche solo di citare il cliente come referenza |

## Come lo dici

Solo i vincoli che **cambiano una scelta tecnica**, ciascuno con la scelta che condiziona: non
«c'è una clausola di esclusiva», ma «l'esclusiva copre il settore X per 24 mesi: il modulo
generico che volevi riusare altrove, in quei 24 mesi non puoi venderlo».

Se il contratto non è ancora firmato, sei in una delle tre eccezioni al divieto di rinvio: dici
tu quali clausole vanno cambiate e perché, poi indichi che quella firma va fatta rivedere,
nominando le clausole precise da portare. Il rinvio resta specifico, mai generico.
