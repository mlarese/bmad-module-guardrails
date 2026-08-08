# Funzioni generative, crawler dei modelli e GEO

Tutti i fatti di questa pagina hanno `as_of` **2026-08-08** e vanno riverificati sulla fonte prima di
diventare una prescrizione. Le classi che invecchiano più in fretta sono segnalate voce per voce.

## Risultato

Una risposta che separa **quello che il proprietario del motore dichiara** da **quello che afferma
chi vende un servizio**, e che dice all'utente cosa può controllare, cosa può misurare e cosa no.

## La posizione ufficiale di Google

Fonte: [Optimizing your website for generative AI features on Google Search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide),
`as_of` 2026-07-10 — annunciata il 2026-05-15.

Cinque citazioni testuali, da usare come tali:

- «The best practices for SEO continue to be relevant because our generative AI features on Google
  Search are **rooted in our core Search ranking and quality systems**.»
- «You don't need to create new machine readable files, AI text files, markup, or Markdown to appear
  in Google Search (including its generative AI capabilities), **as Google Search itself doesn't use
  them**.»
- «It's completely fine if you decide to create and maintain LLMS.txt files (or other similar files)
  for other services or systems that use these files. Doing so will **neither harm nor help your
  site's visibility or rankings in Google Search, as Google Search ignores them**.»
- «**Structured data isn't required for generative AI search**, and there's no special schema.org
  markup you need to add.»
- «To maximize your site's visibility in generative AI search features, ensure your content is
  **crawlable**…»

E il consiglio esplicito: «**Prioritize effective SEO strategies over 'AEO/GEO hacks'**». Google
definisce entrambi gli acronimi in pagina — AEO come «answer engine optimization», GEO come
«generative engine optimization» — e li adotta **per delimitarli**, non per adottarne le pratiche.

Una frase copre tre miti insieme: «you can ignore tactics like 'chunking' content, creating
unnecessary AI text files (like llms.txt), or pursuing inauthentic mentions».

