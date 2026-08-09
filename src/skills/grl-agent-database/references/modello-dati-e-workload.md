---
name: modello-dati-e-workload
description: Traduce requisiti, invarianti e query in un modello dati logico e fisico verificabile.
code: MD
added: 2026-08-09
type: prompt
---

# Modello dati e workload

## Esito

Un modello che dice cosa il sistema deve conservare, quali invarianti non può violare, quali
letture e scritture deve servire e quale forma fisica le rende verificabili. Non è un ERD
decorativo: è un contratto fra dominio, applicazione e persistenza.

## Cosa deve essere vero

- Entità, identità, ownership, cardinalità, lifecycle e confini di tenant sono nominati senza
  affidarsi a un campo `note` o a JSON libero quando il dato deve essere cercabile o vincolato.
- Ogni invariant importante ha un proprietario: vincolo del database, transazione, codice o
  processo di riconciliazione. Se è solo «una regola dell'app», dichiaralo come rischio.
- Le query critiche sono rappresentate con filtri, join, ordinamenti, aggregazioni, paginazione,
  cardinalità e frequenza; le scritture con batch, concorrenza, idempotenza e contention.
- Sono espliciti volume attuale, crescita, hot key, retention, dimensione degli indici, picchi,
  tenant grandi e distribuzione geografica.
- Consistenza, isolamento, latenza p95/p99, throughput, disponibilità, RPO, RTO e budget non
  restano aggettivi: hanno un target o sono marcati `da verificare`.

## Decisione

Produci prima il modello logico e gli access path. Poi scegli normalizzazione, embedding,
denormalizzazione, materialized view, read model, cache o indice specializzato come risposta a
una query o a un failure mode concreto. Per ogni deviazione dal modello più semplice spiega cosa
compra e chi mantiene la sincronizzazione.
