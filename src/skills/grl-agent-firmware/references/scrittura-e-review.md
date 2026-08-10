---
name: scrittura-e-review
description: Porta una modifica firmware da intenzione a codice o finding verificabile da un altro tecnico.
code: FW
added: 2026-08-10
type: prompt
---

# Scrittura e review firmware

## Esito

Il consumatore è un firmware engineer che deve poter compilare, testare e portare la modifica
su una board senza questa conversazione. Consegna una patch o una review che nomina target,
assunzioni, contratto hardware, risorse consumate, comportamento in errore, prova e criterio di
accettazione. Se il materiale non basta, consegna il dato mancante che sblocca il lavoro invece
di inventare registri, pin o valori di timing.

## Contratto minimo

Raccogli solo i fatti che possono cambiare il risultato: MCU/SoC e revisione, board, datasheet e
reference manual, toolchain e versione, build system, startup/linker script, SDK/HAL/BSP, RTOS,
periferiche e pin, layout flash/RAM, frequenza, clock, interrupt, DMA/cache, vincoli di latenza,
stack/heap, consumo, watchdog, aggiornamento e criticità del prodotto.

Un dato assente resta `non noto`. Distingui sempre:

- **osservato:** presente nel codice, nel log, nel datasheet o nella misura;
- **assunto:** necessario per procedere ma non ancora confermato;
- **da verificare:** prova, versione o comportamento che chiuderà l'incertezza.

## Codice che regge

Controlla il contratto di memoria e tempo: tipi di larghezza esplicita, signedness, overflow,
allineamento, endianess, packing, lifetime e ownership dei buffer, `volatile` solo dove protegge
un accesso realmente asincrono o memory-mapped, sezioni linker e inizializzazione prima dell'uso.
Un timeout deve avere unità, origine del clock e comportamento di errore; una conversione deve
dire cosa succede fuori range; un registro deve avere maschera, shift e valore documentati.

Tieni separati ISR, driver, protocollo e logica di dominio quando il confine compra testabilità o
controllo del timing. Non introdurre wrapper e HAL per gusto: ogni astrazione deve nascondere un
contratto reale. Non ottimizzare a occhio: se il rischio è timing, stack, flash o energia, indica
la misura che lo dimostra.

## Forma della review

Ordina da tre a cinque finding per rischio concreto. Ogni finding contiene posizione precisa,
evidenza, conseguenza sul device o sulla produzione, correzione minima e prova che lo chiude.
Se non ci sono problemi sostenuti dal materiale, restituisci `nessun finding verificabile` e
indica cosa non è stato possibile osservare. Non chiamare «critico» un problema senza spiegare
quale funzione o failure mode colpisce.

Una patch non è finita perché compila: esplicita la prova host, simulata o su hardware, il log o
la misura attesa, il comportamento al reset e la via di ritorno. Flashing, erase, modifica di
fuse/option byte e sostituzione di bootloader restano azioni esplicite, non effetti collaterali.
