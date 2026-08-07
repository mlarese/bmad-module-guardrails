# Eval di grl-agent-health (Livia)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-health` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-health/evals/triggers.json` |

## Cosa misurano i casi

Livia parla e non produce documenti: le rubric guardano il testo della risposta e la memoria
condivisa, non file generati. I casi coprono i quattro modi in cui questa figura può fallire:

| Caso | Fallimento che intercetta |
| ---- | ------------------------- |
| `fuori-perimetro` | dire cose sanitarie su un progetto che sanitario non è — il verdetto negativo è metà del valore del modulo |
| `dose-senza-unita` | non riconoscere il difetto clinico più frequente in uno schema |
| `confine-dispositivo-medico` | invadere il campo di Nils, o al contrario fermarsi al rimando senza rispondere |
| `severita-light-eccezione` | tacere su un rischio per il paziente perché il contesto è un prototipo |
| `standard-non-serve` | raccomandare uno standard «per il futuro» senza un interlocutore |
| `memoria-nessuna-scrittura-non-confermata` | scrivere in `accepted-risks.md` senza conferma esplicita |
| `deleghe-portale` | non vedere le deleghe, il buco più frequente di un portale paziente |

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

Venti query, dieci per parte. Le should-not sono **near miss**: parlano tutte di sanità e
condividono il lessico con le should. Ognuna appartiene per confine a un'altra figura —
Nils per la qualificazione MDR, Vera per la base giuridica, Kai per gli accessi, Bruno per
la conservazione, Aldo per le licenze delle terminologie, Iris per l'aspetto, Otto per i
confini del codice, Enzo per il RAG. Se una di queste fa scattare Livia, il confine scritto
nel `SKILL.md` non sta reggendo.
