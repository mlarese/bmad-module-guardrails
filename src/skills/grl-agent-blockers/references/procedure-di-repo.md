# Procedure di repo e pipeline

L'esito sono i punti in cui **chi lavora al progetto resta fermo**: un gate che non passa, uno
script che si arresta, una procedura senza scorciatoia. Chi resta fermo qui non è l'utente finale,
è chi sviluppa, chi rilascia o chi deve correggere in fretta. Ogni voce entra nella tabella del
`SKILL.md`.

Il metro è specifico di questo asse: **cosa succede alle tre di notte con un bug in produzione?**
Un gate che protegge il rilascio ordinario e non prevede il rilascio urgente non è severo, è chiuso.

## Dove si annidano

- **Gate che fermano tutti.** Un controllo obbligatorio in pipeline che non ha modo di essere
  saltato con motivazione tracciata: copertura minima, lint bloccante, scansione delle dipendenze,
  approvazione manuale. La domanda è se esiste un percorso d'emergenza e se lascia traccia.
- **Gate instabili.** Un test intermittente dentro un gate bloccante blocca a caso, ed è peggio di
  un gate assente perché insegna a ignorarlo. Cerca chi ha già imparato a rilanciare finché passa.
- **Script che si arrestano senza dire come proseguire.** Il setup che fallisce su una dipendenza
  mancante, il build che richiede un segreto che solo una persona ha, il comando che va eseguito in
  un ordine che non è scritto da nessuna parte.
- **Un solo detentore.** Una credenziale, un accesso, un ambiente o una conoscenza che sta in una
  persona sola: quando è in ferie, la procedura è chiusa. È un blocco anche se nessuna riga di
  codice lo dice.
- **Rilasci senza ritorno.** Il deploy che non ha rollback, la migrazione che parte insieme al
  rilascio, la versione precedente che non è più eseguibile.
- **Ambienti che non si riproducono.** Se l'ambiente locale non si ricrea da zero, chi entra nuovo
  resta fermo e chi deve riprodurre un bug urgente pure.

## Voluto o accidentale

Molti gate sono rigidi apposta, e vanno riconosciuti come tali: la firma obbligatoria su un
rilascio regolamentato, la separazione dei ruoli fra chi scrive e chi approva, il controllo sui
segreti. Si marcano `sì` e la loro calibrazione resta di chi la governa — **Kai** per i controlli
di sicurezza, **Nils** per gli obblighi normativi, **Bruno** per pipeline e deploy.

La differenza che conta: un gate voluto **prevede il proprio caso eccezionale** e lo traccia. Un
gate voluto senza via d'emergenza è comunque una voce, e la via d'uscita da nominare non è
toglierlo — è renderlo percorribile con traccia e con un secondo ruolo.

## La prova che il blocco esiste

È la più visibile di tutti gli assi: il commit che dice «skip ci», il gate disattivato «per ora»
sei mesi fa, la variabile d'ambiente che qualcuno passa per saltare un controllo, il messaggio
ricorrente che chiede a una persona di far passare qualcosa. Dove trovi una di queste, il blocco è
già costato.
