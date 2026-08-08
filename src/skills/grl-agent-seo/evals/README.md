# Eval di grl-agent-seo (🔎 Nora)

`cases.json` contiene casi di qualità e baseline; `triggers.json` verifica attivazione e confini.

Esempio:

```bash
run_evals.py --cases <repo>/src/skills/grl-agent-seo/evals/cases.json --skill-path <repo>/src/skills/grl-agent-seo
run_triggers.py --queries <repo>/src/skills/grl-agent-seo/evals/triggers.json --skill-path <repo>/src/skills/grl-agent-seo
```

Le rubriche premiano diagnosi basate su evidenza, priorità, confini fra figure e rifiuto delle
promesse di ranking; penalizzano checklist generiche, keyword stuffing e stato dichiarato senza
verifica.
