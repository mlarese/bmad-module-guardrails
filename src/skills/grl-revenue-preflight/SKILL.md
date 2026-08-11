---
name: grl-revenue-preflight
description: Gate tecnico e operativo prima di trasformare un piano revenue in tariffe pubblicabili — contratto e API, mapping di property, room type e rate plan, semantica per-data o LOS, dry-run, riconciliazione, idempotenza e rollback. Usala quando l'utente dice "fai il preflight revenue", "verifica la pubblicazione tariffe", "manda le tariffe in dry-run", chiede se l'integrazione con il PMS o il Channel Manager è pronta, o vuole sapere cosa manca prima di inviare i prezzi. Non pubblica, non chiede credenziali e non chiama API reali.
---

# Revenue Publication Preflight

## Panoramica

Prepara un gate tecnico e operativo prima di tradurre un piano revenue in prezzi pubblicabili.
Agisci in sola lettura o sandbox: `grl-agent-revenue` verifica il dominio PMS/Channel Manager,
mentre il workflow conserva mapping, evidenze, response, riconciliazione, idempotenza e rollback.

Il consumatore è chi autorizza una pubblicazione senza aver seguito il lavoro: deve vedere target,
scope, contratto, dati non noti, prove del test e motivo del verdetto.

## Regole di risoluzione

- I percorsi interni alla skill sono bare paths dalla radice installata.
- `{project-root}` è la directory del progetto.
- `{output_folder}` arriva dalla configurazione core e contiene già `{project-root}`.
- `{slug}` è lo stesso del piano che il gate verifica. Se il piano manca, ricavalo dal nome che
  l'utente dà al lavoro, in kebab-case, dopo aver elencato le cartelle già presenti sotto
  `{output_folder}/revenue/`: un gate su uno slug nuovo non verifica niente.
- `{preflight}` è `{output_folder}/revenue/{slug}`.

## In attivazione

Risolvi la configurazione con `uv run {project-root}/_bmad/scripts/resolve_config.py -p {project-root} -k core`.
Leggi `plan.md` e `audit.md` se presenti prima di chiedere dati già raccolti. Ricava l'intento:

| Intento | Comportamento |
|---|---|
| `preflight` | Costruisce o aggiorna il gate senza inviare tariffe reali. |
| `resume` | Riprende il preflight esistente. Un test già riconciliato si riapre solo per uno di questi motivi, che va scritto accanto alla riapertura: versione del connettore cambiata, mapping cambiato, scope temporale diverso, rate plan nuovo o modificato. |
| `validate` | Ricontrolla evidenze e stato in sola lettura. |

Se manca il piano, marca `plan_status: missing` e valuta soltanto i prerequisiti presenti. Se
`grl-agent-revenue` manca, registra `missing_capability` e lascia il gate `blocked`.

## Stato di lavoro

La cartella persistente è `{preflight}`. Mantieni `preflight.md` con target, scope, versioni,
mapping, perimetro temporale, stato di ogni controllo, evidenza, owner, approvazione, rollback e le
due marcature che l'attivazione impone: `plan_status` e `missing_capability`, con il motivo accanto.
Non conservare credenziali, token o segreti.

**La cartella è condivisa con `grl-revenue-audit` e `grl-revenue-plan`.** Scrivi soltanto
`preflight.md`: `audit.md` e `plan.md` si leggono e non si modificano. Rileggi `preflight.md`
immediatamente prima di scriverlo e, se è cambiato rispetto a quando lo hai letto, fermati: un gate
sovrascritto da un'altra esecuzione autorizzerebbe una pubblicazione su evidenze non sue.

## Gate tecnico

Il preflight deve rendere espliciti:

- contratto/API, PMS e Channel Manager, connettore, versione, autenticazione, endpoint, schema,
  limiti e frequenza;
- **property ID, room type ID, rate plan ID e mapping** osservati in sola lettura — voce decisiva;
- inventario, occupazione, disponibilità, date, tasse, fee, trattamento, valuta e timezone;
- **modello per-data o length-of-stay (LOS)**, restrizioni e semantica `delta`/`overlay`/`remove` — voce decisiva;
- request, response, warning/errori, latenza, logging, monitoraggio e riconciliazione;
- test read-only, sandbox o `validate_only`, **replay idempotente** e **rollback** verso l'ultimo set valido — le ultime due sono voci decisive.

Un campo non provato è `non noto`, non un'inferenza dal nome del prodotto. Il test di idempotenza
deve dimostrare che ripetere lo stesso change set non duplica né sovrascrive effetti estranei; la
riconciliazione deve confrontare atteso e ricevuto; il rollback deve indicare owner e set valido.

Le **voci decisive** sono le quattro marcate qui sopra: mapping degli ID, semantica per-data/LOS,
idempotenza e rollback. Se una sola di esse è `non noto`, il gate non autorizza l'invio.

| Verdetto | Condizione | `status` |
| --- | --- | --- |
| `GO` | evidenza propria per ogni controllo, test concluso, scope delimitato, approvazione esplicita | `complete` |
| `GO_CON_CONDIZIONI` | tutte le voci decisive provate, ma restano azioni non bloccanti: elencale con responsabile, verifica e scadenza futura | `complete` |
| `NO_GO` | un controllo è stato eseguito ed è **fallito** — idempotenza che duplica, riconciliazione che diverge, rollback che non riporta indietro | `blocked` |
| `EVIDENZA_INSUFFICIENTE` | nessun controllo fallito, ma una voce decisiva resta `non noto` perché la prova non è ottenibile | `blocked` |

La differenza fra gli ultimi due è tutta qui: `NO_GO` è una prova negativa, `EVIDENZA_INSUFFICIENTE`
è una prova che manca. Il workflow non pubblica, non chiede
credenziali e non chiama API reali; può consegnare un payload o diff per un successivo dry-run
autorizzato da `grl-automation`.

## Finalize

Controlla che ogni stato abbia una prova, che il piano non venga confuso con l'esito del test e
che nessun output dica “integrazione pronta” senza contratto e riconciliazione. Se `bmad-review`
è disponibile, usalo solo per la prosa. Chiudi con:

```json
{"status":"complete|blocked","folder":"{preflight}","verdict":"GO|GO_CON_CONDIZIONI|NO_GO|EVIDENZA_INSUFFICIENTE","plan_status":"…","missing_capability":[]}
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
