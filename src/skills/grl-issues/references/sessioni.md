# Sessioni di lavoro sulle issue

Una sessione è la fotografia di un ambito all'apertura e il confronto con la realtà alla chiusura.
Serve a rispondere alla domanda che a fine giornata nessuno sa più: **cosa ho chiuso davvero, e
cosa è cambiato mentre lavoravo?**

I file stanno in `{workflow.registry_path}/{slug}/sessions/{YYYYMMDD-HHMM}-{titolo}.json`. Una
sessione senza `ended_at` è aperta; l'attivazione della skill la cerca e propone di riprenderla.

## `session-start`

1. Chiedi l'ambito: numeri di issue, label, milestone o «tutte le aperte». Un ambito vago produce
   una fotografia inutile.
2. Esegui un `sync` prima di fissare la fotografia.
3. Apri la sessione:

   ```bash
   uv run {skill-root}/scripts/registry.py session --start \
     --path {workflow.registry_path}/{slug}/registry.json \
     --file {workflow.registry_path}/{slug}/sessions/{stamp}-{titolo}.json \
     --scope 12,14,21
   ```

   Lo script scrive `started_at`, l'ambito e la baseline (stato GitHub, stato di lavorazione e
   `updated_at` di ogni issue) e segnala quali numeri non sono nel registro.

4. Riporta l'elenco raggruppato per stato. Se una issue in ambito è `IN_ATTESA`, dillo per prima
   cosa e con **chi** l'ha messa.
5. Chiedi quali issue vengono prese in carico adesso e portale a `IN_SVILUPPO` con `registry.py
   set --status IN_SVILUPPO`. L'ambito non basta: una issue guardata non è una issue in lavorazione.

## Durante la sessione

Aggiorna sull'evento, non a intervalli: quando una issue cambia, tocca soltanto quella.

```bash
gh issue view 42 --json number,state,closedAt,updatedAt,labels
```

Le chiusure si riconoscono da tre segnali, e non valgono allo stesso modo:

| Segnale | Vale come |
| --- | --- |
| stato `closed` letto da GitHub | fatto |
| messaggio di commit con una parola chiave di chiusura | fatto, dopo il controllo qui sotto |
| dichiarazione a voce dell'utente | da verificare con la lettura mirata prima di scriverlo |

Le parole chiave che GitHub riconosce sono nove: `close`, `closes`, `closed`, `fix`, `fixes`,
`fixed`, `resolve`, `resolves`, `resolved`. Cercarne due su nove copre un quarto dei casi:

```bash
git log --since={started_at} --format=%s%n%b \
  | grep -iEo '(close[sd]?|fix(e[sd])?|resolve[sd]?) #[0-9]+'
```

## `session-close`

1. Ri-sincronizza, poi chiudi:

   ```bash
   uv run {skill-root}/scripts/registry.py session --close \
     --path {workflow.registry_path}/{slug}/registry.json \
     --file {workflow.registry_path}/{slug}/sessions/{stamp}-{titolo}.json
   ```

   Lo script confronta con la baseline e restituisce cinque insiemi: chiuse, ancora aperte,
   cambiate per mano di altri, nuove in ambito, non verificate. Marca anche `closed_in_session` e
   ti dice quali issue restano in carico.

2. Scrivi il rapporto per una persona. Le colonne che lo script non può riempire sono due, e sono
   quelle che contano: **cosa manca** a ogni issue ancora aperta, e **chi la tiene ferma**.

3. Per ogni issue rimasta `IN_SVILUPPO` o `IN_VERIFICA` chiedi la decisione: resta in carico o
   torna `DA_FARE`. Non sceglierla da solo — una issue lasciata `IN_SVILUPPO` per sbaglio blocca
   chi la prenderebbe, e nessuno capisce perché.

4. Proponi i commenti di chiusura utili, senza pubblicarli: li pubblica `grl-issue-readiness` dopo
   conferma, e la chiusura la esegue una persona. Se il lavoro va verificato contro i criteri della
   issue prima di chiudere, il passo successivo è `grl-issue-verify`.
