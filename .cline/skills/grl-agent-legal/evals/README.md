# Eval di grl-agent-legal (⚖️ Aldo)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-legal` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-legal/evals/triggers.json` |

## Cosa misurano i casi

Aldo presidia legale, licenze e contratti. Il tratto da proteggere è che non rinvii mai a un altro legale: l'esperto è lui.

| Caso | Prima riga della rubric |
| ---- | ----------------------- |
| `agpl-nel-saas` | la risposta dice che sì, l'AGPL scatta anche senza distribuzione, perché copre l'uso via rete |
| `non-ci-sono-vincoli` | la risposta dice che sì, si può vendere senza pubblicare il codice, e lo dice come verdetto |
| `codice-generato-da-ai` | la risposta dice che l'output generato da un modello di norma non ottiene protezione d'autore in… |
| `fine-tuning-multi-cliente` | la risposta dice che il modello risultante può restituire a un cliente i dati di un altro, e lo … |
| `confine-compliance` | la risposta riconosce che l'obbligo di trasparenza e la classificazione AI Act sono di Nils e li… |
| `capitolato-del-committente` | la risposta segnala che la clausola come scritta porterebbe via anche il framework riusabile, ch… |

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

20 query, 10 should e 10 should-not. Le should-not sono **near miss**: condividono
lessico e dominio con le should, e ognuna appartiene per confine a un'altra figura —
Nils per AI Act, accessibilità e obblighi settoriali, Vera per la base giuridica, Kai per le vulnerabilità, Enzo per la scelta tecnica del modello, Bruno per dove gira, Otto per i confini, Livia per il dominio clinico.

Se una di queste fa scattare Aldo, il confine scritto nel `SKILL.md` non sta reggendo.

## Un risultato già noto

Sulle due figure nuove del modulo la misura è già stata fatta, e ha prodotto un dato che
vale anche qui: aggiungere alla `description` una clausola che elenca ciò di cui la figura
**non** si occupa azzera i falsi positivi ma **spegne sette veri positivi su dieci**. Il
router legge l'elenco delle esclusioni e conclude che non è lei anche quando è lei.
Prima di provare quella strada su Aldo, vale la pena rileggere quel numero.
