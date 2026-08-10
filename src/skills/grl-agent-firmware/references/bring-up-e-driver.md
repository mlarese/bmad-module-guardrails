---
name: bring-up-e-driver
description: Trasforma reset, scheda e periferica in un bring-up osservabile e in un driver con contratto verificabile.
code: BD
added: 2026-08-10
type: prompt
---

# Bring-up, startup e driver

## Esito

Un tecnico può seguire l'avvio dalla reset vector alla prima applicazione, distinguere un guasto
di alimentazione/clock/pinmux da un bug software e provare il driver senza dover indovinare cosa
è stato inizializzato. Il risultato deve contenere la sequenza di inizializzazione necessaria,
le dipendenze fra clock, GPIO, periferica e interrupt, le condizioni di errore e la misura che
dimostra il funzionamento.

## Startup e board

Verifica stack iniziale, vector table, reset handler, copia `.data`, azzeramento `.bss`, clock,
watchdog, brownout, memoria e passaggio al `main` o al kernel. Per Cortex-M la vector table e il
nome degli handler devono corrispondere alla variante del dispositivo; per altri core valgono il
manuale architetturale e il boot flow del vendor. Un handler weak o un default fault non è una
diagnosi: va reso osservabile con causa, registri e punto di arresto compatibili con la board.

Non saltare alimentazione, reset, pin multiplexing, livelli elettrici e clock per arrivare subito
all'API del driver. Il codice di inizializzazione deve rendere visibile quale periferica è pronta,
quale no e cosa succede se il dispositivo esterno non risponde.

## Periferiche e DMA

Leggi il reference manual e l'errata della revisione concreta. Per ogni registro usa i bit
riservati e i read/modify/write secondo contratto; non cancellare flag scrivendo un valore copiato
da un esempio per un'altra serie. Per un driver definisci ownership, formato, dimensione e durata
dei buffer, semantica dei timeout, allineamento, cache coherency, ordine degli eventi e recovery.

DMA non significa «più veloce» in automatico: verifica bus, burst, memoria accessibile, cache,
barriere, descrittori, interrupt di fine trasferimento e comportamento se il buffer è riusato
troppo presto. Un test deve poter rilevare dati persi, duplicati, fuori ordine e periferica che
resta bloccata.

## Prova su hardware

Se il target reale non è disponibile, separa ciò che può essere testato su host/simulatore da ciò
che richiede pin, clock, analogica, DMA o timing reale. Chiedi log seriale, misura di alimentazione,
analizzatore logico o oscilloscopio solo quando quel dato cambia il verdetto. Un bring-up chiuso
ha una condizione di successo osservabile, una condizione di timeout e un modo di ripartire senza
perdere la causa del primo errore.
