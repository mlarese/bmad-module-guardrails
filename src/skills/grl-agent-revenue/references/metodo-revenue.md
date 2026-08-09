# Metodo di consulenza revenue

La consulenza non parte da “alza il prezzo”. Parte dall’obiettivo della struttura e dalla domanda che può essere difesa con i dati.

## Dati minimi

Chiedi solo ciò che può cambiare la decisione:

- struttura, tipologia di unità e capacità realmente vendibile;
- data di soggiorno, data di analisi e finestra di prenotazione;
- on-the-books, pickup per intervallo e storico comparabile;
- disponibilità, out-of-order, chiusure, eventi e restrizioni;
- segmento, canale, commissione/costo acquisizione e trattamento;
- ADR/RMC, RevPAR, ricavi ancillary, costi variabili e floor economico;
- obiettivo: occupazione, ricavo, margine, profitto, cash, mix di canale o riempimento di una data.

Se mancano dati decisivi, produci scenari “se/allora” invece di una media inventata.

Quando la richiesta chiede un prezzo ma i dati sono incompleti, la sezione
“Dati mancanti/rischi” deve nominare senza abbreviazioni la data di soggiorno,
la data di analisi, il pickup, la finestra di prenotazione, l’inventario, i
segmenti/canali, la durata del soggiorno, cancellazioni/no-show, obiettivo e
costi rilevanti o costo di acquisizione.

## Lettura della domanda

Separa:

- **stock:** camere/unità disponibili e vendibili;
- **pace:** prenotazioni e pickup rispetto a una data di soggiorno;
- **forecast:** domanda attesa fino alla data, con errore noto;
- **price signal:** ADR, competitive set, eventi, segmento e durata;
- **constraint:** minimum stay, CTA/CTD, chiusura arrivi, inventario, out-of-order e contratti.

Un’occupazione alta oggi non dimostra da sola che il prezzo sia troppo basso; può dipendere da calendario, gruppo, allotment, segmento o perdita di inventario. Un’occupazione bassa non dimostra da sola che serva uno sconto; prima controlla pickup, finestra di prenotazione, canale e domanda prevista.

## Decisione di prezzo

Restituisci, quando i dati lo consentono, una piccola matrice:

| Livello | Cosa rappresenta |
| --- | --- |
| Floor economico | Costo e margine minimo secondo QuoProfit o il conto economico |
| Base di mercato | ADR/RMC, competitive set e rate plan comparabili |
| Domanda prevista | Forecast, pickup, booking curve ed eventi |
| Prezzo consigliato | Scelta che bilancia domanda, margine, inventario e canale |
| Prezzo pubblicabile | Prezzo tradotto nel contratto del PMS/canale, con occupazione, tasse, fee e restrizioni |

Indica sempre quale livello stai usando. Se proponi un aumento o una riduzione, indica trigger, entità, durata, segmento/canale interessato e metrica da monitorare. Se il competitive set, la domanda o il costo canale non sono comparabili, non costruire una media: marca il segnale come non disponibile e usa solo scenari condizionati.

## Gruppi, allotment e overbooking

Per gruppi o contratti non confrontare solo il ricavo totale. Calcola displacement: camere sottratte alla vendita libera, ricavo atteso perso, ricavo del gruppo, ancillary, costi incrementali, rischio di cancellazione e valore strategico. Per overbooking servono storico di cancellazioni/no-show, capacità reale, walk policy e costo del disservizio; senza questi dati non dare un numero operativo.

## Output consigliato

Apri con il verdetto. Poi usa questa forma breve:

```text
Verdetto: ...
Dati usati: ...
Calcolo/lettura: ...
Raccomandazione: ...
Trigger e monitoraggio: ...
Dati mancanti/rischi: ...
Fonte o regola: ...
```

Per una richiesta puramente numerica usa lo script. Per una decisione commerciale combina script e giudizio, senza nascondere il passaggio interpretativo. “Cash” richiede dati finanziari e non si deduce da RevPAR o MUP; se serve, passa il tema alla figura fiscale/finanziaria competente.
