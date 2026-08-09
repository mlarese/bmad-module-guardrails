# KPI e calcoli di revenue management

Usa questa scheda quando l’utente chiede un numero, una formula o un confronto. Prima di calcolare fissa struttura, data/periodo, valuta, regime IVA, ricavi inclusi, costi inclusi e denominatore. Se un denominatore è zero o mancante restituisci **non calcolabile**, non zero.

Nel risultato rendi sempre espliciti periodo, valuta, arrotondamento, perimetro
e omogeneità di ricavi/costi, componenti incluse o escluse e natura del dato:
consuntivo oppure forecast. Un calcolo consuntivo non va presentato come
previsione; i ricavi totali non devono duplicare il ricavo camere.

## KPI alberghieri

| KPI | Formula | Nota |
| --- | --- | --- |
| OCC / Occupancy | `camere vendute / camere disponibili × 100` | Disponibili = capacità effettivamente in vendita, non necessariamente camere fisiche |
| ADR / RMC | `ricavo camere / camere vendute` | Nel modello QuoProfit RMC/ADR è il ricavo medio per unità venduta |
| RevPAR | `ricavo camere / camere disponibili` oppure `ADR × OCC` | OCC va convertita da percentuale a decimale nella moltiplicazione |
| TRevPAR | `(ricavi camere + ancillary inclusi) / camere disponibili` | Non sommare due volte il ricavo camere; esplicita sempre le componenti incluse |
| NRevPAR | `(ricavo camere − costo acquisizione) / camere disponibili` | Il costo acquisizione può essere per canale o per prenotazione |
| GopPAR | `(ricavi totali − costi operativi) / camere disponibili` | Specifica periodo e perimetro dei costi |
| CPOR | `costi operativi identificati / camere vendute` | Non confonderlo con il costo totale per camera disponibile |
| MPI | `OCC struttura / OCC competitive set × 100` | Indice di penetrazione occupazionale |
| ARI | `ADR struttura / ADR competitive set × 100` | Indice di prezzo medio |
| RGI | `RevPAR struttura / RevPAR competitive set × 100` | Indice combinato di ricavo e occupazione |

Le definizioni OCC, ADR, RevPAR, TRevPAR, GopPAR, NRevPAR, CPOR, MPI, ARI e RGI sono allineate alla scheda metriche HSMAI/SIT citata in `references/ricerca-dominio.md`.

## Allocazione costi QuoProfit

Il progetto distribuisce costi totali, eventi e obiettivi tra tipologie di unità abitativa e date. Una forma leggibile della regola è:

```text
costo_tipologia_data = costo_totale × peso_tipologia_data / 100
costo_unità_data = costo_tipologia_data / unità_disponibili_della_tipologia
```

Il `peso_tipologia_data` deve essere già normalizzato sul calendario effettivamente aperto. In gestione automatica deriva dal peso economico delle tipologie; in gestione manuale deriva dai pesi inseriti per categoria. Non sommare pesi di categorie chiuse né dividere per unità fuori servizio.

## MOL e MUP interni

Nel modello QuoProfit il MOL è un margine percentuale scelto tra una base reale e una base auspicata:

```text
MOL_reale = 100 − (100 × costi_presunti / ricavi_anno_precedente)
MOL_auspicato = 100 − (100 × costi_presunti / ricavi_auspicabili)
MUP = costo_unità_data × (1 + MOL_selezionato / 100)
```

Se il ricavo dell’anno precedente o quello auspicabile è zero/mancante, il relativo MOL non è calcolabile. Se il cliente usa un MOL libero, il valore libero vince quello calcolato. La sigla MUP non è sciolta nei documenti: trattala come nome di una metrica interna, non inventarne l’espansione.

## Prezzo revenue e prezzo finale

La tabella di variazione per occupazione del progetto viene interpretata come punti percentuali solo se la configurazione lo dichiara:

```text
prezzo_revenue = MUP × (1 + variazione_occupazione_pct / 100)
```

Il prezzo finale segue questa logica esplicita:

1. scegli la base tariffaria: costo, MUP, listino, BAR, concorrenza, ADR/RMC o prezzo revenue;
2. applica la modifica generale per data;
3. applica la modifica per tipologia/unità;
4. applica il minimo garantito, se valorizzato;
5. applica il prezzo forzato, se valorizzato: vince sul resto, ma segnala se scende sotto MUP o minimo garantito;
6. aggiungi o separa trattamento, ospiti aggiuntivi, tasse e fee secondo il piano tariffario.

Non confondere un prezzo minimo economico con una previsione della disponibilità a pagare. Per una raccomandazione seria affianca almeno pickup, booking curve, disponibilità residua, segmenti, canale, restrizioni, durata del soggiorno, eventi e competitive set.

## Forecast e qualità del calcolo

- Usa booking curve e pickup per leggere il ritmo di acquisizione, non soltanto l’occupazione già raggiunta.
- Confronta forecast e consuntivo sullo stesso perimetro: data di soggiorno, tipologia, segmento e canale.
- Non usare MAPE senza gestire effettivi uguali a zero; usa una metrica complementare e dichiara il limite.
- Se una prenotazione è sintetica, esplodila per notte prima di calcolare occupazione, ADR o pickup.
- Tieni separati soggiorni, prenotazioni, unità fisiche, unità vendibili e unità fuori servizio.
