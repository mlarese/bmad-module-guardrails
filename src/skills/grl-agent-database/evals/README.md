# Eval di grl-agent-database (🗄️ Dario)

La suite verifica quattro contratti: workload prima del brand, ricerca live senza benchmark
inventati, architettura del dato con failure mode e confine esplicito con le altre figure. Include
anche il rifiuto di fissare lo schema quando il linguaggio del dominio è ancora ambiguo.

| File | Modo | Comando |
| --- | --- | --- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-database` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-database/evals/triggers.json` |

Gli input iniziano con `Run headless.` per ottenere un verdetto in un solo passaggio. I casi
includono scelta del motore, vector search, Redis, performance, migrazione Oracle/PostgreSQL e
il punto d'ingaggio nelle fasi BMad.
