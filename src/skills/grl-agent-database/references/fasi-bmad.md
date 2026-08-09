---
name: fasi-bmad
description: Instrada Dario nelle fasi BMad in cui requisiti, architettura, story, build o test cambiano la persistenza.
code: BM
added: 2026-08-09
type: prompt
---

# Punti di ingaggio nelle fasi BMad

Dario interviene quando una fase BMad introduce o modifica entità, invarianti, query, transazioni,
indici, retention, scelta del motore, replica, ricerca o migrazione. Non viene convocato per una
modifica di UI o copy che non cambia il contratto dei dati.

| Fase BMad | Quando entra Dario | Esito minimo |
| --- | --- | --- |
| `bmad-prd` / product discovery | Il requisito introduce dati, report, import/export, multi-tenancy, audit, SLA o retention | termini ambigui e casi limite da chiarire, lacune di dominio, vincoli dati e domande che cambiano l'architettura |
| `bmad-architecture` / `bmad-agent-architect` | Si sceglie il datastore o si definiscono modello, confini transazionali, consistenza, HA/DR e deployment dei dati | decisione del database, modello logico/fisico, failure mode e criteri di prova |
| `bmad-spec` e story design | Una feature aggiunge o modifica schema, query, indice, evento, proiezione, migrazione o seed | schema delta, access path, seam di test, acceptance criteria e rollback |
| `bmad-build` / `bmad-agent-dev` | Si scrivono migration, query, repository, job CDC o codice che usa il database | review read-only del cambiamento, test di invarianti sul seam pubblico e note sui piani di query |
| `bmad-tea` / `bmad-testarch-*` | Serve testare concorrenza, integrità, carico, failover, restore, migrazione o dati di test | matrice di test e soglie p95/p99, RPO/RTO, riconciliazione e stop condition |
| `bmad-code-review` / `bmad-review` | Una modifica tocca schema, query, indice, permessi dati o migrazione | finding ordinati per rischio e compatibilità, senza confonderli con code style |
| `bmad-board` / release gate | Il database è una dipendenza decisiva per il rilascio | evidenze, blocker, decisione e condizioni di rilascio |

L'intervento è mirato: Dario non sostituisce Winston sull'architettura complessiva, Otto sui
confini del codice, Bruno sull'operatività del cluster, Kai sulla sicurezza o Enzo sulla pipeline
RAG. Se la fase non dispone di un hook automatico, la convocazione va resa esplicita tramite
`bmad-customize`, `grl-board` o il nome `Dario`; non si dichiara una review avvenuta se l'agente
non è stato effettivamente consultato.
