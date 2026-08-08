# Modulo Guardrails (`grl`) — istruzioni di progetto

## L'About di GitHub si aggiorna insieme al README

La descrizione **About** del repository su GitHub è una vetrina come il `README.md`, ma vive
fuori dai file versionati: nessun commit la tocca, quindi resta indietro da sola.

**Regola:** ogni volta che cambia il perimetro del modulo — una figura in più o in meno, una
skill o un workflow nuovo, un cambio di posizionamento nell'intestazione del `README.md` —
aggiorna l'About nello stesso turno, senza aspettare che l'utente lo chieda.

```
gh repo edit mlarese/bmad-module-guardrails --description "<testo>"
```

Vincoli:

- massimo **350 caratteri**, altrimenti l'API risponde `HTTP 422: Validation Failed`
- il testo deriva dalle prime righe del `README.md`, in forma compressa
- si verifica con `gh repo view mlarese/bmad-module-guardrails --json description`

## Le altre vetrine da tenere allineate nello stesso passaggio

Cambiano insieme, e tutte e cinque devono dire lo stesso numero di figure e le stesse skill:

| Punto | File |
| ----- | ---- |
| README | `README.md` (intestazione, tabella delle figure, tabella dei workflow) |
| Manifesto del modulo | `src/module.yaml` (`description`, `module_greeting`, `post-install-notes`, `agents`) |
| Copia per l'installazione manuale | `src/skills/grl-setup/assets/module.yaml` — deve restare **identica** a `src/module.yaml` (`diff` senza differenze) |
| Marketplace BMad | `.claude-plugin/marketplace.json` (`description` del marketplace, `description` e `skills` del plugin `grl`) |
| About GitHub | descrizione del repository, via `gh repo edit` |

Una skill nuova va aggiunta anche all'elenco `skills` di `.claude-plugin/marketplace.json`,
altrimenti non viene pubblicata.

## Niente pull request

Il lavoro finisce con i commit e, se richiesto, con il push del branch.

## Modello runtime per gli eval

Per gli eval runtime del modulo usa il runtime della chat e i suoi subagent, che
ereditano il modello corrente. Non avviare OpenCode, Claude CLI, Laguna o altri
harness esterni e non sostituire il modello corrente con un fallback.
