---
name: backup
description: Il backup esiste, è fuori dalla macchina che protegge, ed è stato ripristinato almeno una volta
code: BKP
added: 2026-08-06
type: prompt
---

# Backup e ripristino

## Cosa vuol dire riuscirci

Esiste una copia dei dati che conta, **fuori** dal sistema che protegge, e **qualcuno l'ha ripristinata almeno una volta**. Il consumatore è la persona che scopre alle 7 del mattino che il database è corrotto: deve sapere cosa lanciare e quanto tempo ci vorrà.

**Un backup mai ripristinato non è un backup: è un file di cui non si sa nulla.** Questa frase è il centro di questa capacità. Se la consultazione produce una politica di backup elegante e nessuna prova di ripristino, è fallita.

## Le tre domande

1. **Cosa si perde se sparisce?** Quasi sempre: il database, i file caricati dagli utenti, i segreti e le configurazioni. Quasi mai: il codice (è in git), i container (si ricostruiscono), la cache.
2. **Quanto lavoro si può permettere di perdere?** Un'ora, un giorno, una settimana. Determina la frequenza, e niente altro la determina.
3. **Quanto può restare giù mentre si ripristina?** Determina se basta un dump o serve una replica.

## Cosa conta

- **Fuori dalla macchina.** Uno snapshot che vive sullo stesso provider e sullo stesso account protegge dal guasto del disco, non dalla cancellazione per errore né dalla perdita dell'account. Almeno una copia altrove.
- **Automatico.** Un backup manuale è un backup che non c'è. Un cron, un servizio del provider, un job programmato.
- **Verificabile senza fatica.** Bisogna poter rispondere in dieci secondi a «quand'è l'ultimo backup riuscito?». Un backup fallito in silenzio da tre settimane è lo scenario tipico.
- **Ritenzione.** Se si tengono solo le ultime 24 ore, una corruzione scoperta dopo due giorni è già stata copiata su tutte le versioni. Qualche giorno, qualche settimana, qualche mese.
- **I segreti sono dati.** Se `.env` esiste solo sulla macchina, la macchina è un punto di guasto. Un gestore di password o un vault, non una copia in chiaro accanto al backup.

## La prova di ripristino

Concreta e piccola, non un'esercitazione. Per un Postgres: un container vuoto in locale, il dump più recente, e il conteggio delle righe della tabella principale. Venti minuti, e alla fine si sa se il backup vale.

Da annotare in `notes.md` (una riga): quando è stata fatta l'ultima prova e quanto è durato il ripristino. Il tempo di ripristino è il numero che serve durante l'incidente, ed è sempre più lungo di quanto si crede.

## Forma dell'output

Una tabella corta: **cosa si salva · dove · con che frequenza · quanto si tiene**. Poi la prova di ripristino, con i comandi. Poi cosa **non** vale la pena salvare, detto esplicitamente.

## Trappole

- **La replica scambiata per backup.** Una replica copia anche la `DELETE` sbagliata, all'istante.
- **Il backup del container invece dei dati.** Il container si ricostruisce; il volume no.
- **Il ripristino che sovrascrive la produzione** durante una prova: è un comando distruttivo, protocollo pieno.
- **Un backup non cifrato in un bucket pubblico**: contiene tutti i dati. Sul rischio di esposizione parla **Kai**; se dentro ci sono dati personali, dove possono stare lo dicono **Vera** e **Nils**.
- **Salvare tutto.** Se il backup è enorme, il ripristino è lento e la prova non si fa mai.