**Conseguenza operativa.** Non esiste un secondo campo da gioco con regole proprie. Alla domanda
«serve una strategia GEO separata» la risposta documentata è no, e la fonte è il proprietario del
motore. Dal 2026-05-15 **le spam policy si applicano anche alle risposte generative**
([changelog](https://developers.google.com/search/updates)).

Un solo meccanismo di selezione delle fonti è descritto da Google: il **query fan-out**, cioè più
ricerche su sottoargomenti della domanda. Non è un elenco di fattori di citazione, e nessun
proprietario di motore ne pubblica uno.

## Il controllo: cosa si può togliere e a che prezzo

**Dal 3 giugno 2026 esiste un toggle in Search Console** per uscire dalle funzioni generative
([annuncio](https://blog.google/products-and-platforms/products/search/new-controls-website-owners/)):

> «With this new toggle in Search Console, website owners can decide if they want their site to
> appear in and help ground responses in our generative AI Search features»

Il costo è dichiarato: «Sites that opt out will not receive traffic or impressions from our
generative AI features». Google dichiara che non c'è penalizzazione altrove: «This control will not
be used as a ranking signal for search results outside of these generative AI Search features».

⚠️ **La documentazione tecnica non lo dice.** La pagina
[AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) è
ferma al 2025-12-10 e indica ancora solo `nosnippet`, `data-nosnippet`, `max-snippet` e `noindex`.
Chi risponde alla domanda «come esco da AI Overviews» partendo da lì **dà una risposta obsoleta**.

Prima di giugno 2026 un opt-out selettivo non esisteva: i controlli di snippet agiscono a livello di
pagina e valgono anche per i risultati classici, quindi uscire dall'AI significava uscire dalla
ricerca. Oggi il toggle sembra agire a livello di property — **da verificare** se resti l'unica via
a granularità di pagina.

## Gli user agent dichiarati

`as_of` 2026-08-08. **È la classe che invecchia più in fretta**: riverificare entro il 2026-10-01.

| Proprietario | User agent | Scopo dichiarato | Blocco |
| --- | --- | --- | --- |
| OpenAI | `GPTBot` | addestramento dei foundation model | `robots.txt`; IP su `openai.com/gptbot.json` |
| OpenAI | `OAI-SearchBot` | «to surface websites in search results in ChatGPT's search features» | `robots.txt` |
| OpenAI | `ChatGPT-User` | fetch su richiesta dell'utente — «not used for crawling the web in an automatic fashion» | `robots.txt` |
| OpenAI | `OAI-AdsBot` | dichiarato nella stessa pagina | `robots.txt` |
| Anthropic | `ClaudeBot` | addestramento | `Disallow: /`; IP su `claude.com/crawling/bots.json` |
| Anthropic | `Claude-User` | accesso su richiesta dell'utente | idem |
| Anthropic | `Claude-SearchBot` | qualità dei risultati di ricerca | idem |
| Perplexity | `PerplexityBot/1.0` | indice di ricerca — «not used to crawl content for AI foundation models» | `robots.txt`; IP su `perplexity.com/perplexitybot.json` |
| Perplexity | `Perplexity-User/1.0` | fetch avviata dall'utente | **solo filtro IP**: la pagina dichiara che «generally ignores robots.txt rules» |
| Google | `Google-Extended` | addestramento Gemini e grounding in Gemini Apps e Vertex AI | `robots.txt` |
| Microsoft/Bing | `bingbot` | crawler documentato di Bing Search | `robots.txt`; la relazione con Copilot non è separata nella documentazione pubblica |

Tre conseguenze da dire sempre, perché sono le tre confusioni più frequenti:

1. **Bloccare `GPTBot` non toglie il sito dalla ricerca di ChatGPT** — quella è `OAI-SearchBot`.
2. **`Google-Extended` non incide su Google Search né sul ranking**, e non ha una stringa HTTP
   propria: non è osservabile nei log come token separato. Per uscire dalle funzioni generative
   serve il toggle, non `Google-Extended`.
3. **`anthropic-ai` e `Claude-Web` non compaiono** nella documentazione Anthropic corrente, ma
   circolano ancora in molte blocklist di terzi. Confidenza media: è un'assenza dalla pagina, non
   una negazione esplicita.

### Cosa è documentato da Microsoft/Bing

Fonti ufficiali riverificate `as_of` **2026-08-08**: [istruzioni Bing per
`robots.txt`](https://www.bing.com/webmasters/help/how-to-create-a-robots-txt-file-cb7c31ec) e
[AI Performance in Bing Webmaster Tools](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview),
pubblicato il 2026-02-10.

- La documentazione `robots.txt` nomina `Bingbot` come user agent del crawler Bing.
- AI Performance aggrega citazioni provenienti da Microsoft Copilot, riepiloghi generati in Bing e
  integrazioni partner; misura citazioni e pagine citate, non ranking o posizione nella risposta.
- La stessa fonte dichiara che Bing rispetta le preferenze espresse con `robots.txt` e altri controlli
  supportati.
- Le fonti pubbliche consultate **non documentano un user agent separato per Copilot**, né permettono
  di dedurre che ogni fetch di Copilot passi dal solo `Bingbot`. Questa è un'assenza documentale, non
  la prova che non esista un percorso distinto.

Per una domanda «ho bloccato Bingbot, sono fuori da Copilot?» la risposta corretta resta condizionata:
separa Bing Search, Copilot e integrazioni partner; controlla `robots.txt`, log, user agent, IP e i
dati AI Performance del sito verificato. Non inventare un token `robots.txt` Microsoft e non promettere
copertura del traffico utente.

## Le dichiarazioni dei proprietari non coprono tutto il traffico

Caso Cloudflare–Perplexity, agosto 2025. Cloudflare
([post](https://blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers-to-evade-website-no-crawl-directives/))
ha registrato domini di test nuovi con `robots.txt` che vieta ogni accesso automatico, poi ha
interrogato Perplexity su quei domini e ha ottenuto risposte contenenti il contenuto bloccato, con
uno user agent non dichiarato e IP fuori dai range pubblicati. Perplexity ha replicato che si tratta
di richieste avviate dall'utente e non di crawling, qualificandosi come «agentic AI platform».

**Le due parti non divergono sui fatti osservati, divergono sulla categoria in cui ricadono.**

Due caveat: Cloudflare vende il prodotto che blocca, e la replica di Perplexity non è stata letta in
primaria (il post risponde `403`). Il caso ha un anno e lo stato attuale non è verificato.

Aggiornamento del contesto, `as_of` **2026-08-08**: Cloudflare ora propone controlli distinti per
traffico **Search**, **Agent** e **Training** nella sua
[policy di gestione del traffico AI](https://blog.cloudflare.com/content-independence-day-ai-options/)
(pubblicata 2026-07-01) e dichiara che crawler multipurpose come Googlebot e Bingbot possono ricadere
nelle regole più restrittive. È un cambiamento della classificazione e del prodotto Cloudflare, non una
prova che il comportamento di Perplexity osservato nel 2025 sia cessato o continui: per il sito
specifico servono log, IP e test ripetibili.

Quello che resta valido come regola: **la documentazione che un proprietario pubblica descrive i
crawler dichiarati, e non copre necessariamente tutto il traffico che origina da quel servizio.**

## Standard e semi-standard

| Meccanismo | Cos'è | Stato |
| --- | --- | --- |
| `robots.txt` | standard, RFC 9309 | vigente |
| IETF **AIPREF** | due deliverable standard track; `attach` copre Well-Known URI e header HTTP | **nessun RFC pubblicato**, milestone 2026-08-31 |
| Cloudflare **Content Signals** | riga `Content-Signal:` in `robots.txt` con `search`, `ai-input`, `ai-train` | **policy di un fornitore**, non uno standard |
| `llms.txt` | proposta individuale di Jeremy Howard, 2024-09-03 | mai standardizzata; ignorata da Google Search |

Cloudflare afferma che i suoi segnali valgono come «express reservations of rights under article 4
of the European Union Directive 2019/790»: è **una qualificazione giuridica dell'autore della
policy**, non una pronuncia di un'autorità. Se l'utente vuole appoggiarci una decisione legale, il
tema è di Nils, non di Nora.

## Misurare la visibilità nelle funzioni generative

Da giugno 2026 esiste il report **«Generative AI performance»** in Search Console
([supporto](https://support.google.com/webmasters/answer/16984139)), e i suoi limiti sono la parte
che conta:

- **espone solo impressioni** — «Impressions are how many times links to your site were shown to a
  user in a generative AI feature on Google Search». Click, CTR e posizione non sono metriche del
  report;
- **non separa AI Overviews da AI Mode**: sono elencate insieme, nessun filtro documentato;
- **i dati sono già dentro il Performance report standard**, search type «Web»: non isolabili per
  sottrazione;
- **è in rollout parziale** — «We're rolling out this report to a subset of website owners».

**Conseguenza da dire all'utente prima di qualunque promessa: la domanda «quanto traffico mi porta
AI Overviews» non è rispondibile con Search Console.** Se il link al sito non compare nella risposta,
non c'è nemmeno impression.

## Il paper GEO, e perché il «40%» non si cita

Aggarwal et al., KDD '24 ([arXiv 2311.09735](https://arxiv.org/pdf/2311.09735v3)) è il lavoro su cui
poggia quasi tutta la pubblicistica GEO. Letto per intero, il numero che circola non regge:

- il **40% è un miglioramento relativo** sulla metrica *Position-Adjusted Word Count*, su GEO-bench
  nel suo insieme;
- il motore valutato è **una pipeline costruita dagli autori** — prime 5 fonti da Google, risposta
  generata da `gpt-3.5-turbo`;
- sul motore commerciale reale (Perplexity.ai) i guadagni scendono: Quotation Addition «a 22%
  improvement», Statistics Addition «up to 9% and 37% on the two metrics»;
- **il segno dell'effetto cambia con la posizione di partenza**: Cite Sources dà **+115,1%** ai siti
  in quinta posizione SERP e **−30,3%** a quelli in prima;
- l'effetto dipende dal dominio, e **Keyword Stuffing va peggio della baseline del 10%**;
- il benchmark è composto da 10.000 query **sintetiche e riusate**, non da traffico reale;
- gli autori dichiarano che i metodi «may need to adapt over time as GEs evolve» e che «we didn't
  evaluate how GEO methods affect search rankings».

Il lavoro ha oltre due anni. **Non trasferire quei numeri a un sito reale.**

## L'assenza da dichiarare

Non esiste — a oggi, cercato senza trovarlo — **uno studio con metodologia dichiarata, successivo al
2024, prodotto da un soggetto che non vende strumenti di tracking, sui fattori che correlano con
l'essere citati nelle risposte generative.** Quando l'utente chiede «cosa fa comparire il mio sito
nelle risposte AI», questa assenza è parte della risposta.

## Consegna

Per una domanda su funzioni generative, crawler o GEO consegna:

1. cosa dichiara il proprietario del motore, con citazione e `as_of`;
2. cosa l'utente può controllare, e a che prezzo dichiarato;
3. cosa è misurabile e cosa no, con lo strumento che lo misura;
4. cosa non è verificato — nominandolo, senza riempirlo.
