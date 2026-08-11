# Schema del registro — `grl-issues/registry@3`

Il registro è un contratto fra cinque lettori: `grl-issues` lo costruisce, `grl-issue-readiness`
scrive il verdetto di chiarezza, `grl-issue-build` scrive lo stato `IN_SVILUPPO` quando la
costruzione parte, `grl-issue-verify` scrive l'esito della verifica, `grl-agent-issues`
lo legge e basta. Chi scrive un campo che non gli appartiene rompe il lavoro di un altro senza
prodursi un errore.

**Nessuno modifica il file a mano.** Ogni scrittura passa da `scripts/registry.py`, che valida il
vocabolario, applica la precedenza degli stati e scrive in modo atomico.

## Forma

```json
{
  "schema": "grl-issues/registry@3",
  "repo": "owner/name",
  "account": "login-che-ha-letto",
  "as_of": "2026-08-11T09:12:00+00:00",
  "sync": {"mode": "full|incremental", "state": "open|all", "limit": 500, "truncated": false},
  "issues": [
    {
      "number": 42,
      "title": "…",
      "summary": "una riga presa dalla descrizione, ripulita e redatta",
      "state": "open|closed",
      "labels": ["…"],
      "milestone": "…|null",
      "assignees": ["…"],
      "updated_at": "…",
      "closed_at": null,
      "url": "…",
      "checked_at": "…",
      "status": "DA_VALUTARE|DA_CHIARIRE|DA_FARE|IN_SVILUPPO|IN_VERIFICA|IN_ATTESA|NON_APPROVATA|CHIUSA",
      "status_source": "derivato|dichiarato",
      "status_note": "chi lo ha deciso e quando, se dichiarato",
      "readiness": {
        "verdict": "PRONTA|PRONTA_CON_RISERVA|NON_PRONTA|SOSPESA|null",
        "checked_at": "…",
        "missing": ["criterio_di_accettazione"],
        "criteria": [{"id": "problema_osservato", "esito": "ok|manca", "citazione": "…"}]
      },
      "hold": {"active": false, "source": "label|comment|dependency|milestone", "who": "…", "since": "…", "clears_when": "…"},
      "links": {"blocked_by": [7], "duplicate_of": null, "pr": [123], "code": ["reports/export_csv.py"]},
      "closed_in_session": null
    }
  ]
}
```

## Chi scrive cosa

| Campo | Proprietario | Quando |
| --- | --- | --- |
| `repo`, `account`, `as_of`, `sync` | `grl-issues` | `sync` |
| `number`, `title`, `state`, `labels`, `milestone`, `assignees`, `updated_at`, `closed_at`, `url` | `grl-issues` | `sync`, letti da GitHub |
| `summary` | `scripts/registry.py` | derivata dal corpo al `sync`: prime frasi utili, senza markup, con email, numeri, IP e segreti sostituiti |
| `status`, `status_source`, `status_note` | `scripts/registry.py` | derivati a ogni `sync`, dichiarati da `set-status`, da `decide` e da `grl-issue-build` quando porta la issue a `IN_SVILUPPO` |
| `readiness.*` | `grl-issue-readiness` | azione `check`, via `registry.py set` |
| `hold.*` | `grl-issues` per le label, `grl-issue-readiness` per i commenti | `sync` e `check` |
| `links.blocked_by`, `links.duplicate_of`, `links.pr` | `grl-issue-readiness` e `grl-issue-verify` | quando leggono la issue per intero o la PR collegata |
| `links.code` | chi fa la ricognizione: Tito, readiness, build, verify | i file che la issue tocca davvero, trovati nel codice |
| `closed_in_session` | `grl-issues` | `session-close` |

## Perché i campi locali sopravvivono al `sync`

`readiness`, `hold`, `status_source`, `status_note`, `links` e `closed_in_session` non esistono su
GitHub: nessuna rilettura li ricostruisce. Il `sync` fonde riga per riga e li conserva; una
riscrittura integrale li cancellerebbe in silenzio, e una issue marcata `NON_APPROVATA` a voce
tornerebbe `DA_VALUTARE` per rientrare in lavorazione il giorno dopo.

Per la stessa ragione un `registry.json` illeggibile non viene sovrascritto: lo script lo rinomina
in `registry.corrotto.json`, ricostruisce da GitHub e dichiara cosa è andato perso.

## Versione

`@2` aggiunge `readiness.criteria` — l'esito dei sette criteri con la citazione — e lo stato
`IN_VERIFICA`. Senza `criteria`, `grl-issue-verify` dovrebbe riestrarre da capo i criteri di
accettazione e verificherebbe contro una lista diversa da quella su cui la issue è stata approvata.

`@3` aggiunge `summary`. Un elenco di numeri e titoli non dice a cosa si riferisce una issue:
«Fix export» non distingue il totale sbagliato dal file che non si apre. La sintesi è una vetrina,
non un archivio — il corpo integrale resta su GitHub, e i dati personali non entrano nemmeno nella
sintesi.

`links.code` conserva l'esito della ricognizione del codice: senza di lui ogni sessione ricomincia
la ricerca da capo, e il costo di guardare il repository si paga più volte per la stessa issue.

Chi cambia la forma alza la versione e aggiorna questa tabella nello stesso passaggio. Lo script
rifiuta un registro con un `schema` che non riconosce, invece di leggerlo a metà.
