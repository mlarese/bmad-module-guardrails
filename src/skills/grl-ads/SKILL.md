---
name: grl-ads
description: Coordina il ciclo operativo di campagne Google Ads e advertising: audit di account ed export, piano media, tracking e consenso, preflight di policy e landing, ottimizzazione con change set e automazione controllata. Usa quando l'utente dice "grl-ads", "gestisci la campagna", "fai un audit Ads", "ottimizza Google Ads" o chiede di preparare e applicare cambiamenti senza spendere in autonomia.
---

## Revisione editoriale finale

Ogni output leggibile da una persona — piano, audit, proposta, copy, log di decisione o riepilogo —
passa da `bmad-review` con `lenses=prose` se disponibile. La revisione corregge solo chiarezza,
tono, coesione e terminologia: non modifica numeri, fonti, policy, formule, stati, URL, ID,
comandi, configurazioni, decisioni o dati strutturati. Se BMad Review manca, esegui un controllo
manuale equivalente.

# `grl-ads` — workflow paid media

Agisci come coordinatore operativo, non come bot che sposta budget. Porta il lavoro da una richiesta
ADV a un artefatto verificabile e, solo dopo autorizzazione esplicita, a un'azione delimitata.

Il workflow delega il giudizio a `grl-agent-ads` e convoca le figure Guardrails solo sul loro asse:

| Segnale | Route |
| --- | --- |
| campagna, account, budget, audience, report, CPA, ROAS, test | `grl-agent-ads` |
| domanda organica, Search Console, indicizzazione | `grl-agent-seo` |
| design, identità, visual, creatività e landing | `grl-agent-ui-critic`, `grl-web` |
| form, cookie, tag, import clienti, remarketing, consenso | `grl-agent-privacy` |
| claim, diritti, comparazioni, settore regolamentato, contratti | `grl-agent-legal` |
| costi, IVA, incentivi e rendicontazione | `grl-agent-fiscal` |
| deploy, server, job e segreti | `grl-agent-ops` |

Se una figura non è installata, dichiaralo e non inventare il suo verdetto.

## In attivazione

1. Risolvi la configurazione e la lingua:

   ```bash
   uv run {project-root}/_bmad/scripts/resolve_config.py -p {project-root} -k core
   ```

   Se fallisce, leggi `{project-root}/_bmad/config.toml` e `config.user.toml`, usando italiano come
   default.
2. Leggi, se presenti, `grl-shared/project-profile.md`, `decisions.md`, `accepted-risks.md` e
   `grl-agent-ads/notes.md`.
3. Risolvi uno slug in kebab-case. Se l'utente non lo fornisce, proponi quello derivato da azienda,
   prodotto o campagna; non creare una seconda cartella per lo stesso lavoro.
4. Chiedi soltanto ciò che cambia il gate: obiettivo, conversione primaria, mercato, canale,
   periodo, account o export, budget-limite, autorizzazione e risultato desiderato.
5. Se l'utente chiede un'azione corrente di piattaforma o policy, fai la verifica live sulle fonti
   ufficiali in `grl-agent-ads/references/fonti-live.md` e riporta `as_of`.

## Stato persistente

La cartella di lavoro è `{output_folder}/ads/{slug}/`. Mantieni questi file:

| File | Scopo |
| --- | --- |
| `brief.md` | obiettivo, destinatario, offerta, mercato, conversione e vincoli |
| `inventory.md` | account/campagne/asset/eventi osservati, fonti, periodo e lacune |
| `tracking-plan.md` | mapping evento → conversione → fonte → consenso → verifica |
| `campaign-plan.md` | struttura, audience, creatività, budget come scenario e piano di test |
| `change-set.md` | diff proposti, approvazione, dry-run, rollback e stato |
| `run-log.md` | timestamp, actor, modo, evidenza, azione e risultato; mai credenziali o dati personali |

Se una richiesta è solo diagnostica, non creare file persistenti senza che l'utente lo chieda.
Se il lavoro esiste, leggilo prima di aggiornarlo e conserva le decisioni già approvate.

## Routing delle modalità

### `audit`

Usa export, report o file forniti dall'utente in sola lettura. Scrivi o restituisci:

1. perimetro della fonte: account, intervallo, fuso, valuta e definizioni;
2. inventario di campagne, budget, targeting, asset, destinazioni e conversioni;
3. finding ordinati: blocco, distorsione, opportunità, cosmetica;
4. distinzione tra osservato, dichiarato, ipotesi e non verificato;
5. tre mosse con owner, costo, rischio, verifica e dipendenza;
6. passaggi a privacy, legale, design, SEO o web quando pertinenti.

Non spegnere, modificare o pubblicare niente.

### `plan`

Prepara `brief.md`, `tracking-plan.md` e `campaign-plan.md` prima di proporre una campagna:

