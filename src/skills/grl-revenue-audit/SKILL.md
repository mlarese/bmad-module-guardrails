---
name: grl-revenue-audit
description: Audit dati e KPI revenue alberghieri. Usala quando l'utente dice "fai un audit revenue", "controlla i KPI dell'hotel" o "verifica questi dati di prenotazione".
---

# Revenue Audit

## Overview

Porta dati di prenotazione, inventario, costi e tariffe a un audit revenue leggibile da titolare,
revenue manager o team tecnico. Agisci come coordinatore read-only: convoca `grl-agent-revenue`
per formule e giudizio di dominio, conserva la provenienza dei dati e non trasforma un audit in una
pubblicazione.

Il consumatore deve poter distinguere dato osservato, calcolo, ipotesi, blocker e prossima verifica
senza riaprire questa conversazione.

## Resolution rules

- I percorsi interni alla skill sono bare paths dalla radice installata.
- `{project-root}` è la directory del progetto.
- `{output_folder}` arriva dalla configurazione core e contiene già `{project-root}`.
- `{audit}` è `{output_folder}/revenue/{slug}`.

## In attivazione

Risolvi la configurazione con `uv run {project-root}/_bmad/scripts/resolve_config.py -p {project-root} -k core`.
Se fallisce, usa italiano e i default espliciti. Leggi, se esistono, il profilo condiviso e le
decisioni in `{project-root}/_bmad/memory/grl-shared/`.

Ricava l'intento:

| Intento | Comportamento |
|---|---|
| `audit` | Avvia o aggiorna l'audit da un export, file o dati forniti. |
| `resume` | Legge prima l'audit esistente e continua senza creare una seconda cartella. |
| `validate` | È read-only, verifica l'audit contro le fonti e non lo dichiara più completo di quanto provato. |

Se manca `grl-agent-revenue`, registra `missing_capability` e `handoff_status: pending`; non
sostituire il suo giudizio con una risposta generica.

## Stato di lavoro

La cartella persistente è `{audit}`. Mantieni `audit.md` come fonte canonica con slug, timestamp,
fonti, periodo, valuta, perimetro, stato e decisioni. Non modificare o spostare export originali.
Se l'utente non chiede un artefatto persistente, restituisci il verdetto in conversazione e non
creare una cartella solo per registrare una risposta occasionale.

## Audit

Consegna un `audit.md` o un verdetto con questa sostanza:

- fonte e perimetro osservati: file, struttura, date, timezone, valuta e definizioni;
- qualità del dato: duplicati, cancellazioni/no-show, date, camere vendibili, out-of-order, mapping e campi `non noto`;
- KPI riproducibili con numeratore, denominatore, periodo, arrotondamento, IVA/commissioni e componenti incluse;
- lettura separata di stock, pickup, booking curve, forecast, canale, segmento e floor economico;
- finding classificati come `blocker`, `distorsione`, `opportunità` o `non verificato`;
- scenari condizionati e prossimo controllo, senza prezzo finale inventato.

Carica i riferimenti di `grl-agent-revenue` necessari al caso. MUP e MOL restano regole interne
QuoProfit/RevD, non standard universali né prova del prezzo ottimale. Se mancano dati decisivi,
lo stato è `EVIDENZA_INSUFFICIENTE` e l'audit indica esattamente la prova che lo sblocca.

Un audit non autorizza invii a PMS o Channel Manager: per quello instrada a
`grl-revenue-plan` e poi a `grl-revenue-preflight`.

## Finalize

Prima di consegnare, verifica che ogni numero abbia fonte e perimetro, che i dati mancanti siano
espliciti e che nessun finding sia presentato come decisione di prezzo. Se `bmad-review` è
disponibile, usalo solo per chiarezza della prosa: non può cambiare numeri, formule, stati o fonti.

Chiudi con una riga strutturata:

```json
{"status":"complete|blocked","folder":"{audit}","verdict":"READY_FOR_PLAN|EVIDENZA_INSUFFICIENTE"}
```
