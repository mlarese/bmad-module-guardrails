---
name: grl-revenue-audit
description: "Audit read-only di dati, KPI e prezzi revenue alberghieri, con fonti, formule, qualità del dato, blocker e dati mancanti. Usala quando l'utente dice \"fai un audit revenue\", \"controlla i KPI dell'hotel\", \"verifica questi dati di prenotazione\", porta un export del PMS o del Channel Manager da leggere, chiede se occupazione, ADR, RevPAR o TRevPAR sono calcolati bene, o vuole capire cosa non torna nei numeri prima di decidere una tariffa. Non pubblica prezzi e non decide lo scenario: per quello ci sono `grl-revenue-plan` e `grl-revenue-preflight`."
---

# Revenue Audit

## Panoramica

Porta dati di prenotazione, inventario, costi e tariffe a un audit revenue leggibile da titolare,
revenue manager o team tecnico. Agisci come coordinatore **read-only sui sistemi sorgente** — export, PMS, Channel Manager non si toccano mai; l'audit invece scrive il proprio `audit.md`. Convoca `grl-agent-revenue`
per formule e giudizio di dominio, conserva la provenienza dei dati e non trasforma un audit in una
pubblicazione.

Il consumatore deve poter distinguere dato osservato, calcolo, ipotesi, blocker e prossima verifica
senza riaprire questa conversazione.

## Regole di risoluzione

- I percorsi interni alla skill sono bare paths dalla radice installata.
- `{project-root}` è la directory del progetto.
- `{output_folder}` arriva dalla configurazione core e contiene già `{project-root}`.
- `{slug}` è il nome del lavoro in kebab-case **come lo chiama l'utente** — di norma la struttura, o
  la struttura e il periodo. Prima di aprire una cartella nuova elenca quelle già presenti sotto
  `{output_folder}/revenue/` e cerca la sua: uno slug coniato due volte perde l'audit e con esso il
  piano che ci si appoggia. Se non riesci a ricavarlo, chiedilo; non inventarlo dal nome di un file.
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
| `validate` | Non scrive nemmeno `audit.md`: verifica l'audit esistente contro le fonti e non lo dichiara più completo di quanto provato. |

Se manca `grl-agent-revenue`, registra `missing_capability` e `handoff_status: pending`; non
sostituire il suo giudizio con una risposta generica.

## Stato di lavoro

La cartella persistente è `{audit}`. Mantieni `audit.md` come fonte canonica con slug, timestamp,
fonti, periodo, valuta, perimetro, stato e decisioni. Non modificare o spostare export originali.

**La cartella è condivisa con `grl-revenue-plan` e `grl-revenue-preflight`.** Scrivi soltanto
`audit.md`: `plan.md` e `preflight.md` appartengono agli altri due e non si toccano nemmeno per
correggerli. Rileggi `audit.md` immediatamente prima di scriverlo e, se è cambiato rispetto a quando
lo hai letto, fermati e dichiaralo: un'altra esecuzione sta lavorando sullo stesso slug, e
sovrascriverla perderebbe il suo lavoro. Uno stato incoerente è un blocco, non un'autorizzazione a
riscrivere.
Se l'utente non chiede un artefatto persistente, restituisci il verdetto in conversazione e non
creare una cartella solo per registrare una risposta occasionale.

## Audit

Consegna un `audit.md` o un verdetto con questa sostanza:

- fonte e perimetro osservati: file, struttura, date, timezone, valuta e definizioni;
- qualità del dato: duplicati, cancellazioni/no-show, date, camere vendibili, out-of-order, mapping e campi `non noto`;
- KPI riproducibili con numeratore, denominatore, periodo, arrotondamento, IVA/commissioni e componenti incluse;
- lettura separata di stock, pickup, booking curve, forecast, canale, segmento e floor economico;
- finding classificati come `blocker`, `distorsione`, `opportunità` o `non verificato`;
- scenari condizionati e prossimo controllo, senza prezzo finale inventato;
- **capability mancanti e handoff pendenti**: una voce per ciascuno, con nome, motivo, impatto sul
  verdetto e prossimo passo. È qui che finiscono `missing_capability` e `handoff_status: pending`,
  altrimenti restano dichiarati e invisibili.

Carica dalle reference di `grl-agent-revenue` quello che il caso richiede: la scheda
`kpi-e-calcoli.md` per formule e denominatori, `modello-quoprofit.md` per MUP e MOL,
`integrazioni-pms-channel.md` quando l'export viene da un PMS o da un Channel Manager. I KPI si
calcolano con `uv run` sullo script `revenue_calculator.py` della stessa skill; senza lo script
applica la stessa formula a mano e dichiara il fallback. MUP e MOL restano regole interne
QuoProfit/RevD, non standard universali né prova del prezzo ottimale.

Il verdetto di chiusura ha tre parole, e ognuna dice una cosa diversa:

| Verdetto | Quando | `status` |
| --- | --- | --- |
| `READY_FOR_PLAN` | audit completo, nessun finding `blocker` aperto | `complete` |
| `NO_GO` | audit completo, ma almeno un finding `blocker` aperto: i dati non reggono un piano di prezzo finché quel blocco resta | `blocked` |
| `EVIDENZA_INSUFFICIENTE` | mancano dati decisivi per concludere l'audit; indica esattamente la prova che lo sblocca | `blocked` |

`NO_GO` non è un audit fallito: è un audit riuscito che dice di non procedere. Chiuderlo come
`READY_FOR_PLAN` farebbe partire `grl-revenue-plan` da un via libera che nessuno ha dato.

Un audit non autorizza invii a PMS o Channel Manager: per quello instrada a
`grl-revenue-plan` e poi a `grl-revenue-preflight`.

## Finalize

Prima di consegnare, verifica che ogni numero abbia fonte e perimetro, che i dati mancanti siano
espliciti e che nessun finding sia presentato come decisione di prezzo. Se `bmad-review` è
disponibile, usalo solo per chiarezza della prosa: non può cambiare numeri, formule, stati o fonti.

Chiudi con una riga strutturata:

```json
{"status":"complete|blocked","folder":"{audit}","verdict":"READY_FOR_PLAN|NO_GO|EVIDENZA_INSUFFICIENTE"}
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
