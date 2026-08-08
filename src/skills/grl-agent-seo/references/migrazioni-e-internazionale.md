# Migrazioni e siti internazionali

## Risultato

Un piano di cambiamento che conserva il valore delle URL quando possibile, rende esplicite le
eccezioni e permette di accorgersi presto di perdita di crawling, indicizzazione, traffico o
conversione. Il piano è consegnabile a chi implementa e a chi opera il rilascio.

## Prima del deploy

- inventaria URL vecchie, status, traffico, query, backlink e conversioni; se l'evidenza manca,
  dichiaralo e definisci un campione;
- mappa ogni vecchia URL verso la destinazione nuova più equivalente; una pagina senza equivalente
  non va mandata a caso sulla home;
- definisci redirect server-side, catene da evitare, canonical, sitemap, link interni, immagini,
  feed e riferimenti assoluti;
- prepara test su staging o campione, ma non confondere staging non indicizzato con prova di produzione;
- per lingue o paesi definisci relazione fra versioni, `hreflang`, canonical, fallback, dominio o
  sottocartella e contenuto realmente localizzato;
- pianifica accessi, rollback, annotazione del rilascio e proprietari del controllo.

## Durante e dopo

Verifica con campioni e report: status e redirect, vecchie URL ad alta priorità, nuove URL canoniche,
link interni, sitemap, robots, indicizzazione, query, impression, click, conversioni, errori di
rendering e anomalie di performance. Non chiedere il re-crawl di massa come gesto rituale: prima
assicurati che il nuovo asset sia accessibile e coerente.

### Come qualificare `hreflang`

Google definisce `hreflang` così: «Use `hreflang` to tell Google about the variations of your
content, so that we can understand that these pages are localized variations of the same content».

⚠️ **Google non lo qualifica né come direttiva né come segnale.** La formula corrente del settore —
«hreflang è un segnale, non una direttiva» — compare solo su blog di fornitori di strumenti, che se
la citano l'uno con l'altro e l'attribuiscono a John Mueller senza link alla dichiarazione originale.
Due ricerche indipendenti l'hanno cercata a vuoto su fonte Google (`as_of` 2026-08-08).

Usala con attribuzione al settore, mai a Google. Se la decisione dell'utente dipende dal fatto che
`hreflang` sia vincolante o no, dillo come incertezza documentata, non come regola.

Per una migrazione internazionale, non trattare la traduzione di una stringa come localizzazione:
controlla intenti, disponibilità, valuta, unità, contatti, norme applicabili e competenza editoriale.
Le questioni legali, privacy e di contenuto sanitario restano alle figure titolari.

## Gate

Una migrazione è pronta quando: esiste la mappa, i redirect critici sono testati, non ci sono
blocchi accidentali di crawling/indicizzazione, la sitemap è coerente, le URL principali hanno un
percorso interno, il monitoraggio è acceso e c'è una via di ritorno. Il ranking futuro non è un
criterio di certezza al giorno zero.
