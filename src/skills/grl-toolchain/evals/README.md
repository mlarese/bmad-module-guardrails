# Eval di grl-toolchain

I casi verificano le due cose che questa skill esiste per non sbagliare: installare senza aver
valutato, e assumere che il formato di configurazione sia lo stesso fra harness diversi.

| Caso | Cosa mette alla prova |
| --- | --- |
| `toolchain-ridondante-si-ferma` | il controllo che elimina più candidati di tutti: un server MCP che fa quello che una CLI già installata fa già |
| `toolchain-formati-non-si-copiano` | la traduzione per harness — TOML contro JSON, `command` come array, JSON con commenti |
| `toolchain-segreto-in-chiaro` | il blocco sulla chiave in chiaro in un file che finisce in git, e il mascheramento nel diff |
| `toolchain-audit-collegamenti-rotti` | l'inventario eseguito invece che ricordato, e il difetto silenzioso dei collegamenti rotti |
| `toolchain-scheda-scaduta` | il rifiuto di scrivere su un harness la cui scheda è marcata `da-verificare` |

## Come si eseguono senza falsare l'esito

Due accorgimenti, imparati sbagliandoli al primo run:

- **L'input deve nominare un pacchetto che esiste davvero.** Il controllo 1 della valutazione —
  «esiste con quel nome» — blocca prima di tutti gli altri: con un nome inventato il caso finisce
  per misurare quel controllo invece di quello che voleva misurare.
- **Il vincolo di sola lettura contraddice `toolchain-scheda-scaduta`.** Quel caso chiede di
  *eseguire* un refresh, che scrive dentro la skill. O si concede la scrittura sui soli file di
  `references/`, o il criterio si legge come soddisfatto quando il refresh è prescritto e la
  metà locale è stata fatta.

I trigger separano questa skill dalle figure con cui confina: threat model (Kai), conservazione e
rotazione dei segreti (Bruno), liceità di un trasferimento a un servizio remoto (Vera), licenze
(Aldo), e la scrittura di una skill nuova, che appartiene ai builder e non a questo workflow.

I test unitari degli script stanno in `scripts/tests/test_toolchain.py` e si eseguono con
`python3 -m pytest src/skills/grl-toolchain/scripts/tests/`. Coprono i formati per harness, il
mascheramento dei segreti, il backup, il rifiuto sui file non riscrivibili e l'assenza di
scritture in dry-run.
