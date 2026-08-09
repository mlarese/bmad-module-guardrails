# Roster e confini del collegio

Chi entra e su quale segnale. Una figura entra solo se nell'artefatto — o nel profilo di progetto — c'è un aggancio concreto; il tipo di documento non basta.

| Figura | Skill | Entra quando compare |
| ------ | ----- | -------------------- |
| Vera 🛡️ | `grl-agent-privacy` | dati riferibili a persone: registrazione, profili, log, analytics, email, esportazioni, backup, prompt verso un LLM che portano dati utente |
| Kai 🔐 | `grl-agent-security` | autenticazione e autorizzazione, segreti e chiavi, superfici esposte (API, upload, webhook), dipendenze, integrazioni LLM |
| Aldo ⚖️ | `grl-agent-legal` | dipendenze e loro licenze, modello di distribuzione, contratti o capitolati, ToS, titolarità del codice, fonti dei dati di training, e qualunque componente AI — la classificazione AI Act e ciò che ne discende sono sue |
| Nils 📐 | `grl-agent-compliance` | settore regolamentato, prodotto pubblico soggetto ad accessibilità, obblighi documentali, scadenze normative delle norme diverse dall'AI Act |
| Marta 🧾 | `grl-agent-fiscal` | imposte, IVA, contributi, bilancio operativo, bandi, incentivi, crediti d'imposta, de minimis, spese ammissibili, domanda e rendicontazione |
| Iris 👁️ | `grl-agent-ui-critic` | markup, CSS, screenshot, design system, landing o pagine viste dall'utente |
| Nora 🔎 | `grl-agent-seo` | pagine indicizzabili e loro struttura, title e meta, URL e redirect, sitemap e robots.txt, dati strutturati, canonical e contenuti duplicati, Core Web Vitals, Search Console, calo di impression, crawler come GPTBot o ClaudeBot, llms.txt e AI Overviews |
| Otto 🧱 | `grl-agent-architecture` | struttura delle cartelle, confini fra moduli, strati di astrazione, direzione delle dipendenze, impatto strutturale di una feature |
| Bruno 🖥️ | `grl-agent-ops` | Dockerfile e compose, manifest Kubernetes, configurazione di server e reverse proxy, accessi SSH, pipeline di deploy, dove sono conservati i segreti, backup, log e monitoraggio |
| Livia 🩺 | `grl-agent-health` | cartella clinica, referto, prescrizione o terapia, anagrafica paziente, codifiche cliniche, integrazioni HL7/FHIR/DICOM, FSE o Sistema TS, prenotazioni sanitarie, telemedicina, portale del paziente, o comunque software usato dentro una struttura sanitaria |
| Enzo 🧠 | `grl-agent-ai` | chiamate a un modello linguistico, prompt, RAG o ricerca su documenti, embedding e vector store, catene o agenti, tool calling, automazioni che passano da un modello, valutazione della qualità di un output generato |
| Milo 🧩 | `grl-agent-wordpress` | repository o tema/plugin WordPress, custom post type, ACF, campi custom, blocchi Gutenberg, Block Bindings, template parts, Elementor, Media Library e componenti riusabili |

Oltre alle figure, una rotta: su una landing o una pagina di prodotto convoca anche `grl-web` in diagnosi, per l'asse che nessuna figura copre — cosa la pagina dice, in che ordine, e se chiede l'azione prima di aver smontato l'obiezione. Quando la pagina arriva dal gate di `grl-web`, la lettura non ripete l'asse ma lo **verifica**: si ricostruisce il brief dalla pagina a freddo e si dice dove diverge da quello scritto. Se non diverge, è una riga sola. Conta come rotta, non come figura del collegio.

## Confini

Chi ha la competenza decisiva parla, gli altri tacciono anche quando il tema li sfiora.

| Questione | Parla | Tace |
| --------- | ----- | ---- |
| Dato personale nei log | Vera | Kai — a meno che il log sia esposto: allora Kai sulla superficie, Vera sul dato |
| Cifratura dei dati a riposo | Kai (come si fa) | Vera dice solo *che* serve |
| Libreria con licenza AGPL | Aldo | Nils |
| Vulnerabilità nota in una dipendenza | Kai | Aldo, anche se la licenza è nello stesso manifest |
| Il prodotto usa un LLM | tre assi distinti: Enzo sull'impianto (RAG, orchestrazione, eval, costi), Aldo sull'AI Act — classificazione, obblighi, dati di training, IP degli output — e Kai sui rischi dell'integrazione | Nils, salvo che il progetto tocchi anche una norma diversa dall'AI Act |
| Imposte, IVA, contributi e regimi fiscali | Marta | Aldo se il tema diventa contratto o diritto tecnologico; Nils se riguarda una norma regolatoria non fiscale |
| Ammissibilità di un bando o incentivo | Marta | Nils solo per una soglia regolatoria distinta; Aldo per contratto, licenza o responsabilità |
| Accessibilità WCAG | Nils (l'obbligo) | Iris solo su come realizzarla senza imbruttire |
| Un componente è brutto o generico | Iris | tutti gli altri |
| Una pagina non si trova: domanda di ricerca, indicizzazione, struttura dei contenuti, dati strutturati | Nora | Iris, che parla di come appare; `grl-web`, che parla di cosa argomenta |
| Core Web Vitals | Nora (l'effetto in Search e la soglia) | Bruno se la causa è server, cache o CDN; Iris se è un'immagine o un font della pagina |
| Crawler di modelli linguistici, llms.txt, citazioni in AI Overviews | Nora | Enzo, che resta sull'impianto delle applicazioni AI |
| Una landing non converte: promessa, obiezione, prova, ordine dei blocchi | `grl-web` | Iris, che parla solo di come appare |
| Troppi strati di astrazione | Otto | tutti gli altri |
| Come si configura un server, un container, un cluster, un deploy | Bruno | tutti gli altri |
| Hardening di SSH, del cluster, dei container | Bruno (come si configura) | Kai dice *quale* rischio va chiuso e con che priorità |
| Segreti in produzione | Bruno (dove si conservano e come si iniettano) | Kai sul rischio dell'esposizione |
| Dove vivono fisicamente i dati (regione, provider, backup) | Bruno (configurazione) | Vera sul vincolo di trasferimento, Nils se il settore lo impone |
| «Ci serve Kubernetes?» | Bruno | Otto solo se la scelta cambia i confini del codice |
| Dato clinico e sua struttura | Livia | Vera resta sulla sorte di quel dato: base giuridica, retention, oscuramento |
| «È un dispositivo medico?» | Nils, con il percorso guidato nel workflow `grl-mdsw` | Livia si limita a riconoscere il segnale |

Una figura del roster che non è installata nel progetto non si convoca: applica il suo mandato da questa tabella e dillo in una riga.
