---
name: prestazioni-affidabilita
description: Diagnostica colli di bottiglia e progetta SLO, HA, DR, backup, restore e osservabilità del database.
code: PR
added: 2026-08-09
type: prompt
---

# Prestazioni e affidabilità

## Esito

Un piano di verifica ordinato per impatto: sintomo osservato, misura mancante, ipotesi, test
read-only, modifica minima, costo, rollback e soglia che chiude il lavoro.

## Ordine della diagnosi

Parti da query e transazioni reali: `EXPLAIN`/piano, cardinalità stimata e osservata, selectivity,
join, sort, scansione, lock, deadlock, cache hit, I/O, CPU, memoria, connessioni, WAL/log,
replication lag e hot key. Non aggiungere un indice prima di sapere quale query serve, quanto
costa in scrittura/storage e se il planner può usarlo.

Poi collega la misura al failure mode: perdita di nodo, perdita di zona/regione, restore lento,
corruzione, schema deployato a metà, spike, coda di connessioni o cache incoerente. Definisci
RPO/RTO, p95/p99, throughput, error budget, retention, backup immutabile e drill di restore.

Replica, read scaling, sharding, partitioning, caching, CDC e multi-region sono strumenti con
semantica e costi diversi. Per ciascuno esplicita cosa succede durante il ritardo, il failover,
la riconciliazione e il ritorno alla normalità. Capacity e configurazione del cluster restano di
Bruno; Dario definisce il comportamento dei dati e i target che il cluster deve sostenere.
