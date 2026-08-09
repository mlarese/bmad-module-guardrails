---
name: grl-revenue-plan
description: Pianifica pricing e scenari revenue alberghieri. Usala quando l'utente dice "prepara un piano revenue", "consigliami il prezzo" o "costruisci scenari di domanda".
---

# Revenue Plan

## Overview

Trasforma un audit, un dataset o una domanda commerciale in un piano revenue con scenari e
trigger di monitoraggio. Agisci come coordinatore: `grl-agent-revenue` possiede il giudizio su
KPI, domanda, QuoProfit/RevD, pricing e profitto; il workflow rende la decisione auditabile e
non pubblica tariffe.

Il consumatore deve poter scegliere uno scenario sapendo quali dati lo sostengono, quale ipotesi
lo fa cambiare e quale controllo serve prima di passare al preflight.

## Resolution rules

- I percorsi interni alla skill sono bare paths dalla radice installata.
- `{project-root}` è la directory del progetto.
- `{output_folder}` arriva dalla configurazione core e contiene già `{project-root}`.
- `{plan}` è `{output_folder}/revenue/{slug}`.

## In attivazione

Risolvi la configurazione con `uv run {project-root}/_bmad/scripts/resolve_config.py -p {project-root} -k core`.
Leggi il profilo condiviso e le decisioni se presenti. Se esiste `{plan}/audit.md` o
`{plan}/plan.md`, leggilo prima di chiedere o riscrivere dati.

| Intento | Comportamento |
|---|---|
| `plan` | Costruisce o aggiorna gli scenari dal contesto fornito. |
| `resume` | Riprende il piano esistente e conserva decisioni e ipotesi già approvate. |
| `validate` | Controlla coerenza, formule, fonti e condizioni senza proporre nuovi prezzi. |

Se l'audit manca, usa i dati disponibili come input read-only e marca `audit_status: missing`;
non inventare una validazione precedente. Se `grl-agent-revenue` manca, registra
`missing_capability` e `handoff_status: pending`.

## Stato di lavoro

La cartella persistente è `{plan}`. Mantieni `plan.md` con obiettivo, periodo, fonte dell'audit,
scenari, assunzioni, trigger, metriche, approvazioni e stato. Un piano aggiornato non cancella
le decisioni precedenti: registra il cambiamento e la sua ragione.

## Piano

Il piano deve separare almeno:

- `floor_economico`: costo, margine minimo e regola QuoProfit/RevD, esplicitamente interna;
- `base_mercato`: ADR/RMC, competitive set o rate plan solo se comparabili e verificati;
- `domanda_prevista`: pickup, booking curve, forecast, eventi e relativo errore;
- `scenari`: prezzo o range condizionato a dati e trigger, non una media inventata;
- `decisione`: scenario preferito, segmento/canale, durata, entità e motivazione;
- `monitoraggio`: metrica, finestra, soglia, owner e azione correttiva;
- `gate`: dati mancanti, autorizzazione e passaggio a `grl-revenue-preflight`.

MUP e MOL non sono standard universali né prova del prezzo ottimale. Non trasformare un floor in
una previsione della willingness to pay e non trasformare un forecast isolato in un ordine di
alzare la tariffa. Se il denominatore è zero, il dato è non noto o il competitive set non è
comparabile, conserva scenari `blocked` o `EVIDENZA_INSUFFICIENTE`.

Il workflow può preparare un change set descrittivo, ma non invia prezzi, non modifica PMS e non
usa autorizzazioni implicite. Per il gate tecnico instrada a `grl-revenue-preflight`; per
automazioni ripetibili può passare un piano a `grl-automation` con scope e rollback.

## Finalize

Verifica formule, unità, periodo, valuta, arrotondamento, perimetro, fonti, ipotesi e condizioni
di stop. Se `bmad-review` è disponibile, usalo solo per la prosa. Chiudi con:

```json
{"status":"complete|blocked","folder":"{plan}","verdict":"READY_FOR_PREFLIGHT|EVIDENZA_INSUFFICIENTE|NO_GO"}
```
