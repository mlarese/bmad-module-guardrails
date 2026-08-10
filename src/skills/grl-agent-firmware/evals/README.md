# Eval di grl-agent-firmware (⚙️ Ada)

La suite verifica sei contratti: non inventare il target, distinguere ISR e lavoro differibile,
trattare DMA e buffer come ownership/concorrenza, costruire una prova riproducibile, gestire
aggiornamento e rollback, e non confondere MISRA con la garanzia di sicurezza del prodotto.

| File | Modo | Comando |
| --- | --- | --- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-firmware` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-firmware/evals/triggers.json` |

Gli input iniziano con `Run headless.` quando il caso deve chiudersi in un solo passaggio. I
parametri mancanti sono intenzionali: Ada deve segnalarli, non riempirli con una piattaforma
inventata.
