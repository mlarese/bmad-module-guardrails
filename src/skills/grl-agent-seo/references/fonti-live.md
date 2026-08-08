# Fonti SEO correnti e regola di verifica

## Gate obbligatorio

La verifica live si esegue **a ogni consultazione SEO**, non solo quando la domanda usa parole come
"ultimo aggiornamento" o "oggi". Un principio stabile può avere una documentazione, una feature o
una soglia cambiata; Nora non lo presume. Almeno una fonte primaria corrente deve comparire nella
risposta. Se il web non è raggiungibile, la risposta resta parziale e deve dirlo prima del verdetto.

## Le tre fonti che risolvono più domande di tutte le altre

Verificate l'8 agosto 2026. Prima di cercare altrove, guarda qui.

- [Changelog della documentazione Search Central](https://developers.google.com/search/updates) —
  **la fonte singola più densa**: deprecazioni, modifiche di policy, cambiamenti degli strumenti,
  tutte datate. Quando la domanda è «cosa è cambiato», si parte da qui;
- [Optimizing your website for generative AI features on Google Search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) —
  la posizione ufficiale su AI Overviews, AI Mode, `llms.txt`, GEO/AEO e dati strutturati per le
  funzioni generative (`as_of` 2026-07-10);
- [Google Crawling Infrastructure](https://developers.google.com/crawling/) — host distinto da
  Search Central, dove vive la materia crawling, inclusa la pagina
  [Myths about crawling](https://developers.google.com/crawling/docs/myths-about-crawling)
  (`as_of` 2025-12-18).

## Fonti primarie di riferimento

Per ogni consultazione, parti da fonti primarie e registra la data di verifica (`as_of`):

- [Google Search Essentials](https://developers.google.com/search/docs/essentials) — requisiti
  tecnici, spam policy e pratiche fondamentali;
- [Core update and new spam policies](https://developers.google.com/search/blog/2024/03/core-update-spam-policies) — date
  storiche di annuncio delle tre policy del 2024 e di entrata in vigore di site reputation abuse
  (`as_of` 2026-08-08); per lo stato corrente usare comunque la pagina Spam policies;
- [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) — l'elenco
  vigente, da leggere in pagina e non a memoria;
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) —
  contiene la sezione con le smentite esplicite («Things we believe you shouldn't focus on»);
- [Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) —
  criterio sui contenuti prodotti con automazione e posizione su E-E-A-T;
- [Come funziona Google Search](https://developers.google.com/search/docs/fundamentals/how-search-works) —
  distinzione fra crawling, indexing e serving;
- [Canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization) —
  la definizione e il fatto che `rel="canonical"` sia un `hint`;
- [Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start) —
  ispezione, indicizzazione, performance, rich result;
- [Data anomalies in Search Console](https://support.google.com/webmasters/answer/6211453) —
  **da consultare prima di leggere qualsiasi serie storica**: non esiste una pagina di release notes
  di Search Console, questa è il changelog di fatto sui dati;
- [Search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) —
  i rich result supportati oggi; i tipi dismessi sono **assenti**, non marcati;
- [Web Vitals](https://web.dev/articles/vitals) e le pagine delle singole metriche
  ([LCP](https://web.dev/articles/lcp), [INP](https://web.dev/articles/inp),
  [CLS](https://web.dev/articles/cls)) — le soglie complete stanno sulle pagine delle metriche,
  non su quella riassuntiva;
- [Google crawlers](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) —
  perimetro di `Google-Extended` e degli altri crawler Google;
- [Bing robots.txt](https://www.bing.com/webmasters/help/how-to-create-a-robots-txt-file-cb7c31ec) e
  [Bing AI Performance](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview)
  — `Bingbot`, preferenze `robots.txt` e citazioni aggregate in Copilot/Bing/partner (`as_of`
  2026-08-08); non documentano un user agent Copilot separato;
- [Status Dashboard di Google Search](https://status.search.google.com/) — incidenti e aggiornamenti
  dichiarati sui sistemi di ricerca.

## Due URL che non sono più quelli che sembrano

- **La cronologia degli aggiornamenti di ranking ha traslocato.**
  `developers.google.com/search/updates/ranking` risponde `301` verso il
  [Search Status Dashboard](https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history).
  Chi cita ancora il vecchio URL cita un redirect. Il dashboard espone la **durata** del rollout,
  non la data di fine: le chiusure si ricavano per somma, non si citano.
- **Il PDF linkato come «search quality rater guidelines» non è il documento.**
  `services.google.com/fh/files/misc/hsw-sqrg.pdf` è un opuscolo di 36 pagine intitolato
  «Search Quality Rater Guidelines: An Overview», datato novembre 2023. Il documento completo si
  chiama **General Guidelines** ed è a
  [questo URL](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf)
  (`as_of` versione 2025-09-11).

## Fonti non-Google

- [IndexNow](https://www.indexnow.org/) — aderenti dichiarati dal protocollo stesso: Microsoft Bing,
  Naver, Seznam.cz, Yandex, Yep. **Google non compare**, e non risulta una dichiarazione Google in
  merito su un canale Google: è «non verificato», non «Google ha detto no»;
- [IETF AIPREF](https://datatracker.ietf.org/wg/aipref/about/) — working group sulle preferenze
  verso i crawler AI, due deliverable standard track, **nessun RFC pubblicato**;
- documentazione dei crawler dei modelli: [OpenAI](https://developers.openai.com/api/docs/bots),
  [Anthropic](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler),
  [Perplexity](https://docs.perplexity.ai/guides/bots).
- [Cloudflare — AI traffic options](https://blog.cloudflare.com/content-independence-day-ai-options/) —
  classificazione Search/Agent/Training e comportamento dei crawler multipurpose (`as_of` 2026-08-08);
  fonte del fornitore, non prova indipendente sul traffico di un altro servizio.

## Regola operativa

La documentazione ufficiale descrive requisiti e comportamento documentato, non garantisce il ranking
di una pagina. Dopo aver eseguito il gate live, quando un'azione dipende da una feature attuale, da
una soglia, da un aggiornamento o da una policy:

1. cerca la pagina primaria corrente;
2. verifica che il testo si applichi al tipo di sito e al mercato dell'utente;
3. cita il link vicino alla conclusione e scrivi `as_of`;
4. separa la regola documentata dall'inferenza e dal test ancora da eseguire.

Se non puoi verificare, dichiaralo e non trasformare una memoria datata in una prescrizione.

## Come si pesa una fonte

Ordine di preferenza, senza eccezioni:

1. **documentazione del proprietario** — Google Search Central, web.dev, la documentazione del
   crawler di chi lo pubblica, una specifica o un RFC;
2. **paper o studio con metodologia dichiarata** — campione, periodo, metodo e limiti scritti
   dall'autore;
3. **niente.**

Bandiere rosse che abbassano la confidenza a vista: linguaggio speculativo, registro marketing,
passivo con fonti anonime, numeri non attribuiti, aggregatori che riciclano un unico report a monte
(è un solo publisher, per quanti domini lo rilancino), e chiunque venda il servizio basato
sull'affermazione che sta facendo. Gli answer engine sono aggregatori: si inseguono le loro citazioni
e si citano quelle, mai il motore.

I conflitti si risolvono per recenza, coerenza con i fatti adiacenti già stabiliti e qualità del
publisher — **mai facendo la media**. Quando due pagine Google si contraddicono, vince la più
recente: succede, ed è successo su AI Overviews.

**Un numero senza metodologia dichiarata non si cita.** Vale per le quote di mercato, per gli studi
zero-click e per qualunque percentuale di visibilità.
