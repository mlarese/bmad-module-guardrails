---
name: scelta-database
description: Confronta candidati attuali per un workload e restituisce una scelta condizionata, non una classifica.
code: DB
added: 2026-08-09
type: prompt
---

# Scelta del database

## Esito

Una shortlist di due-cinque candidati che il team può confrontare e provare: requisiti, evidenze
live, trade-off, raccomandazione, condizioni che la invalidano e verifica successiva.

## Panorama da tenere aperto

Considera la categoria prima del nome. A seconda del problema, i candidati possono includere:

- relazionale: PostgreSQL, Oracle Database, MySQL/MariaDB, SQL Server, SQLite e DuckDB;
- managed o distributed SQL: Aurora, AlloyDB, CockroachDB, YugabyteDB, TiDB e Google Spanner;
- documentale e key-value: MongoDB, DynamoDB, Couchbase, CouchDB, Cosmos DB, Redis e Valkey;
- wide-column e throughput distribuito: Cassandra, ScyllaDB e Aerospike;
- search e analytics: Elasticsearch, OpenSearch, ClickHouse, BigQuery, Snowflake, Redshift,
  Databricks/Delta e Apache Iceberg;
- graph e time-series: Neo4j, Neptune, ArangoDB, TimescaleDB, InfluxDB e QuestDB;
- vector e hybrid search: pgvector, Qdrant, Milvus, Weaviate, Pinecone, Vespa, Chroma,
  LanceDB e le capacità vector di MongoDB, Redis, Elasticsearch e OpenSearch.

Questo catalogo orienta la ricerca, non certifica feature, prezzi o maturità. Per la scelta
concreta verifica live engine, versione, piano, regione, licenza, supporto e percorso di uscita.

## Criterio

Pesa solo ciò che può cambiare la decisione: invarianti e transazioni, pattern di query, modello
di consistenza, scala verticale/orizzontale, latenza, disponibilità multi-regione, recovery,
operazioni, skill del team, costi variabili, lock-in, compliance applicabile e migrazione.
Se un candidato vince solo su una feature che il workload non usa, non ha vinto.

## Forma del verdetto

1. «Sceglierei X per queste assunzioni».
2. «Y resta la seconda scelta se cambia questa condizione».
3. «Z lo escludo per questo costo o failure mode».
4. «Verifica prima di impegnarti: questa prova sul workload e questo dato live».

Separare sempre motore, servizio managed, modalità di deploy e vendor. Una compatibilità SQL o
un'API simile non implica stessa semantica di transazione, stesso optimizer o stessa portabilità.
