# Glossario SEO — definizioni e smentite

Questa pagina esiste per **le smentite**, non per le definizioni. La definizione dice cosa un termine
significa; la smentita dice quale fraintendimento diffuso la fonte stessa corregge, ed è quella che
distingue una risposta competente da una ripetizione di folklore.

Tutte le citazioni sono testuali dalla documentazione del proprietario. `as_of` **2026-08-08**: una
definizione riportata a memoria non vale, si apre la pagina.

## Il modello mentale ufficiale

> «Google Search works in three stages, and not all pages make it through each stage»
> — [How Search Works](https://developers.google.com/search/docs/fundamentals/how-search-works)

Le tre fasi si chiamano **crawling**, **indexing**, **serving search results**. Nella terminologia di
Google la terza si chiama *serving*, non *ranking*: il ranking avviene **dentro** il serving.

Frase di copertura su tutte e tre: «Google doesn't guarantee that it will crawl, index, or serve your
page, even if your page follows the Google Search Essentials».

| Termine | Definizione ufficiale | La smentita della stessa fonte |
| --- | --- | --- |
| crawling | «Google downloads text, images, and videos from pages it found on the internet with automated programs called crawlers» | il crawl non implica l'index: «Not every page that is crawled will necessarily be indexed» |
| indexing | «Google analyzes the text, images, and video files on the page, and stores the information in the Google index» | «Indexing isn't guaranteed; not every page that Google processes will be indexed» |
| serving | «When a user searches on Google, Google returns information that's relevant to the user's query» | «Google doesn't accept payment to crawl a site more frequently, or rank it higher» |
| rendering | «During the crawl, Google renders the page and runs any JavaScript it finds using a recent version of Chrome» | — |

## Canonicalizzazione — il soggetto è Google

Fonte: [Canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization).

> «Canonicalization is the process of selecting the representative –canonical– URL of a piece of
> content.»
>
> «a canonical URL is the URL of a page that **Google chose** as the most representative from a set
> of duplicate pages.»
>
> «You can indicate your preference to Google using these techniques, but **Google may choose a
> different page as canonical than you do**, for various reasons.»
>
> «That is, indicating a canonical preference is a **hint, not a rule**.»

**La parola esatta è `hint`** — non «directive», non «suggestion». È il termine da usare quando si
qualifica il segnale. La pagina operativa
[Consolidate duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
usa un registro diverso — `rel="canonical"` è «a strong signal» — e non è una contraddizione: forte
non significa vincolante.

⚠️ La **definizione** non sta in `consolidate-duplicate-urls`, che rimanda a `canonicalization`. Chi
cita la prima come fonte della definizione cita male.

## Le altre definizioni con la loro smentita

| Termine | Definizione ufficiale | La smentita |
| --- | --- | --- |
| `noindex` | «a rule set with either a `<meta>` tag or HTTP response header… used to prevent indexing content by search engines that support the `noindex` rule» | «If the page is blocked by a robots.txt file or the crawler can't access the page, the crawler will never see the `noindex` rule, and the page can still appear in search results»; e «Specifying the `noindex` rule in the robots.txt file is not supported by Google» |
| crawl budget | «the set of URLs that Google can and wants to crawl» — componenti: *crawl capacity limit* e *crawl demand* | la guida esclude la maggior parte dei siti: «If your site doesn't have a large number of pages that change rapidly… you don't need to read this guide». E «Don't use `noindex`» come leva. E il budget liberato non si riversa altrove «unless Google is already hitting your site's crawl capacity limit» |
| sitemap | «A hint: it doesn't guarantee that Google will download the sitemap or use the sitemap for crawling URLs on the site» | «Google ignores `<priority>` and `<changefreq>` values»; `<lastmod>` conta solo «if it's consistently and verifiably… accurate» |
| structured data | «a standardized format for providing information about a page and classifying the page content» | la pagina parla di **eleggibilità**: «required properties for an object to be **eligible** for appearance» e «can make it **more likely** that your information can appear» |
| rich result | risultati «more engaging to users and might encourage them to interact more with your website» | markup corretto = eleggibilità, non comparsa |
| `hreflang` | «Use `hreflang` to tell Google about the variations of your content, so that we can understand that these pages are localized variations of the same content» | vedi sotto: **nessuna qualificazione ufficiale** come direttiva o segnale |
| grounding / RAG | «A technique (also known as grounding) used to improve the quality, accuracy, and freshness of AI responses by relying on our **core Search ranking systems**» | non esiste un ranking «dell'AI» distinto da quello di Search |

## Le metriche di Search Console, e cosa non misurano

Fonte: [Performance report](https://support.google.com/webmasters/answer/7042828).

| Metrica | Definizione | La smentita |
| --- | --- | --- |
| impression | «How often someone saw a link to your site on Google» | in caroselli e sezioni espandibili l'elemento conta solo se entra nella viewport: impression ≠ visualizzazione |
| click | «How often someone clicked a link from Google to your site» | «Clicking to expand an item is not counted»; i click che restano dentro Google non contano |
| position | «A relative ranking of the position of your link on Google, where 1 is the topmost position…» | è la posizione più alta occupata, **mediata su tutte le query** — non «la posizione» della pagina; per Discover non viene registrata |
| CTR | «The calculation of (clicks ÷ impressions)» | — |

Per le funzioni generative la definizione è più stretta: «Impressions are how many times **links to
your site** were shown to a user in a generative AI feature». **Se il link non compare, non c'è
impression** — non basta che la risposta AI venga mostrata.

## I termini da non usare, e con quale autorità

**La forza della prova non è uguale per tutti**: va dichiarata caso per caso, non appiattita.

| Termine | Verdetto | Forza |
| --- | --- | --- |
| meta keywords | «Google Search doesn't use the keywords meta tag» | **primaria** — SEO Starter Guide |
| lunghezza del contenuto | «The length of the content alone doesn't matter for ranking purposes (there's no magical word count target, minimum or maximum…)» | **primaria** |
| keyword nel dominio | «the keywords in the name of the domain (or URL path) alone have hardly any effect beyond appearing in breadcrumbs» | **primaria** |
| ordine degli heading | «From Google Search perspective, it doesn't matter if you're using them out of order» | **primaria** |
| keyword density | la locuzione non compare nella documentazione. Google smentisce il comportamento: «Excessively repeating the same words over and over (even in variations) is tiring for users, and keyword stuffing is against Google's spam policies» | **primaria sul comportamento, non sulla metrica**: non esiste una soglia ufficiale da rispettare |
| E-E-A-T come fattore di ranking | «No, it's not.» — e «While E-E-A-T itself isn't a specific ranking factor, using a mix of factors that can identify content with good E-E-A-T is useful» | **primaria**, doppia fonte |
| crawl budget come leva di posizione | «Improving your crawl rate won't necessarily lead to better positions in Google Search results» | **primaria** — [Myths about crawling](https://developers.google.com/crawling/docs/myths-about-crawling) |
| freschezza cosmetica | «Create and update your content as necessary, but there's no additional value in making pages artificially appear to be fresh» | **primaria** |
| `crawl-delay` | «not processed by Google's crawlers» | **primaria** — è la direttiva che più persone scrivono e che Google ignora del tutto |
| LSI keywords | «There's no such thing as LSI keywords — anyone who's telling you otherwise is mistaken» | **secondaria** — attribuita a John Mueller, tweet 2019-07-30, ripetuta nel 2023. Confidenza media: citazione coerente su più fonti indipendenti, originale non aperto |
| domain authority | nessuna smentita ufficiale recuperata | **nessuna fonte primaria.** Il fatto verificabile è diverso: è una metrica proprietaria di Moz, non un output di Google — e si verifica su Moz. Confidenza bassa su qualunque «Google ha detto che…» |

## Un risultato negativo che è esso stesso il risultato

**`hreflang` non è qualificato da Google né come direttiva né come segnale.** La formula corrente del
settore — «hreflang è un segnale, non una direttiva» — compare solo su blog di fornitori di
strumenti, che se la citano l'uno con l'altro e l'attribuiscono a John Mueller senza link alla
dichiarazione originale. Due ricerche indipendenti l'hanno cercata a vuoto.

**Usala con attribuzione al settore, mai a Google.**

## Regola d'uso

Quando l'utente porta un termine di questa tabella, la risposta è: la definizione, la smentita, e la
**forza della prova**. Un «Google ha detto che…» che poggia su una fonte secondaria si dichiara come
tale, non si promuove.
