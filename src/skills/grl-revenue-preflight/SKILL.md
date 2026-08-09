---
name: grl-revenue-preflight
description: Prepara il gate PMS e Channel Manager. Usala quando l'utente dice "fai il preflight revenue", "verifica la pubblicazione tariffe" o "manda le tariffe in dry-run".
---

# Revenue Publication Preflight

## Overview

Prepara un gate tecnico e operativo prima di tradurre un piano revenue in prezzi pubblicabili.
Agisci in sola lettura o sandbox: `grl-agent-revenue` verifica il dominio PMS/Channel Manager,
mentre il workflow conserva mapping, evidenze, response, riconciliazione, idempotenza e rollback.

Il consumatore è chi autorizza una pubblicazione senza aver seguito il lavoro: deve vedere target,
scope, contratto, dati non noti, prove del test e motivo del verdetto.

## Resolution rules

- I percorsi interni alla skill sono bare paths dalla radice installata.
- `{project-root}` è la directory del progetto.
- `{output_folder}` arriva dalla configurazione core e contiene già `{project-root}`.
- `{preflight}` è `{output_folder}/revenue/{slug}`.

## In attivazione

Risolvi la configurazione con `uv run {project-root}/_bmad/scripts/resolve_config.py -p {project-root} -k core`.
Leggi `plan.md` e `audit.md` se presenti prima di chiedere dati già raccolti. Ricava l'intento:

| Intento | Comportamento |
|---|---|
| `preflight` | Costruisce o aggiorna il gate senza inviare tariffe reali. |
| `resume` | Riprende il preflight esistente e non riapre un test già riconciliato senza motivo. |
| `validate` | Ricontrolla evidenze e stato in sola lettura. |

Se manca il piano, marca `plan_status: missing` e valuta soltanto i prerequisiti presenti. Se
`grl-agent-revenue` manca, registra `missing_capability` e lascia il gate `blocked`.

## Stato di lavoro

La cartella persistente è `{preflight}`. Mantieni `preflight.md` con target, scope, versioni,
mapping, perimetro temporale, stato di ogni controllo, evidenza, owner, approvazione e rollback.
Non conservare credenziali, token o segreti.

## Gate tecnico

Il preflight deve rendere espliciti:

- contratto/API, PMS e Channel Manager, connettore, versione, autenticazione, endpoint, schema,
  limiti e frequenza;
- property ID, room type ID, rate plan ID e mapping osservati in sola lettura;
- inventario, occupazione, disponibilità, date, tasse, fee, trattamento, valuta e timezone;
- modello per-data o length-of-stay (LOS), restrizioni e semantica `delta`/`overlay`/`remove`;
- request, response, warning/errori, latenza, logging, monitoraggio e riconciliazione;
- test read-only, sandbox o `validate_only`, replay idempotente e rollback verso l'ultimo set valido.

Un campo non provato è `non noto`, non un'inferenza dal nome del prodotto. Il test di idempotenza
deve dimostrare che ripetere lo stesso change set non duplica né sovrascrive effetti estranei; la
riconciliazione deve confrontare atteso e ricevuto; il rollback deve indicare owner e set valido.

Il verdetto è `GO`, `GO_CON_CONDIZIONI`, `NO_GO` o `EVIDENZA_INSUFFICIENTE`. `GO` richiede evidenza
propria per ogni controllo, test concluso, scope delimitato e approvazione esplicita. Se una sola
voce decisiva è `non noto`, il gate non autorizza l'invio. Il workflow non pubblica, non chiede
credenziali e non chiama API reali; può consegnare un payload o diff per un successivo dry-run
autorizzato da `grl-automation`.

## Finalize

Controlla che ogni stato abbia una prova, che il piano non venga confuso con l'esito del test e
che nessun output dica “integrazione pronta” senza contratto e riconciliazione. Se `bmad-review`
è disponibile, usalo solo per la prosa. Chiudi con:

```json
{"status":"complete|blocked","folder":"{preflight}","verdict":"GO|GO_CON_CONDIZIONI|NO_GO|EVIDENZA_INSUFFICIENTE"}
```
