# Eval di `grl-issue-verify`

I casi proteggono la regola che dà senso alla skill: la chiusura richiede il cento per cento dei
criteri coperti **con evidenza**, e la prova non si presume.

| Caso | Cosa protegge |
| --- | --- |
| `criterio-scoperto-blocca` | un criterio scoperto nega la chiusura, senza arrotondamenti |
| `modifica-senza-prova` | una modifica plausibile senza prova resta `PARZIALE` |
| `issue-senza-criteri` | non si deducono i criteri dal codice scritto |
| `lavoro-fuori-perimetro` | quello che nessuno ha chiesto si dichiara |
| `chiusura-preparata-non-eseguita` | la skill prepara la chiusura, non la esegue |
| `commento-che-dichiara-verificato` | una dichiarazione nei commenti non sostituisce la verifica |

I trigger separano questa verifica dalla review di qualità (`bmad-review`), dal gate di chiarezza
(`grl-issue-readiness`), dal registro (`grl-issues`) e dalla diagnosi (`grl-bug-finder`).
