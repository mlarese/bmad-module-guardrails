---
name: migrazione-e-benchmark
description: Porta una scelta o migrazione da ipotesi a prova riproducibile, cutover reversibile e criteri di stop.
code: MG
added: 2026-08-09
type: prompt
---

# Migrazione e benchmark

## Esito

Un piano che conserva la fonte di verità fino al cutover, dimostra equivalenza dei dati e delle
query, misura il carico rappresentativo e rende possibile fermarsi o tornare indietro.

## Migrazione

Inventaria schema, tipi, funzioni, trigger, job, dipendenze, query, volumi e ownership. Separa
compatibilità sintattica da compatibilità semantica. Decidi chi è la fonte durante backfill e
CDC, come si rilevano gap e duplicati, quale finestra di cutover serve e come si congela o si
riapre una scrittura.

Dual write è un rischio, non un piano: se lo proponi, definisci idempotenza, ordine, retry,
dead-letter, riconciliazione e condizione di stop. Preferisci shadow read, checksum, conteggi,
invarianti e replay a un «sembra uguale». Non rimuovere il vecchio sistema finché restore,
rollback e osservabilità non sono provati.

## Benchmark

Blocca prima la domanda: quale decisione deve cambiare? Usa dati anonimizzati ma rappresentativi,
query vere, mix read/write, cardinalità, skew, concorrenza, warm/cold state, failure test e costo.
Registra engine/versione, driver, schema, indice, hardware, regione, tuning e dataset. Riporta
throughput, p50/p95/p99, errori, CPU, memoria, I/O, storage e costo; non ridurre tutto a QPS.

Un benchmark vendor o sintetico può generare un'ipotesi, non chiudere la decisione. Definisci
pass/fail, finestra di osservazione, rollback e cosa fare se i risultati sono incompatibili.
