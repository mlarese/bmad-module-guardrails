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
| `dove-metto-la-feature` | la risposta indica un unico modulo responsabile e motiva con la proprietà del dato o del rendering |
| `vincoli-di-storia` | la risposta consegna vincoli, non un disegno né una proposta di ristrutturazione |
| `storia-senza-vincoli` | la risposta dice esplicitamente che questa storia non ha vincoli architetturali |
| `non-architettare-il-futuro` | la risposta dice di no: si scrive l'export CSV di oggi, senza l'astrazione per i formati futuri |

Gli ultimi tre coprono la fase di storia e specifica. Il tratto da proteggere lì è diverso:
un vincolo vale solo se si può rispondere sì o no guardandolo nel diff, e il vuoto lasciato
dal codice che non esiste ancora non si riempie di principi.

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

25 query, 13 should e 12 should-not. Le should-not sono **near miss**: condividono
lessico e dominio con le should, e ognuna appartiene per confine a un'altra figura —
Bruno per infrastruttura e deploy, Kai per i rischi, Aldo per le licenze, Vera per la sorte dei dati, Iris per l'aspetto, Enzo per i confini interni alla pipeline AI, Livia per la struttura del dato clinico.

Le ultime due should-not sono il near miss della fase di storia: riscrivere criteri di
accettazione e stimare punti parlano di storie ma non sono architettura, e appartengono a John
e allo sprint planning.

Se una di queste fa scattare Otto, il confine scritto nel `SKILL.md` non sta reggendo.

## Un risultato già noto

Sulle due figure nuove del modulo la misura è già stata fatta, e ha prodotto un dato che
vale anche qui: aggiungere alla `description` una clausola che elenca ciò di cui la figura
**non** si occupa azzera i falsi positivi ma **spegne sette veri positivi su dieci**. Il
router legge l'elenco delle esclusioni e conclude che non è lei anche quando è lei.
Prima di provare quella strada su Otto, vale la pena rileggere quel numero.
