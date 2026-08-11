# Modello QuoProfit/RevD

Questa è la sintesi operativa dei documenti locali `docs/supporto/quoprofit/Nuovo RevD R25042024.docx`, `RevD Specifiche Calcoli 18_09_2024.docx`, `CALCOLI SIMULATORE.docx` e `Funzionalità Quoprofit.docx`. Sono requisiti e regole proprietarie del progetto, non standard di revenue management.

Ogni risposta che presenta MUP o MOL deve ripetere il confine: sono regole
interne QuoProfit/RevD, non standard universali e non dimostrano da sole che
il prezzo sia ottimale o accettato dal mercato.

## Perimetro

QuoProfit/RevD è pensato come piattaforma per strutture ricettive. Gestisce anagrafica, unità abitative (UA), categorie e sigle, unità madre/derivate, aperture e chiusure, eventi, listini, BAR, costi, trattamenti, extra, prenotazioni, benchmark, report, simulatore e pubblicazione verso PMS/Channel Manager.

## Flusso dati

1. Configura struttura, categorie UA, unità vendibili, capienza, trattamenti, calendari, eventi, listini e costi.
2. Importa prenotazioni da CSV/Excel/Google Sheet o API PMS.
3. Mappa le colonne PMS: prenotazione, check-in/out, data di ospitalità, UA venduta/assegnata, tipologia, prezzo, persone, trattamento e canale.
4. Se l’export è sintetico, esplodi ogni soggiorno in una riga per notte; se attraversa l’anno, taglia e riproporziona la parte di competenza.
5. Calcola venduto, occupazione, ricavi con/senza trattamento, progressivi, extra, contratti e disponibilità.
6. Distribuisci costi e margine per tipologia e data; calcola il simulatore e il prezzo finale.
7. Prepara l’esportazione o la pubblicazione di prezzi e disponibilità; invia solo dopo il gate tecnico e l’autorizzazione, poi riconcilia il risultato con il PMS/canale.

## Pesi e costi

Il peso generale della data deriva dal massimo tra trend della località, percezione/peso inserito dal cliente e trend dell’occupazione. Il valore va normalizzato sulle categorie UA aperte. L’allocazione può essere automatica, basata su numero di UA e prezzo minimo, oppure manuale, basata sui pesi di categoria inseriti dal cliente.

La regola semplificata è:

```text
costo_tipologia_data = costo_totale × peso_tipologia_data / 100
costo_unità_data = costo_tipologia_data / unità_disponibili_della_tipologia
```

Eventi e costi possono essere distribuiti in tutta la stagione oppure pesati sulla data dell’evento. Trattamenti, letti aggiuntivi, extra e contratti devono essere separati dal ricavo camera quando si calcolano ADR/RMC e RevPAR.

## Prezzi del simulatore

Il simulatore mostra costo, MUP, listino, BAR, concorrenza, RMC/ADR, RevPAR, occupazione, disponibilità, profitto, prezzo minimo, minimo garantito, modifica percentuale, prezzo forzato e prezzo finale.

Nel modello documentato:

- il costo viene maggiorato dal MOL reale, auspicato o libero per ottenere il MUP;
- il prezzo revenue modifica il MUP in funzione di una tabella di occupazione;
- il cliente può selezionare un piano tariffario, modificare percentuali, fissare un minimo o forzare un valore assoluto;
- per UA derivate si può ereditare il piano della UA madre e adattarlo a capienza/peso;
- il prezzo forzato vince sul prezzo minimo garantito e sugli altri passaggi.

Rhea deve mostrare la sequenza e non dire soltanto “il prezzo è X”. Se il progetto non specifica se i valori della tabella sono punti percentuali o moltiplicatori, deve fermarsi e chiedere conferma.

## Conflitti da non nascondere

La specifica generale contiene Release, fascia oraria e peso infrasettimanale; `CALCOLI SIMULATORE.docx` chiede di eliminare proprio queste componenti e aggiunge la gestione esplicita di UA virtuali/madri, totali manuali per campeggi/allotment, eventi visibili e mapping di vecchie sigle PMS. Finché non esiste una decisione di versione, l’agente deve presentare entrambe le varianti e non combinarle silenziosamente.

Anche il rapporto tra “QuoProfit” e “RevD” non è formalizzato: usa “modello QuoProfit/RevD” e segnala l’ambiguità quando serve una decisione di prodotto.

## Cosa il modello non dimostra

I documenti non dimostrano da soli un forecast statistico, un modello di elasticità, un competitive set aggiornato, una gestione robusta di overbooking o una integrazione API pronta per la produzione. Quelle conclusioni richiedono dati, contratto del PMS/canale, test e ricerca aggiornata.
