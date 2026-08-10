# Percorsi obbligatori senza uscita

L'esito sono i punti in cui **una persona o un dato resta fermo** perché il software impone un
passaggio e non prevede modo di aggirarlo, saltarlo o tornare indietro. Ogni voce entra nella
tabella del `SKILL.md`.

Il metro non è «questo passaggio è necessario?» — quasi sempre lo è. Il metro è **cosa succede
al caso che il passaggio non aveva previsto**: il cliente estero senza codice fiscale, l'ordine
spedito per errore, il documento firmato dalla persona sbagliata, l'utente che ha perso l'accesso
alla seconda credenziale.

## Dove si annidano

- **Macchine a stati e workflow.** Il segnale è una transizione che esiste solo in avanti: da
  `shipped` non si torna, da `approved` non si annulla, da `closed` non si riapre. Guarda la mappa
  delle transizioni, non i singoli metodi.
- **Validazioni obbligatorie.** Un campo richiesto senza eccezione previste blocca ogni caso che
  non rientra nell'assunzione di chi l'ha scritto. Il segnale è un `required` senza ramo
  alternativo, o una regola che vale per tutti i paesi, tutti i tipi di cliente, tutti i formati.
- **Approvazioni e ruoli.** Un'azione che solo un ruolo può compiere si blocca quando quel ruolo
  è assente, ha lasciato l'azienda o è la persona stessa che deve essere approvata. Cerca il caso
  in cui l'approvatore e il richiedente coincidono.
- **Wizard e sequenze a passi.** Il passo che non si può saltare, il ritorno indietro che perde i
  dati già inseriti, l'uscita che lascia il record a metà.
- **Dipendenze esterne dentro un passaggio obbligatorio.** Se la verifica dell'indirizzo, il
  provider di identità o il servizio di firma non risponde, il percorso è chiuso: il blocco è
  del percorso, non del fornitore.

## Voluto o accidentale

La domanda che separa i due casi: **chi ha deciso che qui non si passa, e per quale conseguenza?**

- Se la risposta è una norma, un controllo di accesso, un obbligo contrattuale o la protezione di
  un dato — è voluto. Si marca `sì`, non si propone di toglierlo, e si nomina in una riga la figura
  che governa quel controllo (Kai, Vera, Nils, Marta).
- Se la risposta è «era il caso che avevamo in mente allora» — è accidentale, e la via d'uscita
  mancante si nomina.

Anche un blocco voluto può avere una via d'uscita legittima: non toglierlo, ma renderlo
percorribile con traccia — l'annullamento registrato, l'eccezione autorizzata da un secondo ruolo,
la scadenza dell'approvazione. Quando è così, dillo in una riga; resta comunque una decisione
della figura che governa il controllo.

## La prova che il blocco esiste

Cerca chi ci è già passato: lo script che corregge lo stato a mano, la richiesta ricorrente
all'assistenza, il flag nascosto che qualcuno ha aggiunto per il caso urgente, la riga di log che
dice «forzato». Un percorso senza uscita che ha già prodotto una scorciatoia fuori procedura è la
voce più alta della lista, perché il costo è già stato pagato e continua a pagarsi.

Se nessuno ci passa — la funzione non è chiamata, lo stato non viene mai raggiunto — dichiaralo e
tienilo fuori dalla lista.
