# Eval di grl-agent-compliance (📐 Nils)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-compliance` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-compliance/evals/triggers.json` |

## Cosa misurano i casi

Nils presidia compliance normativa. Il tratto da proteggere è l'ordine delle mosse: prima esclude, poi prescrive. L'elenco di ciò che non si applica è metà del valore.

| Caso | Prima riga della rubric |
| ---- | ----------------------- |
| `prima-esclude` | la risposta dice che nessuna delle tre si applica, e lo dice prima di qualunque altra cosa |
| `confine-ai-act` | la risposta dice che l'AI Act si applica, perché non ha soglia dimensionale e c'è un sistema di … |
| `accessibilita-soglia` | la risposta si pronuncia su dentro o fuori nominando la soglia concreta che decide — dimensione … |
| `confine-privacy` | la risposta passa la base giuridica a Vera invece di rispondere lei |
| `committente-regolamentato` | la risposta distingue ciò che la norma impone alla banca da ciò che la banca ribalterà su di voi… |
| `dispositivo-medico-rimando` | la risposta riconosce che si tratta di supporto alla decisione diagnostica e colloca il caso alm… |

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

24 query, 10 should e 14 should-not. Le should-not sono **near miss**: condividono
lessico e dominio con le should, e ognuna appartiene per confine a un'altra figura —
Aldo per l'intero AI Act (classificazione, obblighi, corsi, licenze e contratti), Vera per la base giuridica, Iris per come si realizza l'accessibilità, Kai per i rischi, Bruno per la configurazione, Enzo per l'impianto AI, Otto per i confini, Livia per il contenuto clinico.

Le quattro query AI Act fra le should-not sono le più severe del gruppo: erano should fino al
passaggio della materia ad Aldo, e sono il modo di verificare che il travaso abbia funzionato
davvero.

Se una di queste fa scattare Nils, il confine scritto nel `SKILL.md` non sta reggendo.

## Un risultato già noto

Sulle due figure nuove del modulo la misura è già stata fatta, e ha prodotto un dato che
vale anche qui: aggiungere alla `description` una clausola che elenca ciò di cui la figura
**non** si occupa azzera i falsi positivi ma **spegne sette veri positivi su dieci**. Il
router legge l'elenco delle esclusioni e conclude che non è lei anche quando è lei.
Prima di provare quella strada su Nils, vale la pena rileggere quel numero.
