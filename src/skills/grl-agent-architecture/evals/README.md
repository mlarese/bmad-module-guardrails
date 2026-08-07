# Eval di grl-agent-architecture (🧱 Otto)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-architecture` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-architecture/evals/triggers.json` |

## Cosa misurano i casi

Otto presidia architettura del codice. Il tratto da proteggere è «qui non serve» detto senza imbarazzo, e il caso opposto riconosciuto con lo stesso metro.

| Caso | Prima riga della rubric |
| ---- | ----------------------- |
| `qui-non-serve` | la risposta dice che qui non serve, e lo dice senza imbarazzo e senza predica sui principi |
| `manca-un-confine` | la risposta riconosce il caso opposto all'over-engineering: qui un confine manca |
| `microservizi-no` | la risposta dice che con un team, un deploy e un database quelli non sarebbero microservizi ma m… |
| `eccezione-concordata` | la risposta accetta la ragione come buona e chiude la partita, invece di insistere |
| `confine-ops` | la risposta passa la domanda a Bruno, perché la scelta dell'infrastruttura è sua |
| `dove-metto-la-feature` | la risposta dice dove collocare la feature e perché, nominando le cartelle che esistono davvero |

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

20 query, 10 should e 10 should-not. Le should-not sono **near miss**: condividono
lessico e dominio con le should, e ognuna appartiene per confine a un'altra figura —
Bruno per infrastruttura e deploy, Kai per i rischi, Aldo per le licenze, Vera per la sorte dei dati, Iris per l'aspetto, Enzo per i confini interni alla pipeline AI, Livia per la struttura del dato clinico.

Se una di queste fa scattare Otto, il confine scritto nel `SKILL.md` non sta reggendo.

## Un risultato già noto

Sulle due figure nuove del modulo la misura è già stata fatta, e ha prodotto un dato che
vale anche qui: aggiungere alla `description` una clausola che elenca ciò di cui la figura
**non** si occupa azzera i falsi positivi ma **spegne sette veri positivi su dieci**. Il
router legge l'elenco delle esclusioni e conclude che non è lei anche quando è lei.
Prima di provare quella strada su Otto, vale la pena rileggere quel numero.
