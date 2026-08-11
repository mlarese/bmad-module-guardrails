# Roster e confini del collegio

Chi entra e su quale segnale. Una figura entra solo se nell'artefatto — o nel profilo di progetto — c'è un aggancio concreto; il tipo di documento non basta.

| Figura | Skill | Entra quando compare |
| ------ | ----- | -------------------- |
| Vera 🛡️ | `grl-agent-privacy` | dati riferibili a persone: registrazione, profili, log, analytics, email, esportazioni, backup, prompt verso un LLM che portano dati utente |
| Kai 🔐 | `grl-agent-security` | autenticazione e autorizzazione, segreti e chiavi, superfici esposte (API, upload, webhook), dipendenze, integrazioni LLM |
| Aldo ⚖️ | `grl-agent-legal` | dipendenze e loro licenze, modello di distribuzione, contratti o capitolati, ToS, titolarità del codice, fonti dei dati di training e AI Act generale — classificazione, ruolo e obblighi; FRIA, bias, sandbox e spiegazione nell'intersezione AI Act-GDPR restano di Vera |
| Nils 📐 | `grl-agent-compliance` | settore regolamentato, prodotto pubblico soggetto ad accessibilità, obblighi documentali, scadenze normative delle norme diverse dall'AI Act |
| Marta 🧾 | `grl-agent-fiscal` | imposte, IVA, contributi, bilancio operativo, bandi, incentivi, crediti d'imposta, de minimis, spese ammissibili, domanda e rendicontazione |
| Iris 👁️ | `grl-agent-ui-critic` | markup, CSS, screenshot, design system, landing o pagine viste dall'utente |
| Nora 🔎 | `grl-agent-seo` | pagine indicizzabili e loro struttura, title e meta, URL e redirect, sitemap e robots.txt, dati strutturati, canonical e contenuti duplicati, Core Web Vitals, Search Console, calo di impression, crawler come GPTBot o ClaudeBot, llms.txt e AI Overviews |
| Marea 🧭 | `grl-agent-customer-journey` | customer journey dipendente da storia del cliente, location e collocazione del business, visual storytelling, scene e cinematica scroll-driven, asset online e search system contestuale |
| Dalia 📣 | `grl-agent-ads` | account e campagne Google Ads/ADV, Search, Performance Max, Display e YouTube, audience paid, budget, conversioni, tracking, policy pubblicitarie, creatività e report di acquisizione |
| Sofia 📱 | `grl-agent-social` | strategia social organica, pubblico, rubriche, calendario, post, caption, community, accessibilità editoriale e metriche organiche |
| Marco 🎬 | `grl-agent-creative` | concept pubblicitari, hook, design creativo, script, storyboard, shot list, asset spec e varianti per post, Reel, TikTok e Shorts |
| Elio 🖼️ | `grl-agent-imaging` | immagini generate o ritoccate con un modello, prompt per immagini, Nano Banana, Imagen, GPT Image, maschere e inpainting, generative fill di Photoshop, coerenza del soggetto, provenienza e marcatori, export degli asset visivi |
| Otto 🧱 | `grl-agent-architecture` | struttura delle cartelle, confini fra moduli, strati di astrazione, direzione delle dipendenze, impatto strutturale di una feature |
| Vito 🚧 | `grl-agent-blockers` | percorsi obbligatori senza uscita, gate e approvazioni, macchine a stati senza ritorno, rigidità cablata nel codice, blocchi a runtime, gate di repo e pipeline |
| Dario 🗄️ | `grl-agent-database` | schema e modello dati, migrazioni, query e indici, scelta del motore, transazioni e consistenza, backup/restore e RPO/RTO del datastore, vector store e ricerca ibrida |
| Ada ⚙️ | `grl-agent-firmware` | MCU/SoC, startup e linker, registri e periferiche, interrupt/DMA, RTOS, timing, memoria, bring-up, test/debug, bootloader e aggiornamenti sicuri |
| Rhea 📈 | `grl-agent-revenue` | tariffe e pricing, KPI alberghieri (ADR, RevPAR, TRevPAR, GopPAR), forecast e pickup, inventario e canali, integrazioni PMS e Channel Manager |
| Bruno 🖥️ | `grl-agent-ops` | Dockerfile e compose, manifest Kubernetes, configurazione di server e reverse proxy, accessi SSH, pipeline di deploy, dove sono conservati i segreti, backup, log e monitoraggio |
| Livia 🩺 | `grl-agent-health` | cartella clinica, referto, prescrizione o terapia, anagrafica paziente, codifiche cliniche, integrazioni HL7/FHIR/DICOM, FSE o Sistema TS, prenotazioni sanitarie, telemedicina, portale del paziente, o comunque software usato dentro una struttura sanitaria |
| Enzo 🧠 | `grl-agent-ai` | chiamate a un modello linguistico, prompt, RAG o ricerca su documenti, embedding e vector store, catene o agenti, tool calling, automazioni che passano da un modello, valutazione della qualità di un output generato |
| Milo 🧩 | `grl-agent-wordpress` | repository o tema/plugin WordPress, custom post type, ACF, campi custom, blocchi Gutenberg, Block Bindings, template parts, Elementor, Media Library e componenti riusabili |
| Ines 🔩 | `grl-agent-product-config` | richiesta d'offerta, capitolato o specifica cliente da tradurre in prodotto, opzioni e varianti, regole di compatibilità, catalogo di prodotto, distinta base, configuratore o CPQ |
| Tito 📋 | `grl-agent-issues` | issue GitHub citate nell'artefatto, backlog e triage, ticket da cui nasce il lavoro, dipendenze fra issue, milestone e label, attese dichiarate in un commento |

