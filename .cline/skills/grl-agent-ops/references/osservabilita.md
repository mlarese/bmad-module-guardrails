---
name: osservabilita
description: I pochi log, metriche e alert che fanno accorgere del problema prima dell'utente finale
code: OBS
added: 2026-08-06
type: prompt
---

# Osservabilità essenziale

## Cosa vuol dire riuscirci

Quando qualcosa si rompe, **qualcuno lo sa prima dell'utente finale**, e chi apre i log trova la risposta invece di annegarci. Il consumatore è la persona di turno alle tre di notte: se l'alert che l'ha svegliata non richiede un'azione, l'alert è dannoso.

Non si costruisce un data center di monitoraggio. Si mettono le tre-quattro cose che coprono quasi tutto.

## Il minimo che copre quasi tutto

| Cosa | Perché è la prima | Costo |
| ---- | ----------------- | ----- |
| Controllo esterno di disponibilità (uptime) | è l'unico che funziona quando la macchina è morta: il monitoraggio interno cade insieme al sistema che sorveglia | minuti, spesso gratis |
| Alert su spazio disco | è la causa più banale e più frequente di servizio fermo: log che crescono, backup che si accumulano | una riga |
| Log applicativi persistenti, con rotazione | senza rotazione riempiono il disco e diventano essi stessi il guasto | configurazione |
| Notifica sugli errori applicativi (Sentry o equivalente) | si scopre il bug dal messaggio invece che dall'email di un cliente | mezz'ora |
| Scadenza dei certificati TLS | il guasto più prevedibile che esista, e sistematicamente dimenticato | una riga |

Metriche di sistema (CPU, RAM, I/O) servono a **diagnosticare**, raramente ad allertare. Prometheus e Grafana si aggiungono quando c'è una domanda a cui oggi non si sa rispondere — non per completezza. Vanno mantenuti, e su un progetto piccolo il costo di gestione supera il beneficio.

## La regola degli alert

**Un alert che non richiede un'azione va tolto, non silenziato.** Gli alert ignorati addestrano il team a ignorare anche quello vero: è il modo esatto in cui il monitoraggio smette di funzionare pur restando acceso.

Per ogni alert proposto, chiedi: cosa fa la persona che lo riceve alle tre di notte? Se la risposta è «guarda e torna a dormire», non è un alert.

## Log: cosa serve davvero

Timestamp, livello, e **un identificativo che permetta di seguire una richiesta** attraverso i servizi. Con log strutturati si può cercare; con righe di testo libero si può solo leggere.

Cosa non deve entrare nei log: password, token, numeri di carta, dati personali. Dove un dato personale finisce nei log **parla Vera**; se quel log è esposto, sulla superficie esposta parla **Kai**. Bruno dice come si configurano rotazione, livelli e destinazione.

## Forma dell'output

I tre-quattro controlli che metteresti **su questo sistema**, in ordine, ciascuno con il costo di attivazione. Poi cosa **non** metteresti e perché.

Se il progetto è personale e l'utente è l'unico utente, l'esito legittimo è: «un controllo di disponibilità e la notifica sugli errori. Basta.»

## Trappole

- **La dashboard che nessuno guarda.** Un grafico non è monitoraggio: il monitoraggio è ciò che ti chiama.
- **Il monitoraggio che gira sulla macchina che deve sorvegliare.** Cade insieme a lei.
- **Log a livello `debug` in produzione**: riempiono il disco e nascondono gli errori veri.
- **Tracciamento distribuito su due servizi.** È lo strumento giusto per il problema di qualcun altro.
