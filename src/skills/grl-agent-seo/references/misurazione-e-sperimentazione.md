# Misurazione SEO e sperimentazione

## Risultato

Un piano di misura che distingue salute tecnica, visibilità, comportamento e valore commerciale,
con una baseline e una decisione possibile. Non basta dire «il traffico è salito».

## Baseline

Prima della modifica registra, con periodo e segmenti dichiarati:

- URL e template interessati;
- impression, click, CTR e posizione quando disponibili in Search Console;
- query, paesi, dispositivi e trend pertinenti;
- indicizzazione, errori, rich result e dati di esperienza disponibili;
- sessioni organiche, eventi, lead, acquisti o altra conversione definita dal progetto;
- cambi di prodotto, campagne, stagionalità, release, consenso analytics e fattori esterni noti.

Una posizione media o un CTR aggregato non descrive da solo una pagina né dimostra valore. Se il
tracciamento contiene dati personali, il trattamento e il consenso sono di Vera.

## Ipotesi

Formula la modifica come: «Su queste URL, per questo intento, cambiamo X perché osserviamo Y; ci
aspettiamo Z, misurato da M, entro una finestra coerente con il tipo di modifica». Tieni un gruppo
di confronto o un campione pre/post quando è possibile; annota le modifiche simultanee.

Non attribuire a SEO un risultato che potrebbe dipendere da brand, stagionalità, pricing, PR,
algoritmo, tracking o cambi di mercato. Distingui osservazione, correlazione, inferenza e prova.

## Prima di leggere una serie storica

Due controlli obbligatori, entrambi `as_of` 2026-08-08.

**1. L'anomalia delle impressions.** Google dichiara: «A logging error prevented Search Console from
accurately reporting impressions from **May 13, 2025 until April 27, 2026**»
([Data anomalies](https://support.google.com/webmasters/answer/6211453)). Chiunque confronti
impressions a cavallo di quella data **confronta due misure diverse**. La fonte non dichiara il verso
dell'errore: dice che il dato non era accurato, non che fosse sottostimato.

Altre anomalie datate del 2026 sulla stessa pagina: due giorni mancanti nei bulk data export a fine
febbraio; impressions e click non registrati per i search type «Job listing» e «Job details» dal 16
al 27 aprile; calo delle impressions su Performance e Rich result dal 7 maggio per la fine di FAQ;
cali su Discover e su «Generative AI in Discover» a maggio e giugno.

**Non esiste una pagina di release notes di Search Console.** «Data anomalies» è il changelog di
fatto sui dati; il changelog della documentazione è
[`developers.google.com/search/updates`](https://developers.google.com/search/updates). Consultali
prima di attribuire un salto a una modifica del sito.

## Cosa il report generativo non misura

Da giugno 2026 esiste il report **«Generative AI performance»**
([supporto](https://support.google.com/webmasters/answer/16984139)), e i suoi limiti vanno detti
**prima** di accettare una domanda di misura:

- **espone solo impressioni** — click, CTR e posizione non sono metriche del report;
- **non separa AI Overviews da AI Mode**: sono raggruppate, nessun filtro documentato;
- **i dati sono già dentro il Performance report standard**, search type «Web»: non isolabili per
  sottrazione;
- **è in rollout parziale**: un progetto può non avere il report.

**Conseguenza: la domanda «quanto traffico mi porta AI Overviews» non è rispondibile con Search
Console.** Se l'utente la pone, la risposta corretta è che lo strumento non lo consente — non una
stima. La fonte primaria è il [supporto del report Generative AI performance](https://support.google.com/webmasters/answer/16984139),
con `as_of` verificato nella sessione.

## Consegna minima per una domanda sulle funzioni generative

Prima di proporre una misura, scrivi esplicitamente: metrica disponibile, metrica richiesta ma non
disponibile, separazioni che lo strumento non offre, periodo e segmenti, anomalia eventualmente
attraversata, alternativa praticabile e limite dell'inferenza. Non usare il report generativo per
ricavare click, CTR, posizione o traffico da AI Overviews/AI Mode.

## Search Console e strumenti

Usa Search Console per come Google rileva, indicizza e serve il sito; usa analytics per il comportamento
e le conversioni definite dal progetto; usa test, log e browser per la causa tecnica. Le fonti e i
periodi devono essere riportati nell'output. La frequenza di controllo si adatta a release e rischio,
non a una superstizione quotidiana.

## Consegna

Restituisci: baseline, ipotesi, campione, metriche, segmenti, confondenti, data di verifica,
criterio di successo/fallimento, decisione prevista e ciò che resta non misurabile.
