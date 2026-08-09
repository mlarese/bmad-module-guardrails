# Automazione paid con guardrail

## Stati

Ogni job o regola deve avere uno stato esplicito:

`draft → read_only → dry_run → awaiting_approval → applied → observing → rolled_back | closed`

Un errore, un dato mancante o una policy non verificata porta a `blocked`, non a `applied`.

## Contratto di una regola

```yaml
id: budget-guard-001
scope: campaign-or-label
read_only_query: query o report che dimostra il perimetro
condition: soglia e finestra, senza ambiguità di timezone
action: proposta di modifica, non comando implicito
max_daily_delta: limite assoluto
exclusions: campagne, mercati o stati esclusi
approval: ruolo richiesto
dry_run_evidence: diff e risultato della validazione
observe_for: finestra post-azione
rollback: modifica inversa o stop manuale
log: timestamp, actor, scope, before, after, reason
```

## Regole operative

- La modalità predefinita è `read_only`.
- `dry_run` non deve generare spesa né pubblicazione.
- Un budget o una pausa richiedono approvazione separata dalla creazione del change set.
- Una regola non può auto-applicarsi a un nuovo account, a campagne senza storico o a un periodo
  con tracking degradato.
- Dopo un'applicazione si osserva il dato e si registra cosa è successo; non si accumulano modifiche
  prima della verifica.
- Un job non deve contenere credenziali o dati personali: usa secret manager e identità già
  autorizzate, gestiti da Bruno e Vera secondo il caso.
