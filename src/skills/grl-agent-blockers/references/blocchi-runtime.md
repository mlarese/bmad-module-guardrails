# Blocchi a runtime

L'esito sono i punti in cui **il sistema si ferma davvero**: qualcosa attende, e mentre attende
qualcos'altro non può procedere. Ogni voce entra nella tabella del `SKILL.md`, e qui la colonna
«chi resta fermo» include anche il sistema stesso — una richiesta, una coda, tutti gli utenti.

La domanda che ordina questo asse: **per quanto tempo, e chi altro aspetta insieme a lui?** Una
chiamata lenta che blocca solo chi l'ha fatta è una lentezza. La stessa chiamata dentro un lock
condiviso ferma tutti, ed è un blocco.

## Dove si annidano

- **Chiamate sincrone verso l'esterno** dentro un percorso che l'utente attende: invio email,
  generazione PDF, provider di pagamento, servizio di terze parti. Guarda se c'è un timeout e cosa
  succede quando scade: senza timeout, l'attesa è illimitata per definizione.
- **Transazioni che restano aperte troppo a lungo**, in particolare quelle che contengono una
  chiamata di rete o un ciclo su molti record. Il blocco non è la transazione, è ciò che tiene
  aperto mentre aspetta qualcun altro.
- **Lock e sezioni serializzate.** Un lock su una risorsa condivisa, un job che gira in una
  istanza sola, una tabella scritta da tutti i processi. Il segnale è la risorsa unica su cui
  convergono percorsi indipendenti.
- **Code senza uscita d'emergenza.** Un messaggio che fallisce e viene ritentato per sempre ferma
  la coda dietro di sé; una coda senza dead letter accumula finché qualcuno se ne accorge.
- **Operazioni irreversibili in corsa.** Una migrazione senza rollback, un aggiornamento in massa
  senza modo di interromperlo, un batch che se cade a metà lascia i dati in uno stato che nessuna
  procedura sa riprendere.
- **Punti singoli di rottura.** Il servizio, il file, il processo o la credenziale da cui dipende
  tutto: quando manca, non c'è percorso alternativo.

## Cosa serve per farne una voce

Serve il passaggio reale: quante volte quel codice viene eseguito e in quale percorso. Un lock in
un comando amministrativo eseguito una volta l'anno non è la stessa cosa dello stesso lock nel
checkout. Se il traffico non è osservabile, dichiaralo e resta al condizionale.

Serve anche sapere se il blocco è **già stato colpito**: un incidente noto, un riavvio ricorrente,
un job che qualcuno rilancia sempre a mano. Se c'è, la voce sale in cima.

## Il confine con le altre figure

Vito segnala il punto e chi resta fermo. La soluzione appartiene a chi governa quel piano:

- infrastruttura, deploy, rollback, backup, scalabilità del servizio → **Bruno** (`grl-agent-ops`);
- lock, transazioni, migrazioni, indici e reversibilità sul database → **Dario**
  (`grl-agent-database`);
- passi sincroni, timeout e retry dentro una pipeline che chiama un modello → **Enzo**
  (`grl-agent-ai`);
- un'attesa deliberata per rispettare un vincolo temporale sul firmware → **Ada**
  (`grl-agent-firmware`), e in quel caso è voluta.
