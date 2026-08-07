# Eval di grl-agent-ai (Enzo)

Due file, due modi di `bmad-eval-runner`. La cartella ne contiene più di uno: il runner
prende «il primo match» se non gli si dice quale, quindi il file va passato esplicitamente.

| File | Modo | Comando |
| ---- | ---- | ------- |
| `cases.json` | `quality`, `baseline`, `variant` | `run_evals.py --cases <…>/evals/cases.json --skill-path src/skills/grl-agent-ai` |
| `triggers.json` | `trigger` | `run_triggers.py` con `src/skills/grl-agent-ai/evals/triggers.json` |

## Cosa misurano i casi

Cinque casi su otto verificano che Enzo **tolga** invece di aggiungere: è il tratto della
figura, ed è anche il primo a scomparire se il testo della skill si allenta.

| Caso | Fallimento che intercetta |
| ---- | ------------------------- |
| `non-serve-un-llm` | raccomandare un modello dove basta una tabella |
| `rag-non-necessario` | costruire un impianto di recupero su nove documenti |
| `eval-prima-del-prompt` | dare tecniche di prompt engineering a chi non ha un modo di misurare |
| `agente-non-serve` | trattare tre passi fissi come un sistema multi-agente |
| `confine-sicurezza` | rispondere su prompt injection invece di passarla a Kai, o proporre un prompt di sistema più severo come rimedio strutturale |
| `costi-verifica-web` | dare prezzi a memoria invece di verificarli |
| `automazione-senza-controllo` | non chiedere chi si accorge se l'automazione sbaglia in silenzio |
| `memoria-nessuna-scrittura-non-confermata` | scrivere in `accepted-risks.md` senza conferma esplicita |

`Run headless.` in testa a ogni input serve a far produrre il verdetto senza turni di
chiarimento: la figura è interattiva, il runner è a colpo singolo.

## Le query di trigger

Venti query, dieci per parte. Le should-not sono **near miss**: parlano tutte di modelli
linguistici e condividono il lessico con le should. È il caso più delicato del modulo,
perché quattro figure toccano l'AI da lati diversi — Kai i rischi, Aldo le licenze dei pesi
e la proprietà degli output, Nils l'AI Act, Bruno dove il modello gira. Se una di queste
query fa scattare Enzo, il confine non sta reggendo e il rumore ricade su tutto il modulo.
