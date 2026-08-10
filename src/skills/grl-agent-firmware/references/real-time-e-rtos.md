---
name: real-time-e-rtos
description: Progetta il confine fra ISR, task e DMA con timing, priorità, memoria e recovery misurabili.
code: RT
added: 2026-08-10
type: prompt
---

# Real-time, RTOS e concorrenza

## Esito

Il team sa chi esegue cosa, con quale priorità e budget, come passano gli eventi e cosa accade
quando un produttore è più veloce del consumatore. La decisione può essere bare-metal, superloop,
RTOS o una combinazione: non si sceglie un kernel perché il progetto «sembra serio».

## Il contratto temporale

Rendi numerici periodo, deadline, worst-case execution time, latenza di interrupt, jitter,
frequenza di campionamento, durata dei critical section e tempo massimo senza feed del watchdog.
Se non sono noti, definisci la misura e il limite che deve ancora essere concordato. La media non
chiude un requisito hard real-time.

## ISR, task e messaggi

L'ISR riconosce l'evento, cattura il minimo stato necessario e consegna lavoro a un contesto che
può bloccare, loggare o fare parsing. Verifica priorità, nesting, mascheramento, inversione di
priorità, starvation, deadlock, livelock, race, perdita di eventi e sovraccarico quando il buffer
si riempie. Specifica se una coda è bounded, quale dato viene scartato e come l'errore arriva a
chi può reagire.

Per FreeRTOS, Zephyr o altro RTOS, tratta scheduler, API ISR-safe, tick, timer, notifiche,
semafori, mutex, code, allocatore e porting come semantica di versione da verificare nella
documentazione del kernel. Non trasferire un esempio di un RTOS a un altro per analogia.

Misura lo stack per task e il margine reale; separa heap statico e dinamico; considera cache,
barriere e memoria condivisa su multicore. Il watchdog deve distinguere un task lento da un sistema
bloccato e deve lasciare abbastanza evidenza per capire il reset successivo.

## Energia e degradazione

Sleep, wake-up, clock gating e retention cambiano la semantica di periferiche, timer, DMA e
comunicazioni. Definisci chi può svegliare il sistema, cosa viene ricostruito e quale dato sopravvive
al reset. Un errore di sensore o di rete deve portare a uno stato definito, non a un loop infinito
che nasconde il guasto.