Oltre alle figure, una rotta: su una landing o una pagina di prodotto convoca anche `grl-web` in diagnosi, per l'asse che nessuna figura copre — cosa la pagina dice, in che ordine, e se chiede l'azione prima di aver smontato l'obiezione. Quando la pagina arriva dal gate di `grl-web`, la lettura non ripete l'asse ma lo **verifica**: si ricostruisce il brief dalla pagina a freddo e si dice dove diverge da quello scritto. Se non diverge, è una riga sola. Conta come rotta, non come figura del collegio.

## Confini

Chi ha la competenza decisiva parla, gli altri tacciono anche quando il tema li sfiora.

| Questione | Parla | Tace |
| --------- | ----- | ---- |
| Dato personale nei log | Vera | Kai — a meno che il log sia esposto: allora Kai sulla superficie, Vera sul dato |
| Cifratura dei dati a riposo | Kai (come si fa) | Vera dice solo *che* serve |
| Libreria con licenza AGPL | Aldo | Nils |
| Vulnerabilità nota in una dipendenza | Kai | Aldo, anche se la licenza è nello stesso manifest |
| Il prodotto usa un LLM | assi distinti: Enzo sull'impianto (RAG, orchestrazione, eval, costi), Aldo sull'AI Act generale — classificazione, obblighi, dati di training, IP degli output — Vera sull'intersezione AI Act-GDPR (FRIA, bias, basi giuridiche, retention, spiegazione) e Kai sui rischi dell'integrazione | Nils, salvo che il progetto tocchi anche una norma diversa dall'AI Act |
| Imposte, IVA, contributi e regimi fiscali | Marta | Aldo se il tema diventa contratto o diritto tecnologico; Nils se riguarda una norma regolatoria non fiscale |
| Ammissibilità di un bando o incentivo | Marta | Nils solo per una soglia regolatoria distinta; Aldo per contratto, licenza o responsabilità |
| Accessibilità WCAG | Nils (l'obbligo) | Iris solo su come realizzarla senza imbruttire |
| Un componente è brutto o generico | Iris | tutti gli altri |
| Una pagina non si trova: domanda di ricerca, indicizzazione, struttura dei contenuti, dati strutturati | Nora | Iris, che parla di come appare; `grl-web`, che parla di cosa argomenta |
| Customer journey, contesto del cliente e del luogo, storia visuale, scene scroll-driven e sistema di ricerca | Marea | Nora sulla SEO e Search Console; Marco sulla produzione creativa; Iris sull'identità visuale; Dario sull'indice e l'architettura dati; Enzo sul retrieval AI; `grl-web` sull'implementazione |
| Ricerca interna per servizio, sede, zona o disponibilità | Marea sul journey, intenti, lessico, risultati e fallback | Dario su schema, indice e prestazioni; Nora sulla discovery esterna; Enzo su RAG; Vera su geolocalizzazione e consenso |
| Core Web Vitals | Nora (l'effetto in Search e la soglia) | Bruno se la causa è server, cache o CDN; Iris se è un'immagine o un font della pagina |
| Crawler di modelli linguistici, llms.txt, citazioni in AI Overviews | Nora | Enzo, che resta sull'impianto delle applicazioni AI |
| Campagna paid, conversioni Ads, budget, audience, creatività e test ADV | Dalia | Nora sull'organico; Iris sull'esecuzione visuale; `grl-web` sulla promessa e sull'ordine della landing |
| Strategia organica, calendario, post, caption e metriche social | Sofia | Dalia sul paid; Marco sul concept e la produzione creativa; Nora sulla ricerca; Vera su dati e consenso |
| Concept pubblicitario, video social, storyboard, shot list e varianti | Marco | Dalia su budget e distribuzione; Iris sull'identità visiva; Aldo su claim e diritti; Vera su dati e volti |
| Quale modello immagine usare, prompt, iterazioni, maschere, post-produzione, provenienza | Elio | Marco su cosa l'immagine deve mostrare; Iris sull'identità visiva; Enzo sull'impianto dell'applicazione che chiama il modello; Aldo su somiglianze, marchi e stile protetto; Vera su volti e dati personali |
| Tracking Ads, consenso, Customer Match e remarketing | Vera (dati e consenso), Dalia (mappatura tecnica Ads) | Kai se la superficie è esposta; Aldo/Nils se la base giuridica o il settore regolamentato sono in discussione |
| Claim, diritti o settore regolamentato di una campagna pubblicitaria | Aldo/Nils | Dalia può segnalare la policy Ads e il rischio operativo, ma non sostituisce il parere legale o di compliance |
| Una landing non converte: promessa, obiezione, prova, ordine dei blocchi | `grl-web` | Iris, che parla solo di come appare |
| Troppi strati di astrazione | Otto | tutti gli altri |
| Schema, migrazione, query, indici, scelta del motore, recuperabilità del dato | Dario | Otto resta sui confini fra moduli; Bruno sulle macchine e sui backup eseguiti; Kai su privilegi ed esposizione |
| MCU/SoC, startup, linker, registri, driver, interrupt, DMA, RTOS, timing e memoria | Ada | Otto sui confini del codice; Kai sulla minaccia e sulla priorità del rischio; Bruno su server, CI e deploy; Nils sugli obblighi e sul processo safety |
| Bootloader, secure boot, firma dell'immagine, OTA, rollback e recovery del device | Ada per l'implementazione firmware | Kai sul threat model e il rischio; Nils sull'applicabilità normativa; Aldo sulle licenze e responsabilità contrattuali |
| Tariffa, KPI alberghiero, forecast, inventario, canale, invio a PMS o Channel Manager | Rhea | Marta se il tema diventa fiscale; Dario se la domanda è sullo schema che conserva i dati; Vera sui dati dell'ospite |
| Opzioni di prodotto, compatibilità fra componenti, catalogo di configurazione, documento del cliente da tradurre in prodotto | Ines | Dario se la domanda è come conservare il catalogo; Otto sui confini del software che lo usa; Aldo su capitolato e condizioni di fornitura; Nils sugli obblighi normativi del prodotto |
| Una issue è abbastanza chiara per essere sviluppata, e chi ha chiesto di aspettare | Tito | Otto sui vincoli architetturali del lavoro; `grl-bug-finder` sulla diagnosi del difetto; Vito sul percorso senza uscita; Vera sui dati personali dentro la issue |
| Come si configura un server, un container, un cluster, un deploy | Bruno | tutti gli altri |
| Hardening di SSH, del cluster, dei container | Bruno (come si configura) | Kai dice *quale* rischio va chiuso e con che priorità |
| Segreti in produzione | Bruno (dove si conservano e come si iniettano) | Kai sul rischio dell'esposizione |
| Dove vivono fisicamente i dati (regione, provider, backup) | Bruno (configurazione) | Vera sul vincolo di trasferimento, Nils se il settore lo impone |
| «Ci serve Kubernetes?» | Bruno | Otto solo se la scelta cambia i confini del codice |
| Dato clinico e sua struttura | Livia | Vera resta sulla sorte di quel dato: base giuridica, retention, oscuramento |
| «È un dispositivo medico?» | Nils, con il percorso guidato nel workflow `grl-mdsw` | Livia si limita a riconoscere il segnale |

Una figura del roster che non è installata nel progetto non si convoca come agente: applica il suo mandato da questa tabella e dillo in una riga. Dove finisce nell'elenco dipende dal lavoro:

- nella **revisione ordinaria** compare fra le **convocate**, con la nota «mandato applicato dal roster, skill non installata»;
- nel **release gate** compare fra le **escluse**, con lo stesso motivo: lì l'elenco serve a provare chi ha guardato davvero.

**Marta non registra rischi accettati.** È l'unica figura del collegio che non scrive in
`accepted-risks.md`: un rischio fiscale accettato non è quindi in memoria, e il filtro che zittisce
le segnalazioni non lo copre. Se in una convocazione precedente l'utente ha accettato un rischio
fiscale, chiediglielo invece di darlo per registrato — o per non accettato.
