---
name: grl-revenue-plan
description: Costruisce scenari di pricing, domanda e profitto revenue alberghieri separando floor economico, base di mercato e forecast, con trigger di monitoraggio e senza pubblicare tariffe. Usala quando l'utente dice "prepara un piano revenue", "consigliami il prezzo", "costruisci scenari di domanda", chiede a quanto vendere una data o un periodo, vuole confrontare ipotesi di tariffa, o deve decidere fra margine e occupazione. Il gate tecnico verso PMS e Channel Manager resta di `grl-revenue-preflight`.
---

# Revenue Plan

## Panoramica

Trasforma un audit, un dataset o una domanda commerciale in un piano revenue con scenari e
trigger di monitoraggio. Agisci come coordinatore: `grl-agent-revenue` possiede il giudizio su
KPI, domanda, QuoProfit/RevD, pricing e profitto; il workflow rende la decisione auditabile e
non pubblica tariffe.

Il consumatore deve poter scegliere uno scenario sapendo quali dati lo sostengono, quale ipotesi
lo fa cambiare e quale controllo serve prima di passare al preflight.

## Regole di risoluzione

- I percorsi interni alla skill sono bare paths dalla radice installata.
- `{project-root}` è la directory del progetto.
- `{output_folder}` arriva dalla configurazione core e contiene già `{project-root}`.
- `{slug}` è lo stesso dell'audit da cui il piano nasce. Se l'audit non c'è, ricavalo dal nome che
  l'utente dà al lavoro, in kebab-case, dopo aver elencato le cartelle già presenti sotto
  `{output_folder}/revenue/`: uno slug nuovo per un lavoro esistente separa il piano dal suo audit.
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

**La cartella è condivisa con `grl-revenue-audit` e `grl-revenue-preflight`.** Scrivi soltanto
`plan.md`: `audit.md` e `preflight.md` si leggono e non si modificano. Rileggi `plan.md`
immediatamente prima di scriverlo e, se è cambiato rispetto a quando lo hai letto, fermati e
dichiaralo invece di sovrascrivere il lavoro di un'altra esecuzione.

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

## Revisione editoriale finale

Prima di consegnare, rileggi ogni output destinato a una persona e correggi solo la prosa:
chiarezza, grammatica, coesione, tono e terminologia. Se `bmad-review` è disponibile, invocalo con
`lenses=prose`, la lingua dell'output e `reader_type=humans`; altrimenti fai il controllo a mano e
prosegui.

Restano invariati fatti, conclusioni, severità, fonti, citazioni, riferimenti normativi o clinici,
decisioni, stati, numeri e testo fornito dall'utente — e con essi codice, comandi, dati strutturati,
frontmatter, URL, identificatori, date, formule e righe di memoria. Nei file HTML e Markdown si
revisiona solo la prosa leggibile, non il markup. La revisione è interna: consegna il testo già
corretto, non la tabella del revisore.
