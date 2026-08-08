# Guardrails (`grl`)

Modulo [BMad](https://github.com/bmad-code-org/BMAD-METHOD) con **dodici figure di presidio** che
affiancano il team dentro il ciclo di sviluppo software: privacy e GDPR, sicurezza applicativa,
legale e licenze, compliance normativa, fisco e finanza agevolata, qualità visiva della UI, disciplina architetturale del
codice, infrastruttura e operatività, dominio clinico del software sanitario, impianto delle
applicazioni che usano modelli linguistici, architettura WordPress a componenti e SEO.

Guardrail, non autista: il modulo tiene il progetto in carreggiata, le decisioni restano al team.

## Perché

Vincoli normativi, scelte di sicurezza e debiti strutturali, se emergono a fine progetto, costano
riscritture. Guardrails li fa emergere quando cambiare è ancora economico — e li ricontrolla lungo
tutto il ciclo, dai requisiti al pre-rilascio.

Le figure **parlano, non producono documenti formali**: niente DPIA firmate, niente registro dei
trattamenti, niente parere professionale sostitutivo. I due workflow di ricerca producono invece
digest temporali verificabili con fonti e data di accesso; `grl-web` produce landing page e siti.
Le decisioni del modulo restano righe brevi nella memoria condivisa del progetto.

## Le dodici figure

Le figure sono agenti interattivi, non dodici revisori da convocare sempre insieme. In
auto-attivazione parla al massimo una figura — quella con la competenza decisiva — e lascia una
traccia breve nella memoria condivisa solo quando nasce una decisione o l'utente accetta un
rischio. Per una lettura collegiale dello stesso artefatto si usa `grl-board`, che seleziona le
figure pertinenti e rende espliciti anche i motivi di esclusione.

| Agente | Quando coinvolgerlo | Cosa porta e quale esito aspettarsi |
| --- | --- | --- |
| 🛡️ **Vera**<br>Data Protection Officer | Registrazione, profili, email, analytics, log, backup, esportazioni, dati sanitari o dati utente dentro prompt e ambienti di test. | Mappa i dati personali, base giuridica, minimizzazione, retention e cancellazione; segnala se serve approfondire una DPIA. Non produce una DPIA formale e può chiudere con «qui non si applica niente, vai». |
| 🔐 **Kai**<br>Application Security Engineer | Autenticazione e autorizzazione, API, upload e webhook, segreti esposti, dipendenze vulnerabili, CVE, prompt injection e superfici LLM. | Ordina i modi realistici in cui il sistema potrebbe essere attaccato e propone la contromisura minima con il suo costo. La conservazione e l'iniezione dei segreti sono invece di Bruno. |
| ⚖️ **Aldo**<br>Tech Lawyer | Licenze OSS, distribuzione, titolarità del codice, contratti e DPA, termini di servizio, dati di training, output AI e AI Act. | Traduce il vincolo in una decisione: cosa si può usare, vendere o pubblicare, quali accordi mancano e quali obblighi scattano. È il riferimento legale unico del modulo sull'AI Act. |
| 📐 **Nils**<br>Regulatory Compliance | NIS2, DORA, EAA/WCAG, eIDAS, Cyber Resilience Act, MDR e obblighi del settore bancario o sanitario. | Prima stabilisce se una norma si applica davvero e quale soglia lo determina; poi indica obblighi, livello di accessibilità e scadenze. Non sostituisce Kai sull'implementazione tecnica né Aldo su contratti e licenze. |
| 🧾 **Marta**<br>Fiscalista e Finanza Agevolata | Imposte, IVA, contributi, bandi, incentivi, credito d'imposta, de minimis, Invitalia, MIMIT e Agenzia delle Entrate. | Verifica fonte primaria, requisiti, scadenze, spese ammissibili e rendicontazione; restituisce un pre-screening operativo, senza presentare istanze né sostituire il professionista abilitato. |
| 👁️ **Iris**<br>Design Critic | Landing, pagine, screenshot, markup, CSS, design system, tipografia, palette, densità e layout; anche accessibilità quando il tema è come realizzarla senza appiattire il design. | Riconosce i pattern generici e propone una deviazione concreta, con valori visivi utilizzabili. Nils stabilisce invece quale requisito di accessibilità è obbligatorio. |
| 🧱 **Otto**<br>Code Architect | Struttura delle cartelle, confini fra moduli, dipendenze circolari, feature nuove, interfacce e factory introdotte «per il futuro». | Indica il numero minimo di strati e il punto giusto in cui collocare una responsabilità; pesa il costo di non seguire la raccomandazione e non prescrive architetture per dogma. |
| 🖥️ **Bruno**<br>Infrastructure & Ops Engineer | Server e VPS, SSH, Docker, Kubernetes, CI/CD, deploy e rollback, reverse proxy, TLS, segreti, backup, log, monitoraggio e incidenti operativi. | Propone l'impianto più semplice che regge il carico vero e una via di ritorno verificabile. Spiega i comandi prima di darli e non modifica la produzione di propria iniziativa. |
| 🩺 **Livia**<br>Clinical Informatics | Cartella clinica, referti, prescrizioni, pazienti, codifiche ICD/LOINC/SNOMED/ATC, HL7/FHIR/DICOM, FSE, Sistema TS, CUP, LIS/RIS/PACS e telemedicina. | Verifica modello dati, interoperabilità, workflow di reparto e sicurezza del paziente chiedendo chi userà davvero la schermata. Se emerge supporto alla decisione clinica o monitoraggio, indirizza a `grl-mdsw`. |
| 🧠 **Enzo**<br>AI Engineer | LLM, prompt, RAG, embedding e vector store, orchestrazione, tool calling, agenti, output strutturati, eval, allucinazioni, costi, latenza e automazioni. | Parte dalla domanda «serve davvero un modello?» e, se serve, definisce l'impianto minimo che regge quando il modello sbaglia: pipeline, validazione, valutazione, costi e operatività. |
| 🧩 **Milo**<br>WordPress Component Architect | Siti e temi/plugin WordPress, Gutenberg, Elementor, ACF, custom post type, campi custom, template parts, Block Bindings e gestione dei media. | Progetta un modello di contenuti e componenti riusabili, usa Gutenberg come default, delimita Elementor e mantiene gli asset nella Media Library invece di lasciarli in pagine monolitiche. |
| 🔎 **Nora**<br>SEO Strategist & Search Systems Auditor | Domanda e intento di ricerca, architettura informativa, crawling, indicizzazione, contenuti, dati strutturati, performance, migrazioni e Search Console. | Verifica sempre live le regole e le feature SEO, riporta `as_of`, distingue il blocco tecnico dall'ipotesi di ranking e lascia una verifica osservabile; non promette posizionamenti. |

## Workflow: dal profilo alla consegna

I workflow coordinano la conversazione e impongono un percorso; gli agenti presidiano invece un
asse tecnico o di dominio. Questa è la scelta pratica da fare:

| Workflow | Quando usarlo | Come lavora | Risultato |
| --- | --- | --- | --- |
| `grl-setup` | Prima installazione o riconfigurazione di Guardrails in un progetto BMad. | Riconosce la configurazione TOML/YAML, registra le dodici figure, aggiorna il catalogo help e installa le stanze tematiche di `bmad-party-mode`. È idempotente e preserva gli override fuori dal blocco Guardrails. | Configurazione, roster e stanze aggiornati. Non crea la memoria condivisa: propone subito `grl-profile`. |
| `grl-profile` | Primo passo dopo il setup, progetto nuovo, repository vuoto o profilo da riallineare. | Scansiona manifest, README, dipendenze-segnale e documenti; compila gli otto campi del profilo e chiede solo ciò che il repository non sa. La criticità viene sempre dichiarata dall'utente; in sanità aggiunge fino a cinque campi. | Una pagina in `_bmad/memory/grl-shared/project-profile.md`, da cui deriva la severità di default. Su un repository vuoto i campi non deducibili diventano `non noto`. |
| `grl-board` | Revisione di un PRD, un'architettura, una story, una pagina, una configurazione, una cartella o un repository. | Legge memoria e artefatto, convoca in genere due-quattro figure sui segnali concreti, mostra chi è escluso e produce un riepilogo unico con punti azionabili e conflitti non appianati. Ha anche una vista separata dei rischi già accettati. | Riepilogo in conversazione; solo dopo conferma esplicita aggiunge righe a `decisions.md` o `accepted-risks.md`. |
| `grl-mdsw` | Quando vuoi sapere se una **funzione** software, per la finalità dichiarata, rientra nel perimetro dei dispositivi medici. Il solo fatto che usi dati sanitari non basta. | Pone quattro domande: la finalità riguarda un singolo paziente? Il software archivia/mostra il dato oppure lo interpreta, calcola o usa per suggerire una decisione? Quale classe indica la Regola 11? Che cosa cambia nel piano? | Verdetto chiaro: fuori dal MDR oppure classe I, IIa, IIb o III, con conseguenze e non-conseguenze. Non emette una certificazione CE e non produce fascicolo tecnico; registra solo il verdetto in memoria condivisa. |
| `grl-legal-updates` | Ricerca delle novità legali in un periodo preciso, per esempio «dal 1° gennaio a oggi». | Fa ricerca live su fonti primarie, ricostruisce versioni e vigenza degli atti, dichiara la copertura e passa da due gate `bmad-review`. | Digest in `_bmad-output/research` con fonti, data `as_of`, matrice di copertura, registro delle verifiche e mappa di obsolescenza. |
| `grl-fiscal-updates` | Ricerca di novità fiscali, circolari, bandi, incentivi o emendamenti in un periodo preciso. | Applica lo stesso percorso verificabile del workflow legale, aggiungendo requisiti, versioni, scadenze, spese ammissibili e soggetti interessati. | Digest in `_bmad-output/research`, con fonti primarie, copertura dichiarata, requisiti verificati, registro delle verifiche e staleness map. |
| `grl-web` | Creare una landing o un sito, riprendere un mockup, diagnosticare una pagina che non converte o promuovere un mockup approvato a progetto vero. | Parte dal brief di conversione — destinatario, promessa, obiezione, prova e una sola azione — prima di scrivere HTML. Usa uno slug di lavoro riutilizzabile, passa il risultato al gate `grl-board` e coinvolge Iris prima della consegna; per la messa online passa a Bruno. | In `_bmad-output/web`: `brief.md` e mockup HTML a file singolo, oppure `sito.md` e `stack.md` per un sito reale. La promozione produce il progetto statico con SEO, accessibilità e CSS generato. |

### Sequenza consigliata

1. `grl-setup` registra il modulo, se non è già installato.
2. `grl-profile` dà alle figure il contesto del progetto, anche quando il repository è ancora vuoto.
3. Si chiama un agente per una domanda mirata — per esempio Kai su un endpoint o Enzo su una pipeline AI.
4. Si usa `grl-board` quando lo stesso artefatto richiede più assi di revisione e si vuole vedere anche ciò che non è pertinente.
5. Per un sito, `grl-web` guida brief, mockup, diagnosi e promozione; Nora verifica la findability e gli altri agenti entrano solo sui segnali che compaiono.

### Testi e contenuti in più lingue

`grl-mdsw` non revisiona testi: stabilisce se una funzione software è un possibile dispositivo
medico e quale percorso MDR seguire.

Tutte le skill Guardrails applicano ora un passaggio editoriale finale agli output leggibili da una
persona: risposte, riepiloghi, digest, profili e copy delle pagine. La revisione non tocca codice,
configurazioni, citazioni, fonti, decisioni o dati strutturati; se `bmad-review` non è installata, la
skill esegue un controllo manuale equivalente.

Se BMad Core è installato, il passaggio usa `bmad-review` con il solo lens `prose`. Controlla
chiarezza, tono, leggibilità e problemi di comunicazione senza cambiare il significato; per l'ordine
o la struttura del documento si usa `bmad-review` con `lenses=structure`. Sono lens editoriali, non
un agente specializzato in traduzione.

Per un progetto multilingue si esegue la revisione indicando esplicitamente una lingua alla volta,
insieme alla guida di stile e al testo sorgente. BMad può segnalare problemi e proporre correzioni,
ma non equivale alla validazione di un revisore madrelingua, soprattutto per copy commerciale,
terminologia clinica o testi legali. Se è installato WDS, l'agente **Freya** ha inoltre un workflow
per raccogliere i contenuti in tutte le lingue, organizzare le traduzioni e pianificare URL,
`hreflang` e SEO; anche quello non sostituisce l'approvazione linguistica finale.

## Come funziona

**Profilo di progetto.** `grl-profile` scrive `_bmad/memory/grl-shared/project-profile.md`: settore,
tipo di software, dati personali trattati, mercato, stack, componenti AI, vincoli noti e — campo
decisivo — la **criticità dichiarata** (hobby/prototipo · interno · produzione con clienti ·
regolamentato). È la criticità a decidere quanto sono severe tutte e dodici le figure. Se il
settore dichiarato è sanitario, il profilo raccoglie in più finalità del software, contesto d'uso,
integrazioni sanitarie, ruolo GDPR ed eventuale qualificazione MDR; altrimenti quei campi non
vengono nemmeno nominati.

**Un'eccezione alla severità.** Livia segnala a qualsiasi livello, anche `light` e anche su un
prototipo, i difetti che possono portare a somministrare, prescrivere o refertare alla persona
sbagliata. Il motivo è che i prototipi sanitari finiscono in reparto più spesso di quanto chi li
scrive immagini.

**Severità.** Si deriva sempre dalla criticità dichiarata nel profilo di progetto; se il profilo
manca, il default operativo è `normal`.

| Livello | Comportamento |
| ------- | ------------- |
| `light` | parlano solo se il rischio è concreto e imminente; auto-attivazione rara |
| `normal` | segnalano ciò che conta, una volta sola |
| `strict` | segnalano anche i rischi minori e chiedono di mettere per iscritto quelli accettati |

**Memoria condivisa.** Tre file in `_bmad/memory/grl-shared/`, letti da tutte le figure in
attivazione:

- `project-profile.md` — il contesto, scritto da `grl-profile`
- `decisions.md` — le decisioni vincolate: cosa è stato deciso e quale vincolo l'ha imposto
- `accepted-risks.md` — i rischi accettati consapevolmente. **Si scrive solo su conferma esplicita
  dell'utente**, e da quel momento le figure tacciono su quel punto: è il meccanismo anti-rumore
  del modulo

Ogni figura ha inoltre una propria `notes.md` in `_bmad/memory/grl-agent-<code>/`.

**Anti-rumore.** In auto-attivazione parla **al massimo una figura per turno**: quella con la
competenza decisiva secondo le tabelle dei confini, che nomina le altre in una riga e si ferma.
La convocazione multipla è esplicita e si chiama `grl-board`.

**Antipattern vietati a tutte le figure:** allarmismo; citazioni di norme o riferimenti a pioggia
(un riferimento citato = un'azione richiesta); «consulta un esperto» come risposta standard;
checklist recitate a memoria. Il verdetto **«non serve niente» è un risultato legittimo** e si dà
con la stessa sicurezza di un allarme.

## Rapporto con BMM

Guardrails è un'espansione di **BMM** (software development) e funziona anche da sola: nessuna
skill pretende file prodotti da BMM, li legge se ci sono.

Le figure che si sovrappongono a ruoli BMM esistenti non li sostituiscono. Winston e Sally
progettano; Otto e Iris fanno da **revisori critici** su un asse specifico — disciplina strutturale
del codice, originalità visiva. L'attrito è voluto. Enzo si aggiunge alla stessa logica su Amelia:
lei implementa, lui guarda l'impianto della pipeline AI e chiede cosa succede quando il modello
sbaglia.

Tutte e dodici entrano nel roster principale di `bmad-party-mode`, accanto ai cinque agenti BMM.

## Stanze tematiche e sottomoduli

Il bundle `grl` resta oggi l'installazione compatibile unica, ma il dominio è già descritto in
confini topic-oriented in [`src/module-topology.yaml`](src/module-topology.yaml). La topologia
prepara sette futuri package senza duplicare le skill e senza rinominare i comandi già installati:

| Codice | Area | Skill principali |
| ------ | ---- | ---------------- |
| `grc` | Core | setup, profilo, collegio, memoria condivisa |
| `grg` | Governance | privacy, legale, compliance e monitoraggio novità legali |
| `grf` | Fiscalità | fisco, contabilità, bandi, finanza agevolata e monitoraggio novità fiscali |
| `gre` | Engineering | architettura, sicurezza, ops, AI |
| `grh` | Health | dominio clinico, dispositivo medico |
| `grw` | Web Experience | SEO, critica UI, siti e landing |
| `gwp` | WordPress | Gutenberg, campi custom, template, Media Library |

I confini di installazione e quelli di conversazione non coincidono: `grl-setup` registra anche
le stanze di `bmad-party-mode`, che possono convocare agenti di aree diverse:

```text
grl-governance          Vera · Aldo · Nils
grl-fiscal              Marta · Aldo · Nils
grl-engineering         Otto · Kai · Bruno · Enzo
grl-health              Livia · Vera · Nils · Kai
grl-web                 Nora · Iris · Milo · Sally (se BMM è installato)
grl-wordpress-delivery  Milo · Iris · Otto · Bruno
grl-release-gate        Vera · Kai · Aldo · Nils · Otto · Bruno · Nora
grl-full-board          tutte le figure Guardrails
```

Dopo `grl-setup` si apre una stanza con:

```bash
bmad-party-mode --party grl-wordpress-delivery
```

La configurazione viene scritta nel layer non rigenerato
`_bmad/custom/bmad-party-mode.toml`; gli override e i gruppi dell'utente fuori dal blocco
Guardrails vengono preservati. L'estrazione fisica in package indipendenti sarà una migrazione
successiva: prima verranno validati `gwp` e `grh`, poi gli altri domini.

## Installazione

Con l'installer BMad, indicando questo repository come sorgente custom:

```bash
npx bmad-method install --custom-source https://github.com/mlarese/bmad-module-guardrails
```

L'installer copia le diciannove skill, registra le dodici figure come agenti
(`[agents.grl-agent-*]` nella configurazione) — che è ciò che le fa comparire nel roster di
`bmad-party-mode` — aggiunge le voci di help al catalogo `_bmad/_config/bmad-help.csv` e,
eseguendo `grl-setup`, installa anche le stanze tematiche.

In alternativa, per un'installazione manuale o per riconfigurare un'installazione esistente,
si esegue la skill **`grl-setup`**.

**Primo passo dopo l'installazione: `grl-profile`.** Senza profilo le figure partono cieche.

La severità non è una scelta di installazione: viene letta dalla criticità dichiarata in
`_bmad/memory/grl-shared/project-profile.md`, quindi il primo passo dopo l'installazione resta
`grl-profile`.

## Struttura

```
.claude-plugin/marketplace.json   indice letto dall'installer BMad
src/
├── module.yaml                   manifesto del modulo: config e roster delle figure
├── module-topology.yaml           confini dei futuri package topic-oriented
├── module-help.csv               voci di help
└── skills/
    ├── grl-agent-privacy/        🛡️ Vera
    ├── grl-agent-security/       🔐 Kai
    ├── grl-agent-legal/          ⚖️ Aldo
    ├── grl-agent-compliance/     📐 Nils
    ├── grl-agent-fiscal/        🧾 Marta
    ├── grl-agent-ui-critic/      👁️ Iris
    ├── grl-agent-architecture/   🧱 Otto
    ├── grl-agent-ops/            🖥️ Bruno
    ├── grl-agent-health/         🩺 Livia
    ├── grl-agent-ai/             🧠 Enzo
    ├── grl-agent-wordpress/      🧩 Milo
    ├── grl-agent-seo/            🔎 Nora
    ├── grl-profile/              workflow — profilo di progetto
    ├── grl-board/                workflow — revisione collegiale
    ├── grl-mdsw/                 workflow — qualificazione dispositivo medico
    ├── grl-legal-updates/        workflow — ultime novità legali con doppia verifica
    ├── grl-fiscal-updates/       workflow — ultime novità fiscali con doppia verifica
    ├── grl-web/                  workflow che produce landing page e siti
    └── grl-setup/                installazione, roster e stanze party tematiche
        └── assets/party-groups.toml
docs/module-plan.md               il documento di piano del modulo
```

Il piano in `docs/` documenta le decisioni di progetto e il loro razionale: architettura,
contratto di memoria, confini fra le figure e i brief da cui ogni skill è stata costruita.
