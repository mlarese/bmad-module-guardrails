---
name: relazionali-e-distribuiti
description: Progetta persistenza relazionale e distributed SQL con transazioni, indici, partizioni e replica espliciti.
code: SQL
added: 2026-08-09
type: prompt
---

# Relazionale e distributed SQL

## Esito

Una forma fisica coerente con il carico: chiavi e vincoli, isolamento, transazioni, indici,
partizioni, piani di query, pool di connessioni, replica, failover e limiti dichiarati del
motore/servizio scelto.

## Domande decisive

- Quale interleaving concorrente deve essere impossibile? Quale conflitto può essere ritentato?
- Il read-after-write deve attraversare una replica o può essere eventualmente consistente?
- La partizione serve per pruning, retention, isolamento o distribuzione? Qual è la chiave che
  evita partizioni calde e rende la query sargable?
- Il collo di bottiglia è CPU, I/O, lock, WAL/log, memoria, connessioni, rete, indice o storage?
- Il failover conserva la semantica richiesta? Il restore è stato provato nella stessa edizione?

## Famiglie da confrontare

PostgreSQL, Oracle, MySQL/MariaDB, SQL Server e SQLite hanno semantiche, optimizer, estensioni,
strumenti e modalità operative diverse. CockroachDB, YugabyteDB, TiDB e Spanner aggiungono
distribuzione e consistenza con costi di latenza, topologia, compatibilità e operatività che vanno
verificati sul caso concreto. Aurora, AlloyDB e piattaforme PostgreSQL-compatibili non sono
automaticamente equivalenti al motore upstream.

Non promettere portabilità da una sintassi comune. Verifica DDL, transazioni, isolation level,
funzioni, tipi, planner, driver, migrazioni, CDC, backup, estensioni, quote e licenze nella
versione e nel piano realmente acquistabili.
