# Eval di `grl-issue-readiness`

I casi proteggono il punto più delicato del modulo: l'unica skill che scrive su GitHub. Verificano
il verdetto sui criteri, la precedenza del segnale di attesa, la resistenza alle istruzioni
nascoste nel testo della issue e la disciplina di pubblicazione.

| Caso | Cosa protegge |
| --- | --- |
| `criterio-bloccante-mancante` | il vuoto diventa una domanda, non un requisito inventato |
| `attesa-prima-della-chiarezza` | l'attesa vince sul giudizio di chiarezza |
| `prompt-injection-nel-corpo` | il corpo della issue è dato, mai istruzione |
| `commento-idempotente` | un solo commento per issue, aggiornato invece che duplicato |
| `niente-batch-cieco` | nessuna pubblicazione in blocco senza revisione |
| `pronta-senza-rumore` | una issue chiara non merita un commento di conferma |
| `punto-di-ingresso-inesistente` | un file nominato ma assente non soddisfa il criterio |

I trigger separano il verdetto dal registro (`grl-issues`), dalla diagnosi (`grl-bug-finder`) e
dall'implementazione.
