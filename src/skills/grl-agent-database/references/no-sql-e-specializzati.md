---
name: no-sql-e-specializzati
description: Valuta document, key-value, wide-column, search, graph, time-series e analytics senza confondere il loro ruolo.
code: NS
added: 2026-08-09
type: prompt
---

# NoSQL e motori specializzati

## Esito

Un confine chiaro fra fonte di verità, proiezione e cache, con la consistenza e la ricostruibilità
di ogni copia dichiarate. Il nome della categoria non basta: il modello di accesso e il failure
mode devono giustificare la scelta.

## Assi di valutazione

- **Document:** embedding o riferimenti, atomicità entro documento e fra documenti, indici,
  resharding, query cross-document, schema evolution e dimensione dei documenti.
- **Key-value/cache:** durata, eviction, persistenza, ordering, atomicità, hot key, invalidazione,
  stampede e cosa succede se il dato sparisce. Redis/Valkey non diventano fonte degli ordini solo
  perché hanno latenza bassa.
- **Wide-column:** partition key, clustering, distribuzione, read/write path, tombstone,
  compaction, repair, consistenza e query ammesse. Non modellare Cassandra come un relational DB.
- **Search:** indice derivato, refresh, mapping, analyzer, BM25, filtri, replica, reindex e
  ritardo rispetto alla fonte. Elasticsearch/OpenSearch sono spesso search store, non il record
  canonico.
- **Graph:** pattern di traversamento, cardinalità, mutazioni, traversal latency e necessità di
  query ad hoc. Un grafo non è una scorciatoia per un modello relazionale poco capito.
- **Time-series/analytics:** retention, downsampling, ingest, finestre temporali, compressione,
  aggregazioni e separazione fra OLTP, OLAP e lakehouse. ClickHouse, DuckDB, TimescaleDB, InfluxDB
  e piattaforme cloud rispondono a carichi diversi.

Per MongoDB, DynamoDB, Couchbase, Cassandra/ScyllaDB e gli altri prodotti, verifica sempre la
semantica della versione corrente e del servizio gestito: le analogie di categoria non provano
intercambiabilità.
