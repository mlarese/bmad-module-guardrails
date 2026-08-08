# Diagnosi tecnica SEO

## Risultato

Un audit tecnico utile non è un elenco di errori: è una decisione su quali pagine e quali segnali
impediscono al motore di ricerca di scoprire, leggere, indicizzare o comprendere il contenuto. Il
referto deve lasciare al team una tabella di interventi ordinati, non un punteggio.

## Stance

Parti dall'obiettivo e dal campione: sito intero, template, URL critica, migrazione o calo osservato.
Se non sai quali URL contano, non fingere che tutte abbiano lo stesso valore. Distingui:

- **scoperta/crawl:** il crawler può trovare e scaricare la risorsa;
- **rendering:** il contenuto e i link importanti sono disponibili nel risultato renderizzato;
- **indicizzazione:** non esiste un blocco o un segnale contraddittorio che escluda la pagina;
- **comprensione e rilevanza:** la pagina risponde all'intento e si colloca nella struttura;
- **search appearance:** title, snippet, immagini e markup aiutano la scelta senza promesse;
- **conversione:** la visita produce il valore che il progetto misura.

## Evidenze da cercare

Usa ciò che è disponibile e dichiara ciò che manca:

- HTML sorgente e renderizzato, status HTTP, redirect, canonical, meta robots, title, heading,
  link interni, immagini e `alt` pertinente;
- `robots.txt`, sitemap e loro coerenza con le URL che il sito vuole rendere scopribili;
- template, router, framework, generazione statica o client-side, fallback, gestione errori e
  ambiente di staging;
- pagine duplicate o quasi duplicate, parametri, faceted navigation, paginazione, URL orfane,
  redirect chain, 404 e soft 404;
- Search Console: indicizzazione, URL Inspection, query, pagine, paesi, dispositivi, rich result,
  Core Web Vitals e anomalie temporalmente annotate;
- log del crawler o crawl controllato, quando l'utente li fornisce e il campione è dichiarato.

Non dedurre un blocco dall'assenza di una sitemap, né una penalizzazione da un calo. Cerca il
segnale che l'evidenza misura davvero.

## Priorità

Per ogni finding scrivi:

`evidenza → diagnosi → pagine coinvolte → impatto ipotizzato → fix minimo → owner → verifica → confidenza`

Ordina prima i blocchi di scoperta/indicizzazione sulle URL che contano, poi gli errori di
architettura e rendering, quindi contenuto e search appearance, infine ottimizzazioni a rendimento
incerto. Se un fix è rischioso, aggiungi precondizione, campione e rollback.

## Uscita minima

Consegna:

1. una riga di verdetto;
2. da tre a cinque finding prioritari, non tutti gli avvisi;
3. ciò che non è stato verificato;
4. il prossimo test e il criterio che conferma o smentisce la diagnosi.

Non usare soglie di performance, lunghezze di snippet o regole dei crawler come numeri eterni:
quando sono decisivi, verifica la documentazione corrente e registra `as_of`.

## Soglie Core Web Vitals

`as_of` 2026-08-08, copiate dalle pagine delle singole metriche — **la pagina riassuntiva riporta
solo la banda «buono»**, le bande complete stanno su `web.dev/articles/{lcp,inp,cls}`.

| Metrica | Buono | Da migliorare | Scarso |
| ------- | ----- | ------------- | ------ |
| LCP | ≤ 2,5 s | 2,5 – 4,0 s | > 4,0 s |
| INP | ≤ 200 ms | 200 – 500 ms | > 500 ms |
| CLS | ≤ 0,1 | 0,1 – 0,25 | > 0,25 |

Tutte al **75° percentile** dei caricamenti, segmentate fra mobile e desktop. INP ha sostituito FID
il **12 marzo 2024**; FID è uscito dagli strumenti Chrome il 10 settembre 2024 e dal dataset CrUX
`202409`. Un audit che nomina ancora FID cita una metrica ritirata.

Se l'utente porta un INP singolo, il verdetto deve classificare la fascia prima del fix: 350 ms è
**da migliorare**, non «scarso». Riporta le tre bande, il 75° percentile e il segmento (`as_of` e
fonte), poi diagnostica l'interazione e il lavoro JavaScript. Non proporre di riscrivere il copy SEO
come rimedio; server, CDN e caching sono di Bruno, mentre Nora definisce il sintomo SEO e il test di
verifica.

## Rendering — il fatto che spiega le diagnosi strane

Googlebot separa crawling, rendering e indexing, con una coda di rendering: le pagine con status 200
entrano in coda e un'istanza headless di Chromium esegue il JavaScript prima dell'indicizzazione.

Il punto meno noto e più utile in diagnosi: **il Web Rendering Service fa caching aggressivo e può
ignorare gli header di cache** — «Googlebot caches aggressively… WRS may ignore caching headers»
([JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)).
Conseguenza documentata: può usare JavaScript o CSS obsoleti. Rimedio raccomandato dalla stessa
pagina: **content fingerprinting**. Prima di ipotizzare un bug del sito, considera questa causa.

Altri fatti della stessa pagina: Google appiattisce shadow DOM e light DOM e indicizza solo il
contenuto renderizzato visibile; per le SPA raccomanda History API invece dei fragment URL; e
raccomanda status HTTP corretti, niente soft 404.

## `robots.txt` e sitemap — i valori correnti

`as_of` 2026-08-08:

- `robots.txt` è governato da **RFC 9309**. Google supporta quattro campi — `user-agent`, `allow`,
  `disallow`, `sitemap` — e dichiara che «other fields such as `crawl-delay` aren't supported»;
- limite di dimensione **500 KiB**: «Content which is after the maximum file size is ignored»;
- **`noindex` e `nofollow` dentro `robots.txt` non sono supportati**, il codice è stato ritirato il
  1 settembre 2019. La sostituzione è `noindex` come meta tag o header HTTP — e la pagina deve
  restare crawlabile perché la regola venga vista;
- una sitemap singola è limitata a **50 MB non compressi o 50.000 URL**.