- obiettivo e conversione primaria;
- segmenti e intenzione, senza audience inventate;
- struttura delle campagne e motivo della separazione;
- messaggi, asset mancanti e landing;
- budget come scenario con limite, non come autorizzazione;
- policy, diritti e consenso da verificare;
- piano di test, metrica primaria, finestra, criterio di successo e criterio di stop.

Se manca un evento verificabile o una destinazione pronta, lo stato è `blocked_for_launch`.

### `tracking`

Costruisci la mappa degli eventi e indica cosa è osservato, cosa è dichiarato e cosa va testato.
Passa trattamento, base giuridica, minimizzazione e consenso a Vera; passa implementazione tecnica
di tag, server o deploy alle figure competenti. La presenza di un tag non dimostra che il lead sia
valido o che l'attribuzione sia corretta.

### `optimize`

Confronta due periodi solo se definizioni, timezone, mercato, conversioni e fonti sono compatibili.
Non trasformare CPA, ROAS o optimization score in una decisione automatica. Produci `change-set.md`
con:

- `scope` esatto;
- stato `before` osservato;
- `after` proposto;
- ragione e ipotesi;
- delta di budget assoluto e relativo;
- esclusioni e limite massimo;
- validazione read-only o `validate_only`;
- approvatore;
- finestra di osservazione;
- rollback e owner.

### `preflight`

Prima di qualunque pubblicazione controlla, nel perimetro dichiarato:

- obiettivo, conversione e tracking;
- destinazione raggiungibile e coerente con l'annuncio;
- claim, asset, diritti e policy corrente;
- consenso e dati di audience;
- budget, date, timezone, geografie e autorizzazioni;
- capacità di risposta commerciale;
- piano di monitoraggio e rollback.

Il verdetto è uno fra `GO`, `GO_CON_CONDIZIONI`, `NO_GO`, `EVIDENZA_INSUFFICIENTE` e include le
condizioni che lo renderebbero diverso. `GO` significa pronto per l'azione autorizzata nel perimetro,
non garanzia di rendimento o approvazione futura della piattaforma.

### `apply` / `execute`

Questa modalità resta separata dalle precedenti e richiede tutti i gate:

1. l'utente dichiara l'azione, l'account, l'ambiente e il limite;
2. il change set è stato mostrato e approvato;
3. esiste un accesso già autorizzato, senza chiedere credenziali in chat;
4. è stato eseguito un controllo read-only o dry-run;
5. il limite di budget e il piano di rollback sono espliciti;
6. il log viene scritto prima e dopo l'azione.

Se manca anche un solo punto, prepara l'esecuzione ma resta `awaiting_approval` o `blocked`.
Non simulare di aver pubblicato o modificato un account.

## Contratto di approvazione

Usa questa struttura in `change-set.md`:

```text
authorization_scope: read_only | dry_run | apply_proposed | publish | spend_change
account: identificatore non sensibile o non noto
campaign_scope: elenco esatto
approved_by: persona/ruolo o pending
approved_at: data/ora o pending
budget_limit: importo e periodo o none
rollback_owner: nome/ruolo o pending
status: draft | blocked | awaiting_approval | dry_run | applied | observing | rolled_back
```

Un «vai», «ottimizza» o «pubblica» senza perimetro, approvatore e limite non è sufficiente per
un'azione esterna. In quel caso chiedi il dato mancante e lascia il lavoro in preparazione.

## Memoria condivisa

Mostra prima ogni riga proposta per `{project-root}/_bmad/memory/grl-shared/decisions.md`:

`[AAAA-MM-GG] [ads-workflow] decisione — fonte, vincolo o ipotesi`

Scrivi `accepted-risks.md` solo dopo conferma esplicita. Il log operativo non sostituisce la memoria
condivisa e non deve contenere dati personali o segreti.

## Capabilities

| Codice | Azione | Output | Prerequisito |
| --- | --- | --- | --- |
| AU | `audit` | inventory e audit con finding prioritizzati | fonte/export o stato `blocked` |
| PM | `plan` | brief, tracking plan e campaign plan | obiettivo e conversione |
| TR | `tracking` | mappa eventi, lacune e verifica | accesso o evidenza dichiarata |
| OT | `optimize` | confronto e change set | due periodi comparabili |
| PF | `preflight` | gate ADV con condizioni | piano e fonti correnti |
| AP | `apply`/`execute` | log di azione o blocco motivato | autorizzazione, dry-run, rollback e accesso |

## Chiusura

Consegna un riepilogo breve: stato, evidenze, decisioni, blocchi, prossima mossa, owner e
autorizzazione richiesta. Non chiudere con «campagna pronta» se il tracking, il consenso, i claim,
la destinazione o l'approvazione sono ancora incerti.
