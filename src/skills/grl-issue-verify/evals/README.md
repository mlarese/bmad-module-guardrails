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
| `review-mancante-blocca-la-chiusura` | criteri coperti non bastano: senza review la chiusura non si autorizza |

## Limite noto del banco

`chiusura-preparata-non-eseguita` misura cosa succede **dopo** un verdetto `RISOLTA`: commento e
comando pronti, stato `IN_VERIFICA`, nessuna chiusura eseguita. In una sandbox senza repository
reale l'esecutore non ha un diff vero da mappare sui criteri, e la skill — correttamente — rifiuta
di emettere `RISOLTA` su una dichiarazione. Il caso resta com'è: si esegue su un repository con una
issue e una PR vere. Ammorbidire la rubric per farlo passare significherebbe insegnare alla skill
proprio l'errore che deve impedire.

I trigger separano questa verifica dalla review di qualità (`bmad-review`), dal gate di chiarezza
(`grl-issue-readiness`), dal registro (`grl-issues`) e dalla diagnosi (`grl-bug-finder`).
