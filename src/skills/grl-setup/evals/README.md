# Eval di grl-setup

I casi verificano il riconoscimento TOML/YAML, la registrazione del roster, i party group,
il catalogo help corretto, l'idempotenza, la riconfigurazione e lo stop su un progetto senza
installazione BMad. Verificano anche che `grl-setup` non crei la memoria condivisa e proponga
`grl-profile` al termine.

`triggers.json` distingue setup e installazione da profilazione, board, configurazione BMM e
consultazione delle singole figure. Passare esplicitamente i due file a `bmad-eval-runner`.
