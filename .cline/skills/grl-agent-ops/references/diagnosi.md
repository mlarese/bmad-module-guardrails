---
name: diagnosi
description: Cosa è rotto, capito con comandi di sola lettura e ipotesi ordinate per probabilità — non tirando a indovinare
code: DIAG
added: 2026-08-06
type: prompt
---

# Diagnosi di un guasto

## Cosa vuol dire riuscirci

Si passa da «non funziona» a **una causa individuata**, con comandi che non peggiorano la situazione. Il consumatore è chi ha il servizio giù adesso e la tentazione di riavviare tutto: il valore di questa capacità è dargli qualcosa di meglio da fare nei primi cinque minuti.

## Le due domande che tagliano metà dello spazio di ricerca

1. **Cos'è cambiato?** Deploy, aggiornamento, certificato scaduto, cambio di configurazione, aumento di traffico. Nella grande maggioranza dei casi il guasto ha una causa recente, e chiedere «funzionava ieri?» vale più di dieci comandi.
2. **È giù o è lento?** Sono due diagnosi diverse. Giù: qualcosa non risponde. Lento: qualcosa è saturo o sta aspettando.

## L'ordine, dal basso verso l'alto

Si sale finché non si trova il livello che non risponde. Ogni comando è **di sola lettura**.

| Livello | Cosa si guarda |
| ------- | -------------- |
| Macchina | è viva, si entra in SSH, `df -h` (disco pieno è la prima causa banale), `free -h`, `uptime` |
| Servizi | `systemctl status` / `docker compose ps` — cosa è su, cosa riavvia in loop |
| Log | i log del servizio caduto, **partendo dal primo errore, non dall'ultimo**: l'ultimo è spesso una conseguenza |
| Rete e proxy | la porta è in ascolto (`ss -ltnp`), il proxy risponde, il certificato è valido, il DNS punta dove deve |
| Dipendenze | database raggiungibile, connessioni esaurite, servizio esterno degradato |
| Applicazione | errori applicativi, migrazione a metà, variabile d'ambiente mancante dopo un deploy |

**Il primo errore in ordine di tempo è quello che conta.** Un'applicazione che non parte produce cento righe di errore dopo la vera causa.

## I sospetti abituali, per frequenza

Disco pieno (log senza rotazione, backup accumulati) · certificato TLS scaduto · una variabile d'ambiente persa nell'ultimo deploy · connessioni al database esaurite · memoria esaurita e processo terminato dal kernel (`OOM`, visibile in `dmesg`) · un aggiornamento automatico che ha riavviato un servizio · DNS.

## Il riavvio

Riavviare spesso risolve **e cancella le prove**. Se il servizio è giù e serve rialzarlo subito, va bene — ma prima si salvano i log e lo stato, in una riga. E il riavvio di un servizio vivo rientra nel protocollo dei comandi distruttivi: si spiega, si conferma, si esegue.

## Forma dell'output

**Ipotesi ordinate per probabilità**, ciascuna con il comando di verifica non distruttivo e cosa significa il risultato. Non un elenco di tutto ciò che potrebbe essere: tre ipotesi in ordine, e il modo di scartarne due in due minuti.

Se manca l'informazione per ordinare, fai **una** domanda — quasi sempre «cos'è cambiato?» — invece di elencare.

## Trappole

- **Cambiare due cose insieme.** Non si saprà quale ha risolto, e il guasto tornerà.
- **Partire dall'ultimo errore nei log.**
- **Il riavvio come prima mossa**: cancella le prove e nasconde una causa che tornerà.
- **Comandi distruttivi durante il panico** (`prune`, `delete`, `drop`, ripristini): è il momento in cui il protocollo serve di più, non di meno.
- **Chiudere senza la causa.** Se il servizio è tornato su ma non si sa perché era giù, dillo esplicitamente: il guasto è sospeso, non risolto.
