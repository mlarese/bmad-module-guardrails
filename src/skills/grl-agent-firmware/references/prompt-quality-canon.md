# Outcome-Driven Prompt Quality

Ogni riga di una capability deve cambiare il modo in cui Ada giudica o consegna il lavoro.
Scrivi la destinazione: postura, risultato, consumatore dell'output, soglia di qualità e vincoli
che il modello non può inferire. Il consumatore è un tecnico che deve poter agire senza questa
conversazione.

## Test

1. Se un modello competente produrrebbe lo stesso risultato senza una riga, tagliala.
2. Prima di cancellare, tronca: conserva l'istruzione e il perché che protegge un vincolo non ovvio.
3. Scrivi obiettivi, non la trascrizione di una sessione ideale; usa procedure esatte solo quando
   un errore costa davvero.
4. Numera solo sequenze reali; usa punti per obblighi indipendenti.
5. Carva il contenuto branch-specific nelle references solo quando l'indirezione ripaga il costo;
   una reference deve reggersi da sola e non rimandare a una seconda reference.

## Script o giudizio

Parsing, conteggio, confronto, validazione strutturale e trasformazione deterministica appartengono
allo script. Interpretazione, diagnosi, decisione con dati incompleti e sintesi appartengono al
prompt. Quando un controllo può avere un output atteso e un test unitario, non pagare il modello
per reinventarlo a ogni turno.

## Soglia

Il bare model è il pavimento: Ada deve aggiungere giudizio firmware, contratti hardware, confini
con le altre competenze o wiring del progetto. Se una capability non cambia l'esito rispetto al
modello nudo, va ritirata invece di essere gonfiata.
