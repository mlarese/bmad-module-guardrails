# Modulo Guardrails (`grl`) — istruzioni di progetto

## L'About di GitHub si aggiorna insieme al README

La descrizione **About** del repository su GitHub è una vetrina come il `README.md`, ma vive
fuori dai file versionati: nessun commit la tocca, quindi resta indietro da sola.

**Regola:** ogni volta che cambia il perimetro del modulo — una figura in più o in meno, una
skill o un workflow nuovo, un cambio di posizionamento nell'intestazione del `README.md` —
aggiorna l'About nello stesso turno, senza aspettare che l'utente lo chieda. L'About deve restare
aggiornato e scritto nella stessa lingua del `README.md` corrispondente; se cambia la lingua del
README, traduci anche l'About nello stesso turno. La regola vale per il repository fonte e per
tutti i nove sottomoduli: quando un sottomodulo cambia, il suo `README.md` generato e il suo About
GitHub devono essere aggiornati e pubblicati nello stesso passaggio, mai uno senza l'altro.

```
gh repo edit mlarese/bmad-module-guardrails --description "<testo>"
```

Vincoli:

- massimo **350 caratteri**, altrimenti l'API risponde `HTTP 422: Validation Failed`
- il testo deriva dalle prime righe del `README.md`, in forma compressa
- si verifica con `gh repo view mlarese/bmad-module-guardrails --json description`

## Le altre vetrine da tenere allineate nello stesso passaggio

Cambiano insieme, e tutte e quattro devono dire lo stesso numero di figure e le stesse skill:

| Punto | File |
| ----- | ---- |
| README | `README.md` (intestazione, tabella delle figure, tabella dei workflow) |
| Manifesto e catalogo del modulo | `src/module.yaml` e `src/module-help.csv` (`description`, `module_greeting`, `post-install-notes`, `agents`) |
| Marketplace BMad | `.claude-plugin/marketplace.json` (`description` del marketplace, `description` e `skills` del plugin `grl`) |
| About GitHub | descrizione del repository fonte e dei nove derivati, via `gh repo edit`, nella stessa lingua del README corrispondente |

Una skill nuova va aggiunta anche all'elenco `skills` di `.claude-plugin/marketplace.json`,
altrimenti non viene pubblicata.

Una skill nuova va assegnata anche a un modulo in `src/module-topology.yaml`: quello che non
compare in nessuna lista `skills` non finisce in nessun repository derivato.

## README essenziale

Il `README.md` è una vetrina breve, non il manuale completo del progetto. Deve contenere soltanto:

**Lingua obbligatoria:** il `README.md` del repository fonte e il `README.md` di ogni modulo
tematico derivato devono essere scritti interamente in inglese; prima di ogni commit e build
verifica che non contengano testo in italiano o in altre lingue.

- un'introduzione: cosa fa Guardrails e perché esiste;
- la spiegazione degli agenti;
- la spiegazione dei workflow.

Non aggiungere al README dettagli estesi su installazione, severità, configurazione, topologia dei
moduli, build/publish o razionale architetturale. Questi contenuti appartengono a `CLAUDE.md`,
`docs/module-plan.md` e ai manifesti in `src/`.

## I nove moduli derivati si rigenerano e si ripubblicano nello stesso turno

Nove repository derivano da questo e li produce `tools/build_modules.py` leggendo
`src/module-topology.yaml`. Questo repository è la fonte unica delle skill.

| Codice | Repository | Contiene |
| ------ | ---------- | -------- |
| `grg` | `mlarese/bmad-module-guardrails-governance` | Vera, Aldo, Nils, `grl-legal-updates`, `grl-automation` |
| `gre` | `mlarese/bmad-module-guardrails-engineering` | Kai, Otto, Vito, Dario, Ada, Bruno, Enzo, Ines, `grl-bug-finder`, `grl-automation`, `grl-toolchain` |
| `grf` | `mlarese/bmad-module-guardrails-fiscal` | Marta, `grl-fiscal-updates`, `grl-automation` |
| `grh` | `mlarese/bmad-module-guardrails-health` | Livia, `grl-mdsw`, `grl-automation` |
| `grw` | `mlarese/bmad-module-guardrails-web` | Iris, Nora, Dalia, Sofia, Marco, Elio, `grl-web`, `grl-ads`, `grl-social`, `grl-social-creative`, `grl-automation` |
| `gpm` | `mlarese/bmad-module-guardrails-paid-media` | Vera, Aldo, Iris, Nora, Dalia, Sofia, Marco, Elio, `grl-ads`, `grl-social`, `grl-social-creative`, `grl-automation` |
| `grv` | `mlarese/bmad-module-guardrails-revenue` | Rhea, `grl-revenue-audit`, `grl-revenue-plan`, `grl-revenue-preflight`, `grl-automation` |
| `gau` | `mlarese/bmad-module-guardrails-automation` | tutte le ventuno figure, workflow di dominio, `grl-bug-finder` e `grl-automation` |
| `gwp` | `mlarese/bmad-module-guardrails-wordpress` | Milo, `grl-wordpress-delivery`, `grl-automation` |

**Regola: ogni modifica che tocca `src/` va propagata ai derivati nello stesso turno, senza
aspettare che l'utente lo chieda.** Vale per una skill cambiata, una skill nuova, un cambio di
roster, di catalogo di help o di party group. Un derivato che resta indietro pubblica istruzioni
diverse da quelle della fonte, e nessuno se ne accorge finché non le esegue. La pubblicazione del
derivato deve includere sempre sia il `README.md` sia l'About GitHub aggiornato.

```bash
python3 -m pytest tools/tests/                              # test della build
python3 tools/build_modules.py                              # rigenera dist/
python3 tools/publish_modules.py -m "<messaggio di commit>"  # commit e push sui nove repo
```

`publish_modules.py` è idempotente: salta i moduli senza modifiche, crea il repository se manca e
riallinea l'About di GitHub alla `description` della topologia. Con `--module grw` lavora su uno
solo, con `--dry-run` mostra cosa farebbe.

**I derivati non si modificano a mano.** Una modifica fatta lì viene persa alla rigenerazione —
compresi README, `module.yaml` e `marketplace.json`, che sono generati: si correggono cambiando i
template in `tools/build_modules.py` o le descrizioni in `src/module-topology.yaml`.

Il commit sulla fonte resta separato: i derivati si pubblicano sempre, il push di questo
repository si fa quando l'utente lo chiede.

## Niente pull request

Il lavoro finisce con i commit e, se richiesto, con il push del branch.

## Modello runtime per gli eval

Per gli eval runtime del modulo usa il runtime della chat e i suoi subagent, che
ereditano il modello corrente. Non avviare OpenCode, Claude CLI, Laguna o altri
harness esterni e non sostituire il modello corrente con un fallback.
