# Rigidità cablata nel codice

L'esito sono i punti in cui il codice **regge un caso solo** perché quel caso è scritto dentro:
una sequenza fissa, una soglia, un valore, un'assunzione. Non blocca nessuno finché il caso è
quello; blocca il giorno in cui arriva il secondo. Ogni voce entra nella tabella del `SKILL.md`.

Questo asse è il più facile da riempire di rumore, perché ogni costante può essere raccontata come
rigidità. Il filtro è duplice, e serve tutto:

1. **si può nominare il secondo caso?** L'aliquota che cambia, il cliente estero, la seconda
   valuta, il secondo fornitore, il fuso orario diverso. Se il secondo caso è immaginario, non è
   una voce.
2. **quanto costa il giorno che arriva?** Un valore in un punto solo si cambia in un minuto e non
   è un blocco. Lo stesso valore in nove punti, o dentro una migrazione già applicata, sì.

## Dove si annidano

- **Sequenze fisse.** Il codice che esegue A poi B poi C perché è sempre stato così, e non prevede
  il caso in cui B non serve o va dopo C. Il segnale è una funzione lunga che chiama passi in
  ordine senza mai chiedersi se un passo si applichi.
- **Soglie e valori nel codice.** Aliquote, limiti, giorni di scadenza, dimensioni massime,
  percentuali. Conta in quanti punti compaiono: la molteplicità è il blocco, non il valore.
- **Assunzioni sul mondo.** Una valuta sola, un fuso orario, un formato di data, un paese, un
  numero fisso di elementi, un identificatore che si presume numerico. Il segnale è l'operazione
  che funziona solo perché l'input ha sempre avuto quella forma.
- **Configurazione che non arriva a destinazione.** Il parametro esiste in `.env` ma è letto una
  volta all'avvio e mai più, oppure esiste per l'ambiente e non per il singolo cliente. Il valore
  è configurabile in teoria e fisso nella pratica.
- **Formati di scambio.** Import ed export che accettano un solo tracciato: il secondo fornitore
  che manda le colonne in ordine diverso ferma il flusso.

## Cosa non è una voce

Il codice cablato che vive in un punto che nessuno tocca e che nessun caso nuovo raggiungerà.
Prevedere flessibilità per un futuro immaginario è il difetto opposto, ed è materia di Otto
(`grl-agent-architecture`): se la voce sta diventando «qui servirebbe un'astrazione», è finita
fuori asse.

Il confine pratico: Vito segnala la rigidità che **ha già un secondo caso in vista**, non quella
che potrebbe averne uno.

## La via d'uscita che si nomina

Quasi sempre è una di tre, e si dice quale senza scriverla: portare il valore in un punto solo,
rendere il passo condizionato al caso invece che fisso, oppure accettare il caso nuovo come
variante esplicita. Se il punto tocca lo schema dei dati o una migrazione, la soluzione è di Dario
(`grl-agent-database`) e Vito si ferma alla segnalazione.
