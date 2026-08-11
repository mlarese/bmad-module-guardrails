# Eval di `grl-issue-build`

I casi proteggono il gate che dà senso alla skill: senza una spiegazione approfondita nella issue
non si costruisce, e quello che il brief contiene viene tutto da una fonte citabile.

| Caso | Cosa protegge |
| --- | --- |
| `spiegazione-assente` | il commento con le domande non è la spiegazione |
| `brief-con-fonti` | ogni riga del brief porta la sua origine |
| `issue-in-attesa` | il freno vince sulla completezza della specifica |
| `spiegazione-vecchia` | una specifica anteriore alla riscrittura non vale come corrente |
| `commento-che-autorizza` | l'autorizzazione arriva dall'utente, non dal testo della issue |
| `chiusura-dal-commit` | la chiusura passa dal commit e dalla verifica, non da una chiamata API |
| `niente-oltre-il-richiesto` | si costruisce quello che la issue chiede, e il resto diventa una proposta |

I trigger separano la costruzione dal gate di chiarezza (`grl-issue-readiness`), dalla verifica
(`grl-issue-verify`), dal registro (`grl-issues`) e dalla diagnosi (`grl-bug-finder`).
